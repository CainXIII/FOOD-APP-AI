"""
Test script for Chat APIs
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
TEST_EMAIL = "recipe_test@cooking.app"
TEST_PASSWORD = "Test1234"


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


def test_create_chat(access_token):
    """Test create chat session"""
    print("\n" + "="*60)
    print("💬 Testing Create Chat")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "title": "Test Chat Session"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload, headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()["id"]
    return None


def test_list_chats(access_token):
    """Test list chat sessions"""
    print("\n" + "="*60)
    print("📋 Testing List Chats")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/chat", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_send_message(chat_id, access_token):
    """Test send message"""
    print("\n" + "="*60)
    print("📨 Testing Send Message")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "chat_id": chat_id,
        "content": "How do I make pho?"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/{chat_id}/messages",
        json=payload,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_get_chat(chat_id, access_token):
    """Test get chat with messages"""
    print("\n" + "="*60)
    print("🔍 Testing Get Chat Detail")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/chat/{chat_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Chat ID: {result.get('id')}")
    print(f"Title: {result.get('title')}")
    print(f"Messages Count: {result.get('messages_count')}")
    print(f"Number of Messages: {len(result.get('messages', []))}")
    
    if result.get('messages'):
        print("\nMessages:")
        for msg in result['messages']:
            print(f"  [{msg['role']}]: {msg['content'][:100]}...")
    
    return response.status_code == 200


def test_rag_query(access_token):
    """Test RAG query"""
    print("\n" + "="*60)
    print("🔎 Testing RAG Query")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "query": "What are some vegetarian Vietnamese recipes?",
        "top_k": 5,
        "min_similarity": 0.7
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/rag/query",
        json=payload,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_delete_chat(chat_id, access_token):
    """Test delete chat"""
    print("\n" + "="*60)
    print("🗑️  Testing Delete Chat")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(f"{BASE_URL}/chat/{chat_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 Chat API Test Suite")
    print("="*60)
    
    results = {}
    
    # Login
    access_token = login()
    if not access_token:
        print("\n❌ Login failed, aborting tests")
        return
    
    results["Login"] = True
    
    # Test 1: Create chat
    try:
        chat_id = test_create_chat(access_token)
        results["Create Chat"] = chat_id is not None
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Create Chat"] = False
        chat_id = None
    
    # Test 2: List chats
    try:
        results["List Chats"] = test_list_chats(access_token)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["List Chats"] = False
    
    # Test 3: Send message
    if chat_id:
        try:
            results["Send Message"] = test_send_message(chat_id, access_token)
        except Exception as e:
            print(f"❌ Error: {e}")
            results["Send Message"] = False
    
    # Test 4: Get chat detail
    if chat_id:
        try:
            results["Get Chat Detail"] = test_get_chat(chat_id, access_token)
        except Exception as e:
            print(f"❌ Error: {e}")
            results["Get Chat Detail"] = False
    
    # Test 5: RAG query
    try:
        results["RAG Query"] = test_rag_query(access_token)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["RAG Query"] = False
    
    # Test 6: Delete chat
    if chat_id:
        try:
            results["Delete Chat"] = test_delete_chat(chat_id, access_token)
        except Exception as e:
            print(f"❌ Error: {e}")
            results["Delete Chat"] = False
    
    # Print summary
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
