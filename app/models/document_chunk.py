# app/models/document_chunk.py
from sqlalchemy import Integer, Text, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from app.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id:          Mapped[int]   = mapped_column(Integer, primary_key=True, index=True)
    pdf_name:    Mapped[str]   = mapped_column(String, nullable=False)
    chunk_index: Mapped[int]   = mapped_column(Integer, nullable=False)
    content:     Mapped[str]   = mapped_column(Text, nullable=False)
    embedding:   Mapped[list]  = mapped_column(Vector(1024), nullable=True)
    created_at:  Mapped[str]   = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())