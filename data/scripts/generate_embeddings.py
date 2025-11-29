#!/usr/bin/env python3
"""
Generate Vector Embeddings for Recipes and Ingredients using OpenAI API.
Creates embeddings for RAG-based semantic search.
"""

import json
import os
import time
import httpx
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration from .env
OPENAI_API_KEY = os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_EMBEDDING_BASE_URL", "https://aiportalapi.stu-platform.live/jpe")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", "1536"))

# Initialize OpenAI client with SSL verification disabled for self-signed certificates
http_client = httpx.Client(verify=False)
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    http_client=http_client
)


def generate_embedding(text: str, retry_count: int = 3) -> List[float]:
    """
    Generate embedding vector for given text using OpenAI API.
    
    Args:
        text: Input text to embed
        retry_count: Number of retries on failure
        
    Returns:
        List of floats representing the embedding vector
    """
    for attempt in range(retry_count):
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            if attempt < retry_count - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"   ⚠️  Retry {attempt + 1}/{retry_count} after {wait_time}s... Error: {str(e)[:50]}")
                time.sleep(wait_time)
            else:
                raise Exception(f"Failed to generate embedding after {retry_count} attempts: {str(e)}")


def create_recipe_text(recipe: Dict[str, Any]) -> str:
    """
    Create searchable text from recipe data for embedding.
    Combines title, description, ingredients, and instructions.
    """
    parts = []
    
    # Title (weighted more)
    title = recipe.get("title_vi") or recipe.get("title_en") or recipe.get("title")
    if title:
        parts.append(f"Công thức: {title}")
    
    # Description
    description = recipe.get("description_vi") or recipe.get("description_en") or recipe.get("description")
    if description:
        parts.append(description)
    
    # Ingredients
    if recipe.get("ingredients"):
        ingredients_text = ", ".join([
            f"{ing.get('name', '')} ({ing.get('quantity', '')} {ing.get('unit', '')})"
            for ing in recipe["ingredients"]
        ])
        parts.append(f"Nguyên liệu: {ingredients_text}")
    
    # Instructions (first 3 steps only to keep context manageable)
    if recipe.get("instructions"):
        instructions = recipe["instructions"][:3]
        instructions_text = " ".join([
            f"Bước {i+1}: {step.get('instruction', '')}"
            for i, step in enumerate(instructions)
        ])
        parts.append(instructions_text)
    
    # Tags
    if recipe.get("tags"):
        parts.append(f"Tags: {', '.join(recipe['tags'])}")
    
    return " | ".join(parts)


def create_ingredient_text(ingredient: Dict[str, Any]) -> str:
    """
    Create searchable text from ingredient data for embedding.
    """
    parts = []
    
    # Name
    name_vi = ingredient.get("name_vi")
    name_en = ingredient.get("name_en")
    if name_vi:
        parts.append(f"Nguyên liệu: {name_vi}")
    
    # English name
    if name_en:
        parts.append(name_en)
    
    # Aliases
    if ingredient.get("aliases_vi"):
        parts.append(f"Tên khác: {', '.join(ingredient['aliases_vi'])}")
    
    # Description
    description = ingredient.get("description_vi") or ingredient.get("description_en") or ingredient.get("description")
    if description:
        parts.append(description)
    
    # Category
    if ingredient.get("category"):
        parts.append(f"Loại: {ingredient['category']}")
    
    # Nutrition highlights
    nutrition = []
    if ingredient.get("calories"):
        nutrition.append(f"{ingredient['calories']} kcal")
    if ingredient.get("protein_g"):
        nutrition.append(f"{ingredient['protein_g']}g protein")
    if ingredient.get("carbs_g"):
        nutrition.append(f"{ingredient['carbs_g']}g carbs")
    
    if nutrition:
        parts.append(f"Dinh dưỡng: {', '.join(nutrition)}")
    
    return " | ".join(parts)


