"""
AI Chat schemas
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema, UUIDMixin, TimestampMixin


# Request Schemas
class ChatCreate(BaseModel):
    """Create new chat session"""
    title: Optional[str] = Field(None, max_length=200)
    context: Optional[Dict[str, Any]] = None  # Recipe context, etc.


class ChatMessageCreate(BaseModel):
    """Send message in chat"""
    content: str = Field(..., min_length=1, max_length=2000)
    context: Optional[Dict[str, Any]] = None


class ChatMessageStream(BaseModel):
    """Request streaming chat response"""
    content: str = Field(..., min_length=1, max_length=2000)
    use_rag: bool = True  # Whether to use RAG context


class RAGQuery(BaseModel):
    """Direct RAG query (no chat history)"""
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(5, ge=1, le=20)
    min_similarity: float = Field(0.7, ge=0, le=1)


# Response Schemas
class ChatResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Chat session response"""
    user_id: UUID
    title: str
    last_message_at: Optional[datetime]
    message_count: int = 0
    is_active: bool


class ChatMessageResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Chat message response"""
    chat_id: UUID
    role: str  # 'user' or 'assistant'
    content: str
    tokens_used: Optional[int]
    rag_context_used: Optional[Dict[str, Any]]
    feedback: Optional[str]  # 'positive', 'negative', None


class ChatDetailResponse(ChatResponse):
    """Chat with messages"""
    messages: List[ChatMessageResponse]


class ChatStreamChunk(BaseModel):
    """Streaming chat chunk"""
    chunk: str
    is_final: bool = False
    metadata: Optional[Dict[str, Any]] = None


class RAGContextItem(BaseModel):
    """RAG retrieved context item"""
    recipe_id: Optional[UUID] = None
    ingredient_id: Optional[UUID] = None
    title: str
    content: str
    similarity_score: float


class RAGResponse(BaseModel):
    """RAG query response"""
    query: str
    contexts: List[RAGContextItem]
    answer: str
    tokens_used: int
