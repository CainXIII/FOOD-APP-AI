"""
Category and Ingredient models
"""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    """Recipe categories"""
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # Names (bilingual)
    name_vi: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Slug for URLs
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    # Descriptions
    description_vi: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Images
    icon_url: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Display order
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<Category {self.name_vi}>"


class Ingredient(Base):
    """Ingredients with nutritional information"""
    __tablename__ = "ingredients"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # Names (bilingual)
    name_vi: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    # Slug
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    # Descriptions
    description_vi: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Image
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Nutritional information (per 100g)
    calories: Mapped[Optional[float]] = mapped_column(Float)
    protein_g: Mapped[Optional[float]] = mapped_column(Float)
    carbs_g: Mapped[Optional[float]] = mapped_column(Float)
    fat_g: Mapped[Optional[float]] = mapped_column(Float)
    fiber_g: Mapped[Optional[float]] = mapped_column(Float)
    
    # Common unit
    common_unit: Mapped[Optional[str]] = mapped_column(String(50))  # gram, cup, tbsp, etc.
    
    # Additional data
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="ingredient"
    )

    def __repr__(self) -> str:
        return f"<Ingredient {self.name_vi}>"
