# app/utils/file_storage.py
import os
import uuid
from fastapi import UploadFile, HTTPException

# المسار الأساسي للرفع
UPLOAD_DIR = "uploads/videos"

async def save_video(file: UploadFile) -> str:
    # تأكد إن الفولدر موجود
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # تحقق إن الملف فيديو
    allowed_types = ["video/mp4", "video/avi", "video/mkv", "video/mov"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="نوع الملف غير مدعوم. يرجى رفع فيديو mp4/avi/mkv/mov"
        )

    # اعمل اسم unique للفيديو عشان متتعدلش
    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # احفظ الفيديو
    with open(file_path, "wb") as f:
        content = await file.read()  
        f.write(content)

    return file_path


def delete_video(file_path: str):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)