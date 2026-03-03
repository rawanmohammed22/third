# app/services/whisper_service.py
import whisper
import os
from typing import List, Dict


class WhisperService:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, video_path: str) -> List[Dict]:
        """
        بتاخد مسار الفيديو وترجع list of segments
        كل segment فيه: text, start, end
        """
        result = self.model.transcribe(video_path)

        segments = []
        for segment in result["segments"]:
            segments.append({
                "text": segment["text"].strip(),
                "start": segment["start"],
                "end": segment["end"]
            })

        return segments


def get_whisper_service() -> WhisperService:
    return WhisperService()