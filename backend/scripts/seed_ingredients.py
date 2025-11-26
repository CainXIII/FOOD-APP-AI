"""
Seed ingredients data
"""
import asyncio
from uuid import uuid4
from app.database import get_db
from app.models.category import Ingredient
from app.utils.slug import generate_slug

COMMON_INGREDIENTS = [
    {
        "name_vi": "Thịt bò",
        "name_en": "Beef",
        "calories": 250,
        "protein_g": 26,
        "carbs_g": 0,
        "fat_g": 15,
        "common_unit": "g"
    },
    {
        "name_vi": "Thịt heo",
        "name_en": "Pork",
        "calories": 242,
        "protein_g": 27,
        "carbs_g": 0,
        "fat_g": 14,
        "common_unit": "g"
    },
    {
        "name_vi": "Thịt gà",
        "name_en": "Chicken",
        "calories": 165,
        "protein_g": 31,
        "carbs_g": 0,
        "fat_g": 3.6,
        "common_unit": "g"
    },
    {
        "name_vi": "Cá hồi",
        "name_en": "Salmon",
        "calories": 208,
        "protein_g": 20,
        "carbs_g": 0,
        "fat_g": 13,
        "common_unit": "g"
    },
    {
        "name_vi": "Tôm",
        "name_en": "Shrimp",
        "calories": 99,
        "protein_g": 24,
        "carbs_g": 0.2,
        "fat_g": 0.3,
        "common_unit": "g"
    },
    {
        "name_vi": "Trứng gà",
        "name_en": "Chicken Egg",
        "calories": 155,
        "protein_g": 13,
        "carbs_g": 1.1,
        "fat_g": 11,
        "common_unit": "quả"
    },
    {
        "name_vi": "Gạo",
        "name_en": "Rice",
        "calories": 130,
        "protein_g": 2.7,
        "carbs_g": 28,
        "fat_g": 0.3,
        "common_unit": "g"
    },
    {
        "name_vi": "Bún",
        "name_en": "Rice Noodles",
        "calories": 109,
        "protein_g": 1.8,
        "carbs_g": 25,
        "fat_g": 0.2,
        "common_unit": "g"
    },
    {
        "name_vi": "Phở",
        "name_en": "Pho Noodles",
        "calories": 110,
        "protein_g": 1.9,
        "carbs_g": 25,
        "fat_g": 0.3,
        "common_unit": "g"
    },
    {
        "name_vi": "Hành lá",
        "name_en": "Green Onion",
        "calories": 32,
        "protein_g": 1.8,
        "carbs_g": 7.3,
        "fat_g": 0.2,
        "common_unit": "g"
    },
    {
        "name_vi": "Rau mùi",
        "name_en": "Cilantro",
        "calories": 23,
        "protein_g": 2.1,
        "carbs_g": 3.7,
        "fat_g": 0.5,
        "common_unit": "g"
    },
    {
        "name_vi": "Tỏi",
        "name_en": "Garlic",
        "calories": 149,
        "protein_g": 6.4,
        "carbs_g": 33,
        "fat_g": 0.5,
        "common_unit": "g"
    },
    {
        "name_vi": "Hành tây",
        "name_en": "Onion",
        "calories": 40,
        "protein_g": 1.1,
        "carbs_g": 9.3,
        "fat_g": 0.1,
        "common_unit": "g"
    },
    {
        "name_vi": "Cà chua",
        "name_en": "Tomato",
        "calories": 18,
        "protein_g": 0.9,
        "carbs_g": 3.9,
        "fat_g": 0.2,
        "common_unit": "g"
    },
    {
        "name_vi": "Khoai tây",
        "name_en": "Potato",
        "calories": 77,
        "protein_g": 2,
        "carbs_g": 17,
        "fat_g": 0.1,
        "common_unit": "g"
    },
    {
        "name_vi": "Cà rốt",
        "name_en": "Carrot",
        "calories": 41,
        "protein_g": 0.9,
        "carbs_g": 9.6,
        "fat_g": 0.2,
        "common_unit": "g"
    },
    {
        "name_vi": "Dầu ăn",
        "name_en": "Cooking Oil",
        "calories": 884,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 100,
        "common_unit": "ml"
    },
    {
        "name_vi": "Nước mắm",
        "name_en": "Fish Sauce",
        "calories": 35,
        "protein_g": 5.6,
        "carbs_g": 3.6,
        "fat_g": 0.1,
        "common_unit": "ml"
    },
    {
        "name_vi": "Đường",
        "name_en": "Sugar",
        "calories": 387,
        "protein_g": 0,
        "carbs_g": 100,
        "fat_g": 0,
        "common_unit": "g"
    },
    {
        "name_vi": "Muối",
        "name_en": "Salt",
        "calories": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "common_unit": "g"
    }
]

async def seed_ingredients():
    async for db in get_db():
        created_count = 0
        
        for ing_data in COMMON_INGREDIENTS:
            slug = generate_slug(ing_data["name_vi"])
            
            # Check if exists
            from sqlalchemy import select
            result = await db.execute(
                select(Ingredient).where(Ingredient.slug == slug)
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                ingredient = Ingredient(
                    id=uuid4(),
                    name_vi=ing_data["name_vi"],
                    name_en=ing_data["name_en"],
                    slug=slug,
                    calories=ing_data.get("calories"),
                    protein_g=ing_data.get("protein_g"),
                    carbs_g=ing_data.get("carbs_g"),
                    fat_g=ing_data.get("fat_g"),
                    common_unit=ing_data.get("common_unit", "g")
                )
                db.add(ingredient)
                created_count += 1
        
        if created_count > 0:
            await db.commit()
            print(f"✓ Created {created_count} ingredients")
        else:
            print("✓ All ingredients already exist")
        
        break

if __name__ == "__main__":
    asyncio.run(seed_ingredients())
