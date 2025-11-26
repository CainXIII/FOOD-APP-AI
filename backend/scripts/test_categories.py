"""
Test Categories API
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
admin_email = "admin@cooking.app"
admin_password = "Admin1234"
user_email = "recipe_test@cooking.app"
user_password = "Test1234"

async def test_categories():
    async with httpx.AsyncClient() as client:
        print("\n" + "="*60)
        print("CATEGORY MANAGEMENT API TESTS")
        print("="*60)
        
        # 1. Login as admin
        print("\n1. Login as admin...")
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": admin_email,
                "password": admin_password
            }
        )
        assert response.status_code == 200, f"Admin login failed: {response.text}"
        admin_token = response.json()["access_token"]
        print(f"✓ Admin login successful")
        
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        # 2. Login as regular user
        print("\n2. Login as regular user...")
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": user_email,
                "password": user_password
            }
        )
        assert response.status_code == 200, f"User login failed: {response.text}"
        user_token = response.json()["access_token"]
        print(f"✓ User login successful")
        
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        # 3. Create category as admin
        print("\n3. Create category (admin)...")
        response = await client.post(
            f"{BASE_URL}/categories",
            headers=admin_headers,
            json={
                "name_vi": "Món Việt Nam",
                "name_en": "Vietnamese Cuisine",
                "description_vi": "Các món ăn truyền thống Việt Nam",
                "description_en": "Traditional Vietnamese dishes",
                "display_order": 1
            }
        )
        if response.status_code == 400 and "already exists" in response.text:
            # Category exists, get it from list
            list_resp = await client.get(f"{BASE_URL}/categories")
            categories = list_resp.json()["items"]
            category = next((c for c in categories if c["slug"] == "mon-viet-nam"), None)
            category_id = category["id"]
            print(f"✓ Category already exists: {category['name_vi']} (slug: {category['slug']})")
        else:
            assert response.status_code == 200, f"Category creation failed: {response.text}"
            category = response.json()
            category_id = category["id"]
            print(f"✓ Category created: {category['name_vi']} (slug: {category['slug']})")
        
        # 4. Try create category as regular user (should fail)
        print("\n4. Try create category as regular user (should fail)...")
        response = await client.post(
            f"{BASE_URL}/categories",
            headers=user_headers,
            json={
                "name_vi": "Món Âu",
                "name_en": "Western Cuisine",
                "description_vi": "Các món ăn phương Tây",
                "description_en": "Western dishes"
            }
        )
        assert response.status_code == 403, "Regular user should not create categories"
        print(f"✓ Regular user blocked from creating categories")
        
        # 5. Create more categories
        print("\n5. Create more categories...")
        categories_to_create = [
            {"name_vi": "Món Âu", "name_en": "Western Cuisine", "description_vi": "Các món ăn phương Tây", "description_en": "Western dishes", "display_order": 2},
            {"name_vi": "Món Á", "name_en": "Asian Cuisine", "description_vi": "Các món ăn châu Á", "description_en": "Asian dishes", "display_order": 3},
            {"name_vi": "Tráng miệng", "name_en": "Desserts", "description_vi": "Các món tráng miệng", "description_en": "Dessert dishes", "display_order": 4},
            {"name_vi": "Đồ uống", "name_en": "Beverages", "description_vi": "Nước giải khát, sinh tố", "description_en": "Drinks and smoothies", "display_order": 5},
        ]
        
        created_count = 0
        for cat_data in categories_to_create:
            response = await client.post(
                f"{BASE_URL}/categories",
                headers=admin_headers,
                json=cat_data
            )
            if response.status_code == 200:
                created_count += 1
        print(f"✓ Created {created_count} additional categories")
        
        # 6. List all categories (public, no auth)
        print("\n6. List all categories (public)...")
        response = await client.get(f"{BASE_URL}/categories")
        assert response.status_code == 200, f"List categories failed: {response.text}"
        data = response.json()
        print(f"✓ Found {len(data['items'])} categories (total: {data['total']})")
        for cat in data['items']:
            print(f"  - {cat['name_vi']} / {cat['name_en']} (slug: {cat['slug']})")
        
        # 7. List with pagination
        print("\n7. List with pagination...")
        response = await client.get(f"{BASE_URL}/categories?skip=0&limit=3")
        assert response.status_code == 200, f"Pagination failed: {response.text}"
        data = response.json()
        print(f"✓ Page 1: {len(data['items'])} categories (total: {data['total']})")
        
        # 8. Get category detail
        print("\n8. Get category detail...")
        response = await client.get(f"{BASE_URL}/categories/{category_id}")
        assert response.status_code == 200, f"Get category failed: {response.text}"
        cat = response.json()
        print(f"✓ Category detail: {cat['name_vi']} / {cat['name_en']}")
        print(f"  Description VI: {cat.get('description_vi', 'N/A')}")
        print(f"  Description EN: {cat.get('description_en', 'N/A')}")
        print(f"  Display order: {cat['display_order']}, Active: {cat['is_active']}")
        
        # 9. Update category
        print("\n9. Update category...")
        response = await client.put(
            f"{BASE_URL}/categories/{category_id}",
            headers=admin_headers,
            json={
                "name_vi": "Món Việt Nam",
                "name_en": "Vietnamese Cuisine",
                "description_vi": "Các món ăn truyền thống và đặc sản Việt Nam",
                "description_en": "Traditional and special Vietnamese dishes",
                "is_active": True
            }
        )
        assert response.status_code == 200, f"Category update failed: {response.text}"
        updated = response.json()
        print(f"✓ Category updated: {updated.get('description_vi', 'success')}")
        
        # 10. Try update as regular user (should fail)
        print("\n10. Try update category as regular user (should fail)...")
        response = await client.put(
            f"{BASE_URL}/categories/{category_id}",
            headers=user_headers,
            json={"name_vi": "Hacked", "name_en": "Hacked"}
        )
        assert response.status_code == 403, "Regular user should not update categories"
        print(f"✓ Regular user blocked from updating categories")
        
        # 11. Try duplicate slug (should fail)
        print("\n11. Try create duplicate slug (should fail)...")
        response = await client.post(
            f"{BASE_URL}/categories",
            headers=admin_headers,
            json={
                "name_vi": "Mon Viet Nam",  # Different but will create same slug
                "name_en": "Vietnamese",
                "description_vi": "Duplicate test",
                "description_en": "Duplicate test"
            }
        )
        assert response.status_code == 400, "Duplicate slug should fail"
        print(f"✓ Duplicate slug blocked")
        
        # 12. Deactivate category
        print("\n12. Deactivate category...")
        response = await client.put(
            f"{BASE_URL}/categories/{category_id}",
            headers=admin_headers,
            json={"is_active": False}
        )
        assert response.status_code == 200, f"Deactivate failed: {response.text}"
        print(f"✓ Category deactivated")
        
        # 13. List active only (should not show deactivated)
        print("\n13. List active categories only...")
        response = await client.get(f"{BASE_URL}/categories?is_active=true")
        assert response.status_code == 200, f"List active failed: {response.text}"
        data = response.json()
        deactivated_found = any(c['id'] == category_id for c in data['items'])
        assert not deactivated_found, "Deactivated category should not appear"
        print(f"✓ Deactivated category hidden from active list")
        
        # 14. Re-activate category
        print("\n14. Re-activate category...")
        response = await client.put(
            f"{BASE_URL}/categories/{category_id}",
            headers=admin_headers,
            json={"is_active": True}
        )
        assert response.status_code == 200, f"Re-activate failed: {response.text}"
        print(f"✓ Category re-activated")
        
        # 15. Delete category
        print("\n15. Delete category...")
        response = await client.delete(
            f"{BASE_URL}/categories/{category_id}",
            headers=admin_headers
        )
        assert response.status_code == 200, f"Delete failed: {response.text}"
        print(f"✓ Category deleted")
        
        # 16. Try get deleted category (should fail)
        print("\n16. Try get deleted category (should fail)...")
        response = await client.get(f"{BASE_URL}/categories/{category_id}")
        assert response.status_code == 404, "Deleted category should not be found"
        print(f"✓ Deleted category not found (404)")
        
        # 17. Try delete as regular user (should fail)
        print("\n17. Try delete as regular user (should fail)...")
        response = await client.get(f"{BASE_URL}/categories")
        if response.status_code == 200 and response.json()['items']:
            test_id = response.json()['items'][0]['id']
            response = await client.delete(
                f"{BASE_URL}/categories/{test_id}",
                headers=user_headers
            )
            assert response.status_code == 403, "Regular user should not delete categories"
            print(f"✓ Regular user blocked from deleting categories")
        
        print("\n" + "="*60)
        print("✅ ALL CATEGORY TESTS PASSED!")
        print("="*60)

if __name__ == "__main__":
    asyncio.run(test_categories())
