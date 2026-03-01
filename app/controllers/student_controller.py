# app/controllers/student_controller.py
from app.services.student_service import StudentService
from typing import List
from app.schemas.student_schema import StudentResponse

class StudentController:
    def __init__(self, service: StudentService):
        self.service = service

    def get_all_students(self) -> List[StudentResponse]:
        return self.service.get_all_students()

    def add_student(self, name: str, age: int | None, email: str) -> int:
        return self.service.add_student(name, age, email)

    def update_student(self, student_id: int, name: str | None = None, age: int | None = None, email: str | None = None):
        self.service.update_student(student_id, name, age, email)

    def delete_student(self, student_id: int) -> bool:
        return self.service.delete_student(student_id)




