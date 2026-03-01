# app/schemas/student_schema.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0)
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True