from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    model: Optional[str] = "command-r-plus-08-2024"
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(500, ge=50)
    session_id: Optional[str] = None  # ← مهم: لو مش موجود، نستخدم default
    chat_id: Optional[int] = Field(None, description="Chat ID (optional - if not provided, create new chat)")

class ChatResponse(BaseModel):
    reply: Optional[str] = None
    history: Optional[List[dict[str, str]]] = None
    chat_id: Optional[int] = None
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
   