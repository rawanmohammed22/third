# app/services/student_service.py
from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import StudentCreate, StudentUpdate, StudentResponse
from sqlalchemy.orm import Session
from typing import List

class StudentService:
    def __init__(self, db: Session):
        self.repo = StudentRepository(db)

    def get_all_students(self) -> List[StudentResponse]:
        students = self.repo.get_all()
        return [StudentResponse.model_validate(s) for s in students]

    def add_student(self, name: str, age: int | None, email: str) -> int:
        data = StudentCreate(name=name, age=age, email=email)
        return self.repo.create(data)

    def update_student(self, student_id: int, name: str | None = None, age: int | None = None, email: str | None = None):
        data = StudentUpdate(name=name, age=age, email=email)
        self.repo.update(student_id, data)

    def delete_student(self, student_id: int) -> bool:
        return self.repo.delete(student_id)

