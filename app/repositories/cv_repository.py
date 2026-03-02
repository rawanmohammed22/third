# app/repositories/cv_repository.py
from sqlalchemy.orm import Session
from app.models.user_cv import UserCV  # import الـ model اللي عملناه
from typing import Optional

class CVRepository:
    def __init__(self, db: Session):
        self.db = db

    # جلب CV المستخدم
    def get_user_cv(self, user_id: int) -> Optional[UserCV]:
        return self.db.query(UserCV).filter(UserCV.user_id == user_id).first()

    # إنشاء CV جديد
    def create_cv(
        self,
        user_id: int,
        bucket_id: str,
        file_path: str,
        file_url: str,
        original_filename: str,
        # analysis_result: dict | None = None  # لو هتحلي بالـ Cohere بعدين
    ) -> UserCV:

        cv = UserCV(
            user_id=user_id,
            bucket_id=bucket_id,
            file_path=file_path,
            file_url=file_url,
            original_filename=original_filename,
            # analysis_result=analysis_result,
            is_active=True,
            version=1
        )
        self.db.add(cv)
        self.db.commit()
        self.db.refresh(cv)
        return cv

    # تحديث CV موجود
    def update_cv(
        self,
        user_id: int,
        new_file_path: str | None = None,
        new_file_url: str | None = None,
        new_original_filename: str | None = None
    ) -> Optional[UserCV]:
        cv = self.get_user_cv(user_id)
        if not cv:
            return None

        if new_file_path:
            cv.file_path = new_file_path
        if new_file_url:
            cv.file_url = new_file_url
        if new_original_filename:
            cv.original_filename = new_original_filename

        self.db.commit()
        self.db.refresh(cv)
        return cv

    # حذف CV
    def delete_cv(self, user_id: int) -> bool:
        cv = self.get_user_cv(user_id)
        if not cv:
            return False

        self.db.delete(cv)
        self.db.commit()
        return True
    def save_analysis(self, user_id: int, analysis_result: dict):
       cv = self.get_user_cv(user_id)
       if cv:
          cv.analysis_result = analysis_result
          self.db.commit()
          self.db.refresh(cv)
       return cv