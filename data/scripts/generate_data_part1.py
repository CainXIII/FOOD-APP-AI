"""
Generate comprehensive JSON data for Food App AI
Creates 16 JSON files with realistic Vietnamese food data
"""
import json
import uuid
from datetime import datetime, timedelta
import random

# Base timestamp
BASE_TIME = datetime(2025, 1, 1, 0, 0, 0)

def gen_uuid(prefix):
    """Generate UUID with specific prefix pattern"""
    base = str(uuid.uuid4())
    return f"{prefix}{base[8:]}"

def gen_timestamp(days_ago=0, hours_ago=0):
    """Generate ISO timestamp"""
    dt = BASE_TIME - timedelta(days=days_ago, hours=hours_ago)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

# ============================================================================
# 1. CATEGORIES (25 categories)
# ============================================================================
# Create parent categories first
cat_vietnamese_id = gen_uuid("550e8400")

categories = [
    {"id": gen_uuid("550e8400"), "name_vi": "Món chính", "name_en": "Main Dishes", "slug": "main-dishes", "color_hex": "#FF6F00", "parent_id": None, "sort_order": 1},
    {"id": gen_uuid("550e8400"), "name_vi": "Món khai vị", "name_en": "Appetizers", "slug": "appetizers", "color_hex": "#4CAF50", "parent_id": None, "sort_order": 2},
    {"id": gen_uuid("550e8400"), "name_vi": "Món tráng miệng", "name_en": "Desserts", "slug": "desserts", "color_hex": "#E91E63", "parent_id": None, "sort_order": 3},
    {"id": gen_uuid("550e8400"), "name_vi": "Món súp", "name_en": "Soups", "slug": "soups", "color_hex": "#2196F3", "parent_id": None, "sort_order": 4},
    {"id": gen_uuid("550e8400"), "name_vi": "Đồ uống", "name_en": "Beverages", "slug": "beverages", "color_hex": "#9C27B0", "parent_id": None, "sort_order": 5},
    {"id": gen_uuid("550e8400"), "name_vi": "Món ăn sáng", "name_en": "Breakfast", "slug": "breakfast", "color_hex": "#FF9800", "parent_id": None, "sort_order": 6},
    {"id": gen_uuid("550e8400"), "name_vi": "Món salad", "name_en": "Salads", "slug": "salads", "color_hex": "#8BC34A", "parent_id": None, "sort_order": 7},
    {"id": gen_uuid("550e8400"), "name_vi": "Món nướng", "name_en": "Grilled", "slug": "grilled", "color_hex": "#FF5722", "parent_id": None, "sort_order": 8},
    {"id": gen_uuid("550e8400"), "name_vi": "Món chiên", "name_en": "Fried", "slug": "fried", "color_hex": "#FFC107", "parent_id": None, "sort_order": 9},
    {"id": gen_uuid("550e8400"), "name_vi": "Món hấp", "name_en": "Steamed", "slug": "steamed", "color_hex": "#00BCD4", "parent_id": None, "sort_order": 10},
    {"id": gen_uuid("550e8400"), "name_vi": "Món xào", "name_en": "Stir-fried", "slug": "stir-fried", "color_hex": "#F44336", "parent_id": None, "sort_order": 11},
    {"id": gen_uuid("550e8400"), "name_vi": "Món hầm", "name_en": "Braised", "slug": "braised", "color_hex": "#795548", "parent_id": None, "sort_order": 12},
    {"id": gen_uuid("550e8400"), "name_vi": "Bánh mì & Sandwich", "name_en": "Bread & Sandwiches", "slug": "bread-sandwiches", "color_hex": "#FFEB3B", "parent_id": None, "sort_order": 13},
    {"id": gen_uuid("550e8400"), "name_vi": "Món chay", "name_en": "Vegetarian", "slug": "vegetarian", "color_hex": "#66BB6A", "parent_id": None, "sort_order": 14},
    {"id": cat_vietnamese_id, "name_vi": "Món Việt", "name_en": "Vietnamese", "slug": "vietnamese", "color_hex": "#D32F2F", "parent_id": None, "sort_order": 15},
    {"id": gen_uuid("550e8400"), "name_vi": "Bún - Miến", "name_en": "Rice Vermicelli", "slug": "rice-vermicelli", "color_hex": "#FF8A65", "parent_id": cat_vietnamese_id, "sort_order": 16},
    {"id": gen_uuid("550e8400"), "name_vi": "Cơm", "name_en": "Rice Dishes", "slug": "rice-dishes", "color_hex": "#FFCA28", "parent_id": cat_vietnamese_id, "sort_order": 17},
    {"id": gen_uuid("550e8400"), "name_vi": "Bánh", "name_en": "Cakes & Pastries", "slug": "cakes-pastries", "color_hex": "#FFB74D", "parent_id": cat_vietnamese_id, "sort_order": 18},
    {"id": gen_uuid("550e8400"), "name_vi": "Gỏi - Trộn", "name_en": "Salads & Rolls", "slug": "salads-rolls", "color_hex": "#81C784", "parent_id": cat_vietnamese_id, "sort_order": 19},
    {"id": gen_uuid("550e8400"), "name_vi": "Canh", "name_en": "Soups", "slug": "vietnamese-soups", "color_hex": "#64B5F6", "parent_id": cat_vietnamese_id, "sort_order": 20},
    {"id": gen_uuid("550e8400"), "name_vi": "Món Á", "name_en": "Asian Cuisine", "slug": "asian", "color_hex": "#EF5350", "parent_id": None, "sort_order": 21},
    {"id": gen_uuid("550e8400"), "name_vi": "Món Âu", "name_en": "Western Cuisine", "slug": "western", "color_hex": "#AB47BC", "parent_id": None, "sort_order": 22},
    {"id": gen_uuid("550e8400"), "name_vi": "Healthy & Diet", "name_en": "Healthy & Diet", "slug": "healthy-diet", "color_hex": "#66BB6A", "parent_id": None, "sort_order": 23},
    {"id": gen_uuid("550e8400"), "name_vi": "Nhanh & Tiện", "name_en": "Quick & Easy", "slug": "quick-easy", "color_hex": "#FFA726", "parent_id": None, "sort_order": 24},
    {"id": gen_uuid("550e8400"), "name_vi": "Dành cho trẻ em", "name_en": "Kids Friendly", "slug": "kids-friendly", "color_hex": "#FF7043", "parent_id": None, "sort_order": 25},
]

