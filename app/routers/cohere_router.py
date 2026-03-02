# app/routers/cohere_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.cohere_schema import ChatRequest, ChatResponse
from app.schemas.cohere_schema import ChatResponse as ChatHistoryResponse
from app.services.cohere_service import CohereService
from app.dependencies import get_current_user
from app.models.User import User
from app.repositories.chat_repository import ChatRepository
from app.database import get_db
from sqlalchemy.orm import Session
from app.Clients.cohere_client import get_cohere_client


router = APIRouter(prefix="/cohere", tags=["Cohere AI"])


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat_with_cohere(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint:
    - Authenticates user via JWT token
    - Creates new chat if no chat_id provided
    - Verifies ownership if chat_id is provided
    - Calls Cohere with full history
    - Saves messages to database
    - Returns reply and updated history
    """
    service = CohereService(client=get_cohere_client(), db=db)
    return service.chat(request=request, user_id=current_user.id)


@router.get("/history/{chat_id}", response_model=ChatHistoryResponse, status_code=status.HTTP_200_OK)
def get_chat_history(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get full chat history for a specific chat ID
    - Verifies user owns this chat
    - Returns messages sorted by creation time
    """
    repo = ChatRepository(db)
    chat = repo.get_chat_by_id(chat_id)
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    if chat.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this chat")
    
    history = repo.get_chat_history(chat_id)
    
    return ChatHistoryResponse(
        id=chat.id,
        user_id=chat.user_id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        messages=history
    )


@router.get("/my-chats", response_model=List[ChatHistoryResponse], status_code=status.HTTP_200_OK)
def get_my_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of all chats belonging to the current user
    - Returns basic chat info (no full messages)
    """
    repo = ChatRepository(db)
    chats = repo.get_user_chats(user_id=current_user.id)
    
    return chats