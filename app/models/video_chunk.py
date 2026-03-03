# app/models/video_chunk.py
from sqlalchemy import Integer, Text, String, Float, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from app.database import Base


class VideoChunk(Base):
    __tablename__ = "video_chunks"

    id:          Mapped[int]   = mapped_column(Integer, primary_key=True, index=True)
    video_id:    Mapped[int]   = mapped_column(Integer, nullable=False)
    video_name:  Mapped[str]   = mapped_column(String, nullable=False)
    video_url:   Mapped[str]   = mapped_column(String, nullable=False)
    content:     Mapped[str]   = mapped_column(Text, nullable=False)
    start_time:  Mapped[float] = mapped_column(Float, nullable=False)
    end_time:    Mapped[float] = mapped_column(Float, nullable=False)
    chunk_index: Mapped[int]   = mapped_column(Integer, nullable=False)
    embedding:   Mapped[list]  = mapped_column(Vector(1024), nullable=True)
    created_at:  Mapped[str]   = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())