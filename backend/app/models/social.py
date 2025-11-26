"""
Social interaction models - Favorites, Ratings, Comments, Recipe Lists
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, Integer, Float, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Favorite(Base):
    """User favorite recipes"""
    __tablename__ = "favorites"

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
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="favorites")

    def __repr__(self) -> str:
        return f"<Favorite user={self.user_id} recipe={self.recipe_id}>"


# Unique constraint: user can favorite recipe only once
Index('idx_favorites_unique', Favorite.user_id, Favorite.recipe_id, unique=True)


class Rating(Base):
    """Recipe ratings and reviews"""
    __tablename__ = "ratings"

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
    
    # Rating (1-5 stars)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Review text
    review_vi: Mapped[Optional[str]] = mapped_column(Text)
    review_en: Mapped[Optional[str]] = mapped_column(Text)
    
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
    user: Mapped["User"] = relationship("User", back_populates="ratings")
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ratings")

    def __repr__(self) -> str:
        return f"<Rating {self.rating} stars>"


# Unique constraint: user can rate recipe only once
Index('idx_ratings_unique', Rating.user_id, Rating.recipe_id, unique=True)


class Comment(Base):
    """Recipe comments with threading support"""
    __tablename__ = "comments"

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
    
    # Parent comment for threading
    parent_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    # Comment content
    content_vi: Mapped[str] = mapped_column(Text, nullable=False)
    content_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Stats
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    
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
    user: Mapped["User"] = relationship("User", back_populates="comments")
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment by user={self.user_id}>"


class RecipeList(Base):
    """User-created recipe collections"""
    __tablename__ = "recipe_lists"

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
    
    # List info
    name_vi: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[Optional[str]] = mapped_column(String(255))
    
    description_vi: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    
    # Privacy
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Stats
    recipes_count: Mapped[int] = mapped_column(Integer, default=0)
    
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
    user: Mapped["User"] = relationship("User", back_populates="recipe_lists")
    
    items: Mapped[list["RecipeListItem"]] = relationship(
        "RecipeListItem",
        back_populates="recipe_list",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<RecipeList {self.name_vi}>"


class RecipeListItem(Base):
    """Items in recipe lists"""
    __tablename__ = "recipe_list_items"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    recipe_list_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipe_lists.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    recipe_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Display order
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    recipe_list: Mapped["RecipeList"] = relationship("RecipeList", back_populates="items")

    def __repr__(self) -> str:
        return f"<RecipeListItem in list={self.recipe_list_id}>"


# Unique constraint: recipe can appear only once in a list
Index('idx_recipe_list_items_unique', RecipeListItem.recipe_list_id, RecipeListItem.recipe_id, unique=True)
