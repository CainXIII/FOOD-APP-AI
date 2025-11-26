"""
AI Chat models - Conversations and messages with RAG metadata
"""
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Chat(Base):
    """Chat conversations"""
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Conversation title (auto-generated or user-defined)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Context (cooking session, recipe, etc.)
    context_type: Mapped[Optional[str]] = mapped_column(String(50))  # session, recipe, general
    context_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    
    # Stats
    messages_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    last_message_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="chats")
    
    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at"
    )

    def __repr__(self) -> str:
        return f"<Chat {self.title or self.id}>"


class ChatMessage(Base):
    """Chat messages with RAG metadata"""
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    chat_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Message content
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user, assistant, system
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # RAG metadata
    rag_context: Mapped[Optional[dict]] = mapped_column(JSON)  # Retrieved sources
    rag_query: Mapped[Optional[str]] = mapped_column(Text)  # Enhanced query used
    
    # Token usage
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Voice input/output
    audio_url: Mapped[Optional[str]] = mapped_column(Text)  # If voice message
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    def __repr__(self) -> str:
        return f"<ChatMessage {self.role}>"
