"""
Vector embeddings for RAG pipeline
"""
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import String, DateTime, Text, ForeignKey, Index
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class RecipeEmbedding(Base):
    """Recipe embeddings for RAG vector search"""
    __tablename__ = "recipe_embeddings"

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
    
    # Content type (what part of recipe this embedding represents)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # Types: overview, ingredients, step, nutrition, full
    
    # Original text content
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Vector embedding (1536 dimensions for text-embedding-3-small)
    # Stored as JSON array for SQLite compatibility
    embedding: Mapped[List[float]] = mapped_column(JSON, nullable=False)
    
    # Additional data (step_number, language, etc.)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Embedding model used
    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-small")
    
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
        return f"<RecipeEmbedding {self.content_type}>"


# Create HNSW index for fast vector similarity search
Index(
    'idx_recipe_embeddings_hnsw',
    RecipeEmbedding.embedding,
    postgresql_using='hnsw',
    postgresql_with={'m': 16, 'ef_construction': 64},
    postgresql_ops={'embedding': 'vector_cosine_ops'}
)


class IngredientEmbedding(Base):
    """Ingredient embeddings for semantic search"""
    __tablename__ = "ingredient_embeddings"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    ingredient_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Combined text (name + description)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Vector embedding
    embedding: Mapped[List[float]] = mapped_column(Vector(1536), nullable=False)
    
    # Embedding model
    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-small")
    
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
        return f"<IngredientEmbedding {self.ingredient_id}>"


# Create HNSW index for ingredient embeddings
Index(
    'idx_ingredient_embeddings_hnsw',
    IngredientEmbedding.embedding,
    postgresql_using='hnsw',
    postgresql_with={'m': 16, 'ef_construction': 64},
    postgresql_ops={'embedding': 'vector_cosine_ops'}
)
