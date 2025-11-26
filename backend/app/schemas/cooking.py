"""
Cooking session schemas
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema, UUIDMixin, TimestampMixin


# Enums
class SessionStatus(str):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TimerStatus(str):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Request Schemas
class CookingSessionCreate(BaseModel):
    """Start cooking session"""
    recipe_id: UUID
    servings: int = Field(..., ge=1)
    notes: Optional[str] = Field(None, max_length=500)


class CookingSessionUpdate(BaseModel):
    """Update cooking session"""
    status: Optional[str] = None
    current_step: Optional[int] = None
    notes: Optional[str] = None
    rating: Optional[float] = Field(None, ge=1, le=5)


class CookingTimerCreate(BaseModel):
    """Create cooking timer"""
    session_id: UUID
    step_number: int
    duration_seconds: int = Field(..., ge=1)
    label: str = Field(..., max_length=100)


class CookingTimerUpdate(BaseModel):
    """Update timer status"""
    status: str
    remaining_seconds: Optional[int] = None


# Response Schemas
class CookingTimerResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Cooking timer response"""
    session_id: UUID
    step_number: int
    duration_seconds: int
    remaining_seconds: int
    label: str
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


class CookingSessionResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Cooking session response"""
    user_id: UUID
    recipe_id: UUID
    recipe_title_vi: str
    recipe_thumbnail: Optional[str]
    servings: int
    status: str
    current_step: int
    total_steps: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_minutes: Optional[int]
    notes: Optional[str]
    rating: Optional[float]


class CookingSessionDetailResponse(CookingSessionResponse):
    """Cooking session with timers and steps"""
    timers: List[CookingTimerResponse]
    recipe_steps: List[Dict[str, Any]]
    progress_percentage: float


class CookingSessionStats(BaseModel):
    """User's cooking statistics"""
    total_sessions: int
    completed_sessions: int
    total_cooking_time_minutes: int
    favorite_recipes: List[Dict[str, Any]]
    avg_session_rating: float
    sessions_by_difficulty: Dict[str, int]
    recent_sessions: List[CookingSessionResponse]