def generate_recipe_embeddings():
    """Generate embeddings for all recipes."""
    print("\n" + "="*70)
    print("  GENERATING RECIPE EMBEDDINGS")
    print("="*70 + "\n")
    
    # Load recipes
    with open('data/recipes_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        recipes = data['recipes']
    
    print(f"📚 Loaded {len(recipes)} recipes")
    print(f"🤖 Model: {EMBEDDING_MODEL}")
    print(f"📊 Vector size: {VECTOR_SIZE} dimensions")
    print(f"🌐 API: {OPENAI_BASE_URL}\n")
    
    embeddings = []
    
    for idx, recipe in enumerate(recipes, 1):
        try:
            # Create searchable text
            text = create_recipe_text(recipe)
            
            # Generate embedding
            title = recipe.get("title_vi") or recipe.get("title_en") or "Unknown"
            print(f"[{idx:2d}/{len(recipes)}] Embedding: {title[:50]}...")
            vector = generate_embedding(text)
            
            # Verify vector dimension
            if len(vector) != VECTOR_SIZE:
                raise ValueError(f"Expected {VECTOR_SIZE} dims, got {len(vector)}")
            
            embeddings.append({
                "id": recipe["id"],
                "recipe_id": recipe["id"],
                "title": recipe.get("title_vi") or recipe.get("title_en"),
                "content_type": "recipe_full",
                "embedding": vector,
                "metadata": {
                    "prep_time": recipe.get("prep_time"),
                    "cook_time": recipe.get("cook_time"),
                    "servings": recipe.get("servings"),
                    "difficulty": recipe.get("difficulty"),
                    "cuisine": recipe.get("cuisine"),
                    "category_id": recipe.get("category_id"),
                    "rating": recipe.get("rating"),
                    "rating_count": recipe.get("rating_count")
                }
            })
            
            # Rate limiting (avoid API throttling)
            if idx % 10 == 0:
                time.sleep(0.5)
            
        except Exception as e:
            title = recipe.get("title_vi") or recipe.get("title_en") or "Unknown"
            print(f"   ❌ Error processing {title}: {str(e)}")
            continue
    
    # Save to file
    output = {"embeddings": embeddings}
    with open('data/recipe-embeddings_full.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize('data/recipe-embeddings_full.json') / 1024
    print(f"\n✅ Saved recipe-embeddings_full.json")
    print(f"   {len(embeddings)} embeddings, {file_size:.1f} KB")


def generate_ingredient_embeddings():
    """Generate embeddings for all ingredients."""
    print("\n" + "="*70)
    print("  GENERATING INGREDIENT EMBEDDINGS")
    print("="*70 + "\n")
    
    # Load ingredients
    with open('data/ingredients_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        ingredients = data['ingredients']
    
    print(f"📚 Loaded {len(ingredients)} ingredients")
    print(f"🤖 Model: {EMBEDDING_MODEL}")
    print(f"📊 Vector size: {VECTOR_SIZE} dimensions")
    print(f"🌐 API: {OPENAI_BASE_URL}\n")
    
    embeddings = []
    
    for idx, ingredient in enumerate(ingredients, 1):
        try:
            # Create searchable text
            text = create_ingredient_text(ingredient)
            
            # Generate embedding
            name = ingredient.get("name_vi") or ingredient.get("name_en") or "Unknown"
            print(f"[{idx:3d}/{len(ingredients)}] Embedding: {name[:40]}...")
            vector = generate_embedding(text)
            
            # Verify vector dimension
            if len(vector) != VECTOR_SIZE:
                raise ValueError(f"Expected {VECTOR_SIZE} dims, got {len(vector)}")
            
            embeddings.append({
                "id": ingredient["id"],
                "ingredient_id": ingredient["id"],
                "name": ingredient.get("name_vi") or ingredient.get("name_en"),
                "content_type": "ingredient",
                "embedding": vector,
                "metadata": {
                    "name_en": ingredient.get("name_en"),
                    "category": ingredient.get("category"),
                    "unit": ingredient.get("unit"),
                    "calories": ingredient.get("calories"),
                    "protein": ingredient.get("protein_g"),
                    "is_vegetarian": ingredient.get("is_vegetarian"),
                    "is_vegan": ingredient.get("is_vegan")
                }
            })
            
            # Rate limiting
            if idx % 10 == 0:
                time.sleep(0.5)
            
        except Exception as e:
            name = ingredient.get("name_vi") or ingredient.get("name_en") or "Unknown"
            print(f"   ❌ Error processing {name}: {str(e)}")
            continue
    
    # Save to file
    output = {"embeddings": embeddings}
    with open('data/ingredient-embeddings_full.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize('data/ingredient-embeddings_full.json') / 1024
    print(f"\n✅ Saved ingredient-embeddings_full.json")
    print(f"   {len(embeddings)} embeddings, {file_size:.1f} KB")


def main():
    """Main execution."""
    print("\n" + "="*70)
    print("  VECTOR EMBEDDINGS GENERATOR")
    print("="*70)
    print(f"\n🔑 API Key: {'*' * 20}{OPENAI_API_KEY[-8:] if OPENAI_API_KEY else 'NOT SET'}")
    print(f"🌐 Base URL: {OPENAI_BASE_URL}")
    print(f"🤖 Model: {EMBEDDING_MODEL}")
    print(f"📊 Vector Size: {VECTOR_SIZE} dimensions")
    
    if not OPENAI_API_KEY:
        print("\n❌ Error: OPENAI_API_KEY not set in .env file")
        print("   Please set OPENAI_EMBEDDING_API_KEY or OPENAI_API_KEY")
        return
    
    try:
        # Generate recipe embeddings
        generate_recipe_embeddings()
        
        # Generate ingredient embeddings
        generate_ingredient_embeddings()
        
        print("\n" + "="*70)
        print("  🎉 ALL EMBEDDINGS GENERATED SUCCESSFULLY!")
        print("="*70)
        print("\n📁 Output files:")
        print("   - data/recipe-embeddings_full.json")
        print("   - data/ingredient-embeddings_full.json")
        print("\n💡 Next step: Import embeddings to Qdrant")
        print("   Run: python import_to_qdrant.py\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check:")
        print("  1. OpenAI API key is valid")
        print("  2. API endpoint is accessible")
        print("  3. Data files exist in data/ directory")


if __name__ == "__main__":
    main()
