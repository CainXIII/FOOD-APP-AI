"""
Test vector similarity search with SQLite
"""
import asyncio
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.openai_service import get_openai_service
from app.database import async_session_maker
from app.services.rag import cosine_similarity
from sqlalchemy import select
from app.models.recipe import Recipe
from app.models.embedding import RecipeEmbedding


async def test_recipe_search(query_text: str):
    """Test recipe vector search with SQLite"""
    print(f"\n🔎 Searching: {query_text}")

    # Generate query embedding
    service = get_openai_service()
    query_embedding = await service.create_embedding(query_text)

    # Search in database using cosine similarity
    async with async_session_maker() as session:
        # Get all embeddings
        stmt = select(RecipeEmbedding, Recipe).join(
            Recipe, RecipeEmbedding.recipe_id == Recipe.id
        ).where(Recipe.is_published == True)

        result = await session.execute(stmt)
        rows = result.all()

        # Calculate similarities
        similarities = []
        for row in rows:
            embedding_record, recipe = row
            similarity = cosine_similarity(query_embedding, embedding_record.embedding)

            similarities.append({
                'recipe': recipe,
                'similarity': similarity,
                'embedding': embedding_record
            })

        # Sort by similarity (higher is better for cosine similarity)
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        print(f"\n📊 Top {min(5, len(similarities))} Similar Recipes:")
        print("-" * 80)
        for i, item in enumerate(similarities[:5], 1):
            recipe = item['recipe']
            similarity = item['similarity']
            print(f"{i}. {recipe.title_vi}")
            print(f"   Similarity: {similarity:.4f}")
            print(f"   Content Type: {item['embedding'].content_type}")
        print("-" * 80)


async def test_ingredient_search(query_text: str):
    """Test ingredient vector search"""
    print(f"\n🔎 Searching ingredients: {query_text}")
    
    # Generate query embedding
    service = get_openai_service()
    query_embedding = await service.create_embedding(query_text)
    vector_str = '[' + ','.join(map(str, query_embedding)) + ']'
    
    # Search in database
    async with async_session_maker() as session:
        sql = text("""
            SELECT 
                i.id,
                i.name_vi,
                c.name_vi as category,
                (ie.embedding <=> :query_vector::vector) as distance
            FROM ingredients i
            JOIN ingredient_embeddings ie ON i.id = ie.ingredient_id
            LEFT JOIN categories c ON i.category_id = c.id
            ORDER BY ie.embedding <=> :query_vector::vector
            LIMIT 5
        """)
        
async def test_ingredient_search(query_text: str):
    """Test ingredient vector search with SQLite"""
    print(f"\n🔎 Searching ingredients: {query_text}")

    # Generate query embedding
    service = get_openai_service()
    query_embedding = await service.create_embedding(query_text)

    # For now, skip ingredient search as we focus on recipe search
    print("⚠️  Ingredient search not implemented yet")
    print("-" * 80)


async def main():
    print("=" * 80)
    print("🔍 Vector Similarity Search Test with SQLite")
    print("=" * 80)

    # Test recipe searches
    await test_recipe_search("món ăn truyền thống Việt Nam")
    await test_recipe_search("món gà thơm ngon")
    await test_recipe_search("món ăn chay thanh đạm")
    await test_recipe_search("món tráng miệng ngọt ngào")

    # Test ingredient searches (placeholder)
    await test_ingredient_search("thịt gà")


if __name__ == "__main__":
    asyncio.run(main())
    await test_recipe_search("món ăn nhẹ dễ làm")
    
    # Test ingredient searches
    await test_ingredient_search("gia vị cay nồng")
    await test_ingredient_search("protein từ động vật")
    await test_ingredient_search("rau xanh bổ dưỡng")
    
    print("\n✅ Vector search test completed!")


if __name__ == "__main__":
    asyncio.run(main())
