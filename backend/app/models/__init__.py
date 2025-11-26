"""
Import all models for Alembic migrations
"""
from app.database import Base

# Import all models to register them with SQLAlchemy
from app.models.user import User, OAuthAccount, RefreshToken
from app.models.category import Category, Ingredient
from app.models.recipe import Recipe, RecipeIngredient, RecipeStep, NutritionFacts
from app.models.social import Favorite, Rating, Comment, RecipeList, RecipeListItem
from app.models.cooking import CookingSession, CookingTimer
from app.models.chat import Chat, ChatMessage
from app.models.analytics import SearchQuery, TrendingKeyword, UserActivity
from app.models.embedding import RecipeEmbedding, IngredientEmbedding

__all__ = [
    "Base",
    # User
    "User",
    "OAuthAccount",
    "RefreshToken",
    # Content
    "Category",
    "Ingredient",
    # Recipe
    "Recipe",
    "RecipeIngredient",
    "RecipeStep",
    "NutritionFacts",
    # Social
    "Favorite",
    "Rating",
    "Comment",
    "RecipeList",
    "RecipeListItem",
    # Cooking
    "CookingSession",
    "CookingTimer",
    # Chat
    "Chat",
    "ChatMessage",
    # Analytics
    "SearchQuery",
    "TrendingKeyword",
    "UserActivity",
    # Embeddings
    "RecipeEmbedding",
    "IngredientEmbedding",
]
