import os
import re
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
        # شيل كل unicode characters غير standard
        name = name.encode('ascii', 'ignore').decode('ascii')
        # شيل كل حاجة مش letters/numbers
        safe_name = re.sub(r'[^a-zA-Z0-9]', '-', name.lower())
        # شيل الـ dashes المتكررة
        safe_name = re.sub(r'-+', '-', safe_name).strip('-')
        if not safe_name:
            safe_name = "file"
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

        return f"{self.url}/storage/v1/object/public/cvs/{path}"

    def download_cv_by_url(self, public_url: str) -> bytes:
        resp = requests.get(public_url)
        if resp.status_code != 200:
            raise Exception(f"فشل تحميل الملف - {resp.status_code}: {resp.text}")
        return resp.content

    def upload_video(self, file_bytes: bytes, file_name: str, user_id: int | str) -> str:
        safe_name = self._sanitize_filename(file_name)
        path = f"{user_id}/{safe_name}"
        url = f"{self.url}/storage/v1/object/videos/{path}"

        ext = os.path.splitext(file_name)[1].lower()
        content_type_map = {
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".mkv": "video/x-matroska",
        }
        content_type = content_type_map.get(ext, "video/mp4")

        headers = {**self.headers, "Content-Type": content_type, "x-upsert": "true"}

        resp = requests.post(url, headers=headers, data=file_bytes)
        if resp.status_code not in (200, 201):
            raise Exception(f"فشل رفع الفيديو - {resp.status_code}: {resp.text}")

        return f"{self.url}/storage/v1/object/public/videos/{path}"