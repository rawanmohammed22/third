# app/services/pdf_service.py
import fitz  # pymupdf
from typing import List

class PDFService:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def extract_text(self, pdf_path: str) -> str:
        
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text.strip()

    def chunk_text(self, text: str) -> List[str]:
        """
        Recursive splitting:
        بيقسم على \n\n الأول، لو الـ chunk لسه كبير يقسم على \n
        لو لسه كبير يقسم على . (جملة جملة)
        مع overlap بين كل chunk والتاني
        """
        chunks = []
        self._recursive_split(text, chunks)
        return [c.strip() for c in chunks if c.strip()]

    def _recursive_split(self, text: str, chunks: List[str]) -> None:
       
        words = text.split()
        if len(words) <= self.chunk_size:
            chunks.append(text)
            return

      
        separators = ["\n\n", "\n", ". "]
        for sep in separators:
            parts = text.split(sep)
            if len(parts) > 1:
                self._merge_and_split(parts, sep, chunks)
                return

       
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += self.chunk_size - self.overlap

    def _merge_and_split(self, parts: List[str], sep: str, chunks: List[str]) -> None:
        """بيجمع الـ parts الصغيرة مع بعض ولو اتكبرت يقسمها"""
        current = ""
        for part in parts:
            candidate = current + sep + part if current else part
            if len(candidate.split()) <= self.chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
               
                overlap_text = " ".join(current.split()[-self.overlap:])
                current = overlap_text + " " + part if overlap_text else part
        if current:
            chunks.append(current)

    def process_pdf(self, pdf_path: str) -> List[str]:
       
        text = self.extract_text(pdf_path)
        chunks = self.chunk_text(text)
        return chunks


def get_pdf_service() -> PDFService:
    return PDFService()