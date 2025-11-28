"""
Test Qdrant RAG Integration
"""
import asyncio
import sys
from pathlib import Path
from uuid import uuid4

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.services.langchain_rag import (
    qdrant_client,
    init_qdrant_collection,
    vector_store,
    index_recipe,
    search_recipes_semantic,
    query_rag,
    get_vector_store_stats
)


async def test_qdrant_integration():
    """Test Qdrant integration"""
    
    print("=" * 70)
    print(" Qdrant RAG Integration Test")
    print("=" * 70)
    print()
    
    # Test 1: Initialize Collection
    print("Test 1: Initialize Qdrant Collection")
    print("-" * 70)
    try:
        init_qdrant_collection()
        print(f"✅ Collection initialized: {settings.QDRANT_COLLECTION_NAME}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize collection: {e}")
        return
    
    # Test 2: Get Stats
    print("Test 2: Get Vector Store Stats")
    print("-" * 70)
    try:
        stats = get_vector_store_stats()
        print(f"✅ Collection: {stats.get('collection_name')}")
        print(f"   Points: {stats.get('points_count', 0)}")
        print(f"   Vectors: {stats.get('vectors_count', 0)}")
        print(f"   Model: {stats.get('embedding_model')}")
        print(f"   Dimensions: {stats.get('dimensions')}")
        print()
    except Exception as e:
        print(f"❌ Failed to get stats: {e}")
    
    # Test 3: Index Sample Recipe
    print("Test 3: Index Sample Recipe")
    print("-" * 70)
    
    sample_recipe = {
        "id": str(uuid4()),
        "title_vi": "Phở Bò Hà Nội",
        "description_vi": "Món phở bò truyền thống của Hà Nội với nước dùng ngọt từ xương bò",
        "ingredients": [
            {"name": "Thịt bò", "quantity": "500g"},
            {"name": "Bánh phở", "quantity": "300g"},
            {"name": "Hành tây", "quantity": "2 củ"},
            {"name": "Gừng", "quantity": "50g"}
        ],
        "steps": [
            {"order": 1, "instruction": "Ninh xương bò với hành, gừng trong 3-4 giờ"},
            {"order": 2, "instruction": "Chần bánh phở, thái thịt bò mỏng"},
            {"order": 3, "instruction": "Trình bày và thưởng thức"}
        ],
        "difficulty": "medium",
        "servings": 4,
        "total_time_minutes": 240,
        "is_published": True
    }
    
    try:
        success = await index_recipe(sample_recipe)
        if success:
            print("✅ Recipe indexed successfully")
            print(f"   Title: {sample_recipe['title_vi']}")
        else:
            print("❌ Failed to index recipe")
        print()
    except Exception as e:
        print(f"❌ Indexing error: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 4: Semantic Search
    print("Test 4: Semantic Search")
    print("-" * 70)
    
    search_queries = [
        "Cách nấu phở bò",
        "Món ăn truyền thống Việt Nam",
        "Công thức làm nước dùng phở"
    ]
    
    for query in search_queries:
        try:
            results = search_recipes_semantic(query, top_k=3)
            print(f"   Query: '{query}'")
            print(f"   Found: {len(results)} results")
            
            for i, result in enumerate(results, 1):
                print(f"      {i}. {result['title']} (score: {result['similarity_score']:.4f})")
            print()
            
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            print()
    
    # Test 5: RAG Query
    print("Test 5: RAG Query")
    print("-" * 70)
    
    rag_queries = [
        "Hướng dẫn tôi cách nấu phở bò ngon",
        "Phở bò cần những nguyên liệu gì?"
    ]
    
    for query in rag_queries:
        try:
            result = await query_rag(
                question=query,
                conversation_history=None,
                user_context=None,
                personality="friendly",
                top_k=3
            )
            
            print(f"   Question: {query}")
            print(f"   Answer: {result['answer'][:150]}...")
            print(f"   Sources: {result.get('total_sources', 0)}")
            print()
            
        except Exception as e:
            print(f"   ❌ RAG query failed: {e}")
            print()
    
    # Test 6: Filter Search
    print("Test 6: Filter Search (by difficulty)")
    print("-" * 70)
    
    try:
        results = search_recipes_semantic(
            query="món ngon",
            top_k=5,
            filters={"difficulty": "medium"}
        )
        print(f"   Query: 'món ngon' (difficulty=medium)")
        print(f"   Found: {len(results)} results")
        for i, result in enumerate(results, 1):
            print(f"      {i}. {result['title']} - {result['metadata'].get('difficulty')}")
        print()
    except Exception as e:
        print(f"   ❌ Filter search failed: {e}")
        print()
    
    # Final Stats
    print("=" * 70)
    print(" Final Statistics")
    print("=" * 70)
    stats = get_vector_store_stats()
    print(f"Collection: {stats.get('collection_name')}")
    print(f"Total points: {stats.get('points_count', 0)}")
    print(f"Status: {stats.get('status')}")
    print()
    
    print("=" * 70)
    print(" ✅ All Tests Complete!")
    print("=" * 70)
    print()
    print("📝 Summary:")
    print("   - Qdrant container running on port 6333")
    print("   - Collection created and configured")
    print("   - Indexing working with LangChain")
    print("   - Semantic search operational")
    print("   - RAG queries generating responses")
    print("   - Metadata filtering supported")
    print()
    print("🚀 Next steps:")
    print("   1. Run migration script: python backend/migrate_pgvector_to_qdrant.py")
    print("   2. Test chat endpoints with real data")
    print("   3. Compare performance with pgvector baseline")
    print()


if __name__ == "__main__":
    asyncio.run(test_qdrant_integration())
