from typing import List, Optional
from fastapi import HTTPException, UploadFile  # ← ضيف الاتنين
from sqlalchemy.orm import Session
from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import CourseCreate, CourseUpdate, CourseResponse
import os
import uuid

UPLOAD_DIR = "uploads/videos"
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/avi", "video/mkv", "video/mov"]


class CourseService:
    def __init__(self, db: Session):
        self.repo = CourseRepository(db)

    # ← دالة جديدة للفيديو
    async def save_video(self, video: UploadFile) -> str:
        if video.content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(
                status_code=400,
                detail="نوع الملف غير مدعوم. يرجى رفع فيديو mp4/avi/mkv/mov"
            )
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        ext = video.filename.split(".")[-1]
        video_path = f"{UPLOAD_DIR}/{uuid.uuid4()}.{ext}"

        with open(video_path, "wb") as f:
            f.write(await video.read())

        return video_path

    def get_all_courses(self) -> List[CourseResponse]:
        courses = self.repo.get_all()
        return [CourseResponse.model_validate(course) for course in courses]

    def get_course_by_id(self, course_id: int) -> Optional[CourseResponse]:
        course = self.repo.get_by_id(course_id)
        if course:
            return CourseResponse.model_validate(course)
        return None

    # ← بقت async وبتاخد video بدل video_path
    async def create_course(
        self,
        title: str,
        description: Optional[str] = None,
        credits: Optional[int] = None,
        video: Optional[UploadFile] = None,
    ) -> CourseResponse:
        if not title:
            raise ValueError("العنوان لا يمكن أن يكون فارغاً")

        if credits is None:
            credits = 3

        video_path = None
        if video:
            video_path = await self.save_video(video)

        data = CourseCreate(
            title=str(title),
            description=description,
            credits=int(credits),
            video_path=video_path,
        )

        course = self.repo.create(data)
        return CourseResponse.model_validate(course)

    # ← بقت async وبتاخد video بدل video_path
    async def update_course(
        self,
        course_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        credits: Optional[int] = None,
        video: Optional[UploadFile] = None,
    ) -> None:
        video_path = None
        if video:
            video_path = await self.save_video(video)

        data = CourseUpdate(
            title=title,
            description=description,
            credits=credits,
            video_path=video_path,
        )
        self.repo.update(course_id, data)

    def delete_course(self, course_id: int) -> bool:
        return self.repo.delete(course_id)