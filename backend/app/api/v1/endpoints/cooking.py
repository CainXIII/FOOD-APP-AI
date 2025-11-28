"""
Cooking session endpoints - Manage cooking sessions and timers
"""
from typing import Any, Optional, List
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.recipe import Recipe, RecipeStep
from app.models.cooking import CookingSession, CookingTimer, SessionStatus, TimerStatus
from app.schemas.base import MessageResponse
from app.core.deps import get_current_user


router = APIRouter()


# ============================================================================
# COOKING SESSIONS
# ============================================================================

@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def start_cooking_session(
    recipe_id: UUID,
    servings: Optional[int] = Query(None, description="Override default servings"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Start a new cooking session for a recipe
    
    - **recipe_id**: Recipe UUID to cook
    - **servings**: Optional servings override (defaults to recipe servings)
    """
    # Get recipe with steps
    result = await db.execute(
        select(Recipe)
        .options(selectinload(Recipe.steps))
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Count steps
    steps_result = await db.execute(
        select(func.count())
        .select_from(RecipeStep)
        .where(RecipeStep.recipe_id == recipe_id)
    )
    total_steps = steps_result.scalar() or 0
    
    if total_steps == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe has no cooking steps"
        )
    
    # Check for existing active session
    existing_result = await db.execute(
        select(CookingSession).where(
            CookingSession.user_id == current_user.id,
            CookingSession.recipe_id == recipe_id,
            CookingSession.status.in_([SessionStatus.IN_PROGRESS, SessionStatus.PAUSED])
        )
    )
    existing_session = existing_result.scalar_one_or_none()
    
    if existing_session:
        return {
            "id": existing_session.id,
            "user_id": existing_session.user_id,
            "recipe_id": existing_session.recipe_id,
            "status": existing_session.status.value,
            "current_step": existing_session.current_step,
            "total_steps": existing_session.total_steps,
            "servings": existing_session.servings,
            "started_at": existing_session.started_at,
            "message": "Active session already exists for this recipe"
        }
    
    # Create new session
    new_session = CookingSession(
        user_id=current_user.id,
        recipe_id=recipe_id,
        status=SessionStatus.IN_PROGRESS,
        current_step=1,
        total_steps=total_steps,
        servings=servings if servings else recipe.servings,
        session_data={}
    )
    
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return {
        "id": new_session.id,
        "user_id": new_session.user_id,
        "recipe_id": new_session.recipe_id,
        "status": new_session.status.value,
        "current_step": new_session.current_step,
        "total_steps": new_session.total_steps,
        "servings": new_session.servings,
        "started_at": new_session.started_at,
        "message": "Cooking session started successfully"
    }


@router.get("/sessions")
async def get_cooking_sessions(
    status_filter: Optional[str] = Query(None, description="Filter by status: in_progress, paused, completed, cancelled"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Get user's cooking sessions
    
    - **status_filter**: Optional status filter
    - **page**: Page number
    - **page_size**: Items per page (1-100)
    """
    # Build query
    query = select(CookingSession).where(CookingSession.user_id == current_user.id)
    
    # Apply status filter
    if status_filter:
        try:
            status_enum = SessionStatus(status_filter)
            query = query.where(CookingSession.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}"
            )
    
    # Order by started_at descending
    query = query.order_by(CookingSession.started_at.desc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # Execute with relationships
    result = await db.execute(
        query.options(
            selectinload(CookingSession.timers)
        )
    )
    sessions = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(CookingSession).where(
        CookingSession.user_id == current_user.id
    )
    if status_filter:
        count_query = count_query.where(CookingSession.status == status_enum)
    
    count_result = await db.execute(count_query)
    total_count = count_result.scalar()
    
    # Format response
    sessions_data = []
    for session in sessions:
        sessions_data.append({
            "id": session.id,
            "recipe_id": session.recipe_id,
            "status": session.status.value,
            "current_step": session.current_step,
            "total_steps": session.total_steps,
            "servings": session.servings,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
            "paused_at": session.paused_at,
            "active_timers": sum(1 for t in session.timers if t.status == TimerStatus.RUNNING)
        })
    
    return {
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "sessions": sessions_data
    }


@router.get("/sessions/active")
async def get_active_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get user's active cooking sessions (in_progress or paused)"""
    result = await db.execute(
        select(CookingSession)
        .where(
            CookingSession.user_id == current_user.id,
            CookingSession.status.in_([SessionStatus.IN_PROGRESS, SessionStatus.PAUSED])
        )
        .order_by(CookingSession.started_at.desc())
        .options(selectinload(CookingSession.timers))
    )
    sessions = result.scalars().all()
    
    sessions_data = []
    for session in sessions:
        sessions_data.append({
            "id": session.id,
            "recipe_id": session.recipe_id,
            "status": session.status.value,
            "current_step": session.current_step,
            "total_steps": session.total_steps,
            "servings": session.servings,
            "started_at": session.started_at,
            "paused_at": session.paused_at,
            "active_timers": sum(1 for t in session.timers if t.status == TimerStatus.RUNNING),
            "timers": [
                {
                    "id": timer.id,
                    "name": timer.name,
                    "duration_seconds": timer.duration_seconds,
                    "elapsed_seconds": timer.elapsed_seconds,
                    "status": timer.status.value,
                    "step_number": timer.step_number
                }
                for timer in session.timers
            ]
        })
    
    return {
        "total": len(sessions_data),
        "sessions": sessions_data
    }


@router.get("/sessions/{session_id}")
async def get_cooking_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get cooking session details with recipe steps"""
    result = await db.execute(
        select(CookingSession)
        .where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
        .options(selectinload(CookingSession.timers))
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooking session not found"
        )
    
    # Get recipe steps
    steps_result = await db.execute(
        select(RecipeStep)
        .where(RecipeStep.recipe_id == session.recipe_id)
        .order_by(RecipeStep.step_number.asc())
    )
    steps = steps_result.scalars().all()
    
    return {
        "id": session.id,
        "recipe_id": session.recipe_id,
        "status": session.status.value,
        "current_step": session.current_step,
        "total_steps": session.total_steps,
        "servings": session.servings,
        "started_at": session.started_at,
        "completed_at": session.completed_at,
        "paused_at": session.paused_at,
        "session_data": session.session_data,
        "steps": [
            {
                "step_number": step.step_number,
                "title_en": step.title_en,
                "title_vi": step.title_vi,
                "instruction_en": step.instruction_en,
                "instruction_vi": step.instruction_vi,
                "duration_minutes": step.duration_minutes,
                "image_url": step.image_url,
                "is_current": step.step_number == session.current_step
            }
            for step in steps
        ],
        "timers": [
            {
                "id": timer.id,
                "name": timer.name,
                "duration_seconds": timer.duration_seconds,
                "elapsed_seconds": timer.elapsed_seconds,
                "status": timer.status.value,
                "step_number": timer.step_number,
                "started_at": timer.started_at,
                "completed_at": timer.completed_at
            }
            for timer in session.timers
        ]
    }


@router.put("/sessions/{session_id}/progress")
async def update_session_progress(
    session_id: UUID,
    action: str = Query(..., description="Action: next_step, previous_step, go_to_step, complete"),
    step_number: Optional[int] = Query(None, description="Target step number for go_to_step action"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update cooking session progress
    
    - **action**: Action to perform
      - next_step: Move to next step
      - previous_step: Move to previous step
      - go_to_step: Jump to specific step (requires step_number)
      - complete: Mark session as completed
    """
    # Get session
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooking session not found"
        )
    
    if session.status == SessionStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is already completed"
        )
    
    if session.status == SessionStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is cancelled"
        )
    
    # Perform action
    if action == "next_step":
        if session.current_step < session.total_steps:
            session.current_step += 1
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already at last step"
            )
    
    elif action == "previous_step":
        if session.current_step > 1:
            session.current_step -= 1
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already at first step"
            )
    
    elif action == "go_to_step":
        if step_number is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="step_number required for go_to_step action"
            )
        if step_number < 1 or step_number > session.total_steps:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid step number. Must be between 1 and {session.total_steps}"
            )
        session.current_step = step_number
    
    elif action == "complete":
        session.status = SessionStatus.COMPLETED
        session.completed_at = datetime.utcnow()
        session.current_step = session.total_steps
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action: {action}. Use: next_step, previous_step, go_to_step, complete"
        )
    
    await db.commit()
    await db.refresh(session)
    
    return {
        "id": session.id,
        "recipe_id": session.recipe_id,
        "status": session.status.value,
        "current_step": session.current_step,
        "total_steps": session.total_steps,
        "completed_at": session.completed_at,
        "message": f"Session updated: {action}"
    }


