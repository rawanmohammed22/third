# app/services/video_search_service.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.video_chunk import VideoChunk
from app.Clients.cohere_client import CohereClient
from app.services.whisper_service import WhisperService
from typing import List, Dict


class VideoSearchService:
    def __init__(self, db: Session):
        self.db = db
        self.cohere = CohereClient()
        self.whisper = WhisperService()

    # ─────────────── 1. Chunk Segments ───────────────
    def _chunk_segments(self, segments: List[Dict], chunk_size: int = 5) -> List[Dict]:
        chunks = []
        for i in range(0, len(segments), chunk_size - 1):
            group = segments[i:i + chunk_size]
            chunks.append({
                "text": " ".join([s["text"] for s in group]),
                "start": group[0]["start"],
                "end": group[-1]["end"],
                "index": len(chunks)
            })
        return chunks

    # ─────────────── 2. Index Video ───────────────
    def index_video(self, video_path: str, video_name: str, video_url: str, video_id: int) -> int:
        segments = self.whisper.transcribe(video_path)
        chunks = self._chunk_segments(segments)

        for chunk in chunks:
            embedding = self.cohere.embed(chunk["text"])

            video_chunk = VideoChunk(
                video_id=video_id,
                video_name=video_name,
                video_url=video_url,
                content=chunk["text"],
                start_time=chunk["start"],
                end_time=chunk["end"],
                chunk_index=chunk["index"],
                embedding=embedding,
            )
            self.db.add(video_chunk)

        self.db.commit()
        return len(chunks)

    # ─────────────── 3. Search ───────────────
    def search(self, query: str,video_id: int, top_k: int = 5) -> List[Dict]:
        query_embedding = self.cohere.embed(query)

        results = self.db.execute(
            text("""
                SELECT id, video_name, video_url, content, start_time, end_time, chunk_index
                FROM video_chunks
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :top_k
            """),
            {
                "embedding": str(query_embedding),
                "video_id": video_id, 
                "top_k": top_k
            }
        ).fetchall()

        return [
            {
                "chunk_id": row[0],
                "chunk_index": row[6],
                "video_name": row[1],
                "video_url": row[2],
                "content": row[3],
                "start_time": row[4],
                "end_time": row[5],
                "jump_url": f"{row[2]}#t={int(row[4])}"
            }
            for row in results
        ]

    # ─────────────── 4. Analyze Video ───────────────
    def analyze_video(self, video_path: str, video_name: str) -> dict:
        # 1. استخرجي النص
        segments = self.whisper.transcribe(video_path)

        if not segments:
            raise ValueError("مش قادر يستخرج نص من الفيديو")

        # 2. الـ Script والمدة
        full_script = " ".join([s["text"] for s in segments])
        duration = segments[-1]["end"]

        # 3. حلّلي بـ Cohere
        analysis = self.cohere.analyze_video(full_script)

        return {
            "video_name": video_name,
            "duration_seconds": duration,
            "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}",
            "script": full_script,
            "analysis": analysis
        }


def get_video_search_service(db: Session) -> VideoSearchService:
    return VideoSearchService(db)