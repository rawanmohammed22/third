# app/routers/storage_router.py
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.storage_service import StorageService
from app.dependencies import get_current_user  # ← بيفك الـ token

router = APIRouter(prefix="/storage", tags=["Storage"])

@router.post("/upload")
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ← الـ user من الـ token
):
    file_bytes = file.file.read()
    return StorageService(db).upload_pdf(
        file_bytes=file_bytes,
        file_name=file.filename,
        user_id=current_user.id  # ← بتاخدي الـ id من الـ user
    )


## الـ Flow بالكامل:
