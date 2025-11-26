"""
Schemas package exports
"""
from app.schemas.base import (
    BaseSchema,
    UUIDMixin,
    TimestampMixin,
    PaginationParams,
    PaginatedResponse,
    MessageResponse
)
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserUpdate,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm,
    UserResponse,
    UserDetailResponse,
    TokenResponse,
    TokenRefresh,
    OAuthCallback,
    UserRole,
    AIPersonality
)
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeFilter,
    RecipeSearch,
    RecipeListItem,
    RecipeDetailResponse,
    RecipePaginatedResponse,
    RecipeStatsResponse,
    RecipeStep,
    RecipeIngredient,
    NutritionFacts,
    DifficultyLevel
)
from app.schemas.chat import (
    ChatCreate,
    ChatMessageCreate,
    ChatMessageStream,
    RAGQuery,
    ChatResponse,
    ChatMessageResponse,
    ChatDetailResponse,
    ChatStreamChunk,
    RAGContextItem,
    RAGResponse
)
from app.schemas.social import (
    FavoriteCreate,
    FavoriteResponse,
    RatingCreate,
    RatingUpdate,
    RatingResponse,
    RatingPaginatedResponse,
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentWithReplies,
    CommentPaginatedResponse,
    RecipeListCreate,
    RecipeListUpdate,
    RecipeListAddRecipe,
    RecipeListResponse,
    RecipeListDetailResponse,
    UserSocialStats
)
from app.schemas.cooking import (
    CookingSessionCreate,
    CookingSessionUpdate,
    CookingTimerCreate,
    CookingTimerUpdate,
    CookingSessionResponse,
    CookingSessionDetailResponse,
    CookingTimerResponse,
    CookingSessionStats,
    SessionStatus,
    TimerStatus
)

__all__ = [
    # Base
    "BaseSchema",
    "UUIDMixin",
    "TimestampMixin",
    "PaginationParams",
    "PaginatedResponse",
    "MessageResponse",
    
    # User & Auth
    "UserRegister",
    "UserLogin",
    "UserUpdate",
    "PasswordChange",
    "PasswordReset",
    "PasswordResetConfirm",
    "UserResponse",
    "UserDetailResponse",
    "TokenResponse",
    "TokenRefresh",
    "OAuthCallback",
    "UserRole",
    "AIPersonality",
    
    # Recipe
    "RecipeCreate",
    "RecipeUpdate",
    "RecipeFilter",
    "RecipeSearch",
    "RecipeListItem",
    "RecipeDetailResponse",
    "RecipePaginatedResponse",
    "RecipeStatsResponse",
    "RecipeStep",
    "RecipeIngredient",
    "NutritionFacts",
    "DifficultyLevel",
    
    # Chat & RAG
    "ChatCreate",
    "ChatMessageCreate",
    "ChatMessageStream",
    "RAGQuery",
    "ChatResponse",
    "ChatMessageResponse",
    "ChatDetailResponse",
    "ChatStreamChunk",
    "RAGContextItem",
    "RAGResponse",
    
    # Social
    "FavoriteCreate",
    "FavoriteResponse",
    "RatingCreate",
    "RatingUpdate",
    "RatingResponse",
    "RatingPaginatedResponse",
    "CommentCreate",
    "CommentUpdate",
    "CommentResponse",
    "CommentWithReplies",
    "CommentPaginatedResponse",
    "RecipeListCreate",
    "RecipeListUpdate",
    "RecipeListAddRecipe",
    "RecipeListResponse",
    "RecipeListDetailResponse",
    "UserSocialStats",
    
    # Cooking
    "CookingSessionCreate",
    "CookingSessionUpdate",
    "CookingTimerCreate",
    "CookingTimerUpdate",
    "CookingSessionResponse",
    "CookingSessionDetailResponse",
    "CookingTimerResponse",
    "CookingSessionStats",
    "SessionStatus",
    "TimerStatus",
]
