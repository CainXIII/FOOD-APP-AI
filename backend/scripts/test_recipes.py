"""
Test script for Recipe APIs
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
TEST_EMAIL = "recipe_test@cooking.app"
TEST_PASSWORD = "Test1234"


def test_api_root():
    """Test API root"""
    print("\n" + "="*60)
    print("📡 Testing API Root")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def login():
    """Login and get access token"""
    print("\n" + "="*60)
    print("🔐 Logging in...")
    print("="*60)
    
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Login successful")
        return result["access_token"]
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def test_list_recipes(access_token=None):
    """Test list recipes endpoint"""
    print("\n" + "="*60)
    print("📋 Testing List Recipes")
    print("="*60)
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    response = requests.get(f"{BASE_URL}/recipes", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_list_recipes_with_filters(access_token=None):
    """Test list recipes with filters"""
    print("\n" + "="*60)
    print("📋 Testing List Recipes with Filters")
    print("="*60)
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    params = {
        "page": 1,
        "page_size": 10,
        "is_vegetarian": True,
        "sort_by": "average_rating",
        "sort_order": "desc"
    }
    
    response = requests.get(f"{BASE_URL}/recipes", params=params, headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_get_recipe_not_found(access_token=None):
    """Test get non-existent recipe"""
    print("\n" + "="*60)
    print("🔍 Testing Get Recipe (Not Found)")
    print("="*60)
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = requests.get(f"{BASE_URL}/recipes/{fake_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 404


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 Recipe API Test Suite")
    print("="*60)
    
    results = {}
    
    # Test 1: API root
    try:
        results["API Root"] = test_api_root()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["API Root"] = False
    
    # Test 2: Login to get access token
    access_token = None
    try:
        access_token = login()
        results["Login"] = access_token is not None
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Login"] = False
    
    # Test 3: List recipes (public)
    try:
        results["List Recipes (Public)"] = test_list_recipes()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["List Recipes (Public)"] = False
    
    # Test 4: List recipes (authenticated)
    if access_token:
        try:
            results["List Recipes (Authenticated)"] = test_list_recipes(access_token)
        except Exception as e:
            print(f"❌ Error: {e}")
            results["List Recipes (Authenticated)"] = False
    
    # Test 5: List recipes with filters
    if access_token:
        try:
            results["List Recipes with Filters"] = test_list_recipes_with_filters(access_token)
        except Exception as e:
            print(f"❌ Error: {e}")
            results["List Recipes with Filters"] = False
    
    # Test 6: Get non-existent recipe
    try:
        results["Get Recipe (404)"] = test_get_recipe_not_found(access_token)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Get Recipe (404)"] = False
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:35} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
