"""
File upload service for handling images and audio files
Supports both local storage and Cloudinary cloud storage
"""
from typing import Optional, Tuple
from pathlib import Path
import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
import aiofiles

from app.config import get_settings

settings = get_settings()

# Upload directories
UPLOAD_DIR = Path("uploads")
RECIPE_IMAGES_DIR = UPLOAD_DIR / "recipes"
USER_AVATARS_DIR = UPLOAD_DIR / "avatars"
AUDIO_DIR = UPLOAD_DIR / "audio"

# Allowed file types
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg", "audio/webm"}

# Max file sizes (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB


def ensure_upload_directories():
    """Create upload directories if they don't exist"""
    RECIPE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    USER_AVATARS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def validate_file(file: UploadFile, allowed_types: set, max_size: int) -> None:
    """
    Validate uploaded file
    
    Args:
        file: Uploaded file
        allowed_types: Set of allowed MIME types
        max_size: Maximum file size in bytes
        
    Raises:
        HTTPException: If validation fails
    """
    # Check content type
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Check file size (if available in headers)
    if hasattr(file, 'size') and file.size and file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {max_size / (1024*1024):.1f}MB"
        )


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename preserving extension
    
    Args:
        original_filename: Original filename
        
    Returns:
        Unique filename with timestamp and UUID
    """
    # Get file extension
    ext = Path(original_filename).suffix.lower()
    
    # Generate unique name
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{timestamp}_{unique_id}{ext}"


async def save_file_local(file: UploadFile, directory: Path) -> str:
    """
    Save file to local storage
    
    Args:
        file: Uploaded file
        directory: Target directory
        
    Returns:
        Relative file path
    """
    # Generate unique filename
    filename = generate_unique_filename(file.filename)
    file_path = directory / filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Return relative path from uploads directory
    return str(file_path.relative_to(UPLOAD_DIR))


async def upload_recipe_image(file: UploadFile, use_cloud: bool = False) -> str:
    """
    Upload recipe image
    
    Args:
        file: Uploaded image file
        use_cloud: Whether to use cloud storage (Cloudinary)
        
    Returns:
        File URL or path
    """
    ensure_upload_directories()
    validate_file(file, ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE)
    
    if use_cloud:
        # TODO: Implement Cloudinary upload
        # For now, fall back to local storage
        pass
    
    # Save to local storage
    relative_path = await save_file_local(file, RECIPE_IMAGES_DIR)
    
    # Return full URL or path
    base_url = settings.BASE_URL if hasattr(settings, 'BASE_URL') else "http://localhost:8000"
    return f"{base_url}/uploads/{relative_path}"


async def upload_user_avatar(file: UploadFile, use_cloud: bool = False) -> str:
    """
    Upload user avatar image
    
    Args:
        file: Uploaded image file
        use_cloud: Whether to use cloud storage
        
    Returns:
        File URL or path
    """
    ensure_upload_directories()
    validate_file(file, ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE)
    
    if use_cloud:
        # TODO: Implement Cloudinary upload
        pass
    
    # Save to local storage
    relative_path = await save_file_local(file, USER_AVATARS_DIR)
    
    base_url = settings.BASE_URL if hasattr(settings, 'BASE_URL') else "http://localhost:8000"
    return f"{base_url}/uploads/{relative_path}"


async def upload_audio(file: UploadFile, use_cloud: bool = False) -> str:
    """
    Upload audio file (for voice chat)
    
    Args:
        file: Uploaded audio file
        use_cloud: Whether to use cloud storage
        
    Returns:
        File URL or path
    """
    ensure_upload_directories()
    validate_file(file, ALLOWED_AUDIO_TYPES, MAX_AUDIO_SIZE)
    
    if use_cloud:
        # TODO: Implement cloud storage upload
        pass
    
    # Save to local storage
    relative_path = await save_file_local(file, AUDIO_DIR)
    
    base_url = settings.BASE_URL if hasattr(settings, 'BASE_URL') else "http://localhost:8000"
    return f"{base_url}/uploads/{relative_path}"


def delete_file(file_path: str) -> bool:
    """
    Delete file from storage
    
    Args:
        file_path: Path to file (relative to uploads directory)
        
    Returns:
        True if deleted successfully
    """
    try:
        # Extract relative path from URL if it's a full URL
        if file_path.startswith("http"):
            file_path = file_path.split("/uploads/")[-1]
        
        full_path = UPLOAD_DIR / file_path
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


# Optional: Cloudinary integration (requires cloudinary package)
try:
    import cloudinary
    import cloudinary.uploader
    
    CLOUDINARY_ENABLED = False  # Set to True when configured
    
    def configure_cloudinary():
        """Configure Cloudinary with environment variables"""
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET")
        )
    
    async def upload_to_cloudinary(file: UploadFile, folder: str) -> str:
        """
        Upload file to Cloudinary
        
        Args:
            file: Uploaded file
            folder: Cloudinary folder name
            
        Returns:
            Cloudinary URL
        """
        configure_cloudinary()
        
        # Read file content
        content = await file.read()
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            content,
            folder=folder,
            resource_type="auto"
        )
        
        return result["secure_url"]

except ImportError:
    CLOUDINARY_ENABLED = False
