"""
Test Authentication APIs
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_register():
    """Test user registration"""
    print("\n" + "="*60)
    print("🔐 Testing User Registration")
    print("="*60)
    
    payload = {
        "email": "test@cooking.app",
        "password": "Test1234",
        "full_name": "Test User",
        "display_name": "testuser"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 201, response.json()


def test_register_duplicate():
    """Test duplicate email registration"""
    print("\n" + "="*60)
    print("🔐 Testing Duplicate Email Registration")
    print("="*60)
    
    payload = {
        "email": "test@cooking.app",
        "password": "Test1234",
        "full_name": "Test User 2"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 400


def test_register_weak_password():
    """Test weak password validation"""
    print("\n" + "="*60)
    print("🔐 Testing Weak Password Validation")
    print("="*60)
    
    payload = {
        "email": "test2@cooking.app",
        "password": "weak",  # Too short, no uppercase, no digit
        "full_name": "Test User 2"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 422


def test_login():
    """Test user login"""
    print("\n" + "="*60)
    print("🔐 Testing User Login")
    print("="*60)
    
    payload = {
        "email": "test@cooking.app",
        "password": "Test1234"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✅ Access Token: {result['access_token'][:50]}...")
        print(f"✅ Refresh Token: {result['refresh_token'][:50]}...")
        return True, result
    
    return False, result


def test_login_wrong_password():
    """Test login with wrong password"""
    print("\n" + "="*60)
    print("🔐 Testing Login with Wrong Password")
    print("="*60)
    
    payload = {
        "email": "test@cooking.app",
        "password": "WrongPassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 401


def test_get_current_user(access_token):
    """Test get current user profile"""
    print("\n" + "="*60)
    print("👤 Testing Get Current User Profile")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_get_current_user_no_token():
    """Test get current user without token"""
    print("\n" + "="*60)
    print("👤 Testing Get Current User Without Token")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/auth/me")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 401


def test_refresh_token(refresh_token):
    """Test token refresh"""
    print("\n" + "="*60)
    print("🔄 Testing Token Refresh")
    print("="*60)
    
    payload = {
        "refresh_token": refresh_token
    }
    
    response = requests.post(f"{BASE_URL}/auth/refresh", json=payload)
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✅ New Access Token: {result['access_token'][:50]}...")
        return True, result
    
    return False, result


def test_change_password(access_token):
    """Test password change"""
    print("\n" + "="*60)
    print("🔑 Testing Password Change")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "old_password": "Test1234",
        "new_password": "NewTest1234"
    }
    
    response = requests.post(f"{BASE_URL}/auth/change-password", json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_login_with_new_password():
    """Test login with new password"""
    print("\n" + "="*60)
    print("🔐 Testing Login with New Password")
    print("="*60)
    
    payload = {
        "email": "test@cooking.app",
        "password": "NewTest1234"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if response.status_code == 200:
        return True, result
    return False, result


def test_logout(access_token):
    """Test logout"""
    print("\n" + "="*60)
    print("🚪 Testing Logout")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def main():
    """Run all authentication tests"""
    print("\n" + "="*60)
    print("🧪 Authentication API Test Suite")
    print("="*60)
    
    results = {}
    
    # Test 1: Register new user
    try:
        success, _ = test_register()
        results["Register"] = success
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Register"] = False
    
    # Test 2: Duplicate email
    try:
        results["Duplicate Email Check"] = test_register_duplicate()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Duplicate Email Check"] = False
    
    # Test 3: Weak password
    try:
        results["Weak Password Validation"] = test_register_weak_password()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Weak Password Validation"] = False
    
    # Test 4: Login
    try:
        success, tokens = test_login()
        results["Login"] = success
        if not success:
            print("\n⚠️  Login failed, skipping remaining tests")
            print_summary(results)
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Login"] = False
        print_summary(results)
        return
    
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    
    # Test 5: Wrong password
    try:
        results["Wrong Password Check"] = test_login_wrong_password()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Wrong Password Check"] = False
    
    # Test 6: Get current user
    try:
        results["Get Current User"] = test_get_current_user(access_token)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Get Current User"] = False
    
    # Test 7: No token
    try:
        results["No Token Check"] = test_get_current_user_no_token()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["No Token Check"] = False
    
    # Test 8: Refresh token
    try:
        success, new_tokens = test_refresh_token(refresh_token)
        results["Refresh Token"] = success
        if success:
            access_token = new_tokens["access_token"]
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Refresh Token"] = False
    
    # Test 9: Change password
    try:
        results["Change Password"] = test_change_password(access_token)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Change Password"] = False
    
    # Test 10: Login with new password
    try:
        success, new_tokens = test_login_with_new_password()
        results["Login with New Password"] = success
        if success:
            access_token = new_tokens["access_token"]
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Login with New Password"] = False
    
    # Test 11: Logout
    try:
        results["Logout"] = test_logout(access_token)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Logout"] = False
    
    # Print summary
    print_summary(results)


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
