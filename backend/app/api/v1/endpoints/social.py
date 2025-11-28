"""
Social endpoints - Ratings, Comments, Favorites, User Profiles
"""
from typing import Any, Optional, List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.social import Rating, Comment, Favorite
from app.schemas.base import MessageResponse
from app.core.deps import get_current_user


router = APIRouter()


# ============================================================================
# RATINGS
# ============================================================================

@router.post("/recipes/{recipe_id}/ratings", status_code=status.HTTP_201_CREATED)
async def create_rating(
    recipe_id: UUID,
    rating_value: int = Query(..., ge=1, le=5, description="Rating from 1 to 5"),
    review: Optional[str] = Query(None, max_length=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Rate a recipe (1-5 stars) with optional review
    
    - **recipe_id**: Recipe UUID
    - **rating_value**: 1-5 stars
    - **review**: Optional text review (max 1000 chars)
    """
    # Verify recipe exists
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check if user already rated this recipe
    result = await db.execute(
        select(Rating).where(
            Rating.recipe_id == recipe_id,
            Rating.user_id == current_user.id
        )
    )
    existing_rating = result.scalar_one_or_none()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_value
        existing_rating.review = review
        existing_rating.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(existing_rating)
        
        # Recalculate recipe average
        await _update_recipe_rating_stats(recipe_id, db)
        
        return {
            "id": existing_rating.id,
            "recipe_id": existing_rating.recipe_id,
            "user_id": existing_rating.user_id,
            "rating": existing_rating.rating,
            "review": existing_rating.review,
            "helpful_count": existing_rating.helpful_count,
            "created_at": existing_rating.created_at,
            "updated_at": existing_rating.updated_at,
            "message": "Rating updated successfully"
        }
    else:
        # Create new rating
        new_rating = Rating(
            recipe_id=recipe_id,
            user_id=current_user.id,
            rating=rating_value,
            review=review,
            helpful_count=0
        )
        
        db.add(new_rating)
        await db.commit()
        await db.refresh(new_rating)
        
        # Update recipe stats
        await _update_recipe_rating_stats(recipe_id, db)
        
        return {
            "id": new_rating.id,
            "recipe_id": new_rating.recipe_id,
            "user_id": new_rating.user_id,
            "rating": new_rating.rating,
            "review": new_rating.review,
            "helpful_count": new_rating.helpful_count,
            "created_at": new_rating.created_at,
            "updated_at": new_rating.updated_at,
            "message": "Rating created successfully"
        }


@router.get("/recipes/{recipe_id}/ratings")
async def get_recipe_ratings(
    recipe_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("helpful", enum=["helpful", "recent", "highest", "lowest"]),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get ratings for a recipe
    
    - **recipe_id**: Recipe UUID
    - **page**: Page number
    - **page_size**: Items per page (1-100)
    - **sort_by**: Sort order (helpful, recent, highest, lowest)
    """
    # Build query
    query = select(Rating).where(Rating.recipe_id == recipe_id)
    
    # Apply sorting
    if sort_by == "helpful":
        query = query.order_by(Rating.helpful_count.desc(), Rating.created_at.desc())
    elif sort_by == "recent":
        query = query.order_by(Rating.created_at.desc())
    elif sort_by == "highest":
        query = query.order_by(Rating.rating.desc(), Rating.created_at.desc())
    elif sort_by == "lowest":
        query = query.order_by(Rating.rating.asc(), Rating.created_at.desc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # Execute query
    result = await db.execute(query.options(selectinload(Rating.user)))
    ratings = result.scalars().all()
    
    # Get total count
    count_result = await db.execute(
        select(func.count()).select_from(Rating).where(Rating.recipe_id == recipe_id)
    )
    total_count = count_result.scalar()
    
    # Format response
    ratings_data = []
    for rating in ratings:
        ratings_data.append({
            "id": rating.id,
            "recipe_id": rating.recipe_id,
            "user": {
                "id": rating.user.id,
                "username": rating.user.username,
                "full_name": rating.user.full_name,
                "avatar_url": rating.user.avatar_url
            },
            "rating": rating.rating,
            "review": rating.review,
            "helpful_count": rating.helpful_count,
            "created_at": rating.created_at,
            "updated_at": rating.updated_at
        })
    
    return {
        "recipe_id": recipe_id,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "ratings": ratings_data
    }


@router.delete("/recipes/{recipe_id}/ratings")
async def delete_rating(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """Delete user's rating for a recipe"""
    result = await db.execute(
        select(Rating).where(
            Rating.recipe_id == recipe_id,
            Rating.user_id == current_user.id
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    await db.delete(rating)
    await db.commit()
    
    # Update recipe stats
    await _update_recipe_rating_stats(recipe_id, db)
    
    return {
        "message": "Rating deleted successfully"
    }


# ============================================================================
# COMMENTS
# ============================================================================

@router.post("/recipes/{recipe_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(
    recipe_id: UUID,
    content: str = Query(..., min_length=1, max_length=2000),
    parent_id: Optional[UUID] = Query(None, description="Parent comment ID for replies"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Add comment to recipe (supports nested replies)
    
    - **recipe_id**: Recipe UUID
    - **content**: Comment text (1-2000 chars)
    - **parent_id**: Optional parent comment ID for threaded replies
    """
    # Verify recipe exists
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # If parent_id provided, verify parent exists
    if parent_id:
        result = await db.execute(select(Comment).where(Comment.id == parent_id))
        parent = result.scalar_one_or_none()
        
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent comment not found"
            )
        
        if parent.recipe_id != recipe_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent comment belongs to different recipe"
            )
    
    # Create comment
    new_comment = Comment(
        recipe_id=recipe_id,
        user_id=current_user.id,
        parent_id=parent_id,
        content=content,
        likes_count=0
    )
    
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    
    return {
        "id": new_comment.id,
        "recipe_id": new_comment.recipe_id,
        "user_id": new_comment.user_id,
        "parent_id": new_comment.parent_id,
        "content": new_comment.content,
        "likes_count": new_comment.likes_count,
        "created_at": new_comment.created_at,
        "updated_at": new_comment.updated_at,
        "message": "Comment created successfully"
    }


@router.get("/recipes/{recipe_id}/comments")
async def get_recipe_comments(
    recipe_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("recent", enum=["recent", "likes"]),
    include_replies: bool = Query(True),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get comments for a recipe
    
    - **recipe_id**: Recipe UUID
    - **page**: Page number
    - **page_size**: Items per page (1-100)
    - **sort_by**: Sort order (recent, likes)
    - **include_replies**: Include nested replies (default: True)
    """
    # Get top-level comments only (parent_id is null)
    query = select(Comment).where(
        Comment.recipe_id == recipe_id,
        Comment.parent_id.is_(None)
    )
    
    # Apply sorting
    if sort_by == "likes":
        query = query.order_by(Comment.likes_count.desc(), Comment.created_at.desc())
    else:  # recent
        query = query.order_by(Comment.created_at.desc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # Execute query with user relationship
    result = await db.execute(query.options(selectinload(Comment.user)))
    comments = result.scalars().all()
    
    # Get total count of top-level comments
    count_result = await db.execute(
        select(func.count()).select_from(Comment).where(
            Comment.recipe_id == recipe_id,
            Comment.parent_id.is_(None)
        )
    )
    total_count = count_result.scalar()
    
    # Format response
    comments_data = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "recipe_id": comment.recipe_id,
            "user": {
                "id": comment.user.id,
                "username": comment.user.username,
                "full_name": comment.user.full_name,
                "avatar_url": comment.user.avatar_url
            },
            "content": comment.content,
            "likes_count": comment.likes_count,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "replies": []
        }
        
        # Load replies if requested
        if include_replies:
            replies_result = await db.execute(
                select(Comment)
                .where(Comment.parent_id == comment.id)
                .order_by(Comment.created_at.asc())
                .options(selectinload(Comment.user))
            )
            replies = replies_result.scalars().all()
            
            for reply in replies:
                comment_dict["replies"].append({
                    "id": reply.id,
                    "recipe_id": reply.recipe_id,
                    "user": {
                        "id": reply.user.id,
                        "username": reply.user.username,
                        "full_name": reply.user.full_name,
                        "avatar_url": reply.user.avatar_url
                    },
                    "content": reply.content,
                    "likes_count": reply.likes_count,
                    "created_at": reply.created_at,
                    "updated_at": reply.updated_at
                })
        
        comments_data.append(comment_dict)
    
    return {
        "recipe_id": recipe_id,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "comments": comments_data
    }


@router.put("/comments/{comment_id}")
async def update_comment(
    comment_id: UUID,
    content: str = Query(..., min_length=1, max_length=2000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Update user's own comment"""
    result = await db.execute(
        select(Comment).where(
            Comment.id == comment_id,
            Comment.user_id == current_user.id
        )
    )
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or you don't have permission"
        )
    
    comment.content = content
    comment.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(comment)
    
    return {
        "id": comment.id,
        "recipe_id": comment.recipe_id,
        "user_id": comment.user_id,
        "parent_id": comment.parent_id,
        "content": comment.content,
        "likes_count": comment.likes_count,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "message": "Comment updated successfully"
    }


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """Delete user's own comment"""
    result = await db.execute(
        select(Comment).where(
            Comment.id == comment_id,
            Comment.user_id == current_user.id
        )
    )
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or you don't have permission"
        )
    
    # Delete comment and its replies (cascade should handle this)
    await db.delete(comment)
    await db.commit()
    
    return {
        "message": "Comment deleted successfully"
    }


@router.post("/comments/{comment_id}/like")
async def like_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Like a comment (toggle)"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Simple increment (in production, track who liked in separate table)
    comment.likes_count += 1
    
    await db.commit()
    
    return {
        "comment_id": comment_id,
        "likes_count": comment.likes_count,
        "message": "Comment liked"
    }


# ============================================================================
# FAVORITES
# ============================================================================

@router.post("/users/me/favorites/{recipe_id}", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Add recipe to user's favorites"""
    # Verify recipe exists
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check if already favorited
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.recipe_id == recipe_id
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return {
            "id": existing.id,
            "user_id": existing.user_id,
            "recipe_id": existing.recipe_id,
            "created_at": existing.created_at,
            "message": "Recipe already in favorites"
        }
    
    # Create favorite
    new_favorite = Favorite(
        user_id=current_user.id,
        recipe_id=recipe_id
    )
    
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    
    return {
        "id": new_favorite.id,
        "user_id": new_favorite.user_id,
        "recipe_id": new_favorite.recipe_id,
        "created_at": new_favorite.created_at,
        "message": "Recipe added to favorites"
    }


@router.get("/users/me/favorites")
async def get_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get user's favorite recipes"""
    # Build query with recipe relationship
    query = (
        select(Favorite)
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
        .options(selectinload(Favorite.recipe))
    )
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # Execute query
    result = await db.execute(query)
    favorites = result.scalars().all()
    
    # Get total count
    count_result = await db.execute(
        select(func.count()).select_from(Favorite).where(Favorite.user_id == current_user.id)
    )
    total_count = count_result.scalar()
    
    # Format response
    favorites_data = []
    for fav in favorites:
        recipe = fav.recipe
        favorites_data.append({
            "favorite_id": fav.id,
            "created_at": fav.created_at,
            "recipe": {
                "id": recipe.id,
                "title_en": recipe.title_en,
                "title_vi": recipe.title_vi,
                "description_en": recipe.description_en,
                "description_vi": recipe.description_vi,
                "difficulty": recipe.difficulty.value,
                "prep_time": recipe.prep_time_minutes,
                "cook_time": recipe.cook_time_minutes,
                "servings": recipe.servings,
                "image_url": recipe.image_url,
                "rating": recipe.average_rating,
                "rating_count": recipe.ratings_count
            }
        })
    
    return {
        "user_id": current_user.id,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size,
        "favorites": favorites_data
    }


@router.delete("/users/me/favorites/{recipe_id}")
async def remove_favorite(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """Remove recipe from favorites"""
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.recipe_id == recipe_id
        )
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    await db.delete(favorite)
    await db.commit()
    
    return {
        "message": "Recipe removed from favorites"
    }


# ============================================================================
# USER PROFILES
# ============================================================================

@router.get("/users/{user_id}/profile")
async def get_user_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Get user's public profile"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get stats
    ratings_count = await db.execute(
        select(func.count()).select_from(Rating).where(Rating.user_id == user_id)
    )
    ratings_total = ratings_count.scalar()
    
    comments_count = await db.execute(
        select(func.count()).select_from(Comment).where(Comment.user_id == user_id)
    )
    comments_total = comments_count.scalar()
    
    favorites_count = await db.execute(
        select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
    )
    favorites_total = favorites_count.scalar()
    
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "bio": user.bio,
        "dietary_preferences": user.dietary_preferences,
        "allergies": user.allergies,
        "created_at": user.created_at,
        "stats": {
            "ratings_count": ratings_total,
            "comments_count": comments_total,
            "favorites_count": favorites_total
        }
    }


@router.put("/users/me/profile")
async def update_profile(
    full_name: Optional[str] = Query(None, max_length=100),
    bio: Optional[str] = Query(None, max_length=500),
    avatar_url: Optional[str] = Query(None, max_length=500),
    dietary_preferences: Optional[List[str]] = Query(None),
    allergies: Optional[List[str]] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Update user's profile"""
    # Update fields if provided
    if full_name is not None:
        current_user.full_name = full_name
    if bio is not None:
        current_user.bio = bio
    if avatar_url is not None:
        current_user.avatar_url = avatar_url
    if dietary_preferences is not None:
        current_user.dietary_preferences = dietary_preferences
    if allergies is not None:
        current_user.allergies = allergies
    
    await db.commit()
    await db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
        "bio": current_user.bio,
        "dietary_preferences": current_user.dietary_preferences,
        "allergies": current_user.allergies,
        "message": "Profile updated successfully"
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def _update_recipe_rating_stats(recipe_id: UUID, db: AsyncSession):
    """Recalculate recipe's average rating and count"""
    result = await db.execute(
        select(
            func.avg(Rating.rating).label('avg_rating'),
            func.count(Rating.id).label('rating_count')
        )
        .where(Rating.recipe_id == recipe_id)
    )
    stats = result.one()
    
    # Update recipe
    await db.execute(
        update(Recipe)
        .where(Recipe.id == recipe_id)
        .values(
            rating=float(stats.avg_rating) if stats.avg_rating else 0.0,
            rating_count=stats.rating_count
        )
    )
    
    await db.commit()
