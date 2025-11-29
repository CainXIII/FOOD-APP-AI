"""
Generate nutrition facts for all 50 recipes
"""
import json
import random

# Load recipes
with open("data/recipes_full.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)["recipes"]

print(f"Generating nutrition facts for {len(recipes)} recipes...")

def gen_uuid(prefix):
    import uuid
    base = str(uuid.uuid4())
    return f"{prefix}{base[8:]}"

nutrition_facts = []

for idx, recipe in enumerate(recipes, 1):
    # Base calories on meal type
    base_calories = 400
    if "phở" in recipe["title_vi"].lower() or "bún" in recipe["title_vi"].lower():
        base_calories = 500
    elif "cơm" in recipe["title_vi"].lower():
        base_calories = 600
    elif "chè" in recipe["title_vi"].lower() or "bánh" in recipe["title_vi"].lower():
        base_calories = 300
    elif "đồ uống" in recipe["title_vi"].lower():
        base_calories = 150
    
    servings = recipe["servings"]
    calories_per_serving = base_calories + random.randint(-50, 100)
    
    # Calculate macros (somewhat realistic ratios)
    protein = random.randint(15, 35)
    carbs = random.randint(40, 80)
    fat = random.randint(8, 25)
    fiber = random.randint(2, 8)
    sugar = random.randint(2, 15)
    
    # Micronutrients
    sodium = random.randint(500, 2000)
    cholesterol = 0 if recipe["is_vegetarian"] else random.randint(30, 150)
    saturated_fat = random.randint(2, 10)
    trans_fat = round(random.uniform(0, 0.5), 1)
    
    # Vitamins (% daily value)
    vitamin_a = random.randint(5, 40)
    vitamin_c = random.randint(5, 60)
    vitamin_d = random.randint(0, 20)
    calcium = random.randint(5, 30)
    iron = random.randint(5, 25)
    
    nutrition = {
        "id": gen_uuid("k50e8400"),
        "recipe_id": recipe["id"],
        "serving_size": f"{random.randint(250, 500)}g",
        "servings_per_recipe": servings,
        "calories": calories_per_serving,
        "calories_from_fat": fat * 9,
        "total_fat_g": fat,
        "saturated_fat_g": saturated_fat,
        "trans_fat_g": trans_fat,
        "cholesterol_mg": cholesterol,
        "sodium_mg": sodium,
        "total_carbohydrates_g": carbs,
        "dietary_fiber_g": fiber,
        "sugars_g": sugar,
        "protein_g": protein,
        "vitamin_a_percent": vitamin_a,
        "vitamin_c_percent": vitamin_c,
        "vitamin_d_percent": vitamin_d,
        "calcium_percent": calcium,
        "iron_percent": iron,
        "created_at": recipe["created_at"],
        "updated_at": recipe["updated_at"]
    }
    
    nutrition_facts.append(nutrition)
    
    if idx % 10 == 0:
        print(f"  ✅ Generated {idx}/{len(recipes)} nutrition facts...")

print(f"\n✅ Created {len(nutrition_facts)} nutrition facts")

# Save
with open("data/nutrition-facts_full.json", "w", encoding="utf-8") as f:
    json.dump({"nutrition_facts": nutrition_facts}, f, ensure_ascii=False, indent=2)

print("✅ Saved nutrition-facts_full.json")
