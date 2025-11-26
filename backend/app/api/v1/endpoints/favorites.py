"""
Favorite & Rating endpoints
"""
from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, and_

from app.database import get_db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.social import Favorite, Rating
from app.core.deps import get_current_user
from app.schemas.base import MessageResponse


router = APIRouter()


# ============================================================================
# Favorites
# ============================================================================

@router.post("/recipes/{recipe_id}/favorite", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Add recipe to favorites
    """
    # Check recipe exists
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check if already favorited
    result = await db.execute(
        select(Favorite).where(
            and_(
                Favorite.user_id == current_user.id,
                Favorite.recipe_id == recipe_id
            )
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe already in favorites"
        )
    
    # Create favorite
    favorite = Favorite(
        user_id=current_user.id,
        recipe_id=recipe_id
    )
    db.add(favorite)
    
    # Update recipe favorites count
    recipe.favorites_count += 1
    
    await db.commit()
    
    return {
        "message": "Recipe added to favorites",
        "recipe_id": str(recipe_id),
        "favorites_count": recipe.favorites_count
    }


@router.delete("/recipes/{recipe_id}/favorite")
async def remove_favorite(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remove recipe from favorites
    """
    result = await db.execute(
        select(Favorite).where(
            and_(
                Favorite.user_id == current_user.id,
                Favorite.recipe_id == recipe_id
            )
        )
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not in favorites"
        )
    
    # Get recipe to update count
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    await db.delete(favorite)
    
    if recipe:
        recipe.favorites_count = max(0, recipe.favorites_count - 1)
    
    await db.commit()
    
    return {
        "message": "Recipe removed from favorites",
        "recipe_id": str(recipe_id)
    }


@router.get("/favorites")
async def get_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's favorite recipes
    """
    # Count total
    count_result = await db.execute(
        select(func.count(Favorite.id)).where(Favorite.user_id == current_user.id)
    )
    total = count_result.scalar_one()
    
    # Get favorites with recipes
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Favorite, Recipe)
        .join(Recipe, Favorite.recipe_id == Recipe.id)
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    
    items = []
    for favorite, recipe in result:
        items.append({
            "id": recipe.id,
            "title_vi": recipe.title_vi,
            "title_en": recipe.title_en,
            "thumbnail_url": recipe.thumbnail_url,
            "difficulty": recipe.difficulty.value,
            "prep_time_minutes": recipe.prep_time_minutes,
            "cook_time_minutes": recipe.cook_time_minutes,
            "average_rating": recipe.average_rating,
            "favorited_at": favorite.created_at
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


# ============================================================================
# Ratings
# ============================================================================

@router.post("/recipes/{recipe_id}/rating", status_code=status.HTTP_201_CREATED)
async def add_rating(
    recipe_id: UUID,
    rating_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Rate a recipe
    
    - **rating**: 1-5 stars
    - **review_vi**: Optional Vietnamese review
    - **review_en**: Optional English review
    """
    # Validate rating
    rating_value = rating_data.get("rating")
    if not rating_value or rating_value < 1 or rating_value > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    # Check recipe exists
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check if already rated
    result = await db.execute(
        select(Rating).where(
            and_(
                Rating.user_id == current_user.id,
                Rating.recipe_id == recipe_id
            )
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing rating
        old_rating = existing.rating
        existing.rating = rating_value
        existing.review_vi = rating_data.get("review_vi")
        existing.review_en = rating_data.get("review_en")
        
        # Recalculate average
        total_ratings = recipe.ratings_count
        old_total = recipe.average_rating * total_ratings
        new_total = old_total - old_rating + rating_value
        recipe.average_rating = new_total / total_ratings
        
        message = "Rating updated successfully"
    else:
        # Create new rating
        new_rating = Rating(
            user_id=current_user.id,
            recipe_id=recipe_id,
            rating=rating_value,
            review_vi=rating_data.get("review_vi"),
            review_en=rating_data.get("review_en")
        )
        db.add(new_rating)
        
        # Update recipe stats
        total_ratings = recipe.ratings_count
        old_total = recipe.average_rating * total_ratings
        new_total = old_total + rating_value
        recipe.ratings_count += 1
        recipe.average_rating = new_total / recipe.ratings_count
        
        message = "Rating added successfully"
    
    await db.commit()
    
    return {
        "message": message,
        "recipe_id": str(recipe_id),
        "rating": rating_value,
        "average_rating": round(recipe.average_rating, 2),
        "total_ratings": recipe.ratings_count
    }


@router.get("/recipes/{recipe_id}/ratings")
async def get_recipe_ratings(
    recipe_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get all ratings for a recipe
    """
    # Count total
    count_result = await db.execute(
        select(func.count(Rating.id)).where(Rating.recipe_id == recipe_id)
    )
    total = count_result.scalar_one()
    
    # Get ratings
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Rating, User)
        .join(User, Rating.user_id == User.id)
        .where(Rating.recipe_id == recipe_id)
        .order_by(Rating.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    
    items = []
    for rating, user in result:
        items.append({
            "id": rating.id,
            "user_id": rating.user_id,
            "user_name": user.full_name,
            "user_avatar": user.avatar_url,
            "rating": rating.rating,
            "review_vi": rating.review_vi,
            "review_en": rating.review_en,
            "created_at": rating.created_at,
            "updated_at": rating.updated_at
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.delete("/recipes/{recipe_id}/rating")
async def delete_rating(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete user's rating for a recipe
    """
    result = await db.execute(
        select(Rating).where(
            and_(
                Rating.user_id == current_user.id,
                Rating.recipe_id == recipe_id
            )
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    # Get recipe to update stats
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    await db.delete(rating)
    
    if recipe and recipe.ratings_count > 0:
        # Recalculate average
        old_total = recipe.average_rating * recipe.ratings_count
        new_total = old_total - rating.rating
        recipe.ratings_count -= 1
        
        if recipe.ratings_count > 0:
            recipe.average_rating = new_total / recipe.ratings_count
        else:
            recipe.average_rating = 0.0
    
    await db.commit()
    
    return {
        "message": "Rating deleted successfully",
        "recipe_id": str(recipe_id)
    }
