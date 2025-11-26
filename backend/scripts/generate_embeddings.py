"""
Generate embeddings for all recipes using OpenAI
This enables semantic search functionality with vector similarity

Vector Search Implementation:
- Embeddings stored as JSON arrays in SQLite
- Cosine similarity calculated in Python using NumPy
- No external vector database required
- Suitable for development and small-scale production
"""
import asyncio
import json
import sys
sys.path.insert(0, "d:/Projects/Hackathon/backend")

from sqlalchemy import select
from app.database import async_session_maker
from app.models.recipe import Recipe
from app.models.embedding import RecipeEmbedding
from app.services.rag import embed_recipe


async def generate_embeddings():
    """Generate embeddings for all recipes"""
    async with async_session_maker() as session:
        try:
            # Get all published recipes
            result = await session.execute(
                select(Recipe).where(Recipe.is_published == True)
            )
            recipes = result.scalars().all()
            
            if not recipes:
                print("No recipes found")
                return
            
            print(f"Found {len(recipes)} recipes to process")
            
            success_count = 0
            error_count = 0
            
            for i, recipe in enumerate(recipes, 1):
                try:
                    # Skip if already has embedding (check RecipeEmbedding table)
                    existing_embedding = await session.execute(
                        select(RecipeEmbedding).where(
                            RecipeEmbedding.recipe_id == recipe.id,
                            RecipeEmbedding.content_type == "overview"
                        )
                    )
                    if existing_embedding.scalar_one_or_none():
                        print(f"[{i}/{len(recipes)}] ✓ {recipe.title_vi} (already embedded)")
                        success_count += 1
                        continue

                    # Generate embedding
                    print(f"[{i}/{len(recipes)}] Generating embedding for: {recipe.title_vi}")
                    embedding_vector = await embed_recipe(recipe)

                    # Create RecipeEmbedding record for SQLite
                    recipe_embedding = RecipeEmbedding(
                        recipe_id=recipe.id,
                        content_type="overview",
                        content_text=f"{recipe.title_vi} {recipe.description_vi}",
                        embedding=embedding_vector,  # Stored as JSON in SQLite
                        embedding_model="text-embedding-3-small"
                    )
                    session.add(recipe_embedding)

                    # Also store as JSON string in recipe for backward compatibility
                    recipe.embedding = json.dumps(embedding_vector)

                    # Commit after each recipe to avoid losing progress
                    await session.commit()
                    
                    print(f"[{i}/{len(recipes)}] ✓ {recipe.title_vi}")
                    success_count += 1
                    
                except Exception as e:
                    print(f"[{i}/{len(recipes)}] ✗ Error for {recipe.title_vi}: {e}")
                    error_count += 1
                    await session.rollback()
                    continue
            
            print(f"\n{'='*60}")
            print(f"Embedding Generation Complete")
            print(f"{'='*60}")
            print(f"✓ Success: {success_count}/{len(recipes)}")
            if error_count > 0:
                print(f"✗ Errors: {error_count}/{len(recipes)}")
            
        except Exception as e:
            print(f"✗ Fatal error: {e}")
            raise


async def test_embedding():
    """Test embedding generation with a single recipe"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(Recipe).where(Recipe.is_published == True).limit(1)
        )
        recipe = result.scalar_one_or_none()
        
        if not recipe:
            print("No recipes found")
            return
        
        print(f"Testing embedding generation for: {recipe.title_vi}")
        
        try:
            embedding_vector = await embed_recipe(recipe)
            print(f"✓ Generated embedding with {len(embedding_vector)} dimensions")
            print(f"  First 5 values: {embedding_vector[:5]}")

            # Create RecipeEmbedding record
            recipe_embedding = RecipeEmbedding(
                recipe_id=recipe.id,
                content_type="overview",
                content_text=f"{recipe.title_vi} {recipe.description_vi}",
                embedding=embedding_vector,
                embedding_model="text-embedding-3-small"
            )
            session.add(recipe_embedding)

            # Also store in recipe for backward compatibility
            recipe.embedding = json.dumps(embedding_vector)
            await session.commit()
            print(f"✓ Saved embedding to database")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            raise


if __name__ == "__main__":
    import sys
    
    # If 'test' argument, only test one recipe
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("Running test mode (single recipe)...")
        asyncio.run(test_embedding())
    else:
        print("Generating embeddings for all recipes...")
        asyncio.run(generate_embeddings())
