"""
Generate 50 Vietnamese recipes with full details
Reads categories, ingredients, users from existing JSON files
"""
import json
import uuid
from datetime import datetime, timedelta
import random

# Load existing data
with open("data/categories_full.json", "r", encoding="utf-8") as f:
    categories = json.load(f)["categories"]

with open("data/ingredients_full.json", "r", encoding="utf-8") as f:
    ingredients = json.load(f)["ingredients"]

with open("data/users_full.json", "r", encoding="utf-8") as f:
    users = json.load(f)["users"]

print("Loaded data:")
print(f"  - {len(categories)} categories")
print(f"  - {len(ingredients)} ingredients") 
print(f"  - {len(users)} users")
print()

# Helper functions
BASE_TIME = datetime(2025, 1, 1, 0, 0, 0)

def gen_uuid(prefix):
    base = str(uuid.uuid4())
    return f"{prefix}{base[8:]}"

def gen_timestamp(days_ago=0):
    dt = BASE_TIME - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

# Get category and user IDs
vietnamese_cats = [c for c in categories if "việt" in c["name_vi"].lower() or c["slug"] == "vietnamese"]
all_cat_ids = [c["id"] for c in categories]
user_ids = [u["id"] for u in users]

# Vietnamese recipe templates (50 recipes)
recipe_templates = [
    {"name_vi": "Phở Bò Hà Nội", "name_en": "Hanoi Beef Pho", "time": 720, "difficulty": "hard", "servings": 4},
    {"name_vi": "Phở Gà", "name_en": "Chicken Pho", "time": 180, "difficulty": "medium", "servings": 4},
    {"name_vi": "Bún Bò Huế", "name_en": "Hue Beef Noodle Soup", "time": 240, "difficulty": "hard", "servings": 4},
    {"name_vi": "Bún Chả Hà Nội", "name_en": "Hanoi Grilled Pork with Noodles", "time": 60, "difficulty": "medium", "servings": 2},
    {"name_vi": "Bún Riêu Cua", "name_en": "Crab Noodle Soup", "time": 90, "difficulty": "medium", "servings": 4},
    {"name_vi": "Bánh Mì Thịt", "name_en": "Vietnamese Pork Sandwich", "time": 20, "difficulty": "easy", "servings": 1},
    {"name_vi": "Bánh Xèo", "name_en": "Vietnamese Crepe", "time": 45, "difficulty": "medium", "servings": 4},
    {"name_vi": "Gỏi Cuốn Tôm Thịt", "name_en": "Fresh Spring Rolls", "time": 30, "difficulty": "easy", "servings": 4},
    {"name_vi": "Chả Giò", "name_en": "Fried Spring Rolls", "time": 60, "difficulty": "medium", "servings": 6},
    {"name_vi": "Cơm Tấm Sườn Bì Chả", "name_en": "Broken Rice with Grilled Pork", "time": 90, "difficulty": "medium", "servings": 2},
    {"name_vi": "Cơm Gà Hải Nam", "name_en": "Hainanese Chicken Rice", "time": 60, "difficulty": "medium", "servings": 4},
    {"name_vi": "Cơm Chiên Dương Châu", "name_en": "Yang Chow Fried Rice", "time": 30, "difficulty": "easy", "servings": 4},
    {"name_vi": "Cháo Gà", "name_en": "Chicken Congee", "time": 90, "difficulty": "easy", "servings": 4},
    {"name_vi": "Canh Chua Cá", "name_en": "Sour Fish Soup", "time": 45, "difficulty": "medium", "servings": 4},
    {"name_vi": "Canh Khổ Qua Nhồi Thịt", "name_en": "Stuffed Bitter Melon Soup", "time": 60, "difficulty": "medium", "servings": 4},
    {"name_vi": "Lẩu Thái", "name_en": "Thai Hot Pot", "time": 45, "difficulty": "medium", "servings": 4},
    {"name_vi": "Thịt Kho Tàu", "name_en": "Braised Pork with Eggs", "time": 90, "difficulty": "easy", "servings": 4},
    {"name_vi": "Cá Kho Tộ", "name_en": "Caramelized Fish in Clay Pot", "time": 60, "difficulty": "medium", "servings": 4},
    {"name_vi": "Gà Kho Gừng", "name_en": "Braised Chicken with Ginger", "time": 45, "difficulty": "easy", "servings": 4},
    {"name_vi": "Thịt Heo Quay", "name_en": "Crispy Roast Pork Belly", "time": 180, "difficulty": "hard", "servings": 6},
    {"name_vi": "Gà Nướng Muối Ớt", "name_en": "Salt and Chili Grilled Chicken", "time": 60, "difficulty": "medium", "servings": 4},
    {"name_vi": "Cá Nướng Muối Ớt", "name_en": "Salt and Chili Grilled Fish", "time": 45, "difficulty": "medium", "servings": 4},
    {"name_vi": "Thịt Bò Nướng Sả", "name_en": "Lemongrass Grilled Beef", "time": 30, "difficulty": "easy", "servings": 4},
    {"name_vi": "Nem Nướng", "name_en": "Grilled Pork Sausage", "time": 90, "difficulty": "hard", "servings": 6},
    {"name_vi": "Bò Lúc Lắc", "name_en": "Shaking Beef", "time": 30, "difficulty": "easy", "servings": 2},
    {"name_vi": "Tôm Rang Thịt", "name_en": "Shrimp and Pork Stir-fry", "time": 25, "difficulty": "easy", "servings": 4},
    {"name_vi": "Mực Xào Chua Ngọt", "name_en": "Sweet and Sour Squid", "time": 30, "difficulty": "easy", "servings": 4},
    {"name_vi": "Rau Muống Xào Tỏi", "name_en": "Stir-fried Water Spinach with Garlic", "time": 10, "difficulty": "easy", "servings": 4},
    {"name_vi": "Đậu Phụ Sốt Cà Chua", "name_en": "Tofu in Tomato Sauce", "time": 25, "difficulty": "easy", "servings": 4},
    {"name_vi": "Cà Tím Kho", "name_en": "Braised Eggplant", "time": 30, "difficulty": "easy", "servings": 4},
    {"name_vi": "Bánh Cuốn", "name_en": "Steamed Rice Rolls", "time": 60, "difficulty": "hard", "servings": 4},
    {"name_vi": "Bánh Bao Nhân Thịt", "name_en": "Steamed Pork Buns", "time": 120, "difficulty": "hard", "servings": 8},
    {"name_vi": "Bánh Bột Lọc", "name_en": "Tapioca Dumplings", "time": 90, "difficulty": "medium", "servings": 6},
    {"name_vi": "Xôi Gà", "name_en": "Sticky Rice with Chicken", "time": 60, "difficulty": "medium", "servings": 4},
    {"name_vi": "Xôi Xéo", "name_en": "Sticky Rice with Mung Bean", "time": 45, "difficulty": "medium", "servings": 4},
    {"name_vi": "Chè Đậu Xanh", "name_en": "Mung Bean Sweet Soup", "time": 60, "difficulty": "easy", "servings": 6},
    {"name_vi": "Chè Ba Màu", "name_en": "Three Color Dessert", "time": 90, "difficulty": "medium", "servings": 6},
    {"name_vi": "Bánh Flan", "name_en": "Vietnamese Flan", "time": 90, "difficulty": "easy", "servings": 8},
    {"name_vi": "Sữa Chua Nếp Cẩm", "name_en": "Purple Rice Yogurt", "time": 480, "difficulty": "easy", "servings": 4},
    {"name_vi": "Cà Phê Sữa Đá", "name_en": "Vietnamese Iced Coffee", "time": 10, "difficulty": "easy", "servings": 1},
    {"name_vi": "Trà Sữa Trân Châu", "name_en": "Bubble Milk Tea", "time": 30, "difficulty": "easy", "servings": 2},
    {"name_vi": "Sinh Tố Bơ", "name_en": "Avocado Smoothie", "time": 5, "difficulty": "easy", "servings": 2},
    {"name_vi": "Nước Mía", "name_en": "Sugarcane Juice", "time": 5, "difficulty": "easy", "servings": 2},
    {"name_vi": "Miến Xào Cua", "name_en": "Stir-fried Glass Noodles with Crab", "time": 35, "difficulty": "medium", "servings": 4},
    {"name_vi": "Hủ Tiếu Nam Vang", "name_en": "Phnom Penh Noodle Soup", "time": 120, "difficulty": "medium", "servings": 4},
    {"name_vi": "Mì Quảng", "name_en": "Quang Noodles", "time": 90, "difficulty": "medium", "servings": 4},
    {"name_vi": "Cao Lầu Hội An", "name_en": "Hoi An Cao Lau", "time": 60, "difficulty": "medium", "servings": 4},
    {"name_vi": "Bánh Bèo", "name_en": "Water Fern Cakes", "time": 60, "difficulty": "medium", "servings": 6},
    {"name_vi": "Nem Rán", "name_en": "Hanoi Fried Spring Rolls", "time": 60, "difficulty": "medium", "servings": 6},
    {"name_vi": "Bún Đậu Mắm Tôm", "name_en": "Noodles with Tofu and Shrimp Paste", "time": 45, "difficulty": "easy", "servings": 4},
]

