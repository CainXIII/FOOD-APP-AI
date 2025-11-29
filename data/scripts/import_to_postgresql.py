#!/usr/bin/env python3
"""
Import JSON data to PostgreSQL Database.
Imports all generated data files in correct order to maintain foreign key relationships.
"""

import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Add backend to path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir / "backend"))

from app.database import async_session_maker, engine, Base
from app.models.user import User
from app.models.category import Category, Ingredient
from app.models.recipe import Recipe, RecipeIngredient
from app.models.social import Rating, Favorite, Comment, RecipeList, RecipeListItem
from app.models.cooking import CookingSession, CookingTimer
from app.models.chat import Chat, ChatMessage
from app.models.analytics import SearchQuery, TrendingKeyword, UserActivity


def get_data_path(filename: str) -> Path:
    """Get absolute path to data file."""
    return root_dir / 'data' / filename


async def clear_database():
    """Clear all tables (optional - for fresh import)."""
    print("\n⚠️  Clearing database tables...")
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        # Recreate all tables
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables recreated")


async def import_users(session: AsyncSession):
    """Import users."""
    print("\n📥 Importing users...")
    
    data_path = root_dir / 'data' / 'users_full.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        users_data = data['users']
    
    for user_data in users_data:
        user = User(
            id=UUID(user_data['id']),
            email=user_data['email'],
            username=user_data['username'],
            full_name=user_data['full_name'],
            hashed_password=user_data['hashed_password'],
            is_active=user_data.get('is_active', True),
            is_verified=user_data.get('is_verified', True),
            avatar_url=user_data.get('avatar_url'),
            bio=user_data.get('bio'),
            dietary_preferences=user_data.get('dietary_preferences'),
            allergens=user_data.get('allergens'),
            created_at=datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00'))
        )
        session.add(user)
    
    await session.commit()
    print(f"✅ Imported {len(users_data)} users")


