from sqlalchemy.orm import Session
from app.Clients.supabase_client import SupabaseStorageClient
from app.models.Documents import Document

class StorageService:
    def __init__(self, db: Session):
        self.db = db
        self.storage = SupabaseStorageClient()

    def upload_pdf(self, file_bytes: bytes, file_name: str, user_id: int) -> dict:
      
        url = self.storage.upload_file(file_bytes, file_name)
        
        
        document = Document(
            file_name=file_name,
            file_url=url,
            user_id=user_id
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return {
            "id": document.id,
            "file_name": document.file_name,
            "url": document.file_url,
            
        } 