

# app/repositories/chat_repository.py
from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.chat_message import ChatMessage
from typing import List, Optional

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, user_id: int, title: str = "New Conversation") -> Chat:
        """
        Create a new chat for the given user.
        """
        chat = Chat(user_id=user_id, title=title)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def get_chat_history(self, chat_id: int) -> List[dict]:
        messages = self.db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at).all()
        return [{"role": m.role, "content": m.content} for m in messages]

    def save_message(self, chat_id: int, role: str, content: str):
        message = ChatMessage(chat_id=chat_id, role=role, content=content)
        self.db.add(message)
        self.db.commit()

    def get_user_chats(self, user_id: int) -> List[Chat]:
        return (
            self.db.query(Chat)
            .filter(Chat.user_id == user_id)
            .order_by(Chat.updated_at.desc())
            .all()
        )