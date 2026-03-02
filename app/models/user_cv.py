# app/models/user_cv.py   (أو resumes.py – اختاري اسم واضح)

from sqlalchemy import ForeignKey, String, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime


class UserCV(Base):
    __tablename__ = "user_cvs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True     # ← ده اللي هيضمن one CV per user
    )
    
    bucket_id: Mapped[str] = mapped_column(String, nullable=False, default="documents")
    file_path: Mapped[str] = mapped_column(Text, nullable=False)          # resumes/{user_id}/cv.pdf
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    
    uploaded_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )
    file_url: Mapped[str] = mapped_column(String, nullable=False)   
    # نتيجة التحليل من Cohere (مهارات، خبرة، تلخيص، إلخ)
    analysis_result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    # optional – لو هتسمحي replace / versions في المستقبل
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # العلاقة العكسية مع User
    user: Mapped["User"] = relationship("User", back_populates="cv")

    # indexes مفيدة
    __table_args__ = (
        # لو عايزة تمنعي duplicates بشكل إضافي (لكن unique على user_id كافي)
        # UniqueConstraint("user_id", name="uq_user_cvs_user_id"),
    )