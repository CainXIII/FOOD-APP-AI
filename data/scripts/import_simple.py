#!/usr/bin/env python3
"""Simple import - users, categories, ingredients, recipes."""
import json
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from uuid import UUID

root_dir = Path(__file__).parent
backend_dir = root_dir / "backend"

# Load .env from backend folder
from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

sys.path.insert(0, str(backend_dir))

from app.database import async_session_maker, engine, Base
from app.models.user import User
from app.models.category import Category, Ingredient
from app.models.recipe import Recipe, RecipeIngredient


async def import_all():
    """Import core data."""
    print("\n*** Simple Import Script ***")
    print("="*70)
    
    # Recreate tables
    print("\n[1/5] Recreating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("-> Tables ready")
    
    async with async_session_maker() as session:
        # 1. Import users
        print("\n[2/5] Importing users...")
        with open(root_dir / 'data' / 'users_full.json', encoding='utf-8') as f:
            users_data = json.load(f)['users']
        
        for user_data in users_data:
            user = User(
                id=UUID(user_data['id']),
                email=user_data['email'],
                username=user_data.get('display_name', user_data['email'].split('@')[0]),
                full_name=user_data['full_name'],
                password_hash=user_data['password_hash'],
                created_at=datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(user)
        await session.commit()
        print(f"-> Imported {len(users_data)} users")
        
        # 2. Import categories
        print("\n[3/5] Importing categories...")
        with open(root_dir / 'data' / 'categories_full.json', encoding='utf-8') as f:
            categories_data = json.load(f)['categories']
        
        for cat_data in categories_data:
            category = Category(
                id=UUID(cat_data['id']),
                name_vi=cat_data['name_vi'],
                name_en=cat_data['name_en'],
                slug=cat_data['slug']
            )
            session.add(category)
        await session.commit()
        print(f"-> Imported {len(categories_data)} categories")
        
        # 3. Import ingredients
        print("\n[4/5] Importing ingredients...")
        with open(root_dir / 'data' / 'ingredients_full.json', encoding='utf-8') as f:
            ingredients_data = json.load(f)['ingredients']
        
        imported = 0
        skipped = 0
        for ing_data in ingredients_data:
            try:
                ingredient = Ingredient(
                    id=UUID(ing_data['id']),
                    name_vi=ing_data['name_vi'],
                    name_en=ing_data['name_en'],
                    slug=ing_data['slug'],
                    calories=ing_data.get('calories'),
                    protein_g=ing_data.get('protein_g'),
                    carbs_g=ing_data.get('carbs_g'),
                    fat_g=ing_data.get('fat_g')
                )
                session.add(ingredient)
                await session.flush()
                imported += 1
            except Exception as e:
                if 'duplicate' in str(e).lower():
                    skipped += 1
                    await session.rollback()
                else:
                    raise
        await session.commit()
        print(f"-> Imported {imported} ingredients (skipped {skipped} duplicates)")
        
        # 4. Import recipes
        print("\n[5/5] Importing recipes...")
        with open(root_dir / 'data' / 'recipes_full.json', encoding='utf-8') as f:
            recipes_data = json.load(f)['recipes']
        
        for recipe_data in recipes_data:
            recipe = Recipe(
                id=UUID(recipe_data['id']),
                user_id=UUID(recipe_data['author_id']),  # author_id -> user_id
                category_id=UUID(recipe_data['category_id']) if recipe_data.get('category_id') else None,
                title_vi=recipe_data['title_vi'],
                title_en=recipe_data['title_en'],
                slug=recipe_data['slug'],
                description_vi=recipe_data['description_vi'],
                description_en=recipe_data['description_en'],
                prep_time_minutes=recipe_data['prep_time_minutes'],
                cook_time_minutes=recipe_data['cook_time_minutes'],
                total_time_minutes=recipe_data['total_time_minutes'],
                servings=recipe_data['servings'],
                difficulty=recipe_data['difficulty'],
                is_published=recipe_data.get('is_published', True),
                created_at=datetime.fromisoformat(recipe_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(recipe)
            
            # Import recipe ingredients
            if 'ingredients' in recipe_data:
                for idx, ing in enumerate(recipe_data['ingredients']):
                    recipe_ing = RecipeIngredient(
                        recipe_id=recipe.id,
                        ingredient_id=UUID(ing['ingredient_id']),
                        quantity=ing['quantity'],
                        unit=ing['unit'],
                        order_index=idx
                    )
                    session.add(recipe_ing)
        
        await session.commit()
        print(f"-> Imported {len(recipes_data)} recipes")
    
    print("\n" + "="*70)
    print("SUCCESS: Import completed!")
    print("\nTest API:")
    print("   curl http://localhost:8000/api/v1/categories/")
    print("   curl http://localhost:8000/api/v1/recipes/")
    print("   curl http://localhost:8000/api/v1/ingredients/\n")


if __name__ == "__main__":
    asyncio.run(import_all())
