"""
Session API - Cooking session management endpoints
Handles session creation, navigation, and state management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.services.session_service import session_service
from app.models.database import CookingSession
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


# Request/Response Models
class CreateSessionRequest(BaseModel):
    """Create session request"""
    recipe_id: int


class SessionResponse(BaseModel):
    """Session response"""
    id: int
    user_id: int
    recipe_id: int
    status: str
    current_step: int
    total_steps: int
    started_at: datetime
    paused_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InstructionResponse(BaseModel):
    """Instruction response"""
    step: int
    instruction: str
    current_step: int
    total_steps: int


@router.post("", response_model=SessionResponse)
async def create_cooking_session(
    request: CreateSessionRequest,
    user_id: int = 1,  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new cooking session
    
    Args:
        request: Create session request with recipe ID
        user_id: User ID (from auth)
        db: Database session
        
    Returns:
        Created session
    """
    try:
        session = await session_service.create_session(
            db,
            user_id,
            request.recipe_id
        )
        
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=SessionResponse)
async def get_cooking_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get session by ID
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Session details
    """
    try:
        session = await session_service.get_session(db, session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionResponse.model_validate(session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/active", response_model=Optional[SessionResponse])
async def get_active_session(
    user_id: int = 1,  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Get active session for current user
    
    Args:
        user_id: User ID (from auth)
        db: Database session
        
    Returns:
        Active session or None
    """
    try:
        session = await session_service.get_active_session(db, user_id)
        
        if not session:
            return None
        
        return SessionResponse.model_validate(session)
    except Exception as e:
        logger.error(f"Error getting active session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/instruction", response_model=InstructionResponse)
async def get_current_instruction(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get current cooking instruction
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Current instruction
    """
    try:
        instruction = await session_service.get_current_instruction(db, session_id)
        
        if not instruction:
            raise HTTPException(status_code=404, detail="Instruction not found")
        
        return InstructionResponse(**instruction)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting instruction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/next", response_model=SessionResponse)
async def next_step(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Move to next step
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Updated session
    """
    try:
        session = await session_service.next_step(db, session_id)
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error moving to next step: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/previous", response_model=SessionResponse)
async def previous_step(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Move to previous step
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Updated session
    """
    try:
        session = await session_service.previous_step(db, session_id)
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error moving to previous step: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/pause", response_model=SessionResponse)
async def pause_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Pause cooking session
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Updated session
    """
    try:
        session = await session_service.pause_session(db, session_id)
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error pausing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/resume", response_model=SessionResponse)
async def resume_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Resume paused session
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Updated session
    """
    try:
        session = await session_service.resume_session(db, session_id)
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error resuming session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/complete", response_model=SessionResponse)
async def complete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Complete cooking session
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        Completed session
    """
    try:
        session = await session_service.complete_session(db, session_id)
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error completing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
