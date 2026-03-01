# app/models/student_course.py
# app/models/student_course.py
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.database import Base

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)