for cat in categories:
    cat.update({
        "description_vi": f"Danh mục {cat['name_vi'].lower()}",
        "description_en": f"{cat['name_en']} category",
        "icon_url": f"https://storage.cooking.app/icons/{cat['slug']}.svg",
        "image_url": f"https://storage.cooking.app/categories/{cat['slug']}.jpg",
        "is_active": True,
        "created_at": gen_timestamp(),
        "updated_at": gen_timestamp()
    })

#============================================================================
# 2. INGREDIENTS (100+ ingredients)
# ============================================================================
ingredients_data = [
    # Proteins (20)
    ("Xương bò", "Beef bones", "meat", 150, 20, 0, 8, 0, False, False, True, True, []),
    ("Thịt bò", "Beef", "meat", 250, 26, 0, 15, 0, False, False, True, True, []),
    ("Thịt gà", "Chicken", "meat", 165, 31, 0, 3.6, 0, False, False, True, True, []),
    ("Thịt heo", "Pork", "meat", 242, 27, 0, 14, 0, False, False, True, True, []),
    ("Thịt vịt", "Duck", "meat", 337, 19, 0, 28, 0, False, False, True, True, []),
    ("Tôm", "Shrimp", "seafood", 99, 24, 0.2, 0.3, 0, False, False, True, True, ["shellfish"]),
    ("Cá hồi", "Salmon", "seafood", 208, 20, 0, 13, 0, False, False, True, True, ["fish"]),
    ("Cá rô phi", "Tilapia", "seafood", 128, 26, 0, 2.7, 0, False, False, True, True, ["fish"]),
    ("Mực", "Squid", "seafood", 92, 15.6, 3.1, 1.4, 0, False, False, True, True, ["shellfish"]),
    ("Nghêu", "Clams", "seafood", 74, 12.8, 2.6, 1, 0, False, False, True, True, ["shellfish"]),
    ("Trứng gà", "Chicken egg", "dairy", 155, 13, 1.1, 11, 0, True, False, True, False, ["egg"]),
    ("Trứng vịt", "Duck egg", "dairy", 185, 13, 1.4, 14, 0, True, False, True, False, ["egg"]),
    ("Đậu phụ", "Tofu", "protein", 76, 8, 1.9, 4.8, 0.3, True, True, True, True, ["soy"]),
    ("Đậu hũ non", "Silken tofu", "protein", 55, 4.8, 2.7, 2.7, 0.2, True, True, True, True, ["soy"]),
    ("Chả cá", "Fish cake", "processed", 113, 12, 7.5, 4.5, 0, False, False, False, True, ["fish"]),
    ("Chả lụa", "Vietnamese pork roll", "processed", 160, 14, 6, 9, 0, False, False, False, True, []),
    ("Thịt xông khói", "Bacon", "meat", 541, 37, 1.4, 42, 0, False, False, True, True, []),
    ("Xúc xích", "Sausage", "processed", 301, 12, 3.5, 27, 0, False, False, False, True, []),
    ("Sườn heo", "Pork ribs", "meat", 277, 27, 0, 18, 0, False, False, True, True, []),
    ("Thăn bò", "Beef tenderloin", "meat", 201, 29, 0, 9, 0, False, False, True, True, []),
    
    # Vegetables (30)
    ("Cà chua", "Tomato", "vegetable", 18, 0.9, 3.9, 0.2, 1.2, True, True, True, True, []),
    ("Hành tây", "Onion", "vegetable", 40, 1.1, 9.3, 0.1, 1.7, True, True, True, True, []),
    ("Tỏi", "Garlic", "vegetable", 149, 6.4, 33, 0.5, 2.1, True, True, True, True, []),
    ("Gừng", "Ginger", "spice", 80, 1.8, 18, 0.8, 2, True, True, True, True, []),
    ("Ớt", "Chili pepper", "spice", 40, 1.9, 8.8, 0.4, 1.5, True, True, True, True, []),
    ("Cà rốt", "Carrot", "vegetable", 41, 0.9, 10, 0.2, 2.8, True, True, True, True, []),
    ("Khoai tây", "Potato", "vegetable", 77, 2, 17, 0.1, 2.1, True, True, True, True, []),
    ("Khoai lang", "Sweet potato", "vegetable", 86, 1.6, 20, 0.1, 3, True, True, True, True, []),
    ("Bí đỏ", "Pumpkin", "vegetable", 26, 1, 6.5, 0.1, 0.5, True, True, True, True, []),
    ("Bí ngòi", "Zucchini", "vegetable", 17, 1.2, 3.1, 0.3, 1, True, True, True, True, []),
    ("Dưa chuột", "Cucumber", "vegetable", 15, 0.7, 3.6, 0.1, 0.5, True, True, True, True, []),
    ("Cải thảo", "Napa cabbage", "vegetable", 16, 1.2, 3.2, 0.2, 1.2, True, True, True, True, []),
    ("Bắp cải", "Cabbage", "vegetable", 25, 1.3, 5.8, 0.1, 2.5, True, True, True, True, []),
    ("Rau muống", "Water spinach", "vegetable", 19, 2.6, 3.1, 0.2, 2.1, True, True, True, True, []),
    ("Rau ngót", "Sweet leaf", "vegetable", 31, 4.3, 5.1, 0.4, 1.5, True, True, True, True, []),
    ("Rau diếp", "Lettuce", "vegetable", 15, 1.4, 2.9, 0.2, 1.3, True, True, True, True, []),
    ("Giá đỗ", "Bean sprouts", "vegetable", 30, 3.0, 5.9, 0.2, 1.8, True, True, True, True, []),
    ("Hành lá", "Spring onion", "vegetable", 32, 1.8, 7.3, 0.2, 2.6, True, True, True, True, []),
    ("Húng quế", "Basil", "herb", 23, 3.2, 2.7, 0.6, 1.6, True, True, True, True, []),
    ("Ngò rí", "Cilantro", "herb", 23, 2.1, 3.7, 0.5, 2.8, True, True, True, True, []),
    ("Rau thơm", "Vietnamese herbs", "herb", 25, 2.5, 4, 0.5, 2, True, True, True, True, []),
    ("Bông cải xanh", "Broccoli", "vegetable", 34, 2.8, 7, 0.4, 2.6, True, True, True, True, []),
    ("Cà tím", "Eggplant", "vegetable", 25, 1, 6, 0.2, 3, True, True, True, True, []),
    ("Đậu cove", "Snow peas", "vegetable", 42, 2.8, 7.6, 0.2, 2.6, True, True, True, True, []),
    ("Măng", "Bamboo shoots", "vegetable", 27, 2.6, 5.2, 0.3, 2.2, True, True, True, True, []),
    ("Nấm rơm", "Straw mushroom", "vegetable", 26, 2.8, 4, 0.4, 1.6, True, True, True, True, []),
    ("Nấm hương", "Shiitake", "vegetable", 34, 2.2, 7, 0.5, 2.5, True, True, True, True, []),
    ("Hạt sen", "Lotus seeds", "grain", 89, 4.1, 20, 0.5, 0, True, True, True, True, []),
    ("Củ sen", "Lotus root", "vegetable", 74, 2.6, 17, 0.1, 4.9, True, True, True, True, []),
    ("Rau má", "Pennywort", "herb", 20, 1.8, 3.9, 0.1, 0, True, True, True, True, []),
    
    # Grains & Noodles (15)
    ("Gạo tẻ", "White rice", "grain", 130, 2.7, 28, 0.3, 0.4, True, True, True, True, []),
    ("Gạo nếp", "Glutinous rice", "grain", 97, 2, 21, 0.2, 0.9, True, True, False, True, []),
    ("Bánh phở", "Pho noodles", "noodle", 109, 1.8, 24, 0.2, 1, True, True, False, True, []),
    ("Bún", "Rice vermicelli", "noodle", 192, 1.7, 44, 0.1, 0.8, True, True, False, True, []),
    ("Mì trứng", "Egg noodles", "noodle", 138, 4.5, 25, 2.1, 0.9, True, False, False, False, ["egg", "gluten"]),
    ("Miến", "Glass noodles", "noodle", 351, 0.2, 86, 0, 0.5, True, True, True, True, []),
    ("Bánh canh", "Thick noodles", "noodle", 88, 1.5, 20, 0.1, 0.7, True, True, False, True, []),
    ("Bánh tráng", "Rice paper", "wrap", 333, 0.6, 83, 0.3, 1.3, True, True, False, True, []),
    ("Bánh mì", "Baguette", "bread", 265, 9, 49, 3.2, 2.7, True, False, False, True, ["gluten"]),
    ("Bột mì", "Wheat flour", "grain", 364, 10, 76, 1, 2.7, True, False, False, True, ["gluten"]),
    ("Bột năng", "Tapioca starch", "grain", 358, 0.2, 88, 0, 1.1, True, True, True, True, []),
    ("Bột nếp", "Glutinous rice flour", "grain", 366, 6.4, 80, 1.4, 2.4, True, True, False, True, []),
    ("Yến mạch", "Oats", "grain", 389, 17, 66, 7, 11, True, True, True, True, []),
    ("Ngũ cốc", "Cereal", "grain", 379, 8, 84, 2, 7, True, False, False, True, ["gluten"]),
    ("Quinoa", "Quinoa", "grain", 120, 4.4, 21, 1.9, 2.8, True, True, True, True, []),
    
    # Seasonings & Sauces (20)
    ("Muối", "Salt", "seasoning", 0, 0, 0, 0, 0, True, True, True, True, []),
    ("Đường", "Sugar", "seasoning", 387, 0, 100, 0, 0, True, True, True, True, []),
    ("Nước mắm", "Fish sauce", "sauce", 35, 5.6, 3.6, 0.1, 0, False, False, True, True, ["fish"]),
    ("Tương ớt", "Sriracha", "sauce", 93, 1.8, 18, 1.1, 1.8, True, True, True, True, []),
    ("Tương đen", "Soy sauce", "sauce", 53, 5.6, 4.9, 0.1, 0.8, True, True, False, True, ["soy"]),
    ("Dầu ăn", "Cooking oil", "oil", 884, 0, 0, 100, 0, True, True, True, True, []),
    ("Dầu mè", "Sesame oil", "oil", 884, 0, 0, 100, 0, True, True, True, True, []),
    ("Dầu ô liu", "Olive oil", "oil", 884, 0, 0, 100, 0, True, True, True, True, []),
    ("Giấm", "Vinegar", "seasoning", 18, 0, 0.04, 0, 0, True, True, True, True, []),
    ("Nước cốt dừa", "Coconut milk", "dairy", 230, 2.3, 6, 24, 0, True, True, True, True, []),
    ("Sữa tươi", "Milk", "dairy", 61, 3.2, 4.8, 3.3, 0, True, False, True, False, ["dairy"]),
    ("Kem tươi", "Heavy cream", "dairy", 340, 2.1, 3.4, 36, 0, True, False, True, False, ["dairy"]),
    ("Bơ", "Butter", "dairy", 717, 0.9, 0.1, 81, 0, True, False, True, False, ["dairy"]),
    ("Tỏi phi", "Fried garlic", "seasoning", 458, 12, 59, 20, 3.6, True, True, True, True, []),
    ("Hạt nêm", "Seasoning powder", "seasoning", 180, 8, 32, 2, 0, True, False, True, True, []),
    ("Bột ngọt", "MSG", "seasoning", 0, 0, 0, 0, 0, True, True, True, True, []),
    ("Tiêu", "Pepper", "spice", 251, 10, 64, 3.3, 25, True, True, True, True, []),
    ("Nghệ", "Turmeric", "spice", 354, 8, 65, 10, 21, True, True, True, True, []),
    ("Sả", "Lemongrass", "herb", 99, 1.8, 25, 0.5, 0, True, True, True, True, []),
    ("Hạt điều", "Cashew", "nut", 553, 18, 30, 44, 3.3, True, True, True, True, ["tree nut"]),
    
    # Fruits (10)
    ("Chuối", "Banana", "fruit", 89, 1.1, 23, 0.3, 2.6, True, True, True, True, []),
    ("Táo", "Apple", "fruit", 52, 0.3, 14, 0.2, 2.4, True, True, True, True, []),
    ("Cam", "Orange", "fruit", 47, 0.9, 12, 0.1, 2.4, True, True, True, True, []),
    ("Xoài", "Mango", "fruit", 60, 0.8, 15, 0.4, 1.6, True, True, True, True, []),
    ("Dứa", "Pineapple", "fruit", 50, 0.5, 13, 0.1, 1.4, True, True, True, True, []),
    ("Dưa hấu", "Watermelon", "fruit", 30, 0.6, 8, 0.2, 0.4, True, True, True, True, []),
    ("Đu đủ", "Papaya", "fruit", 43, 0.5, 11, 0.3, 1.7, True, True, True, True, []),
    ("Chanh", "Lime", "fruit", 30, 0.7, 11, 0.2, 2.8, True, True, True, True, []),
    ("Me", "Tamarind", "fruit", 239, 2.8, 63, 0.6, 5.1, True, True, True, True, []),
    ("Vải", "Lychee", "fruit", 66, 0.8, 17, 0.4, 1.3, True, True, True, True, []),
    
    # Others (10)
    ("Dừa", "Coconut", "fruit", 354, 3.3, 15, 33, 9, True, True, True, True, []),
    ("Đậu xanh", "Mung bean", "legume", 347, 24, 63, 1.2, 16, True, True, True, True, []),
    ("Đậu đỏ", "Red bean", "legume", 333, 24, 63, 0.5, 12, True, True, True, True, []),
    ("Lạc", "Peanut", "nut", 567, 26, 16, 49, 8.5, True, True, True, True, ["peanut"]),
    ("Mè", "Sesame", "seed", 573, 18, 23, 50, 12, True, True, True, True, []),
    ("Hạt chia", "Chia seeds", "seed", 486, 17, 42, 31, 34, True, True, True, True, []),
    ("Đường phên", "Rock sugar", "sweetener", 387, 0, 100, 0, 0, True, True, True, True, []),
    ("Mật ong", "Honey", "sweetener", 304, 0.3, 82, 0, 0.2, True, True, True, True, []),
    ("Rượu trắng", "White wine", "alcohol", 82, 0.1, 2.6, 0, 0, True, True, True, True, []),
    ("Bia", "Beer", "alcohol", 43, 0.5, 3.6, 0, 0, True, True, True, True, []),
]

