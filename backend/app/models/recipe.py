"""
Recipe models - Main recipe and related entities
"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
import enum

from sqlalchemy import (
    String, DateTime, Text, Integer, Float, Boolean, 
    ForeignKey, Enum as SQLEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class DifficultyLevel(str, enum.Enum):
    """Recipe difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Recipe(Base):
    """Main recipe model"""
    __tablename__ = "recipes"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # User (author)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Category
    category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Basic info (bilingual)
    title_vi: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    description_vi: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Images
    thumbnail_url: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Recipe details
    prep_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    cook_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)
    
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        SQLEnum(DifficultyLevel, name="difficulty_level"),
        nullable=False,
        index=True
    )
    
    # Dietary flags
    is_vegetarian: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_vegan: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_gluten_free: Mapped[bool] = mapped_column(Boolean, default=False)
    is_dairy_free: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Allergens
    allergens: Mapped[Optional[List[str]]] = mapped_column(JSON)
    
    # Tips and notes
    tips_vi: Mapped[Optional[str]] = mapped_column(Text)
    tips_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Stats (denormalized for performance)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    favorites_count: Mapped[int] = mapped_column(Integer, default=0)
    ratings_count: Mapped[int] = mapped_column(Integer, default=0)
    average_rating: Mapped[float] = mapped_column(Float, default=0.0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    
    # Full-text search
    # search_vector: Mapped[Optional[str]] = mapped_column(Text)  # Skip for SQLite
    
    # Vector embedding for semantic search (OpenAI text-embedding-3-small: 1536 dimensions)
    # NOTE: Vector embeddings stored in Qdrant, metadata tracked in recipe_embeddings table
    # This field is deprecated and kept for backward compatibility only
    embedding: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional data
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="recipes")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="recipes")
    
    ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeIngredient.order_index"
    )
    
    steps: Mapped[List["RecipeStep"]] = relationship(
        "RecipeStep",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStep.step_number"
    )
    
    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    
    ratings: Mapped[List["Rating"]] = relationship(
        "Rating",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    
    nutrition_facts: Mapped[Optional["NutritionFacts"]] = relationship(
        "NutritionFacts",
        back_populates="recipe",
        cascade="all, delete-orphan",
        uselist=False
    )

    def __repr__(self) -> str:
        return f"<Recipe {self.title_vi}>"


# Create composite index for full-text search (PostgreSQL only)
# Index('idx_recipes_search_vector', Recipe.search_vector, postgresql_using='gin')


class RecipeIngredient(Base):
    """Recipe ingredients junction table"""
    __tablename__ = "recipe_ingredients"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    recipe_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    ingredient_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Quantity
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)  # gram, cup, tbsp, etc.
    
    # Alternative names if different from ingredient name
    name_vi: Mapped[Optional[str]] = mapped_column(String(255))
    name_en: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Notes
    notes_vi: Mapped[Optional[str]] = mapped_column(Text)
    notes_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Optional/substitutable
    is_optional: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Display order
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", back_populates="recipe_ingredients")

    def __repr__(self) -> str:
        return f"<RecipeIngredient {self.quantity} {self.unit}>"


class RecipeStep(Base):
    """Recipe cooking steps"""
    __tablename__ = "recipe_steps"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    recipe_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Title
    title_vi: Mapped[Optional[str]] = mapped_column(String(255))
    title_en: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Instructions
    instruction_vi: Mapped[str] = mapped_column(Text, nullable=False)
    instruction_en: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Media
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timing
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Tips
    tips_vi: Mapped[Optional[str]] = mapped_column(Text)
    tips_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="steps")

    def __repr__(self) -> str:
        return f"<RecipeStep {self.step_number}>"


class NutritionFacts(Base):
    """Nutritional information per serving"""
    __tablename__ = "nutrition_facts"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    recipe_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Macros
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    protein_g: Mapped[float] = mapped_column(Float, nullable=False)
    carbs_g: Mapped[float] = mapped_column(Float, nullable=False)
    fat_g: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Detailed nutrients
    fiber_g: Mapped[Optional[float]] = mapped_column(Float)
    sugar_g: Mapped[Optional[float]] = mapped_column(Float)
    sodium_mg: Mapped[Optional[float]] = mapped_column(Float)
    cholesterol_mg: Mapped[Optional[float]] = mapped_column(Float)
    
    # Vitamins & minerals (% of daily value)
    vitamin_a_percent: Mapped[Optional[float]] = mapped_column(Float)
    vitamin_c_percent: Mapped[Optional[float]] = mapped_column(Float)
    calcium_percent: Mapped[Optional[float]] = mapped_column(Float)
    iron_percent: Mapped[Optional[float]] = mapped_column(Float)
    
    # Relationships
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="nutrition_facts")

    def __repr__(self) -> str:
        return f"<NutritionFacts {self.calories} kcal>"
