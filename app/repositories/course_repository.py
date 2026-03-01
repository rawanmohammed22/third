from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional

from app.models.Course import Course
from app.schemas.course_schema import CourseCreate, CourseUpdate


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    # استرجاع كل الكورسات
    def get_all(self) -> List[Course]:
        stmt = select(Course)
        result = self.db.execute(stmt)
        return result.scalars().all()

    # استرجاع كورس واحد بالـ id
    def get_by_id(self, course_id: int) -> Optional[Course]:
        return self.db.get(Course, course_id)

    # إنشاء كورس جديد
    def create(self, data: CourseCreate) -> int:
        try:
            course = Course(**data.model_dump())
            self.db.add(course)
            self.db.commit()
            self.db.refresh(course)
            return  course

        except IntegrityError as e:
            self.db.rollback()
            error_msg = str(e).lower()
            if "unique constraint" in error_msg or "duplicate key" in error_msg:
                if "title" in error_msg:
                    raise ValueError("اسم الكورس موجود مسبقاً")
                else:
                    raise ValueError("بيانات مكررة غير مسموح بها")
            else:
                raise ValueError("خطأ في سلامة البيانات: تأكد من صحة المدخلات")

        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"خطأ في قاعدة البيانات: {str(e)}")

    # تحديث كورس موجود
    def update(self, course_id: int, data: CourseUpdate) -> bool:
        course = self.get_by_id(course_id)
        if not course:
            raise ValueError("الكورس غير موجود")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(course, key, value)

        try:
            self.db.commit()
            self.db.refresh(course)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"خطأ في تحديث الكورس: {str(e)}")

    # حذف كورس
    def delete(self, course_id: int) -> bool:
        course = self.get_by_id(course_id)
        if not course:
            return False
        try:
            self.db.delete(course)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"خطأ في حذف الكورس: {str(e)}")