"""
User model - Authentication and user profile
"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, String, DateTime, Text, Integer, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import String as SQLString
import json
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    """User roles"""
    USER = "user"
    PREMIUM = "premium"
    CHEF = "chef"
    MODERATOR = "moderator"
    ADMIN = "admin"


class AIPersonality(str, enum.Enum):
    """AI chat personality types"""
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    NUTRITIONIST = "nutritionist"
    EFFICIENT = "efficient"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Nullable for OAuth users
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Profile
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Role & Permissions
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role"),
        default=UserRole.USER,
        nullable=False
    )

    # Preferences (JSON for SQLite compatibility)
    dietary_preferences: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list
    )  # vegetarian, vegan, keto, etc.
    
    allergies: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list
    )  # peanuts, shellfish, dairy, etc.
    
    default_servings: Mapped[int] = mapped_column(Integer, default=2)
    preferred_language: Mapped[str] = mapped_column(String(10), default="vi")
    
    ai_personality: Mapped[AIPersonality] = mapped_column(
        SQLEnum(AIPersonality, name="ai_personality"),
        default=AIPersonality.FRIENDLY
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified_chef: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Relationships
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    ratings: Mapped[List["Rating"]] = relationship(
        "Rating",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    cooking_sessions: Mapped[List["CookingSession"]] = relationship(
        "CookingSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    chats: Mapped[List["Chat"]] = relationship(
        "Chat",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    recipe_lists: Mapped[List["RecipeList"]] = relationship(
        "RecipeList",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class OAuthAccount(Base):
    """OAuth account linking"""
    __tablename__ = "oauth_accounts"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # google, facebook, apple
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<OAuthAccount {self.provider}:{self.provider_user_id}>"


class RefreshToken(Base):
    """Refresh tokens for session management"""
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    # Device info
    device_id: Mapped[Optional[str]] = mapped_column(String(255))
    device_name: Mapped[Optional[str]] = mapped_column(String(255))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))  # IPv6 max length
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Activity
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_activity: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Expiry
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<RefreshToken {self.token[:8]}...>"
