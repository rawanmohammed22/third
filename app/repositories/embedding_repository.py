# app/repositories/embedding_repository.py

from sqlalchemy.orm import Session
from app.models.embedding import Embedding


class EmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_embedding(self, text: str, embedding: list[float]) -> Embedding:
        """Save text and its vector embedding to the database."""
        db_embedding = Embedding(
            text=text,
            embedding=embedding
        )
        self.db.add(db_embedding)
        self.db.commit()
        self.db.refresh(db_embedding)
        return db_embedding

    def get_all(self) -> list[Embedding]:
        """Get all stored embeddings."""
        return self.db.query(Embedding).all()