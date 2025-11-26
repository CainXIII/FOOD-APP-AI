"""
User authentication schemas
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.base import BaseSchema, UUIDMixin, TimestampMixin


# Enums
class UserRole(str):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class AIPersonality(str):
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    NUTRITIONIST = "nutritionist"


# Request Schemas
class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=100)
    display_name: Optional[str] = Field(None, max_length=50)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User profile update request"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_name: Optional[str] = Field(None, max_length=50)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    ai_personality: Optional[str] = None
    dietary_preferences: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    cooking_skill_level: Optional[str] = None
    preferred_cuisines: Optional[List[str]] = None


class PasswordChange(BaseModel):
    """Password change request"""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordReset(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


# Response Schemas
class UserResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """User response (public profile)"""
    email: EmailStr
    username: Optional[str]
    full_name: str
    avatar_url: Optional[str]
    bio: Optional[str]
    role: str
    is_active: bool
    email_verified: bool
    ai_personality: str
    
    # Don't expose sensitive fields
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "750e8400-e29b-41d4-a716-446655440001",
                "email": "user@example.com",
                "full_name": "John Doe",
                "display_name": "johndoe",
                "role": "user",
                "is_active": True,
                "ai_personality": "friendly"
            }
        }
    }


class UserDetailResponse(UserResponse):
    """User detail response (own profile)"""
    dietary_preferences: List[str] = []
    allergies: List[str] = []
    preferred_cuisines: List[str] = []
    notification_settings: Optional[dict] = None
    last_active_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefresh(BaseModel):
    """Token refresh request"""
    refresh_token: str


class OAuthCallback(BaseModel):
    """OAuth callback data"""
    provider: str = Field(..., pattern="^(google|facebook|apple)$")
    code: str
    state: Optional[str] = None
