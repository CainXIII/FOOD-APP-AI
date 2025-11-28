"""
Recipe endpoints - CRUD operations for recipes
"""
from typing import Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, or_, and_
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.recipe import Recipe, RecipeIngredient, RecipeStep, NutritionFacts, DifficultyLevel
from app.models.category import Category
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeDetailResponse,
    RecipeListItem,
    RecipePaginatedResponse,
    RecipeFilter
)
from app.schemas.base import MessageResponse
from app.core.deps import get_current_user, get_optional_current_user
from app.utils.slug import generate_slug


router = APIRouter()


@router.post("", response_model=RecipeDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_data: RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new recipe
    
    - **title_vi**: Vietnamese title (required)
    - **title_en**: English title (optional)
    - **description_vi**: Vietnamese description (required)
    - **category_id**: Category UUID
    - **ingredients**: List of ingredients with quantities
    - **steps**: List of cooking steps
    """
    # Verify category exists
    result = await db.execute(
        select(Category).where(Category.id == recipe_data.category_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Generate slug from title
    slug = generate_slug(recipe_data.title_vi)
    
    # Check slug uniqueness
    result = await db.execute(
        select(Recipe).where(Recipe.slug == slug)
    )
    if result.scalar_one_or_none():
        # Add random suffix if slug exists
        import random
        slug = f"{slug}-{random.randint(1000, 9999)}"
    
    # Calculate total time
    total_time = recipe_data.prep_time_minutes + recipe_data.cook_time_minutes
    
    # Create recipe
    recipe = Recipe(
        user_id=current_user.id,
        category_id=recipe_data.category_id,
        title_vi=recipe_data.title_vi,
        title_en=recipe_data.title_en or recipe_data.title_vi,
        slug=slug,
        description_vi=recipe_data.description_vi,
        description_en=recipe_data.description_en or recipe_data.description_vi,
        thumbnail_url=recipe_data.thumbnail_url,
        image_url=recipe_data.thumbnail_url,
        video_url=recipe_data.video_url,
        prep_time_minutes=recipe_data.prep_time_minutes,
        cook_time_minutes=recipe_data.cook_time_minutes,
        total_time_minutes=total_time,
        servings=recipe_data.servings,
        difficulty=DifficultyLevel(recipe_data.difficulty),
        is_vegetarian=recipe_data.is_vegetarian,
        is_vegan=recipe_data.is_vegan,
        is_gluten_free=recipe_data.is_gluten_free,
        is_dairy_free=recipe_data.is_dairy_free,
        allergens=recipe_data.allergens,
        is_published=True,
        is_featured=False
    )
    
    db.add(recipe)
    await db.flush()  # Get recipe ID
    
    # Add ingredients
    for idx, ing_data in enumerate(recipe_data.ingredients):
        ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ing_data.ingredient_id,
            quantity=ing_data.quantity,
            unit=ing_data.unit,
            name_vi=ing_data.ingredient_name_vi,
            name_en=ing_data.ingredient_name_en,
            notes_vi=ing_data.notes,
            notes_en=ing_data.notes,
            is_optional=False,
            order_index=idx
        )
        db.add(ingredient)
    
    # Add steps
    for step_data in recipe_data.steps:
        step = RecipeStep(
            recipe_id=recipe.id,
            step_number=step_data.step_number,
            instruction_vi=step_data.instruction_vi,
            instruction_en=step_data.instruction_en or step_data.instruction_vi,
            image_url=step_data.image_url,
            video_url=None,
            duration_minutes=step_data.duration_minutes,
            tips_vi=step_data.tips,
            tips_en=step_data.tips
        )
        db.add(step)
    
    # Add nutrition facts if provided
    if recipe_data.nutrition:
        nutrition = NutritionFacts(
            recipe_id=recipe.id,
            calories=recipe_data.nutrition.calories or 0,
            protein_g=recipe_data.nutrition.protein_g or 0,
            carbs_g=recipe_data.nutrition.carbs_g or 0,
            fat_g=recipe_data.nutrition.fat_g or 0,
            fiber_g=recipe_data.nutrition.fiber_g,
            sugar_g=recipe_data.nutrition.sugar_g,
            sodium_mg=recipe_data.nutrition.sodium_mg,
            cholesterol_mg=recipe_data.nutrition.cholesterol_mg
        )
        db.add(nutrition)
    
    await db.commit()
    await db.refresh(recipe)
    
    # Load relationships for response
    result = await db.execute(
        select(Recipe)
        .options(
            selectinload(Recipe.ingredients),
            selectinload(Recipe.steps),
            selectinload(Recipe.nutrition_facts)
        )
        .where(Recipe.id == recipe.id)
    )
    recipe = result.scalar_one()
    
    # Build response (simplified - would need proper mapping)
    return {
        "id": recipe.id,
        "title_vi": recipe.title_vi,
        "title_en": recipe.title_en,
        "slug": recipe.slug,
        "description_vi": recipe.description_vi,
        "description_en": recipe.description_en,
        "thumbnail_url": recipe.thumbnail_url,
        "category_id": recipe.category_id,
        "category_name_vi": category.name_vi,
        "author_id": recipe.user_id,
        "author_name": current_user.full_name,
        "author_avatar": current_user.avatar_url,
        "prep_time_minutes": recipe.prep_time_minutes,
        "cook_time_minutes": recipe.cook_time_minutes,
        "total_time_minutes": recipe.total_time_minutes,
        "servings": recipe.servings,
        "difficulty": recipe.difficulty.value,
        "is_vegetarian": recipe.is_vegetarian,
        "is_vegan": recipe.is_vegan,
        "is_gluten_free": recipe.is_gluten_free,
        "is_dairy_free": recipe.is_dairy_free,
        "allergens": recipe.allergens or [],
        "avg_rating": recipe.average_rating,
        "total_ratings": recipe.ratings_count,
        "total_favorites": recipe.favorites_count,
        "total_comments": recipe.comments_count,
        "view_count": recipe.views_count,
        "is_featured": recipe.is_featured,
        "is_published": recipe.is_published,
        "video_url": recipe.video_url,
        "ingredients": [],
        "steps": [],
        "nutrition": None,
        "created_at": recipe.created_at,
        "updated_at": recipe.updated_at
    }


@router.get("", response_model=RecipePaginatedResponse)
async def list_recipes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[UUID] = None,
    difficulty: Optional[str] = None,
    is_vegetarian: Optional[bool] = None,
    is_vegan: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|average_rating|views_count)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Get paginated list of recipes
    
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **category_id**: Filter by category
    - **difficulty**: Filter by difficulty (easy/medium/hard)
    - **is_vegetarian**: Filter vegetarian recipes
    - **is_vegan**: Filter vegan recipes
    - **is_featured**: Filter featured recipes
    - **search**: Search in title and description
    - **sort_by**: Sort field (created_at, average_rating, views_count)
    - **sort_order**: Sort direction (asc, desc)
    """
    # Build query
    query = select(Recipe).where(Recipe.is_published == True)
    
    # Apply filters
    if category_id:
        query = query.where(Recipe.category_id == category_id)
    
    if difficulty:
        try:
            diff_level = DifficultyLevel(difficulty)
            query = query.where(Recipe.difficulty == diff_level)
        except ValueError:
            pass
    
    if is_vegetarian is not None:
        query = query.where(Recipe.is_vegetarian == is_vegetarian)
    
    if is_vegan is not None:
        query = query.where(Recipe.is_vegan == is_vegan)
    
    if is_featured is not None:
        query = query.where(Recipe.is_featured == is_featured)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Recipe.title_vi.ilike(search_term),
                Recipe.title_en.ilike(search_term),
                Recipe.description_vi.ilike(search_term),
                Recipe.description_en.ilike(search_term)
            )
        )
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()
    
    # Apply sorting
    sort_column = getattr(Recipe, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # Add joins for category and user
    query = query.options(
        selectinload(Recipe.category),
        selectinload(Recipe.user)
    )
    
    # Execute query
    result = await db.execute(query)
    recipes = result.scalars().all()
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size
    
    # Transform to list items with proper joins
    items = []
    for recipe in recipes:
        items.append({
            "id": recipe.id,
            "title_vi": recipe.title_vi,
            "title_en": recipe.title_en,
            "slug": recipe.slug,
            "description_vi": recipe.description_vi,
            "thumbnail_url": recipe.thumbnail_url,
            "category_id": recipe.category_id,
            "category_name_vi": recipe.category.name_vi if recipe.category else "",
            "author_id": recipe.user_id,
            "author_name": recipe.user.full_name if recipe.user else "Unknown",
            "author_avatar": recipe.user.avatar_url if recipe.user else None,
            "prep_time_minutes": recipe.prep_time_minutes,
            "cook_time_minutes": recipe.cook_time_minutes,
            "total_time_minutes": recipe.total_time_minutes,
            "servings": recipe.servings,
            "difficulty": recipe.difficulty.value,
            "is_vegetarian": recipe.is_vegetarian,
            "is_vegan": recipe.is_vegan,
            "avg_rating": recipe.average_rating or 0.0,
            "total_ratings": recipe.ratings_count or 0,
            "total_favorites": recipe.favorites_count or 0,
            "is_featured": recipe.is_featured,
            "created_at": recipe.created_at,
            "updated_at": recipe.updated_at
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Get recipe by ID
    
    Increments view count
    """
    result = await db.execute(
        select(Recipe)
        .options(
            selectinload(Recipe.ingredients),
            selectinload(Recipe.steps),
            selectinload(Recipe.nutrition_facts)
        )
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Increment view count
    recipe.views_count += 1
    await db.commit()
    
    # Return placeholder response
    return {
        "id": recipe.id,
        "title_vi": recipe.title_vi,
        "created_at": recipe.created_at,
        "updated_at": recipe.updated_at
    }


@router.put("/{recipe_id}", response_model=RecipeDetailResponse)
async def update_recipe(
    recipe_id: UUID,
    recipe_data: RecipeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update recipe
    
    Only recipe author or admin can update
    """
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check permission
    if recipe.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this recipe"
        )
    
    # Update fields
    update_data = recipe_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(recipe, field):
            setattr(recipe, field, value)
    
    # Recalculate total time if prep or cook time changed
    if 'prep_time_minutes' in update_data or 'cook_time_minutes' in update_data:
        recipe.total_time_minutes = recipe.prep_time_minutes + recipe.cook_time_minutes
    
    await db.commit()
    await db.refresh(recipe)
    
    return {"id": recipe.id, "title_vi": recipe.title_vi}


@router.delete("/{recipe_id}", response_model=MessageResponse)
async def delete_recipe(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete recipe
    
    Only recipe author or admin can delete
    """
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check permission
    if recipe.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this recipe"
        )
    
    await db.execute(delete(Recipe).where(Recipe.id == recipe_id))
    await db.commit()
    
    return {
        "message": "Recipe deleted successfully",
        "detail": f"Recipe '{recipe.title_vi}' has been deleted"
    }


@router.get("/{recipe_id}/ingredients")
async def get_recipe_ingredients(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get recipe ingredients"""
    result = await db.execute(
        select(RecipeIngredient)
        .where(RecipeIngredient.recipe_id == recipe_id)
        .order_by(RecipeIngredient.order_index)
    )
    ingredients = result.scalars().all()
    
    return {"ingredients": []}


@router.get("/{recipe_id}/steps")
async def get_recipe_steps(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get recipe steps"""
    result = await db.execute(
        select(RecipeStep)
        .where(RecipeStep.recipe_id == recipe_id)
        .order_by(RecipeStep.step_number)
    )
    steps = result.scalars().all()
    
    return {"steps": []}
