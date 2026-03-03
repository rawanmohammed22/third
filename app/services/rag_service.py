# app/services/rag_service.py
from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.Clients.cohere_client import CohereClient
from app.services.pdf_service import PDFService
from sqlalchemy import text


class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.cohere = CohereClient()
        self.pdf_service = PDFService()

    # ─────────────── 1. Index PDF ───────────────
    def index_pdf(self, pdf_path: str, pdf_name: str) -> int:
        """بتاخد مسار الـ PDF وتقسمه وتخزن الـ embeddings"""

        chunks = self.pdf_service.process_pdf(pdf_path)

        for i, chunk in enumerate(chunks):
            embedding = self.cohere.embed(chunk)

            doc_chunk = DocumentChunk(
                pdf_name=pdf_name,
                chunk_index=i,
                content=chunk,
                embedding=embedding,
            )
            self.db.add(doc_chunk)

        self.db.commit()
        return len(chunks)

    # ─────────────── 2. Retrieve ───────────────
    def retrieve(self, query: str, top_k: int = 5):
        """بتاخد السؤال وترجع أقرب chunks"""

        query_embedding = self.cohere.embed(query)

        # بحث بـ cosine similarity في pgvector
        results = self.db.execute(
            text("""
                SELECT content
                FROM document_chunks
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :top_k
            """),
            {
                "embedding": str(query_embedding),
                "top_k": top_k
            }
        ).fetchall()

        return [row[0] for row in results]

    # ─────────────── 3. Generate ───────────────
    def answer(self, question: str) -> str:
        """بتاخد سؤال وترجع إجابة من الـ PDF"""

        chunks = self.retrieve(question)

        if not chunks:
            return "مش لاقي معلومات كافية في الـ PDF للإجابة على السؤال ده."

        context = "\n\n".join(chunks)

        prompt = f"""
 You are a smart assistant. Answer the question below based ONLY on the provided context.
 If the answer is not found in the context, say "This information is not available in the document."

Context:
{context}

Question:
{question}

Answer:
        """

        return self.cohere.chat(prompt)


def get_rag_service(db: Session) -> RAGService:
    return RAGService(db)