"""
Category endpoints - Recipe category management
"""
from typing import Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.category import Category
from app.core.deps import get_current_user, get_current_admin_user, get_optional_current_user
from app.schemas.base import MessageResponse


router = APIRouter()


@router.get("")
async def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get all categories (public endpoint)
    
    - **page**: Page number
    - **page_size**: Items per page
    - **is_active**: Filter by active status
    """
    query = select(Category).order_by(Category.display_order, Category.name_vi)
    
    if is_active is not None:
        query = query.where(Category.is_active == is_active)
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()
    
    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    result = await db.execute(query)
    categories = result.scalars().all()
    
    return {
        "items": [
            {
                "id": cat.id,
                "name_vi": cat.name_vi,
                "name_en": cat.name_en,
                "slug": cat.slug,
                "description_vi": cat.description_vi,
                "description_en": cat.description_en,
                "icon_url": cat.icon_url,
                "image_url": cat.image_url,
                "display_order": cat.display_order,
                "is_active": cat.is_active,
                "created_at": cat.created_at,
                "updated_at": cat.updated_at
            }
            for cat in categories
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.get("/{category_id}")
async def get_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get category by ID"""
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return {
        "id": category.id,
        "name_vi": category.name_vi,
        "name_en": category.name_en,
        "slug": category.slug,
        "description_vi": category.description_vi,
        "description_en": category.description_en,
        "icon_url": category.icon_url,
        "image_url": category.image_url,
        "display_order": category.display_order,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "updated_at": category.updated_at
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Create new category (admin only)
    """
    from app.utils.slug import generate_slug
    
    slug = generate_slug(category_data["name_vi"])
    
    # Check slug uniqueness
    result = await db.execute(
        select(Category).where(Category.slug == slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    category = Category(
        name_vi=category_data["name_vi"],
        name_en=category_data.get("name_en", category_data["name_vi"]),
        slug=slug,
        description_vi=category_data.get("description_vi"),
        description_en=category_data.get("description_en"),
        icon_url=category_data.get("icon_url"),
        image_url=category_data.get("image_url"),
        display_order=category_data.get("display_order", 0),
        is_active=category_data.get("is_active", True)
    )
    
    db.add(category)
    await db.commit()
    await db.refresh(category)
    
    return {
        "id": category.id,
        "name_vi": category.name_vi,
        "name_en": category.name_en,
        "slug": category.slug,
        "display_order": category.display_order,
        "is_active": category.is_active
    }


@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """Update category (admin only)"""
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    for field, value in category_data.items():
        if hasattr(category, field):
            setattr(category, field, value)
    
    await db.commit()
    await db.refresh(category)
    
    return {
        "id": category.id,
        "name_vi": category.name_vi,
        "name_en": category.name_en,
        "slug": category.slug,
        "is_active": category.is_active
    }


@router.delete("/{category_id}", response_model=MessageResponse)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """Delete category (admin only)"""
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    await db.delete(category)
    await db.commit()
    
    return {
        "message": "Category deleted successfully",
        "detail": f"Category '{category.name_vi}' has been deleted"
    }
