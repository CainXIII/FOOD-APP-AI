"""
Test OpenAI service with custom base URL
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.openai_service import (
    get_openai_service,
    generate_recipe_embedding,
    chat_with_assistant,
    chat_with_assistant_stream
)
from app.config import get_settings


async def test_config():
    """Test OpenAI configuration"""
    print("=" * 60)
    print("🔧 Testing OpenAI Configuration")
    print("=" * 60)
    
    settings = get_settings()
    print(f"\n📍 Base URL: {settings.OPENAI_BASE_URL}")
    print(f"🤖 Chat Model: {settings.OPENAI_MODEL}")
    print(f"📊 Embedding Model: {settings.OPENAI_EMBEDDING_MODEL}")
    print(f"🌡️  Temperature: {settings.OPENAI_TEMPERATURE}")
    print(f"🔑 API Key: {settings.OPENAI_API_KEY[:20]}..." if len(settings.OPENAI_API_KEY) > 20 else "Not set")


async def test_embedding():
    """Test embedding generation"""
    print("\n" + "=" * 60)
    print("📊 Testing Embedding Generation")
    print("=" * 60)
    
    try:
        test_text = "Phở bò Việt Nam với nước dùng thơm ngon"
        print(f"\n📝 Input: {test_text}")
        
        embedding = await generate_recipe_embedding(test_text)
        
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        print(f"📈 First 5 values: {embedding[:5]}")
        print(f"📉 Last 5 values: {embedding[-5:]}")
        
        return True
    except Exception as e:
        print(f"❌ Embedding test failed: {e}")
        return False


async def test_chat():
    """Test chat completion"""
    print("\n" + "=" * 60)
    print("💬 Testing Chat Completion")
    print("=" * 60)
    
    try:
        user_message = "Cho tôi một công thức nấu phở đơn giản"
        print(f"\n👤 User: {user_message}")
        
        response = await chat_with_assistant(user_message)
        
        print(f"\n🤖 Assistant: {response[:200]}...")
        print(f"\n✅ Response length: {len(response)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False


async def test_chat_stream():
    """Test streaming chat completion"""
    print("\n" + "=" * 60)
    print("🌊 Testing Streaming Chat")
    print("=" * 60)
    
    try:
        user_message = "3 mẹo để làm trứng chiên ngon hơn"
        print(f"\n👤 User: {user_message}")
        print("\n🤖 Assistant (streaming): ", end="", flush=True)
        
        chunks = []
        async for chunk in chat_with_assistant_stream(user_message):
            print(chunk, end="", flush=True)
            chunks.append(chunk)
        
        print(f"\n\n✅ Streamed {len(chunks)} chunks")
        
        return True
    except Exception as e:
        print(f"\n❌ Streaming test failed: {e}")
        return False


async def test_moderation():
    """Test content moderation"""
    print("\n" + "=" * 60)
    print("🛡️  Testing Content Moderation")
    print("=" * 60)
    
    try:
        service = get_openai_service()
        
        # Test safe content
        safe_text = "Công thức làm bánh mì sandwich thơm ngon"
        print(f"\n📝 Testing: {safe_text}")
        
        result = await service.moderate_content(safe_text)
        
        print(f"{'❌' if result['flagged'] else '✅'} Flagged: {result['flagged']}")
        print(f"📋 Categories: {result['categories']}")
        
        return True
    except Exception as e:
        print(f"❌ Moderation test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n🧪 OpenAI Service Test Suite\n")
    
    # Test configuration
    await test_config()
    
    # Check if API key is set
    settings = get_settings()
    if settings.OPENAI_API_KEY == "your-openai-api-key-here":
        print("\n⚠️  WARNING: OpenAI API key not set in .env file")
        print("Please set OPENAI_API_KEY in backend/.env to run API tests")
        return
    
    # Run tests
    results = {
        "Embedding": await test_embedding(),
        "Chat": await test_chat(),
        "Streaming": await test_chat_stream(),
        "Moderation": await test_moderation()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:15} {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n🎯 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    asyncio.run(main())
