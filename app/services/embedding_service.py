# app/services/embedding_service.py

from sqlalchemy.orm import Session
from app.repositories.embedding_repository import EmbeddingRepository
from app.Clients.cohere_client import CohereClient


class EmbeddingService:
    def __init__(self, db: Session):
        self.repo = EmbeddingRepository(db)
        self.cohere = CohereClient()

    def embed_and_save(self, text: str) -> dict:
        """Take a text, generate its embedding, and save it to the database."""
        
        # Generate embedding vector from Cohere
        vector = self.cohere.embed(text)

        # Save text + vector to database
        saved = self.repo.save_embedding(text=text, embedding=vector)

        return {
            "id": saved.id,
            "text": saved.text,
            "vector_size": len(vector),
            "vector": vector,
            "message": "Embedding saved successfully"
        }