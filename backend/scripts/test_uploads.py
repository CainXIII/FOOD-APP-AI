"""
Test File Upload Endpoints
Tests image and audio file uploads with various scenarios
"""
import asyncio
import httpx
from pathlib import Path
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
USER_CREDS = {
    "email": "recipe_test@cooking.app",
    "password": "Test1234"
}

ADMIN_CREDS = {
    "email": "admin@cooking.app",
    "password": "Admin1234"
}


async def get_token(email: str, password: str) -> str:
    """Login and get access token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        return response.json()["access_token"]


def create_test_image(width: int = 800, height: int = 600) -> BytesIO:
    """Create a test image in memory"""
    img = Image.new('RGB', (width, height), color=(73, 109, 137))
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer


def create_test_audio() -> BytesIO:
    """Create a test audio file (simple WAV header)"""
    # Simple WAV file header for testing
    buffer = BytesIO()
    # Write minimal WAV header
    buffer.write(b'RIFF')
    buffer.write((36).to_bytes(4, 'little'))  # File size - 8
    buffer.write(b'WAVE')
    buffer.write(b'fmt ')
    buffer.write((16).to_bytes(4, 'little'))  # Format chunk size
    buffer.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
    buffer.write((1).to_bytes(2, 'little'))   # Number of channels
    buffer.write((44100).to_bytes(4, 'little'))  # Sample rate
    buffer.write((88200).to_bytes(4, 'little'))  # Byte rate
    buffer.write((2).to_bytes(2, 'little'))   # Block align
    buffer.write((16).to_bytes(2, 'little'))  # Bits per sample
    buffer.write(b'data')
    buffer.write((0).to_bytes(4, 'little'))   # Data size
    buffer.seek(0)
    return buffer


async def get_test_recipe_id(token: str) -> str:
    """Get a test recipe ID"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/recipes",
            headers={"Authorization": f"Bearer {token}"}
        )
        recipes = response.json()
        if recipes['items']:
            return recipes['items'][0]['id']
        return None


async def test_upload_avatar():
    """Test: Upload user avatar"""
    print("\n=== Test: Upload User Avatar ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    # Create test image
    image_data = create_test_image(400, 400)
    
    async with httpx.AsyncClient() as client:
        files = {"file": ("avatar.jpg", image_data, "image/jpeg")}
        response = await client.post(
            f"{BASE_URL}/uploads/users/avatar",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Failed: {response.text}"
        result = response.json()
        print(f"✓ Avatar uploaded successfully")
        print(f"  - URL: {result['avatar_url']}")
        return result['avatar_url']


async def test_delete_avatar():
    """Test: Delete user avatar"""
    print("\n=== Test: Delete User Avatar ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}/uploads/users/avatar",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Failed: {response.text}"
        print(f"✓ Avatar deleted successfully")


async def test_upload_recipe_image():
    """Test: Upload recipe image"""
    print("\n=== Test: Upload Recipe Image ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    # Get a recipe
    recipe_id = await get_test_recipe_id(token)
    if not recipe_id:
        print("⊘ Skipped (no recipes found)")
        return None
    
    # Create test image
    image_data = create_test_image(1200, 800)
    
    async with httpx.AsyncClient() as client:
        files = {"file": ("recipe.jpg", image_data, "image/jpeg")}
        response = await client.post(
            f"{BASE_URL}/uploads/recipes/{recipe_id}/image",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Failed: {response.text}"
        result = response.json()
        print(f"✓ Recipe image uploaded successfully")
        print(f"  - Recipe ID: {recipe_id}")
        print(f"  - URL: {result['image_url']}")
        return recipe_id


async def test_delete_recipe_image(recipe_id: str):
    """Test: Delete recipe image"""
    print("\n=== Test: Delete Recipe Image ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}/uploads/recipes/{recipe_id}/image",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Failed: {response.text}"
        print(f"✓ Recipe image deleted successfully")


async def test_upload_audio():
    """Test: Upload audio file"""
    print("\n=== Test: Upload Audio File ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    # Create test audio
    audio_data = create_test_audio()
    
    async with httpx.AsyncClient() as client:
        files = {"file": ("voice.wav", audio_data, "audio/wav")}
        response = await client.post(
            f"{BASE_URL}/uploads/chat/audio",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Failed: {response.text}"
        result = response.json()
        print(f"✓ Audio uploaded successfully")
        print(f"  - URL: {result['audio_url']}")
        print(f"  - Filename: {result['filename']}")


async def test_invalid_file_type():
    """Test: Upload invalid file type (should fail)"""
    print("\n=== Test: Invalid File Type (Should Fail) ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    # Create a text file
    text_data = BytesIO(b"This is not an image")
    
    async with httpx.AsyncClient() as client:
        files = {"file": ("test.txt", text_data, "text/plain")}
        response = await client.post(
            f"{BASE_URL}/uploads/users/avatar",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400, f"Should be bad request, got: {response.status_code}"
        print(f"✓ Invalid file type rejected (400 Bad Request)")


async def test_unauthorized_upload():
    """Test: Upload without authentication (should fail)"""
    print("\n=== Test: Unauthorized Upload (Should Fail) ===")
    
    image_data = create_test_image()
    
    async with httpx.AsyncClient() as client:
        files = {"file": ("avatar.jpg", image_data, "image/jpeg")}
        response = await client.post(
            f"{BASE_URL}/uploads/users/avatar",
            files=files
        )
        
        assert response.status_code == 401, f"Should be unauthorized, got: {response.status_code}"
        print(f"✓ Unauthorized upload rejected (401 Unauthorized)")


async def test_file_info():
    """Test: Get file info without saving"""
    print("\n=== Test: Test Upload (Get File Info) ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    image_data = create_test_image(1920, 1080)
    
    async with httpx.AsyncClient() as client:
        files = {"file": ("test.jpg", image_data, "image/jpeg")}
        response = await client.post(
            f"{BASE_URL}/uploads/test/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Failed: {response.text}"
        result = response.json()
        print(f"✓ File info retrieved")
        print(f"  - Filename: {result['filename']}")
        print(f"  - Type: {result['content_type']}")
        print(f"  - Size: {result['size_mb']} MB")


async def main():
    """Run all upload tests"""
    print("=" * 60)
    print("FILE UPLOAD ENDPOINTS TESTS")
    print("=" * 60)
    
    try:
        # Test file info
        await test_file_info()
        
        # Test avatar upload/delete
        await test_upload_avatar()
        await test_delete_avatar()
        
        # Upload avatar again for subsequent tests
        await test_upload_avatar()
        
        # Test recipe image upload/delete
        recipe_id = await test_upload_recipe_image()
        if recipe_id:
            await test_delete_recipe_image(recipe_id)
            # Upload again for visual testing
            await test_upload_recipe_image()
        
        # Test audio upload
        await test_upload_audio()
        
        # Test error cases
        await test_invalid_file_type()
        await test_unauthorized_upload()
        
        print("\n" + "=" * 60)
        print("✓ ALL UPLOAD TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
