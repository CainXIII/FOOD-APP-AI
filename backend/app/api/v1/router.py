"""
API Router - aggregates all API endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, recipes, chat, categories, favorites, ingredients, uploads

api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Include recipe endpoints
api_router.include_router(
    recipes.router,
    prefix="/recipes",
    tags=["Recipes"]
)

# Include chat endpoints
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["AI Chat"]
)

# Include category endpoints
api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["Categories"]
)

# Include ingredient endpoints
api_router.include_router(
    ingredients.router,
    prefix="/ingredients",
    tags=["Ingredients"]
)

# Include favorite & rating endpoints
api_router.include_router(
    favorites.router,
    prefix="",
    tags=["Favorites & Ratings"]
)

# Include upload endpoints
api_router.include_router(
    uploads.router,
    prefix="/uploads",
    tags=["File Uploads"]
)

# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
# api_router.include_router(ingredients.router, prefix="/ingredients", tags=["Ingredients"])
# api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
# api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat"])
# api_router.include_router(search.router, prefix="/search", tags=["Search"])
# api_router.include_router(cooking.router, prefix="/cooking", tags=["Cooking Sessions"])


@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "AI Cooking Assistant API",
        "version": "v1",
        "status": "operational"
    }
