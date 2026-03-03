# app/routers/embedding_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])


@router.post("/embed")
def embed_text(text: str, db: Session = Depends(get_db)):
    """Take a text string, generate its embedding, and save it to the database."""
    service = EmbeddingService(db)
    return service.embed_and_save(text=text)