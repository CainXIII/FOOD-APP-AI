"""
Create a test recipe for favorites testing
"""
import asyncio
from uuid import uuid4
from app.database import get_db
from app.models.recipe import Recipe, DifficultyLevel
from app.models.category import Category
from app.models.user import User
from sqlalchemy import select

async def create_test_recipe():
    async for db in get_db():
        # Get a category
        result = await db.execute(select(Category).limit(1))
        category = result.scalar_one_or_none()
        if not category:
            print("❌ No category found. Run category tests first.")
            break
            
        # Get a user
        result = await db.execute(select(User).where(User.email == "recipe_test@cooking.app"))
        user = result.scalar_one_or_none()
        if not user:
            print("❌ User not found")
            break
        
        # Check if recipe exists
        result = await db.execute(
            select(Recipe).where(Recipe.slug == "pho-bo-test")
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            print(f"✓ Test recipe already exists: {existing.title_vi} (ID: {existing.id})")
        else:
            # Create recipe
            recipe = Recipe(
                id=uuid4(),
                user_id=user.id,
                category_id=category.id,
                title_vi="Phở Bò Test",
                title_en="Beef Pho Test",
                slug="pho-bo-test",
                description_vi="Món phở truyền thống",
                description_en="Traditional pho",
                prep_time_minutes=30,
                cook_time_minutes=60,
                total_time_minutes=90,
                servings=4,
                difficulty=DifficultyLevel.MEDIUM,
                is_published=True,
                is_vegetarian=False,
                is_vegan=False,
                is_gluten_free=False,
                is_dairy_free=False
            )
            db.add(recipe)
            await db.commit()
            await db.refresh(recipe)
            print(f"✓ Test recipe created: {recipe.title_vi} (ID: {recipe.id})")
        
        break

if __name__ == "__main__":
    asyncio.run(create_test_recipe())
