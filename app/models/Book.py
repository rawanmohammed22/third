from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base 




class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Many-to-Many مع Student
    students: Mapped[list["student"]] = relationship(
        "Student",
        secondary="student_book",
        back_populates="books"
    )
