from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from app.services.course_service import CourseService
from app.dependencies import get_course_service
from app.dependencies import get_current_user , get_admin_user
from app.models.User import User

router = APIRouter()


@router.get("/")
def get_all_courses(
    current_user: User = Depends(get_current_user), 
    service: CourseService = Depends(get_course_service)
):
    return service.get_all_courses()


@router.get("/{course_id}")
def get_course(
    course_id: int,
     current_user: User = Depends(get_current_user), 
    service: CourseService = Depends(get_course_service)
):
    return service.get_course_by_id(course_id)


@router.post("/")
async def create_course(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    credits: int = Form(3),
    video: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_admin_user),
    service: CourseService = Depends(get_course_service)
):
    return await service.create_course(
        title=title,
        description=description,
        credits=credits,
        video=video
    )


@router.put("/{course_id}")
async def update_course(
    course_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    credits: Optional[int] = Form(None),
    video: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_admin_user),
    service: CourseService = Depends(get_course_service)
):
    await service.update_course(
        course_id=course_id,
        title=title,
        description=description,
        credits=credits,
        video=video
    )
    return {"message": "تم تحديث الكورس بنجاح"}


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    current_user: User = Depends(get_admin_user),
    service: CourseService = Depends(get_course_service)
):
    return service.delete_course(course_id)