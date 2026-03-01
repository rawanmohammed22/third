# app/dependencies.py

from sqlalchemy.orm import Session
from app.database import get_db
from app.services.student_service import StudentService
from app.controllers.student_controller import StudentController
from app.services.course_service import CourseService
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.utils.jwt import verify_token
from app.models.User import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = verify_token(credentials.credentials)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="المستخدم غير موجود"
        )
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="مش عندك صلاحية"
        )
    return current_user



def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    return CourseService(db)

def get_student_controller(db: Session = Depends(get_db)) -> StudentController:
    service = StudentService(db)
    return StudentController(service)