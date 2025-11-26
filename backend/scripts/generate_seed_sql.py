"""
Simple database seeding script using SQL generation
Converts JSON data to SQL INSERT statements
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

def load_json(filename):
    """Load JSON data file"""
    filepath = DATA_DIR / filename
    print(f"📄 Loading {filename}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape_sql(value):
    """Escape single quotes for SQL"""
    if value is None:
        return 'NULL'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    if isinstance(value, list):
        if len(value) == 0:
            return "ARRAY[]::text[]"
        escaped_items = ["'" + str(item).replace("'", "''") + "'" for item in value]
        return "ARRAY[" + ','.join(escaped_items) + "]::text[]"
    return str(value)

def generate_categories_sql():
    """Generate SQL for categories"""
    print("\n🗂️  Generating categories SQL...")
    data = load_json('categories.json')
    
    sql_lines = ["-- Insert categories\n"]
    for cat in data['categories']:
        sql = f"""INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('{cat['id']}', {escape_sql(cat['name_vi'])}, {escape_sql(cat['name_en'])}, {escape_sql(cat['slug'])},
        {escape_sql(cat.get('description_vi'))}, {escape_sql(cat.get('description_en'))},
        {escape_sql(cat.get('icon_url'))}, {escape_sql(cat.get('image_url'))},
        {cat.get('sort_order', 0)}, {str(cat.get('is_active', True)).lower()})