print(f"Generating {len(recipe_templates)} recipes...")
print()

recipes = []
for idx, template in enumerate(recipe_templates, 1):
    recipe_id = gen_uuid("850e8400")
    author_id = random.choice(user_ids)
    category_id = random.choice(all_cat_ids)
    
    # Basic recipe info
    recipe = {
        "id": recipe_id,
        "title_vi": template["name_vi"],
        "title_en": template["name_en"],
        "slug": template["name_en"].lower().replace(" ", "-"),
        "description_vi": f"Công thức {template['name_vi']} truyền thống, hướng dẫn chi tiết từng bước.",
        "description_en": f"Traditional {template['name_en']} recipe with detailed step-by-step instructions.",
        "author_id": author_id,
        "category_id": category_id,
        "image_url": f"https://storage.cooking.app/recipes/{template['name_en'].lower().replace(' ', '-')}.jpg",
        "video_url": f"https://storage.cooking.app/videos/{template['name_en'].lower().replace(' ', '-')}.mp4" if idx % 3 == 0 else None,
        "prep_time_minutes": max(10, template["time"] // 6),
        "cook_time_minutes": template["time"] - max(10, template["time"] // 6),
        "total_time_minutes": template["time"],
        "servings": template["servings"],
        "difficulty": template["difficulty"],
        "cuisine": "Vietnamese",
        "meal_type": ["lunch", "dinner"] if idx % 5 != 0 else ["breakfast"],
        "tags": ["traditional", "vietnamese", "home-cooking"],
        "is_vegetarian": "chay" in template["name_vi"].lower() or "đậu" in template["name_vi"].lower(),
        "is_vegan": False,
        "is_gluten_free": "phở" in template["name_vi"].lower() or "bún" in template["name_vi"].lower(),
        "is_dairy_free": True,
        "allergens": [] if idx % 5 != 0 else ["shellfish"],
        
        # Simplified ingredients (3-5 main ingredients)
        "ingredients_summary": [
            {
                "ingredient_id": ingredients[random.randint(0, min(20, len(ingredients)-1))]["id"],
                "name_vi": ingredients[random.randint(0, min(20, len(ingredients)-1))]["name_vi"],
                "name_en": ingredients[random.randint(0, min(20, len(ingredients)-1))]["name_en"],
                "quantity": random.choice([200, 300, 500]),
                "unit": "g",
                "notes": None
            }
            for _ in range(random.randint(3, 5))
        ],
        
        # Simplified steps (3-5 steps)
        "steps": [
            {
                "step_number": i,
                "instruction_vi": f"Bước {i}: Chuẩn bị và chế biến nguyên liệu.",
                "instruction_en": f"Step {i}: Prepare and process ingredients.",
                "duration_minutes": template["time"] // random.randint(3, 5),
                "timer_required": i == 2,
                "timer_label_vi": "Hầm nước dùng" if i == 2 else None,
                "timer_label_en": "Simmer broth" if i == 2 else None,
                "image_url": f"https://storage.cooking.app/steps/{recipe_id}-{i}.jpg" if i % 2 == 0 else None,
                "warnings": []
            }
            for i in range(1, random.randint(3, 6))
        ],
        
        # Stats
        "rating_average": round(random.uniform(4.0, 5.0), 1),
        "rating_count": random.randint(10, 200),
        "view_count": random.randint(100, 5000),
        "favorite_count": random.randint(10, 500),
        "cooked_count": random.randint(5, 300),
        "share_count": random.randint(0, 100),
        
        # Status
        "is_featured": idx <= 10,
        "is_published": True,
        "created_at": gen_timestamp(days_ago=random.randint(1, 180)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 30)),
        "published_at": gen_timestamp(days_ago=random.randint(1, 180))
    }
    
    recipes.append(recipe)
    if idx % 10 == 0:
        print(f"   Generated {idx}/{len(recipe_templates)} recipes...")

print()
print(f"✅ Generated {len(recipes)} recipes")

# Save
with open("data/recipes_full.json", "w", encoding="utf-8") as f:
    json.dump({"recipes": recipes}, f, ensure_ascii=False, indent=2)

print("✅ Saved recipes_full.json")
print()
print(f"Total data: 30 categories + 155 ingredients + 5 users + 50 recipes = 240 records")
