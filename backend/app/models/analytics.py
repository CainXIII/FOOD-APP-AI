"""
Search and analytics models
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class SearchQuery(Base):
    """Search query log for analytics and autocomplete"""
    __tablename__ = "search_queries"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    user_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Query details
    query: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(10), default="vi")
    
    # Results
    results_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Clicked result (if any)
    clicked_recipe_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="SET NULL")
    )
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    def __repr__(self) -> str:
        return f"<SearchQuery {self.query}>"


class TrendingKeyword(Base):
    """Trending search keywords (aggregated)"""
    __tablename__ = "trending_keywords"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    keyword: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    
    # Search counts
    daily_count: Mapped[int] = mapped_column(Integer, default=0)
    weekly_count: Mapped[int] = mapped_column(Integer, default=0)
    monthly_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Last update
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<TrendingKeyword {self.keyword}>"


class UserActivity(Base):
    """User activity log for personalization"""
    __tablename__ = "user_activity"

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
    
    # Activity type
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # Types: view_recipe, start_cooking, complete_recipe, search, favorite, rate
    
    # Target resource
    resource_type: Mapped[Optional[str]] = mapped_column(String(50))
    resource_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    
    # Additional data
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    def __repr__(self) -> str:
        return f"<UserActivity {self.activity_type}>"