ON CONFLICT (id) DO NOTHING;
"""
        sql_lines.append(sql)
    
    print(f"✅ Generated SQL for {len(data['categories'])} categories")
    return '\n'.join(sql_lines)

def generate_users_sql():
    """Generate SQL for users"""
    print("\n👥 Generating users SQL...")
    data = load_json('users.json')
    
    sql_lines = ["-- Insert users\n"]
    for user in data['users']:
        dietary_prefs = escape_sql(user.get('dietary_preferences', []))
        allergies = escape_sql(user.get('allergies', []))
        preferred_cuisines = escape_sql(user.get('preferred_cuisines', []))
        
        sql = f"""INSERT INTO users (id, email, username, full_name, password_hash, avatar_url, role, is_active, is_email_verified, ai_personality, dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
VALUES ('{user['id']}', {escape_sql(user['email'])}, {escape_sql(user.get('username'))},
        {escape_sql(user.get('full_name'))}, {escape_sql(user.get('password_hash'))},
        {escape_sql(user.get('avatar_url'))}, {escape_sql(user.get('role', 'user'))},
        {str(user.get('is_active', True)).lower()}, {str(user.get('is_email_verified', False)).lower()},
        {escape_sql(user.get('ai_personality', 'friendly'))}, {dietary_prefs}, {allergies},
        {escape_sql(user.get('cooking_skill_level'))}, {preferred_cuisines})
ON CONFLICT (id) DO NOTHING;
"""
        sql_lines.append(sql)
    
    print(f"✅ Generated SQL for {len(data['users'])} users")
    return '\n'.join(sql_lines)

def generate_ingredients_sql():
    """Generate SQL for ingredients"""
    print("\n🥕 Generating ingredients SQL...")
    data = load_json('ingredients.json')
    
    sql_lines = ["-- Insert ingredients\n"]
    for ing in data['ingredients']:
        allergen_types = escape_sql(ing.get('allergen_types', []))
        
        sql = f"""INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('{ing['id']}', {escape_sql(ing['name_vi'])}, {escape_sql(ing['name_en'])}, {escape_sql(ing['slug'])},
        {escape_sql(ing.get('description_vi'))}, {escape_sql(ing.get('description_en'))},
        {escape_sql(ing.get('image_url'))}, {escape_sql(ing.get('category_id'))},
        {ing.get('calories_per_100g') if ing.get('calories_per_100g') else 'NULL'},
        {ing.get('protein_g') if ing.get('protein_g') else 'NULL'},
        {ing.get('carbs_g') if ing.get('carbs_g') else 'NULL'},
        {ing.get('fat_g') if ing.get('fat_g') else 'NULL'},
        {ing.get('fiber_g') if ing.get('fiber_g') else 'NULL'},
        {escape_sql(ing.get('common_unit'))}, {allergen_types})
ON CONFLICT (id) DO NOTHING;
"""
        sql_lines.append(sql)
    
    print(f"✅ Generated SQL for {len(data['ingredients'])} ingredients")
    return '\n'.join(sql_lines)

def generate_recipes_sql():
    """Generate SQL for recipes"""
    print("\n🍳 Generating recipes SQL...")
    data = load_json('recipes.json')
    
    sql_lines = ["-- Insert recipes\n"]
    for recipe in data['recipes']:
        allergens = escape_sql(recipe.get('allergens', []))
        
        sql = f"""INSERT INTO recipes (id, title_vi, title_en, slug, description_vi, description_en, author_id, category_id, prep_time_minutes, cook_time_minutes, total_time_minutes, servings, difficulty, thumbnail_url, video_url, is_vegetarian, is_vegan, is_gluten_free, is_dairy_free, allergens, is_published, is_featured)
VALUES ('{recipe['id']}', {escape_sql(recipe['title_vi'])}, {escape_sql(recipe['title_en'])}, {escape_sql(recipe['slug'])},
        {escape_sql(recipe.get('description_vi'))}, {escape_sql(recipe.get('description_en'))},
        {escape_sql(recipe.get('author_id'))}, {escape_sql(recipe.get('category_id'))},
        {recipe.get('prep_time_minutes') if recipe.get('prep_time_minutes') else 'NULL'},
        {recipe.get('cook_time_minutes') if recipe.get('cook_time_minutes') else 'NULL'},
        {recipe.get('total_time_minutes') if recipe.get('total_time_minutes') else 'NULL'},
        {recipe.get('servings', 1)}, {escape_sql(recipe.get('difficulty', 'medium'))},
        {escape_sql(recipe.get('thumbnail_url'))}, {escape_sql(recipe.get('video_url'))},
        {str(recipe.get('is_vegetarian', False)).lower()}, {str(recipe.get('is_vegan', False)).lower()},
        {str(recipe.get('is_gluten_free', False)).lower()}, {str(recipe.get('is_dairy_free', False)).lower()},
        {allergens}, {str(recipe.get('is_published', True)).lower()}, {str(recipe.get('is_featured', False)).lower()})
ON CONFLICT (id) DO NOTHING;
"""
        sql_lines.append(sql)
    
    print(f"✅ Generated SQL for {len(data['recipes'])} recipes")
    return '\n'.join(sql_lines)

def generate_all_sql():
    """Generate complete SQL file"""
    print("=" * 60)
    print("🌱 Generating database seed SQL...")
    print("=" * 60)
    
    try:
        sql_parts = [
            "-- Database Seed Data",
            "-- Generated from JSON files",
            "-- Run with: Get-Content seed_data.sql | docker exec -i cooking_assistant_db psql -U cooking_admin -d cooking_assistant",
            "\n-- Disable triggers for faster bulk insert",
            "SET session_replication_role = 'replica';",
            "\n",
            generate_categories_sql(),
            "\n",
            generate_users_sql(),
            "\n",
            generate_ingredients_sql(),
            "\n",
            generate_recipes_sql(),
            "\n-- Re-enable triggers",
            "SET session_replication_role = 'origin';",
            "\n-- Update sequences",
            "SELECT setval(pg_get_serial_sequence('categories', 'id'), (SELECT MAX(id) FROM categories));",
            "\n-- Verify data",
            "SELECT 'Categories' as table_name, COUNT(*) as count FROM categories",
            "UNION ALL SELECT 'Users', COUNT(*) FROM users",
            "UNION ALL SELECT 'Ingredients', COUNT(*) FROM ingredients",
            "UNION ALL SELECT 'Recipes', COUNT(*) FROM recipes;",
            "\nDO $$",
            "BEGIN",
            "    RAISE NOTICE 'Database seeding completed successfully!';",
            "END $$;"
        ]
        
        output_file = Path(__file__).parent / 'seed_data.sql'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_parts))
        
        print("\n" + "=" * 60)
        print(f"✅ SQL file generated: {output_file}")
        print("=" * 60)
        print("\nTo apply seeds, run:")
        print("Get-Content scripts\\seed_data.sql | docker exec -i cooking_assistant_db psql -U cooking_admin -d cooking_assistant")
        
        return output_file
        
    except Exception as e:
        print(f"\n❌ Error generating SQL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    generate_all_sql()
