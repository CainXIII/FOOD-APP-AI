"""
Chat endpoints - AI chat with RAG integration
"""
from typing import Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.chat import Chat, ChatMessage
from app.schemas.chat import (
    ChatCreate,
    ChatMessageCreate,
    ChatResponse,
    ChatDetailResponse,
    ChatMessageResponse,
    ChatMessageStream,
    RAGQuery,
    RAGResponse
)
from app.schemas.base import MessageResponse
from app.core.deps import get_current_user
from app.services.rag import get_rag_context, generate_chat_response


router = APIRouter()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new chat session
    
    - **title**: Optional chat title
    - **context**: Optional context (recipe being viewed, etc.)
    """
    chat = Chat(
        user_id=current_user.id,
        title=chat_data.title or "New Conversation",
        messages_count=0
    )
    
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    
    return {
        "id": chat.id,
        "user_id": chat.user_id,
        "title": chat.title,
        "context_type": chat.context_type,
        "context_id": chat.context_id,
        "messages_count": chat.messages_count,
        "created_at": chat.created_at,
        "last_message_at": chat.last_message_at
    }


@router.get("", response_model=list)
async def list_chats(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's chat sessions
    
    - **page**: Page number
    - **page_size**: Items per page
    """
    offset = (page - 1) * page_size
    
    result = await db.execute(
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.last_message_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    chats = result.scalars().all()
    
    return [
        {
            "id": chat.id,
            "user_id": chat.user_id,
            "title": chat.title,
            "context_type": chat.context_type,
            "context_id": chat.context_id,
            "messages_count": chat.messages_count,
            "created_at": chat.created_at,
            "last_message_at": chat.last_message_at
        }
        for chat in chats
    ]


@router.get("/{chat_id}", response_model=dict)
async def get_chat(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get chat session with messages
    """
    result = await db.execute(
        select(Chat)
        .options(selectinload(Chat.messages))
        .where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    messages = [
        {
            "id": msg.id,
            "chat_id": msg.chat_id,
            "role": msg.role,
            "content": msg.content,
            "rag_context": msg.rag_context,
            "rag_query": msg.rag_query,
            "prompt_tokens": msg.prompt_tokens,
            "completion_tokens": msg.completion_tokens,
            "total_tokens": msg.total_tokens,
            "audio_url": msg.audio_url,
            "created_at": msg.created_at
        }
        for msg in chat.messages
    ]
    
    return {
        "id": chat.id,
        "user_id": chat.user_id,
        "title": chat.title,
        "context_type": chat.context_type,
        "context_id": chat.context_id,
        "messages_count": chat.messages_count,
        "created_at": chat.created_at,
        "last_message_at": chat.last_message_at,
        "messages": messages
    }


@router.delete("/{chat_id}", response_model=MessageResponse)
async def delete_chat(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete chat session
    """
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    await db.execute(delete(Chat).where(Chat.id == chat_id))
    await db.commit()
    
    return {
        "message": "Chat deleted successfully",
        "detail": f"Chat '{chat.title}' has been deleted"
    }


@router.post("/{chat_id}/messages", response_model=dict)
async def send_message(
    chat_id: UUID,
    message_data: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Send message to chat (non-streaming)
    
    - **content**: User message
    - **context**: Optional context data
    """
    # Verify chat belongs to user
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Save user message
    user_message = ChatMessage(
        chat_id=chat_id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    await db.flush()  # Get user_message.id
    
    # Get RAG context from database
    rag_context = await get_rag_context(
        query=message_data.content,
        db=db,
        top_k=3
    )
    
    # Get conversation history
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(10)  # Last 10 messages for context
    )
    history = result.scalars().all()
    
    # Build message list for AI
    messages = []
    for msg in history:
        if msg.id != user_message.id:  # Exclude current user message
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
    
    # Add current user message
    messages.append({
        "role": "user",
        "content": message_data.content
    })
    
    # Generate AI response using OpenAI
    assistant_content = await generate_chat_response(
        messages=messages,
        rag_context=rag_context,
        stream=False
    )
    
    # Save assistant message
    assistant_message = ChatMessage(
        chat_id=chat_id,
        role="assistant",
        content=assistant_content,
        rag_context=rag_context,
        rag_query=message_data.content,
        prompt_tokens=0,  # TODO: Extract from OpenAI response
        completion_tokens=0,
        total_tokens=0
    )
    db.add(assistant_message)
    
    # Update chat stats
    chat.messages_count += 2
    from datetime import datetime
    chat.last_message_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(assistant_message)
    
    return {
        "id": assistant_message.id,
        "chat_id": assistant_message.chat_id,
        "role": assistant_message.role,
        "content": assistant_message.content,
        "rag_context": assistant_message.rag_context,
        "rag_query": assistant_message.rag_query,
        "prompt_tokens": assistant_message.prompt_tokens,
        "completion_tokens": assistant_message.completion_tokens,
        "total_tokens": assistant_message.total_tokens,
        "audio_url": assistant_message.audio_url,
        "created_at": assistant_message.created_at
    }


@router.post("/{chat_id}/stream")
async def stream_message(
    chat_id: UUID,
    message_data: ChatMessageStream,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> StreamingResponse:
    """
    Send message with streaming response
    
    Returns Server-Sent Events (SSE) stream
    """
    # Verify chat belongs to user
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    async def event_generator():
        """Generate SSE events"""
        import json
        
        # Mock streaming response
        response_text = "I'm here to help you with cooking! This is a mock streaming response. RAG integration is pending."
        
        # Stream word by word
        words = response_text.split()
        for word in words:
            chunk = {
                "type": "token",
                "content": word + " "
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            
            # Small delay for streaming effect
            import asyncio
            await asyncio.sleep(0.1)
        
        # Send done event
        done_chunk = {
            "type": "done",
            "message_id": str(chat_id)
        }
        yield f"data: {json.dumps(done_chunk)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@router.post("/rag/query", response_model=dict)
async def rag_query(
    query_data: RAGQuery,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Direct RAG query without chat history
    
    - **query**: Search query
    - **top_k**: Number of results
    - **min_similarity**: Minimum similarity threshold
    """
    # Mock RAG response
    return {
        "query": query_data.query,
        "contexts": [
            {
                "recipe_id": None,
                "ingredient_id": None,
                "title": "Mock Recipe",
                "content": "This is a mock RAG context. Real implementation pending.",
                "similarity_score": 0.95
            }
        ],
        "answer": f"Based on your query '{query_data.query}', here's what I found... (Mock RAG response)",
        "tokens_used": 200
    }
