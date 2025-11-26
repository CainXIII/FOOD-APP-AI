"""
Ingredient endpoints - CRUD operations for ingredients
"""
from typing import Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.category import Ingredient
from app.core.deps import get_current_admin_user
from app.utils.slug import generate_slug


router = APIRouter()


@router.get("")
async def list_ingredients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    List all ingredients (public endpoint)
    
    - **skip**: Number of items to skip
    - **limit**: Number of items to return
    - **search**: Search in ingredient names
    """
    query = select(Ingredient).order_by(Ingredient.name_vi)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Ingredient.name_vi.ilike(search_term)) | 
            (Ingredient.name_en.ilike(search_term))
        )
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Get ingredients
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    ingredients = result.scalars().all()
    
    return {
        "items": [
            {
                "id": ing.id,
                "name_vi": ing.name_vi,
                "name_en": ing.name_en,
                "slug": ing.slug,
                "image_url": ing.image_url,
                "common_unit": ing.common_unit,
                "calories": ing.calories,
                "protein_g": ing.protein_g,
                "carbs_g": ing.carbs_g,
                "fat_g": ing.fat_g
            }
            for ing in ingredients
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{ingredient_id}")
async def get_ingredient(
    ingredient_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get ingredient by ID"""
    result = await db.execute(
        select(Ingredient).where(Ingredient.id == ingredient_id)
    )
    ingredient = result.scalar_one_or_none()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )
    
    return {
        "id": ingredient.id,
        "name_vi": ingredient.name_vi,
        "name_en": ingredient.name_en,
        "slug": ingredient.slug,
        "description_vi": ingredient.description_vi,
        "description_en": ingredient.description_en,
        "image_url": ingredient.image_url,
        "calories": ingredient.calories,
        "protein_g": ingredient.protein_g,
        "carbs_g": ingredient.carbs_g,
        "fat_g": ingredient.fat_g,
        "fiber_g": ingredient.fiber_g,
        "common_unit": ingredient.common_unit,
        "created_at": ingredient.created_at,
        "updated_at": ingredient.updated_at
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    ingredient_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Create new ingredient (admin only)
    
    - **name_vi**: Vietnamese name (required)
    - **name_en**: English name (required)
    - **description_vi**: Vietnamese description
    - **description_en**: English description
    - **image_url**: Image URL
    - **calories**: Calories per 100g
    - **protein_g**: Protein in grams per 100g
    - **carbs_g**: Carbohydrates in grams per 100g
    - **fat_g**: Fat in grams per 100g
    - **fiber_g**: Fiber in grams per 100g
    - **common_unit**: Common measurement unit
    """
    slug = generate_slug(ingredient_data["name_vi"])
    
    # Check slug uniqueness
    result = await db.execute(
        select(Ingredient).where(Ingredient.slug == slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this name already exists"
        )
    
    ingredient = Ingredient(
        name_vi=ingredient_data["name_vi"],
        name_en=ingredient_data["name_en"],
        slug=slug,
        description_vi=ingredient_data.get("description_vi"),
        description_en=ingredient_data.get("description_en"),
        image_url=ingredient_data.get("image_url"),
        calories=ingredient_data.get("calories"),
        protein_g=ingredient_data.get("protein_g"),
        carbs_g=ingredient_data.get("carbs_g"),
        fat_g=ingredient_data.get("fat_g"),
        fiber_g=ingredient_data.get("fiber_g"),
        common_unit=ingredient_data.get("common_unit", "g")
    )
    
    db.add(ingredient)
    await db.commit()
    await db.refresh(ingredient)
    
    return {
        "id": ingredient.id,
        "name_vi": ingredient.name_vi,
        "name_en": ingredient.name_en,
        "slug": ingredient.slug,
        "description_vi": ingredient.description_vi,
        "description_en": ingredient.description_en,
        "calories": ingredient.calories,
        "protein_g": ingredient.protein_g,
        "carbs_g": ingredient.carbs_g,
        "fat_g": ingredient.fat_g,
        "fiber_g": ingredient.fiber_g,
        "common_unit": ingredient.common_unit,
        "created_at": ingredient.created_at,
        "updated_at": ingredient.updated_at
    }


@router.put("/{ingredient_id}")
async def update_ingredient(
    ingredient_id: UUID,
    ingredient_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """Update ingredient (admin only)"""
    result = await db.execute(
        select(Ingredient).where(Ingredient.id == ingredient_id)
    )
    ingredient = result.scalar_one_or_none()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )
    
    # Update fields
    for field, value in ingredient_data.items():
        if hasattr(ingredient, field):
            setattr(ingredient, field, value)
    
    # If name changed, regenerate slug and check for duplicates
    if "name_vi" in ingredient_data:
        new_slug = generate_slug(ingredient.name_vi)
        
        # Check if new slug conflicts with another ingredient
        result = await db.execute(
            select(Ingredient).where(
                Ingredient.slug == new_slug,
                Ingredient.id != ingredient_id
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient with this name already exists"
            )
        
        ingredient.slug = new_slug
    
    await db.commit()
    await db.refresh(ingredient)
    
    return {
        "id": ingredient.id,
        "name_vi": ingredient.name_vi,
        "name_en": ingredient.name_en,
        "slug": ingredient.slug,
        "description_vi": ingredient.description_vi,
        "description_en": ingredient.description_en,
        "calories": ingredient.calories,
        "protein_g": ingredient.protein_g,
        "carbs_g": ingredient.carbs_g,
        "fat_g": ingredient.fat_g,
        "fiber_g": ingredient.fiber_g,
        "common_unit": ingredient.common_unit,
        "created_at": ingredient.created_at,
        "updated_at": ingredient.updated_at
    }


@router.delete("/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """Delete ingredient (admin only)"""
    result = await db.execute(
        select(Ingredient).where(Ingredient.id == ingredient_id)
    )
    ingredient = result.scalar_one_or_none()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )
    
    name = ingredient.name_vi
    await db.delete(ingredient)
    await db.commit()
    
    return {
        "message": "Ingredient deleted successfully",
        "detail": f"Ingredient '{name}' has been deleted"
    }
