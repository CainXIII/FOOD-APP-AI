"""
Test script for Ingredient Management API
Tests all ingredient endpoints with proper authentication
"""

import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
ADMIN_CREDS = {
    "email": "admin@cooking.app",
    "password": "Admin1234"
}

USER_CREDS = {
    "email": "recipe_test@cooking.app",
    "password": "Test1234"
}

async def get_token(email: str, password: str) -> str:
    """Login and get access token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        return response.json()["access_token"]

async def test_list_ingredients():
    """Test: List all ingredients (public endpoint)"""
    print("\n=== Test: List All Ingredients ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/ingredients")
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        print(f"✓ Total ingredients: {data['total']}")
        print(f"✓ Page 1 items: {len(data['items'])}")
        if data['items']:
            ingredient = data['items'][0]
            print(f"✓ Sample: {ingredient['name_vi']} ({ingredient['name_en']})")
            print(f"  - Slug: {ingredient['slug']}")
            print(f"  - Calories: {ingredient['calories']} per 100{ingredient['common_unit']}")
            print(f"  - Protein: {ingredient['protein_g']}g, Carbs: {ingredient['carbs_g']}g, Fat: {ingredient['fat_g']}g")
        return data['items'][0]['id'] if data['items'] else None

async def test_search_ingredients():
    """Test: Search ingredients by name"""
    print("\n=== Test: Search Ingredients ===")
    async with httpx.AsyncClient() as client:
        # Search for "thịt" (meat)
        response = await client.get(f"{BASE_URL}/ingredients?search=thịt")
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        print(f"✓ Search 'thịt': {data['total']} results")
        for item in data['items'][:3]:
            print(f"  - {item['name_vi']} ({item['name_en']})")
        
        # Search for "chicken"
        response = await client.get(f"{BASE_URL}/ingredients?search=chicken")
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        print(f"✓ Search 'chicken': {data['total']} results")

async def test_pagination():
    """Test: Pagination"""
    print("\n=== Test: Pagination ===")
    async with httpx.AsyncClient() as client:
        # Get first page (5 items)
        response = await client.get(f"{BASE_URL}/ingredients?page=1&page_size=5")
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        print(f"✓ Page 1 (size=5): {len(data['items'])} items")
        
        # Get second page
        response = await client.get(f"{BASE_URL}/ingredients?page=2&page_size=5")
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        print(f"✓ Page 2 (size=5): {len(data['items'])} items")

async def test_get_ingredient_detail(ingredient_id: str):
    """Test: Get ingredient detail"""
    print("\n=== Test: Get Ingredient Detail ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/ingredients/{ingredient_id}")
        assert response.status_code == 200, f"Failed: {response.text}"
        ingredient = response.json()
        print(f"✓ Ingredient: {ingredient['name_vi']} ({ingredient['name_en']})")
        print(f"  - ID: {ingredient['id']}")
        print(f"  - Slug: {ingredient['slug']}")
        print(f"  - Nutritional Info (per 100{ingredient['common_unit']}):")
        print(f"    * Calories: {ingredient['calories']} kcal")
        print(f"    * Protein: {ingredient['protein_g']}g")
        print(f"    * Carbs: {ingredient['carbs_g']}g")
        print(f"    * Fat: {ingredient['fat_g']}g")
        if ingredient['fiber_g']:
            print(f"    * Fiber: {ingredient['fiber_g']}g")
        print(f"  - Created: {ingredient['created_at']}")

async def test_create_ingredient_as_user():
    """Test: Create ingredient as regular user (should fail)"""
    print("\n=== Test: Create Ingredient as User (Should Fail) ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/ingredients",
            json={
                "name_vi": "Test Ingredient",
                "name_en": "Test Ingredient",
                "calories": 100.0,
                "protein_g": 5.0,
                "carbs_g": 10.0,
                "fat_g": 2.0,
                "common_unit": "g"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403, f"Should be forbidden, got: {response.status_code}"
        print("✓ Regular user cannot create ingredient (403 Forbidden)")

async def test_create_ingredient_as_admin():
    """Test: Create ingredient as admin"""
    print("\n=== Test: Create Ingredient as Admin ===")
    token = await get_token(ADMIN_CREDS["email"], ADMIN_CREDS["password"])
    async with httpx.AsyncClient() as client:
        # Use a timestamp-based name to avoid duplicates
        import time
        timestamp = int(time.time() * 1000) % 10000
        
        new_ingredient = {
            "name_vi": f"Ớt chuông test {timestamp}",
            "name_en": f"Bell Pepper Test {timestamp}",
            "description_vi": "Ớt ngọt nhiều màu sắc",
            "description_en": "Sweet colorful peppers",
            "calories": 31.0,
            "protein_g": 1.0,
            "carbs_g": 6.0,
            "fat_g": 0.3,
            "fiber_g": 2.1,
            "common_unit": "g"
        }
        
        response = await client.post(
            f"{BASE_URL}/ingredients",
            json=new_ingredient,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code in [200, 201], f"Failed: {response.text}"
        ingredient = response.json()
        print(f"✓ Created ingredient: {ingredient['name_vi']} ({ingredient['name_en']})")
        print(f"  - ID: {ingredient['id']}")
        print(f"  - Slug: {ingredient['slug']}")
        return ingredient['id']

async def test_update_ingredient(ingredient_id: str):
    """Test: Update ingredient"""
    print("\n=== Test: Update Ingredient ===")
    token = await get_token(ADMIN_CREDS["email"], ADMIN_CREDS["password"])
    async with httpx.AsyncClient() as client:
        update_data = {
            "description_vi": "Ớt ngọt giàu vitamin C",
            "description_en": "Sweet peppers rich in vitamin C",
            "calories": 32.0  # Updated calorie count
        }
        
        response = await client.put(
            f"{BASE_URL}/ingredients/{ingredient_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        ingredient = response.json()
        print(f"✓ Updated ingredient: {ingredient['name_vi']}")
        print(f"  - New calories: {ingredient['calories']}")
        print(f"  - New description: {ingredient['description_en']}")

async def test_update_duplicate_slug():
    """Test: Update ingredient with duplicate slug (should fail)"""
    print("\n=== Test: Update with Duplicate Slug (Should Fail) ===")
    token = await get_token(ADMIN_CREDS["email"], ADMIN_CREDS["password"])
    
    async with httpx.AsyncClient() as client:
        # Get two ingredients
        response = await client.get(f"{BASE_URL}/ingredients?page_size=2")
        ingredients = response.json()['items']
        
        if len(ingredients) >= 2:
            # Try to update second ingredient with first ingredient's name (will create same slug)
            response = await client.put(
                f"{BASE_URL}/ingredients/{ingredients[1]['id']}",
                json={"name_vi": ingredients[0]['name_vi'], "name_en": ingredients[0]['name_en']},
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 400, f"Should be bad request, got: {response.status_code}"
            print("✓ Duplicate slug prevented (400 Bad Request)")
        else:
            print("⊘ Skipped (need at least 2 ingredients)")

async def test_delete_ingredient(ingredient_id: str):
    """Test: Delete ingredient"""
    print("\n=== Test: Delete Ingredient ===")
    token = await get_token(ADMIN_CREDS["email"], ADMIN_CREDS["password"])
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}/ingredients/{ingredient_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        print(f"✓ Deleted ingredient: {ingredient_id}")
        
        # Verify deletion
        response = await client.get(f"{BASE_URL}/ingredients/{ingredient_id}")
        assert response.status_code == 404, "Ingredient should not exist"
        print("✓ Ingredient no longer exists (404)")

async def test_get_nonexistent_ingredient():
    """Test: Get non-existent ingredient"""
    print("\n=== Test: Get Non-existent Ingredient ===")
    async with httpx.AsyncClient() as client:
        # Use a valid UUID format that doesn't exist
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"{BASE_URL}/ingredients/{fake_uuid}")
        assert response.status_code == 404, f"Should be 404, got: {response.status_code}"
        print("✓ Non-existent ingredient returns 404")

async def test_unauthenticated_create():
    """Test: Create ingredient without authentication"""
    print("\n=== Test: Create Without Authentication (Should Fail) ===")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/ingredients",
            json={
                "name_vi": "Test",
                "name_en": "Test",
                "calories": 100.0,
                "protein_g": 5.0,
                "carbs_g": 10.0,
                "fat_g": 2.0,
                "common_unit": "g"
            }
        )
        assert response.status_code == 401, f"Should be unauthorized, got: {response.status_code}"
        print("✓ Unauthenticated request rejected (401 Unauthorized)")

async def main():
    """Run all ingredient tests"""
    print("=" * 60)
    print("INGREDIENT MANAGEMENT API TESTS")
    print("=" * 60)
    
    try:
        # Public endpoints (no auth needed)
        ingredient_id = await test_list_ingredients()
        await test_search_ingredients()
        await test_pagination()
        
        if ingredient_id:
            await test_get_ingredient_detail(ingredient_id)
        
        await test_get_nonexistent_ingredient()
        
        # Auth/permission tests
        await test_unauthenticated_create()
        await test_create_ingredient_as_user()
        
        # Admin operations
        new_ingredient_id = await test_create_ingredient_as_admin()
        await test_update_ingredient(new_ingredient_id)
        await test_update_duplicate_slug()
        await test_delete_ingredient(new_ingredient_id)
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
