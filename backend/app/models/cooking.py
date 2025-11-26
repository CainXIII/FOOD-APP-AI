"""
Cooking session models - Track active cooking sessions and timers
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4
import enum

from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class SessionStatus(str, enum.Enum):
    """Cooking session status"""
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CookingSession(Base):
    """Active cooking sessions"""
    __tablename__ = "cooking_sessions"

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
    
    recipe_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Session state
    status: Mapped[SessionStatus] = mapped_column(
        SQLEnum(SessionStatus, name="session_status"),
        default=SessionStatus.IN_PROGRESS,
        nullable=False
    )
    
    current_step: Mapped[int] = mapped_column(Integer, default=1)
    total_steps: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Servings (may differ from recipe default)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Session metadata (ingredient scaling, notes, etc.)
    session_data: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    paused_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cooking_sessions")
    
    timers: Mapped[list["CookingTimer"]] = relationship(
        "CookingTimer",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CookingSession {self.status}>"


class TimerStatus(str, enum.Enum):
    """Timer status"""
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CookingTimer(Base):
    """Cooking timers for sessions"""
    __tablename__ = "cooking_timers"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cooking_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Timer details
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    elapsed_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    status: Mapped[TimerStatus] = mapped_column(
        SQLEnum(TimerStatus, name="timer_status"),
        default=TimerStatus.RUNNING,
        nullable=False
    )
    
    # Step reference
    step_number: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    paused_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    session: Mapped["CookingSession"] = relationship("CookingSession", back_populates="timers")

    def __repr__(self) -> str:
        return f"<CookingTimer {self.name}>"
