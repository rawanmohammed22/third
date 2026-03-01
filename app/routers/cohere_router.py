# app/routers/cohere_router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.Clients.cohere_client import CohereClient, get_cohere_client

router = APIRouter(
    prefix="/cohere",
    tags=["Cohere AI"]
)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="الرسالة اللي هتبعتيها للـ AI")
    model: str = Field("command-r-plus-08-2024", description="اسم النموذج")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="درجة الإبداع")
    max_tokens: int = Field(500, ge=50, description="أقصى عدد كلمات في الرد")

@router.post("/chat", summary="محادثة بسيطة مع Cohere")
async def simple_chat(
    request: ChatRequest,
    client: CohereClient = Depends(get_cohere_client)
):
    """
    ابعتي رسالة، و Cohere هيرد عليكِ مباشرة (بدون حفظ تاريخ في الوقت الحالي)
    
    مثال body:
    {
      "message": "ازيك؟ عايزة أتعلم بايثون منين؟",
      "model": "command-r-plus-08-2024",
      "temperature": 0.8
    }
    """
    try:
        reply = client.chat(
            message=request.message,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return {
            "reply": reply,
            "model_used": request.model
        }
    except RuntimeError as e:
        return {"error": str(e)}