@router.put("/sessions/{session_id}/pause")
async def pause_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Pause cooking session and all running timers"""
    result = await db.execute(
        select(CookingSession)
        .where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
        .options(selectinload(CookingSession.timers))
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooking session not found"
        )
    
    if session.status != SessionStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only pause sessions that are in progress"
        )
    
    # Pause session
    session.status = SessionStatus.PAUSED
    session.paused_at = datetime.utcnow()
    
    # Pause all running timers
    paused_timers = 0
    for timer in session.timers:
        if timer.status == TimerStatus.RUNNING:
            timer.status = TimerStatus.PAUSED
            timer.paused_at = datetime.utcnow()
            paused_timers += 1
    
    await db.commit()
    
    return {
        "id": session.id,
        "status": session.status.value,
        "paused_at": session.paused_at,
        "paused_timers": paused_timers,
        "message": "Session paused successfully"
    }


@router.put("/sessions/{session_id}/resume")
async def resume_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Resume paused cooking session and timers"""
    result = await db.execute(
        select(CookingSession)
        .where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
        .options(selectinload(CookingSession.timers))
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooking session not found"
        )
    
    if session.status != SessionStatus.PAUSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only resume paused sessions"
        )
    
    # Resume session
    session.status = SessionStatus.IN_PROGRESS
    session.paused_at = None
    
    # Resume paused timers
    resumed_timers = 0
    for timer in session.timers:
        if timer.status == TimerStatus.PAUSED:
            timer.status = TimerStatus.RUNNING
            timer.paused_at = None
            resumed_timers += 1
    
    await db.commit()
    
    return {
        "id": session.id,
        "status": session.status.value,
        "resumed_timers": resumed_timers,
        "message": "Session resumed successfully"
    }


