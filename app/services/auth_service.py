from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.Student import Student
from app.models.User import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.utils.jwt import create_access_token, create_refresh_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: RegisterRequest) -> TokenResponse:
        # bcrypt supports passwords up to 72 bytes only
        if len(data.password.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="???? ?????? ????? ???. ???? ?????? 72 ????.",
            )

        if self.db.query(User).filter(User.email == data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="??????? ???? ??????",
            )

        user = User(
            email=data.email,
            password=pwd_context.hash(data.password),
        )
        self.db.add(user)
        self.db.flush()

        student = Student(name=data.name, email=data.email, user_id=user.id)
        self.db.add(student)
        self.db.commit()

        token_data = {"sub": str(user.id), "email": user.email}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.db.query(User).filter(User.email == data.email).first()

        if not user or not pwd_context.verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="??????? ?? ???????? ???",
            )

        token_data = {"sub": str(user.id), "email": user.email}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )
