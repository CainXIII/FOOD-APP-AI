"""
Test Real AI Integration
Tests OpenAI chat completion and RAG context retrieval
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
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


async def test_create_chat():
    """Test: Create new chat session"""
    print("\n=== Test: Create Chat Session ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/chat",
            json={"title": "AI Chat Test"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, f"Failed: {response.text}"
        chat = response.json()
        print(f"✓ Created chat session: {chat['id']}")
        print(f"  - Title: {chat['title']}")
        return chat['id']


async def test_send_message_with_ai(chat_id: str):
    """Test: Send message and get real AI response"""
    print("\n=== Test: Send Message with Real AI ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test 1: General cooking question
        print("\n📝 Test 1: General cooking question")
        response = await client.post(
            f"{BASE_URL}/chat/{chat_id}/messages",
            json={"content": "Làm sao để nấu phở ngon?"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        message = response.json()
        print(f"✓ Received AI response")
        print(f"  User: Làm sao để nấu phở ngon?")
        print(f"  AI: {message['content'][:200]}...")
        print(f"  - Tokens: {message.get('total_tokens', 0)}")
        print(f"  - RAG contexts found: {len(message.get('rag_context', {}).get('contexts', []))}")
        
        # Test 2: Recipe search question
        print("\n📝 Test 2: Recipe search question")
        response = await client.post(
            f"{BASE_URL}/chat/{chat_id}/messages",
            json={"content": "Tìm cho tôi công thức món chay"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        message = response.json()
        print(f"✓ Received AI response")
        print(f"  User: Tìm cho tôi công thức món chay")
        print(f"  AI: {message['content'][:200]}...")
        print(f"  - RAG contexts found: {len(message.get('rag_context', {}).get('contexts', []))}")
        if message.get('rag_context', {}).get('contexts'):
            print(f"  - Found recipes:")
            for ctx in message['rag_context']['contexts'][:3]:
                print(f"    * {ctx['title']}")


async def test_rag_context():
    """Test: RAG context retrieval"""
    print("\n=== Test: RAG Context Retrieval ===")
    
    from app.database import async_session_maker
    from app.services.rag import get_rag_context
    
    async with async_session_maker() as session:
        # Test search for "phở"
        context = await get_rag_context("phở", session, top_k=3)
        
        print(f"✓ RAG search for 'phở'")
        print(f"  - Found {context['total']} contexts")
        
        if context['contexts']:
            for i, ctx in enumerate(context['contexts'], 1):
                print(f"  {i}. {ctx['title']}")
                print(f"     Similarity: {ctx['similarity']}")


async def test_embedding_generation():
    """Test: Generate embedding for a recipe"""
    print("\n=== Test: Embedding Generation ===")
    
    from app.database import async_session_maker
    from app.models.recipe import Recipe
    from app.services.rag import embed_recipe
    from sqlalchemy import select
    
    async with async_session_maker() as session:
        # Get a recipe
        result = await session.execute(
            select(Recipe).where(Recipe.is_published == True).limit(1)
        )
        recipe = result.scalar_one_or_none()
        
        if not recipe:
            print("No recipes found")
            return
        
        print(f"✓ Testing embedding for: {recipe.title_vi}")
        
        # Generate embedding
        embedding = await embed_recipe(recipe)
        
        print(f"  - Dimensions: {len(embedding)}")
        print(f"  - First 5 values: {embedding[:5]}")
        print(f"  - Type: {type(embedding[0])}")


async def test_chat_history():
    """Test: Get chat history"""
    print("\n=== Test: Get Chat History ===")
    token = await get_token(USER_CREDS["email"], USER_CREDS["password"])
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/chat",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        chats = response.json()
        
        print(f"✓ Retrieved {len(chats)} chat sessions")
        if chats:
            chat = chats[0]
            print(f"  Latest chat:")
            print(f"  - ID: {chat['id']}")
            print(f"  - Title: {chat['title']}")
            print(f"  - Messages: {chat['messages_count']}")


async def main():
    """Run all AI integration tests"""
    print("=" * 60)
    print("REAL AI INTEGRATION TESTS")
    print("=" * 60)
    
    try:
        # Test embedding generation
        await test_embedding_generation()
        
        # Test RAG context
        await test_rag_context()
        
        # Test chat flow
        chat_id = await test_create_chat()
        await test_send_message_with_ai(chat_id)
        await test_chat_history()
        
        print("\n" + "=" * 60)
        print("✓ ALL AI INTEGRATION TESTS PASSED!")
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
