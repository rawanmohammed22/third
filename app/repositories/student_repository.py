# app/repositories/student_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models.Student import Student
from app.schemas.student_schema import StudentCreate, StudentUpdate

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Student]:
        stmt = select(Student)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, student_id: int) -> Student | None:
        return self.db.get(Student, student_id)

    def create(self, data: StudentCreate) -> int:
        student = Student(**data.model_dump())
        self.db.add(student)
        try:
            self.db.commit()
            self.db.refresh(student)
            return student.id
        except IntegrityError:
            self.db.rollback()
            raise ValueError("الإيميل موجود بالفعل")

    def update(self, student_id: int, data: StudentUpdate) -> bool:
        student = self.get_by_id(student_id)
        if not student:
            raise ValueError("الطالب غير موجود")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(student, key, value)

        try:
            self.db.commit()
            self.db.refresh(student)
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("الإيميل موجود بالفعل")

    def delete(self, student_id: int) -> bool:
        student = self.get_by_id(student_id)
        if not student:
            return False
        self.db.delete(student)
        self.db.commit()
        return True
