from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    credits: int = 3

class CourseCreate(CourseBase):
    video_path: Optional[str] = None  # ← إضافة جديدة


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    video_path: Optional[str] = None


class CourseResponse(CourseBase):
    id: int
    video_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True    