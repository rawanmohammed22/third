# app/routers/cv_router.py

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.dependencies import get_current_user
from app.services.cv_service import CVService

router = APIRouter(prefix="/cv", tags=["CV"])

@router.post("/upload")
async def upload_user_cv(file: UploadFile = File(...),
                         db: Session = Depends(get_db),
                         current_user = Depends(get_current_user)):
    service = CVService(db)
    return await service.upload_cv(user_id=current_user.id, file=file)

@router.post("/analyze")
def analyze_user_cv(db: Session = Depends(get_db),
                    current_user = Depends(get_current_user)):
    return CVService(db).analyze_cv(user_id=current_user.id)