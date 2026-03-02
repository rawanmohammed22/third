# app/services/cv_service.py

import pdfplumber
import io
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.repositories.cv_repository import CVRepository
from app.Clients.supabase_client import SupabaseStorageClient
from app.Clients.cohere_client import CohereClient

class CVService:
    def __init__(self, db: Session):
        self.db = db
        self.storage = SupabaseStorageClient()
        self.cohere = CohereClient()
        self.repo = CVRepository(db)

    async def upload_cv(self, user_id: int, file: UploadFile) -> dict:
        # التحقق من نوع الملف
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="الملف يجب أن يكون PDF فقط"
            )

        # قراءة محتوى الملف
        file_bytes = await file.read()
        file_path = f"cvs/{user_id}/{file.filename}"

        # رفع الملف على Supabase Storage
        try:
            public_url = self.storage.upload_cv(file_bytes, file.filename, user_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"فشل رفع الملف في الـ storage: {str(e)}"
            )

        # التحقق إذا كان هناك CV موجود مسبقاً
        existing_cv = self.repo.get_user_cv(user_id)

        if existing_cv:
            # تحديث CV موجودة
            cv = self.repo.update_cv(
                user_id=user_id,
                new_file_url=public_url,
                new_original_filename=file.filename
            )
            message = "تم تحديث الـ CV بنجاح"
        else:
            # إنشاء CV جديدة — بنبعت file_url من الأول مباشرة
            cv = self.repo.create_cv(
                user_id=user_id,
                bucket_id="cvs",
                file_path=file_path,
                original_filename=file.filename,
                file_url=public_url  # ← الإضافة اللي كانت ناقصة
            )
            message = "تم رفع الـ CV بنجاح"

        return {
            "status": "success",
            "message": message,
            "public_url": public_url,
            "original_filename": file.filename,
            "user_id": user_id
        }

    def analyze_cv(self, user_id: int) -> dict:
        # الحصول على CV من قاعدة البيانات
        cv = self.repo.get_user_cv(user_id)
        if not cv:
            raise HTTPException(status_code=404, detail="مفيش CV، ارفع CV الأول")

        # تحميل الملف من الـ storage
        try:
            file_bytes = self.storage.download_cv_by_url(cv.file_url)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"فشل تحميل الـ CV من الـ storage: {str(e)}"
            )

        # استخراج النص من PDF
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            cv_text = ""
            for page in pdf.pages:
                cv_text += page.extract_text() or ""

        if not cv_text.strip():
            raise HTTPException(status_code=400, detail="مش قادر يقرأ النص من الـ PDF")

        # تحليل النص باستخدام Cohere
        analysis = self.cohere.analyze_cv(cv_text)

        self.repo.save_analysis(user_id=user_id, analysis_result=analysis)

        return {
            "user_id": user_id,
            "file": cv.original_filename,
            "analysis": analysis
        }