ingredients = []
for i, (name_vi, name_en, category, cal, prot, carb, fat, fiber, veg, vegan, gf, df, allergens) in enumerate(ingredients_data, 1):
    ing_id = gen_uuid("650e8400")
    ingredients.append({
        "id": ing_id,
        "name_vi": name_vi,
        "name_en": name_en,
        "slug": name_en.lower().replace(" ", "-"),
        "aliases_vi": [name_vi.lower()],
        "aliases_en": [name_en.lower()],
        "category": category,
        "image_url": f"https://storage.cooking.app/ingredients/{name_en.lower().replace(' ', '-')}.jpg",
        "calories": cal,
        "protein_g": prot,
        "carbs_g": carb,
        "fat_g": fat,
        "fiber_g": fiber,
        "is_vegetarian": veg,
        "is_vegan": vegan,
        "is_gluten_free": gf,
        "is_dairy_free": df,
        "allergens": allergens,
        "created_at": gen_timestamp(),
        "updated_at": gen_timestamp()
    })

print(f"✅ Created {len(categories)} categories")
print(f"✅ Created {len(ingredients)} ingredients")

# Save categories and ingredients
with open("data/categories_full.json", "w", encoding="utf-8") as f:
    json.dump({"categories": categories}, f, ensure_ascii=False, indent=2)

with open("data/ingredients_full.json", "w", encoding="utf-8") as f:
    json.dump({"ingredients": ingredients}, f, ensure_ascii=False, indent=2)

print("\n✅ Saved categories_full.json and ingredients_full.json")
print("\nNext: Run this script again to generate remaining data files")
print("(users, recipes, social features, cooking features, analytics)")
