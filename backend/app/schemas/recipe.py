"""
Recipe schemas
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema, UUIDMixin, TimestampMixin, PaginatedResponse


# Enums
class DifficultyLevel(str):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# Nested schemas
class RecipeStep(BaseModel):
    """Recipe step (nested)"""
    step_number: int
    instruction_vi: str
    instruction_en: Optional[str] = None
    image_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    temperature: Optional[int] = None
    tips: Optional[str] = None


class RecipeIngredient(BaseModel):
    """Recipe ingredient with quantity"""
    ingredient_id: UUID
    ingredient_name_vi: str
    ingredient_name_en: Optional[str] = None
    quantity: float
    unit: str
    notes: Optional[str] = None


class NutritionFacts(BaseModel):
    """Nutrition facts per serving"""
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    cholesterol_mg: Optional[float] = None


# Request Schemas
class RecipeCreate(BaseModel):
    """Create recipe request"""
    title_vi: str = Field(..., min_length=1, max_length=200)
    title_en: Optional[str] = Field(None, max_length=200)
    description_vi: str = Field(..., min_length=1, max_length=1000)
    description_en: Optional[str] = Field(None, max_length=1000)
    category_id: UUID
    prep_time_minutes: int = Field(..., ge=0)
    cook_time_minutes: int = Field(..., ge=0)
    servings: int = Field(..., ge=1)
    difficulty: str
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_dairy_free: bool = False
    allergens: List[str] = []
    ingredients: List[RecipeIngredient]
    steps: List[RecipeStep]
    nutrition: Optional[NutritionFacts] = None


class RecipeUpdate(BaseModel):
    """Update recipe request"""
    title_vi: Optional[str] = Field(None, min_length=1, max_length=200)
    title_en: Optional[str] = Field(None, max_length=200)
    description_vi: Optional[str] = Field(None, min_length=1, max_length=1000)
    description_en: Optional[str] = Field(None, max_length=1000)
    category_id: Optional[UUID] = None
    prep_time_minutes: Optional[int] = Field(None, ge=0)
    cook_time_minutes: Optional[int] = Field(None, ge=0)
    servings: Optional[int] = Field(None, ge=1)
    difficulty: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    is_dairy_free: Optional[bool] = None
    allergens: Optional[List[str]] = None
    is_featured: Optional[bool] = None


class RecipeFilter(BaseModel):
    """Recipe filter parameters"""
    category_id: Optional[UUID] = None
    difficulty: Optional[str] = None
    max_prep_time: Optional[int] = None
    max_cook_time: Optional[int] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    is_dairy_free: Optional[bool] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    search_query: Optional[str] = None
    author_id: Optional[UUID] = None


class RecipeSearch(BaseModel):
    """Recipe semantic search request"""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(10, ge=1, le=50)
    min_similarity: float = Field(0.7, ge=0, le=1)
    filters: Optional[RecipeFilter] = None


# Response Schemas
class RecipeListItem(BaseSchema, UUIDMixin, TimestampMixin):
    """Recipe in list view (summary)"""
    title_vi: str
    title_en: Optional[str]
    slug: str
    description_vi: str
    thumbnail_url: Optional[str]
    category_id: UUID
    category_name_vi: str
    author_id: UUID
    author_name: str
    author_avatar: Optional[str]
    prep_time_minutes: int
    cook_time_minutes: int
    total_time_minutes: int
    servings: int
    difficulty: str
    is_vegetarian: bool
    is_vegan: bool
    avg_rating: float
    total_ratings: int
    total_favorites: int
    is_featured: bool


class RecipeDetailResponse(RecipeListItem):
    """Recipe detail response"""
    description_en: Optional[str]
    video_url: Optional[str]
    is_gluten_free: bool
    is_dairy_free: bool
    allergens: List[str]
    ingredients: List[RecipeIngredient]
    steps: List[RecipeStep]
    nutrition: Optional[NutritionFacts]
    total_comments: int
    view_count: int
    is_published: bool
    
    # User-specific fields (if authenticated)
    is_favorited: Optional[bool] = None
    user_rating: Optional[float] = None


class RecipePaginatedResponse(PaginatedResponse):
    """Paginated recipe list"""
    items: List[RecipeListItem]


class RecipeStatsResponse(BaseModel):
    """Recipe statistics"""
    total_recipes: int
    total_views: int
    total_favorites: int
    total_ratings: int
    avg_rating: float
    by_category: dict
    by_difficulty: dict
    trending_recipes: List[RecipeListItem]
