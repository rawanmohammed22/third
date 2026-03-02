# app/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, default="student")  # student / admin

    # ربط بالـ Student
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="user",
        uselist=False  # one-to-one
    )

    documents = relationship("Document", back_populates="user")

    cv: Mapped["UserCV"] = relationship(
        "UserCV",
        back_populates="user",
        uselist=False,          # one-to-one من ناحية الـ User
        cascade="all, delete-orphan"   # optional: لو حذفت الـ user يتمسح الـ CV
    )