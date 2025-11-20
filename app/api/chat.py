"""
Chat API - RAG-powered chat assistant endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.orchestration.chat_orchestrator import chat_orchestrator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models
class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role (user/assistant)", example="user")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message", example="Caramel bị đắng, sửa sao?")
    chat_history: Optional[List[ChatMessage]] = Field(None, description="Previous chat history")
    user_id: Optional[str] = Field(None, description="User ID for personalization")

class ChatSource(BaseModel):
    type: str = Field(..., description="Source type (recipe/technique/tip)")
    title: str = Field(..., description="Source title")

class ChatResponse(BaseModel):
    success: bool
    answer: str
    intent: str
    used_rag: bool
    used_tools: bool
    sources: List[ChatSource]
    timestamp: str

class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessage]
    total: int

# Endpoints
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with AI cooking assistant powered by RAG
    
    Features:
    - Recipe search and recommendations
    - Cooking technique explanations
    - Ingredient substitutions
    - Menu generation
    - Unit conversions
    - Troubleshooting advice
    
    The assistant uses RAG (Retrieval Augmented Generation) to provide
    accurate answers based on the knowledge base.
    
    - **message**: User question or request
    - **chat_history**: Optional previous conversation history
    - **user_id**: Optional user ID for personalized responses
    """
    try:
        logger.info(f"Chat request: {request.message[:100]}...")
        
        # Convert chat history to dict format
        history = None
        if request.chat_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
            ]
        
        # Process chat
        result = await chat_orchestrator.chat(
            message=request.message,
            chat_history=history,
            user_id=request.user_id
        )
        
        # Convert sources to response model
        sources = [
            ChatSource(type=src["type"], title=src["title"])
            for src in result.get("sources", [])
        ]
        
        return ChatResponse(
            success=True,
            answer=result["answer"],
            intent=result["intent"],
            used_rag=result["used_rag"],
            used_tools=result["used_tools"],
            sources=sources,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý chat: {str(e)}")

class SimpleChatRequest(BaseModel):
    """Simple chat request"""
    message: str

@router.post("/chat/simple")
async def chat_simple(request: SimpleChatRequest):
    """
    Simple chat without RAG for quick questions
    
    - **message**: User message
    """
    try:
        logger.info(f"Simple chat: {request.message[:100]}...")
        
        answer = await chat_orchestrator.chat_simple(request.message)
        
        return {
            "success": True,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in simple chat: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý chat: {str(e)}")

@router.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: str,
    limit: int = 50
):
    """
    Get chat history for a user
    
    Note: This endpoint requires database integration.
    Currently returns a placeholder response.
    
    - **user_id**: User ID (query parameter)
    - **limit**: Maximum number of messages to return
    """
    # Placeholder - requires database integration
    logger.info(f"Fetching chat history for user: {user_id}")
    
    return ChatHistoryResponse(
        messages=[],
        total=0
    )

@router.delete("/chat/history")
async def clear_chat_history(user_id: str):
    """
    Clear chat history for a user
    
    Note: This endpoint requires database integration.
    
    - **user_id**: User ID (query parameter)
    """
    # Placeholder - requires database integration
    logger.info(f"Clearing chat history for user: {user_id}")
    
    return {
        "success": True,
        "message": "Chat history cleared"
    }
