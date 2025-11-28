"""
Vector embeddings metadata for RAG pipeline
Note: Actual vectors are stored in Qdrant, this table tracks metadata only
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, ForeignKey, Boolean, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class RecipeEmbedding(Base):
    """
    Recipe embeddings metadata (vectors stored in Qdrant)
    Tracks what has been indexed and when
    """
    __tablename__ = "recipe_embeddings"

    id: Mapped[uuid4] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4
    )
    
    recipe_id: Mapped[uuid4] = mapped_column(
        Uuid,
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Content type (what part of recipe this embedding represents)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # Types: overview, ingredients, step, nutrition, full
    
    # Original text content (for reference)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Qdrant point ID (for lookups)
    qdrant_point_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # Embedding model used
    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-small")
    
    # Sync status
    is_synced: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<RecipeEmbedding {self.content_type} -> Qdrant:{self.qdrant_point_id}>"


class IngredientEmbedding(Base):
    """
    Ingredient embeddings metadata (vectors stored in Qdrant)
    """
    __tablename__ = "ingredient_embeddings"

    id: Mapped[uuid4] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4
    )
    
    ingredient_id: Mapped[uuid4] = mapped_column(
        Uuid,
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Combined text (name + description)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Qdrant point ID
    qdrant_point_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # Embedding model
    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-small")
    
    # Sync status
    is_synced: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<IngredientEmbedding {self.ingredient_id} -> Qdrant:{self.qdrant_point_id}>"
