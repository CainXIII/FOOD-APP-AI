"""
File upload endpoints
Handles image and audio uploads for recipes, avatars, and voice chat
"""
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.database import get_db
from app.models.user import User
from app.models.recipe import Recipe
from app.core.deps import get_current_user
from app.services.upload_service import (
    upload_recipe_image,
    upload_user_avatar,
    upload_audio,
    delete_file
)

router = APIRouter()


@router.post("/recipes/{recipe_id}/image")
async def upload_recipe_image_endpoint(
    recipe_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Upload recipe image
    
    - **recipe_id**: Recipe UUID
    - **file**: Image file (JPEG, PNG, WebP, GIF, max 10MB)
    
    Returns:
        Image URL
    """
    # Convert recipe_id to UUID if needed
    from uuid import UUID
    try:
        recipe_uuid = UUID(recipe_id) if isinstance(recipe_id, str) else recipe_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recipe ID format"
        )
    
    # Verify recipe exists and belongs to user
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_uuid)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check ownership (or admin)
    if recipe.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload image for this recipe"
        )
    
    # Upload image
    image_url = await upload_recipe_image(file)
    
    # Delete old image if exists
    if recipe.thumbnail_url:
        delete_file(recipe.thumbnail_url)
    
    # Update recipe with new image URL
    recipe.thumbnail_url = image_url
    recipe.image_url = image_url  # Use same image for both thumbnail and full size
    
    await db.commit()
    
    return {
        "message": "Image uploaded successfully",
        "image_url": image_url,
        "thumbnail_url": image_url
    }


@router.delete("/recipes/{recipe_id}/image")
async def delete_recipe_image_endpoint(
    recipe_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete recipe image
    
    - **recipe_id**: Recipe UUID
    """
    # Convert recipe_id to UUID if needed
    from uuid import UUID
    try:
        recipe_uuid = UUID(recipe_id) if isinstance(recipe_id, str) else recipe_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recipe ID format"
        )
    
    # Verify recipe exists and belongs to user
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_uuid)
    )
    recipe = result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Check ownership (or admin)
    if recipe.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete image for this recipe"
        )
    
    if not recipe.thumbnail_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe has no image"
        )
    
    # Delete file
    delete_file(recipe.thumbnail_url)
    
    # Remove from database
    recipe.thumbnail_url = None
    recipe.image_url = None
    
    await db.commit()
    
    return {"message": "Image deleted successfully"}


@router.post("/users/avatar")
async def upload_avatar_endpoint(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Upload user avatar
    
    - **file**: Image file (JPEG, PNG, WebP, GIF, max 10MB)
    
    Returns:
        Avatar URL
    """
    # Upload avatar
    avatar_url = await upload_user_avatar(file)
    
    # Delete old avatar if exists
    if current_user.avatar_url:
        delete_file(current_user.avatar_url)
    
    # Update user with new avatar URL
    current_user.avatar_url = avatar_url
    
    await db.commit()
    
    return {
        "message": "Avatar uploaded successfully",
        "avatar_url": avatar_url
    }


@router.delete("/users/avatar")
async def delete_avatar_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete user avatar
    """
    if not current_user.avatar_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no avatar"
        )
    
    # Delete file
    delete_file(current_user.avatar_url)
    
    # Remove from database
    current_user.avatar_url = None
    
    await db.commit()
    
    return {"message": "Avatar deleted successfully"}


@router.post("/chat/audio")
async def upload_audio_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Upload audio file for voice chat
    
    - **file**: Audio file (MP3, WAV, OGG, WebM, max 50MB)
    
    Returns:
        Audio URL and file info
    """
    # Upload audio
    audio_url = await upload_audio(file)
    
    return {
        "message": "Audio uploaded successfully",
        "audio_url": audio_url,
        "filename": file.filename,
        "content_type": file.content_type
    }


@router.post("/test/upload")
async def test_upload_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Test file upload endpoint
    
    Returns file info without saving
    """
    # Read file to check size
    content = await file.read()
    file_size = len(content)
    
    # Reset file pointer
    await file.seek(0)
    
    return {
        "message": "File info retrieved successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": file_size,
        "size_mb": round(file_size / (1024 * 1024), 2)
    }
