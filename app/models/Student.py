# app/models/student.py
# app/models/student.py
from sqlalchemy import String, Integer ,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base 
from app.models.student_course import student_course
from app.models.student_book import student_book


 # ← ده اللي كان بيطلع إيرور قبل كده

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

     # ربط بالـ User ← جديد
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="student")

    courses: Mapped[list["Course"]] = relationship(
        "Course",                        # ← string بدل import الكلاس
        secondary="student_course",
        back_populates="students"
    )
    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary="student_book",
        back_populates="students"
    )