@router.delete("/sessions/{session_id}")
async def cancel_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """Cancel cooking session (keeps record but marks as cancelled)"""
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooking session not found"
        )
    
    session.status = SessionStatus.CANCELLED
    
    await db.commit()
    
    return {
        "message": "Cooking session cancelled successfully"
    }


# ============================================================================
# TIMERS
# ============================================================================

@router.post("/timers", status_code=status.HTTP_201_CREATED)
async def create_timer(
    session_id: UUID,
    name: str = Query(..., min_length=1, max_length=255),
    duration_minutes: int = Query(..., ge=1, description="Timer duration in minutes"),
    step_number: Optional[int] = Query(None, description="Associated step number"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create a timer for a cooking session
    
    - **session_id**: Cooking session UUID
    - **name**: Timer name (e.g., "Simmer broth", "Let dough rise")
    - **duration_minutes**: Timer duration in minutes
    - **step_number**: Optional step number reference
    """
    # Verify session belongs to user
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cooking session not found"
        )
    
    if session.status not in [SessionStatus.IN_PROGRESS, SessionStatus.PAUSED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add timers to completed or cancelled sessions"
        )
    
    # Create timer
    new_timer = CookingTimer(
        session_id=session_id,
        name=name,
        duration_seconds=duration_minutes * 60,
        elapsed_seconds=0,
        status=TimerStatus.RUNNING if session.status == SessionStatus.IN_PROGRESS else TimerStatus.PAUSED,
        step_number=step_number
    )
    
    db.add(new_timer)
    await db.commit()
    await db.refresh(new_timer)
    
    return {
        "id": new_timer.id,
        "session_id": new_timer.session_id,
        "name": new_timer.name,
        "duration_seconds": new_timer.duration_seconds,
        "duration_minutes": duration_minutes,
        "elapsed_seconds": new_timer.elapsed_seconds,
        "status": new_timer.status.value,
        "step_number": new_timer.step_number,
        "started_at": new_timer.started_at,
        "message": "Timer created successfully"
    }


@router.get("/timers/{timer_id}")
async def get_timer(
    timer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get timer details"""
    result = await db.execute(
        select(CookingTimer)
        .join(CookingSession)
        .where(
            CookingTimer.id == timer_id,
            CookingSession.user_id == current_user.id
        )
    )
    timer = result.scalar_one_or_none()
    
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found"
        )
    
    # Calculate remaining time
    remaining_seconds = max(0, timer.duration_seconds - timer.elapsed_seconds)
    
    return {
        "id": timer.id,
        "session_id": timer.session_id,
        "name": timer.name,
        "duration_seconds": timer.duration_seconds,
        "elapsed_seconds": timer.elapsed_seconds,
        "remaining_seconds": remaining_seconds,
        "status": timer.status.value,
        "step_number": timer.step_number,
        "started_at": timer.started_at,
        "completed_at": timer.completed_at,
        "paused_at": timer.paused_at
    }


@router.put("/timers/{timer_id}/update")
async def update_timer(
    timer_id: UUID,
    elapsed_seconds: int = Query(..., ge=0, description="Current elapsed time in seconds"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update timer elapsed time (called by client periodically)
    
    - **elapsed_seconds**: Current elapsed time in seconds
    """
    result = await db.execute(
        select(CookingTimer)
        .join(CookingSession)
        .where(
            CookingTimer.id == timer_id,
            CookingSession.user_id == current_user.id
        )
    )
    timer = result.scalar_one_or_none()
    
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found"
        )
    
    # Update elapsed time
    timer.elapsed_seconds = elapsed_seconds
    
    # Auto-complete if duration reached
    if elapsed_seconds >= timer.duration_seconds and timer.status == TimerStatus.RUNNING:
        timer.status = TimerStatus.COMPLETED
        timer.completed_at = datetime.utcnow()
    
    await db.commit()
    
    remaining_seconds = max(0, timer.duration_seconds - timer.elapsed_seconds)
    
    return {
        "id": timer.id,
        "elapsed_seconds": timer.elapsed_seconds,
        "remaining_seconds": remaining_seconds,
        "status": timer.status.value,
        "completed_at": timer.completed_at
    }


@router.put("/timers/{timer_id}/pause")
async def pause_timer(
    timer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Pause a running timer"""
    result = await db.execute(
        select(CookingTimer)
        .join(CookingSession)
        .where(
            CookingTimer.id == timer_id,
            CookingSession.user_id == current_user.id
        )
    )
    timer = result.scalar_one_or_none()
    
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found"
        )
    
    if timer.status != TimerStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only pause running timers"
        )
    
    timer.status = TimerStatus.PAUSED
    timer.paused_at = datetime.utcnow()
    
    await db.commit()
    
    return {
        "id": timer.id,
        "status": timer.status.value,
        "paused_at": timer.paused_at,
        "message": "Timer paused"
    }


@router.put("/timers/{timer_id}/resume")
async def resume_timer(
    timer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Resume a paused timer"""
    result = await db.execute(
        select(CookingTimer)
        .join(CookingSession)
        .where(
            CookingTimer.id == timer_id,
            CookingSession.user_id == current_user.id
        )
    )
    timer = result.scalar_one_or_none()
    
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found"
        )
    
    if timer.status != TimerStatus.PAUSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only resume paused timers"
        )
    
    timer.status = TimerStatus.RUNNING
    timer.paused_at = None
    
    await db.commit()
    
    return {
        "id": timer.id,
        "status": timer.status.value,
        "message": "Timer resumed"
    }


@router.delete("/timers/{timer_id}")
async def cancel_timer(
    timer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """Cancel/delete a timer"""
    result = await db.execute(
        select(CookingTimer)
        .join(CookingSession)
        .where(
            CookingTimer.id == timer_id,
            CookingSession.user_id == current_user.id
        )
    )
    timer = result.scalar_one_or_none()
    
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found"
        )
    
    await db.delete(timer)
    await db.commit()
    
    return {
        "message": "Timer cancelled successfully"
    }
