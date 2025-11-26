"""
Social interaction schemas (favorites, ratings, comments)
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema, UUIDMixin, TimestampMixin, PaginatedResponse


# Favorite Schemas
class FavoriteCreate(BaseModel):
    """Add recipe to favorites"""
    recipe_id: UUID


class FavoriteResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Favorite response"""
    user_id: UUID
    recipe_id: UUID
    recipe_title_vi: str
    recipe_thumbnail: Optional[str]


# Rating Schemas
class RatingCreate(BaseModel):
    """Create or update rating"""
    recipe_id: UUID
    rating: float = Field(..., ge=1, le=5)
    review: Optional[str] = Field(None, max_length=1000)


class RatingUpdate(BaseModel):
    """Update existing rating"""
    rating: Optional[float] = Field(None, ge=1, le=5)
    review: Optional[str] = Field(None, max_length=1000)


class RatingResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Rating response"""
    user_id: UUID
    user_name: str
    user_avatar: Optional[str]
    recipe_id: UUID
    rating: float
    review: Optional[str]
    helpful_count: int = 0
    
    # User-specific (if authenticated)
    is_helpful: Optional[bool] = None


class RatingPaginatedResponse(PaginatedResponse):
    """Paginated ratings"""
    items: List[RatingResponse]


# Comment Schemas
class CommentCreate(BaseModel):
    """Create comment"""
    recipe_id: UUID
    content: str = Field(..., min_length=1, max_length=2000)
    parent_id: Optional[UUID] = None  # For replies


class CommentUpdate(BaseModel):
    """Update comment"""
    content: str = Field(..., min_length=1, max_length=2000)


class CommentResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Comment response"""
    user_id: UUID
    user_name: str
    user_avatar: Optional[str]
    recipe_id: UUID
    content: str
    parent_id: Optional[UUID]
    likes_count: int = 0
    replies_count: int = 0
    is_edited: bool
    
    # User-specific (if authenticated)
    is_liked: Optional[bool] = None
    is_owner: Optional[bool] = None


class CommentWithReplies(CommentResponse):
    """Comment with nested replies"""
    replies: List[CommentResponse] = []


class CommentPaginatedResponse(PaginatedResponse):
    """Paginated comments"""
    items: List[CommentWithReplies]


# Recipe List Schemas
class RecipeListCreate(BaseModel):
    """Create recipe collection"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: bool = True


class RecipeListUpdate(BaseModel):
    """Update recipe list"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None


class RecipeListAddRecipe(BaseModel):
    """Add recipe to list"""
    recipe_id: UUID
    notes: Optional[str] = Field(None, max_length=200)


class RecipeListResponse(BaseSchema, UUIDMixin, TimestampMixin):
    """Recipe list response"""
    user_id: UUID
    user_name: str
    name: str
    description: Optional[str]
    is_public: bool
    recipe_count: int = 0
    thumbnail_urls: List[str] = []  # First 4 recipe thumbnails


class RecipeListDetailResponse(RecipeListResponse):
    """Recipe list with recipes"""
    recipes: List[dict]  # Recipe summaries


# Social Stats
class UserSocialStats(BaseModel):
    """User's social statistics"""
    total_recipes: int
    total_favorites: int
    total_ratings: int
    avg_rating_given: float
    total_comments: int
    total_lists: int
    followers_count: int = 0
    following_count: int = 0
