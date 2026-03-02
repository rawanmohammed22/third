import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

class SupabaseStorageClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "apikey": self.key
        }

    def _sanitize_filename(self, filename: str) -> str:
        name, ext = os.path.splitext(filename)
        safe_name = name.lower().replace(" ", "-").replace("_", "-")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        return f"{safe_name}-{timestamp}{ext}"

    def upload_cv(self, file_bytes: bytes, file_name: str, user_id: int | str) -> str:
        safe_name = self._sanitize_filename(file_name)
        path = f"{user_id}/{safe_name}"
        url = f"{self.url}/storage/v1/object/cvs/{path}"
        headers = {**self.headers, "Content-Type": "application/pdf", "x-upsert": "true"}

        resp = requests.post(url, headers=headers, data=file_bytes)
        if resp.status_code not in (200, 201):
            raise Exception(f"فشل رفع الملف - {resp.status_code}: {resp.text}")

        # public URL جاهز للتحميل مباشرة
        return f"{self.url}/storage/v1/object/public/cvs/{path}"

    def download_cv_by_url(self, public_url: str) -> bytes:
        resp = requests.get(public_url)
        if resp.status_code != 200:
            raise Exception(f"فشل تحميل الملف - {resp.status_code}: {resp.text}")
        return resp.content