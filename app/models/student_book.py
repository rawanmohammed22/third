from sqlalchemy import Table, Column, ForeignKey
from app.database import Base

student_book = Table(
    "student_book",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)