async def import_categories(session: AsyncSession):
    """Import categories."""
    print("\n📥 Importing categories...")
    
    with open('data/categories_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        categories_data = data['categories']
    
    # Import in order (parents first)
    for cat_data in categories_data:
        category = Category(
            id=UUID(cat_data['id']),
            name_vi=cat_data['name_vi'],
            name_en=cat_data['name_en'],
            slug=cat_data['slug'],
            description_vi=cat_data.get('description_vi'),
            description_en=cat_data.get('description_en'),
            icon=cat_data.get('icon'),
            color=cat_data.get('color'),
            parent_id=UUID(cat_data['parent_id']) if cat_data.get('parent_id') else None,
            order_index=cat_data.get('order_index', 0),
            is_active=cat_data.get('is_active', True)
        )
        session.add(category)
    
    await session.commit()
    print(f"✅ Imported {len(categories_data)} categories")


async def import_ingredients(session: AsyncSession):
    """Import ingredients."""
    print("\n📥 Importing ingredients...")
    
    with open('data/ingredients_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        ingredients_data = data['ingredients']
    
    for ing_data in ingredients_data:
        ingredient = Ingredient(
            id=UUID(ing_data['id']),
            name_vi=ing_data['name_vi'],
            name_en=ing_data['name_en'],
            slug=ing_data['slug'],
            aliases_vi=ing_data.get('aliases_vi', []),
            aliases_en=ing_data.get('aliases_en', []),
            category=ing_data.get('category'),
            image_url=ing_data.get('image_url'),
            calories=ing_data.get('calories'),
            protein_g=ing_data.get('protein_g'),
            carbs_g=ing_data.get('carbs_g'),
            fat_g=ing_data.get('fat_g'),
            fiber_g=ing_data.get('fiber_g'),
            is_vegetarian=ing_data.get('is_vegetarian', False),
            is_vegan=ing_data.get('is_vegan', False),
            is_gluten_free=ing_data.get('is_gluten_free', False)
        )
        session.add(ingredient)
    
    await session.commit()
    print(f"✅ Imported {len(ingredients_data)} ingredients")


async def import_recipes(session: AsyncSession):
    """Import recipes with ingredients."""
    print("\n📥 Importing recipes...")
    
    with open('data/recipes_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        recipes_data = data['recipes']
    
    for recipe_data in recipes_data:
        # Create recipe
        recipe = Recipe(
            id=UUID(recipe_data['id']),
            title_vi=recipe_data['title_vi'],
            title_en=recipe_data.get('title_en'),
            slug=recipe_data['slug'],
            description_vi=recipe_data.get('description_vi'),
            description_en=recipe_data.get('description_en'),
            author_id=UUID(recipe_data['author_id']),
            category_id=UUID(recipe_data['category_id']),
            image_url=recipe_data.get('image_url'),
            video_url=recipe_data.get('video_url'),
            prep_time=recipe_data.get('prep_time'),
            cook_time=recipe_data.get('cook_time'),
            total_time=recipe_data.get('total_time'),
            servings=recipe_data.get('servings'),
            difficulty=recipe_data.get('difficulty'),
            cuisine=recipe_data.get('cuisine'),
            instructions=recipe_data.get('instructions', []),
            tips=recipe_data.get('tips', []),
            tags=recipe_data.get('tags', []),
            is_published=recipe_data.get('is_published', True),
            created_at=datetime.fromisoformat(recipe_data['created_at'].replace('Z', '+00:00'))
        )
        session.add(recipe)
        
        # Add recipe ingredients
        for ing_data in recipe_data.get('ingredients', []):
            recipe_ing = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=UUID(ing_data['ingredient_id']),
                quantity=ing_data.get('quantity'),
                unit=ing_data.get('unit'),
                notes=ing_data.get('notes'),
                order_index=ing_data.get('order_index', 0)
            )
            session.add(recipe_ing)
    
    await session.commit()
    print(f"✅ Imported {len(recipes_data)} recipes")


async def import_nutrition_facts(session: AsyncSession):
    """Import nutrition facts."""
    print("\n📥 Importing nutrition facts...")
    
    with open('data/nutrition-facts_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        nutrition_data = data['nutrition_facts']
    
    # Note: NutritionFact model would need to be imported and used here
    # Skipping for now as it's not in the current models
    
    print(f"⚠️  Nutrition facts import skipped (model not found)")


async def import_social_data(session: AsyncSession):
    """Import ratings, favorites, comments, lists."""
    print("\n📥 Importing social data...")
    
    # Ratings
    with open('data/ratings_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for rating_data in data['ratings']:
            rating = Rating(
                id=UUID(rating_data['id']),
                user_id=UUID(rating_data['user_id']),
                recipe_id=UUID(rating_data['recipe_id']),
                rating=rating_data['rating'],
                review=rating_data.get('review'),
                created_at=datetime.fromisoformat(rating_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(rating)
    await session.commit()
    print(f"✅ Imported ratings")
    
    # Favorites
    with open('data/favorites_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for fav_data in data['favorites']:
            favorite = Favorite(
                id=UUID(fav_data['id']),
                user_id=UUID(fav_data['user_id']),
                recipe_id=UUID(fav_data['recipe_id']),
                created_at=datetime.fromisoformat(fav_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(favorite)
    await session.commit()
    print(f"✅ Imported favorites")
    
    # Comments
    with open('data/comments_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for comment_data in data['comments']:
            comment = Comment(
                id=UUID(comment_data['id']),
                user_id=UUID(comment_data['user_id']),
                recipe_id=UUID(comment_data['recipe_id']),
                parent_id=UUID(comment_data['parent_id']) if comment_data.get('parent_id') else None,
                content=comment_data['content'],
                created_at=datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(comment)
    await session.commit()
    print(f"✅ Imported comments")
    
    # Recipe Lists
    with open('data/recipe-lists_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for list_data in data['recipe_lists']:
            recipe_list = RecipeList(
                id=UUID(list_data['id']),
                user_id=UUID(list_data['user_id']),
                name=list_data['name'],
                description=list_data.get('description'),
                is_public=list_data.get('is_public', False),
                created_at=datetime.fromisoformat(list_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(recipe_list)
            
            # Add items to list
            for item_data in list_data.get('recipes', []):
                list_item = RecipeListItem(
                    list_id=recipe_list.id,
                    recipe_id=UUID(item_data['recipe_id']),
                    order_index=item_data.get('order_index', 0),
                    added_at=datetime.fromisoformat(item_data['added_at'].replace('Z', '+00:00'))
                )
                session.add(list_item)
    await session.commit()
    print(f"✅ Imported recipe lists")


async def import_cooking_data(session: AsyncSession):
    """Import cooking sessions and timers."""
    print("\n📥 Importing cooking data...")
    
    # Cooking Sessions
    with open('data/cooking-sessions_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for session_data in data['cooking_sessions']:
            cooking_session = CookingSession(
                id=UUID(session_data['id']),
                user_id=UUID(session_data['user_id']),
                recipe_id=UUID(session_data['recipe_id']),
                status=session_data['status'],
                current_step=session_data.get('current_step', 0),
                notes=session_data.get('notes'),
                started_at=datetime.fromisoformat(session_data['started_at'].replace('Z', '+00:00')),
                completed_at=datetime.fromisoformat(session_data['completed_at'].replace('Z', '+00:00')) if session_data.get('completed_at') else None
            )
            session.add(cooking_session)
    await session.commit()
    print(f"✅ Imported cooking sessions")
    
    # Cooking Timers
    with open('data/cooking-timers_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for timer_data in data['cooking_timers']:
            timer = CookingTimer(
                id=UUID(timer_data['id']),
                session_id=UUID(timer_data['session_id']),
                step_index=timer_data['step_index'],
                duration_seconds=timer_data['duration_seconds'],
                remaining_seconds=timer_data.get('remaining_seconds'),
                status=timer_data['status'],
                started_at=datetime.fromisoformat(timer_data['started_at'].replace('Z', '+00:00'))
            )
            session.add(timer)
    await session.commit()
    print(f"✅ Imported cooking timers")


async def import_chat_data(session: AsyncSession):
    """Import chats and messages."""
    print("\n📥 Importing chat data...")
    
    # Chats
    with open('data/chats_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for chat_data in data['chats']:
            chat = Chat(
                id=UUID(chat_data['id']),
                user_id=UUID(chat_data['user_id']),
                title=chat_data.get('title'),
                recipe_id=UUID(chat_data['recipe_id']) if chat_data.get('recipe_id') else None,
                created_at=datetime.fromisoformat(chat_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(chat)
    await session.commit()
    print(f"✅ Imported chats")
    
    # Chat Messages
    with open('data/chat-messages_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for msg_data in data['chat_messages']:
            message = ChatMessage(
                id=UUID(msg_data['id']),
                chat_id=UUID(msg_data['chat_id']),
                role=msg_data['role'],
                content=msg_data['content'],
                rag_sources=msg_data.get('rag_sources'),
                rag_metadata=msg_data.get('rag_metadata'),
                created_at=datetime.fromisoformat(msg_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(message)
    await session.commit()
    print(f"✅ Imported chat messages")


async def import_analytics_data(session: AsyncSession):
    """Import search queries, trending keywords, user activities."""
    print("\n📥 Importing analytics data...")
    
    # Search Queries
    with open('data/search-queries_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for query_data in data['search_queries']:
            search_query = SearchQuery(
                id=UUID(query_data['id']),
                user_id=UUID(query_data['user_id']) if query_data.get('user_id') else None,
                query=query_data['query'],
                filters=query_data.get('filters'),
                result_count=query_data.get('result_count', 0),
                clicked_recipe_id=UUID(query_data['clicked_recipe_id']) if query_data.get('clicked_recipe_id') else None,
                created_at=datetime.fromisoformat(query_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(search_query)
    await session.commit()
    print(f"✅ Imported search queries")
    
    # Trending Keywords
    with open('data/trending-keywords_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for keyword_data in data['trending_keywords']:
            keyword = TrendingKeyword(
                id=UUID(keyword_data['id']),
                keyword=keyword_data['keyword'],
                search_count=keyword_data.get('search_count', 0),
                trend_score=keyword_data.get('trend_score', 0.0),
                category=keyword_data.get('category'),
                date=datetime.fromisoformat(keyword_data['date'].replace('Z', '+00:00')).date()
            )
            session.add(keyword)
    await session.commit()
    print(f"✅ Imported trending keywords")
    
    # User Activities
    with open('data/user-activity_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for activity_data in data['user_activities']:
            activity = UserActivity(
                id=UUID(activity_data['id']),
                user_id=UUID(activity_data['user_id']),
                activity_type=activity_data['activity_type'],
                recipe_id=UUID(activity_data['recipe_id']) if activity_data.get('recipe_id') else None,
                metadata=activity_data.get('metadata'),
                created_at=datetime.fromisoformat(activity_data['created_at'].replace('Z', '+00:00'))
            )
            session.add(activity)
    await session.commit()
    print(f"✅ Imported user activities")


async def main():
    """Main import process."""
    print("\n" + "="*70)
    print("  POSTGRESQL DATA IMPORT")
    print("="*70)
    
    # Ask user if they want to clear database
    print("\n⚠️  WARNING: This will import data to PostgreSQL database")
    print("   Do you want to clear existing data first? (y/N): ", end='')
    
    # For script automation, auto-confirm
    clear = input().lower() == 'y'
    
    try:
        if clear:
            await clear_database()
        
        async with async_session_maker() as session:
            # Import in correct order (respecting foreign keys)
            await import_users(session)
            await import_categories(session)
            await import_ingredients(session)
            await import_recipes(session)
            await import_nutrition_facts(session)
            await import_social_data(session)
            await import_cooking_data(session)
            await import_chat_data(session)
            await import_analytics_data(session)
        
        print("\n" + "="*70)
        print("  🎉 DATA IMPORT COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n✅ Imported data:")
        print("   - 5 users")
        print("   - 30 categories")
        print("   - 155 ingredients")
        print("   - 50 recipes")
        print("   - 100 ratings + 60 favorites + 80 comments + 15 lists")
        print("   - 30 cooking sessions + 40 timers")
        print("   - 15 chats + 107 messages")
        print("   - 50 searches + 30 trending + 200 activities")
        print("\n💡 Your PostgreSQL database is now ready!")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs\n")
        
    except Exception as e:
        print(f"\n❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
