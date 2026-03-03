# app/routers/video_router.py
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.video_search_service import VideoSearchService
from app.Clients.supabase_client import SupabaseStorageClient
from typing import Optional
import yt_dlp
import os

router = APIRouter(prefix="/videos", tags=["Video Search"])


def download_youtube(url: str) -> tuple[str, str]:
    filename = "youtube_video.mp4"
    temp_path = f"temp_{filename}"
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temp_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = info.get("title", "youtube_video")
    
    return f"{temp_path}.mp3", filename


@router.post("/index")
def index_video(
    video_id: int = Form(...),
    youtube_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    storage = SupabaseStorageClient()
    temp_path = None

    try:
        if youtube_url:
            temp_path, video_name = download_youtube(youtube_url)
            video_url = youtube_url
            with open(temp_path, "rb") as f:
                file_bytes = f.read()

        elif file:
            file_bytes = file.file.read()
            video_name = file.filename
            video_url = storage.upload_video(file_bytes, file.filename, video_id)
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(file_bytes)

        else:
            return {"error": "لازم ترفع file أو تحط YouTube URL"}

        service = VideoSearchService(db)
        count = service.index_video(
            video_path=temp_path,
            video_name=video_name,
            video_url=video_url,
            video_id=video_id
        )

        return {
            "message": "Video indexed successfully",
            "video_url": video_url,
            "chunks_stored": count
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/search")
def search_video(video_id: int,query: str, top_k: int = 5,  db: Session = Depends(get_db)):
    service = VideoSearchService(db)
    return {"query": query, "results": service.search(query=query,video_id=video_id, top_k=top_k)}


@router.post("/analyze")
def analyze_video(
    youtube_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    temp_path = None
    try:
        if youtube_url:
            temp_path, video_name = download_youtube(youtube_url)

        elif file:
            file_bytes = file.file.read()
            video_name = file.filename
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(file_bytes)

        else:
            return {"error": "لازم ترفع file أو تحط YouTube URL"}

        service = VideoSearchService(db)
        return service.analyze_video(
            video_path=temp_path,
            video_name=video_name
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)