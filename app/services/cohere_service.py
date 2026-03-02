# app/services/cohere_service.py
from typing import Optional, List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.Clients.cohere_client import CohereClient, get_cohere_client
from app.schemas.cohere_schema import ChatRequest, ChatResponse
from app.repositories.chat_repository import ChatRepository
from app.database import get_db

class CohereService:
    def __init__(
        self,
        client: CohereClient = Depends(get_cohere_client),
        db: Session = Depends(get_db)
    ):
        self.client = client
        self.repo = ChatRepository(db)

    def chat(
        self,
        request: ChatRequest,
        user_id: int
    ) -> ChatResponse:
        """
        Handle chat request:
        - Create new chat or use existing one
        - Verify ownership
        - Fetch history from DB
        - Call Cohere with full history
        - Save messages to DB
        - Return updated response
        """
        chat_id = request.chat_id

        if chat_id:
            # Fetch existing chat and verify ownership
            chat = self.repo.get_chat_by_id(chat_id)
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")
            if chat.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not own this chat")
        else:
            # Create a new chat for this user
            chat = self.repo.create_chat(user_id=user_id, title="New Conversation")
            chat_id = chat.id

        # Get history from database
        history = self.repo.get_chat_history(chat_id)

        # Call Cohere with full history + new user message
        reply = self.client.chat(
            messages=history + [{"role": "user", "content": request.message}],
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Save both the user message and AI reply to database
        self.repo.save_message(chat_id, "user", request.message)
        self.repo.save_message(chat_id, "assistant", reply)

        # Fetch updated history from DB
        updated_history = self.repo.get_chat_history(chat_id)

        return ChatResponse(
            reply=reply,
            history=updated_history,
            chat_id=chat_id
        )