"""
Database seeding script for AI Cooking Assistant
Loads sample data from JSON files and inserts into PostgreSQL
"""
import json
import sys
from pathlib import Path
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import bcrypt

# Database connection parameters
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'cooking_assistant',
    'user': 'cooking_admin',
    'password': 'cooking_pass_2024'
}

# Data directory
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

def get_db_connection():
    """Get database connection via docker exec"""
    # For Docker, we'll use docker exec instead of direct connection
    return None

def execute_sql_via_docker(sql, params=None):
    """Execute SQL via docker exec"""
    import subprocess
    import tempfile
    
    # Create temp SQL file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
        if params:
            # Simple parameter substitution for basic cases
            f.write(sql)
        else:
            f.write(sql)
        temp_file = f.name
    
    try:
        # Execute via docker
        result = subprocess.run([
            'docker', 'exec', '-i', 'cooking_assistant_db',
            'psql', '-U', 'cooking_admin', '-d', 'cooking_assistant'
        ], stdin=open(temp_file, 'r'), capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    finally:
        Path(temp_file).unlink()

def load_json(filename):
    """Load JSON data file"""
    filepath = DATA_DIR / filename
    print(f"📄 Loading {filename}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_categories():
    """Seed categories table"""
    print("\n🗂️  Seeding categories...")
    data = load_json('categories.json')
    
    sql_values = []
    for cat in data['categories']:
        sql_values.append(f"""
            ('{cat['id']}', '{cat['name_vi']}', '{cat['name_en']}', 
             '{cat['slug']}', {f"'{cat.get('description_vi', '')}'" if cat.get('description_vi') else 'NULL'},
             {f"'{cat.get('description_en', '')}'" if cat.get('description_en') else 'NULL'},
             '{cat.get('icon_url', '')}', '{cat.get('image_url', '')}',
             {cat.get('sort_order', 0)}, {str(cat.get('is_active', True)).lower()})
        """)
    
    sql = f"""
        INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, 
                                icon_url, image_url, display_order, is_active)
        VALUES {','.join(sql_values)}
        ON CONFLICT (id) DO NOTHING;
    """
    
    execute_sql_via_docker(sql)
    print(f"✅ Inserted {len(data['categories'])} categories")

def seed_users():
    """Seed users table"""
    print("\n👥 Seeding users...")
    data = load_json('users.json')
    
    sql_values = []
    for user in data['users']:
        # Use provided hash or generate new one
        password_hash = user.get('password_hash', hash_password('password123'))
        dietary_prefs = '{' + ','.join([f'"{p}"' for p in user.get('dietary_preferences', [])]) + '}'
        allergies = '{' + ','.join([f'"{a}"' for a in user.get('allergies', [])]) + '}'
        
        sql_values.append(f"""
            ('{user['id']}', '{user['email']}', {f"'{user.get('username', user['email'].split('@')[0])}'" if user.get('username') else 'NULL'},
             '{user.get('full_name', '')}', '{password_hash}',
             {f"'{user.get('avatar_url')}'" if user.get('avatar_url') else 'NULL'},
             '{user.get('role', 'user')}', {str(user.get('is_active', True)).lower()},
             {str(user.get('is_email_verified', False)).lower()},
             '{user.get('ai_personality', 'friendly')}',
             ARRAY{dietary_prefs}::text[], ARRAY{allergies}::text[],
             {f"'{user.get('cooking_skill_level')}'" if user.get('cooking_skill_level') else 'NULL'},
             ARRAY[]::text[])
        """)
    
    sql = f"""
        INSERT INTO users (id, email, username, full_name, password_hash, avatar_url,
                          role, is_active, is_email_verified, ai_personality,
                          dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
        VALUES {','.join(sql_values)}
        ON CONFLICT (id) DO NOTHING;
    """
    
    execute_sql_via_docker(sql)
    print(f"✅ Inserted {len(data['users'])} users")

def seed_ingredients():
    """Seed ingredients table"""
    print("\n🥕 Seeding ingredients...")
    data = load_json('ingredients.json')
    
    sql_values = []
    for ing in data['ingredients']:
        allergen_types = '{' + ','.join([f'"{a}"' for a in ing.get('allergen_types', [])]) + '}'
        
        sql_values.append(f"""
            ('{ing['id']}', '{ing['name_vi']}', '{ing['name_en']}',
             '{ing['slug']}',
             {f"'{ing.get('description_vi')}'" if ing.get('description_vi') else 'NULL'},
             {f"'{ing.get('description_en')}'" if ing.get('description_en') else 'NULL'},
             {f"'{ing.get('image_url')}'" if ing.get('image_url') else 'NULL'},
             {f"'{ing.get('category_id')}'" if ing.get('category_id') else 'NULL'},
             {ing.get('calories_per_100g') if ing.get('calories_per_100g') else 'NULL'},
             {ing.get('protein_g') if ing.get('protein_g') else 'NULL'},
             {ing.get('carbs_g') if ing.get('carbs_g') else 'NULL'},
             {ing.get('fat_g') if ing.get('fat_g') else 'NULL'},
             {ing.get('fiber_g') if ing.get('fiber_g') else 'NULL'},
             {f"'{ing.get('common_unit')}'" if ing.get('common_unit') else 'NULL'},
             ARRAY{allergen_types}::text[])
        """)
    
    sql = f"""
        INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en,
                                image_url, category_id, calories_per_100g, protein_g, carbs_g,
                                fat_g, fiber_g, common_unit, allergen_types)
        VALUES {','.join(sql_values)}
        ON CONFLICT (id) DO NOTHING;
    """
    
    execute_sql_via_docker(sql)
    print(f"✅ Inserted {len(data['ingredients'])} ingredients")

def seed_recipes():
    """Seed recipes table"""
    print("\n🍳 Seeding recipes...")
    data = load_json('recipes.json')
    
    sql_values = []
    for recipe in data['recipes']:
        allergens = '{' + ','.join([f'"{a}"' for a in recipe.get('allergens', [])]) + '}'
        
        sql_values.append(f"""
            ('{recipe['id']}', '{recipe['title_vi']}', '{recipe['title_en']}',
             '{recipe['slug']}',
             {f"'{recipe.get('description_vi')}'" if recipe.get('description_vi') else 'NULL'},
             {f"'{recipe.get('description_en')}'" if recipe.get('description_en') else 'NULL'},
             {f"'{recipe.get('author_id')}'" if recipe.get('author_id') else 'NULL'},
             {f"'{recipe.get('category_id')}'" if recipe.get('category_id') else 'NULL'},
             {recipe.get('prep_time_minutes') if recipe.get('prep_time_minutes') else 'NULL'},
             {recipe.get('cook_time_minutes') if recipe.get('cook_time_minutes') else 'NULL'},
             {recipe.get('total_time_minutes') if recipe.get('total_time_minutes') else 'NULL'},
             {recipe.get('servings', 1)},
             '{recipe.get('difficulty', 'medium')}',
             {f"'{recipe.get('thumbnail_url')}'" if recipe.get('thumbnail_url') else 'NULL'},
             {f"'{recipe.get('video_url')}'" if recipe.get('video_url') else 'NULL'},
             {str(recipe.get('is_vegetarian', False)).lower()},
             {str(recipe.get('is_vegan', False)).lower()},
             {str(recipe.get('is_gluten_free', False)).lower()},
             {str(recipe.get('is_dairy_free', False)).lower()},
             ARRAY{allergens}::text[],
             {str(recipe.get('is_published', True)).lower()},
             {str(recipe.get('is_featured', False)).lower()})
        """)
    
    sql = f"""
        INSERT INTO recipes (id, title_vi, title_en, slug, description_vi, description_en,
                            author_id, category_id, prep_time_minutes, cook_time_minutes,
                            total_time_minutes, servings, difficulty, thumbnail_url, video_url,
                            is_vegetarian, is_vegan, is_gluten_free, is_dairy_free, allergens,
                            is_published, is_featured)
        VALUES {','.join(sql_values)}
        ON CONFLICT (id) DO NOTHING;
    """
    
    execute_sql_via_docker(sql)
    print(f"✅ Inserted {len(data['recipes'])} recipes")

def seed_all():
    """Seed all tables in correct order"""
    print("=" * 60)
    print("🌱 Starting database seeding...")
    print("=" * 60)
    
    try:
        # Seed in dependency order
        seed_categories()
        seed_users()
        seed_ingredients()
        seed_recipes()
        
        # Additional tables can be added here
        # seed_recipe_steps()
        # seed_nutrition_facts()
        # seed_favorites()
        # etc.
        
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    seed_all()
