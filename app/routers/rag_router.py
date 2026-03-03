# app/routers/rag_router.py

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.rag_service import RAGService
import shutil
import os

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/index")
def index_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF file, chunk it, embed it, and store it in the database."""
    
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        service = RAGService(db)
        count = service.index_pdf(pdf_path=temp_path, pdf_name=file.filename)
        return {"message": "PDF indexed successfully", "chunks_stored": count}
    finally:
        os.remove(temp_path)


@router.post("/ask")
def ask_question(question: str, db: Session = Depends(get_db)):
    """Ask a question and get an answer based on indexed PDFs."""
    service = RAGService(db)
    answer = service.answer(question)
    return {"question": question, "answer": answer}