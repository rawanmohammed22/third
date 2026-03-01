# app/routers/auth_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth_schema import RegisterRequest, LoginRequest

router = APIRouter()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register(data)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(data)


@router.post("/logout")
def logout():
    # JWT stateless — الـ logout بيتعمل من الـ client بحذف التوكن
    return {"message": "تم تسجيل الخروج بنجاح"}