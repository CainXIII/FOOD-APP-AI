"""Initial PostgreSQL schema without pgvector

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-12-21 10:00:00.000000

Description:
- Creates all tables for the Food App backend
- Uses standard PostgreSQL types only (NO pgvector extension)
- Embedding metadata tables use qdrant_point_id for Qdrant references
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types (IF NOT EXISTS)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE user_role AS ENUM ('user', 'premium', 'chef', 'moderator', 'admin');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        DO $$ BEGIN
            CREATE TYPE ai_personality AS ENUM ('friendly', 'professional', 'humorous', 'nutritionist', 'efficient');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        DO $$ BEGIN
            CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        DO $$ BEGIN
            CREATE TYPE cooking_session_status AS ENUM ('active', 'paused', 'completed', 'cancelled');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        DO $$ BEGIN
            CREATE TYPE timer_status AS ENUM ('active', 'paused', 'completed', 'cancelled');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('email_verified', sa.Boolean(), default=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('username', sa.String(100), unique=True, index=True),
        sa.Column('avatar_url', sa.Text()),
        sa.Column('bio', sa.Text()),
        sa.Column('role', postgresql.ENUM('user', 'premium', 'chef', 'moderator', 'admin', name='user_role'), default='user', nullable=False),
        sa.Column('dietary_preferences', postgresql.JSON),
        sa.Column('allergies', postgresql.JSON),
        sa.Column('default_servings', sa.Integer(), default=2),
        sa.Column('preferred_language', sa.String(10), default='vi'),
        sa.Column('ai_personality', postgresql.ENUM('friendly', 'professional', 'humorous', 'nutritionist', 'efficient', name='ai_personality'), default='friendly'),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified_chef', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True)),
    )

    # OAuth accounts
    op.create_table(
        'oauth_accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('provider_user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Refresh tokens
    op.create_table(
        'refresh_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('token', sa.String(255), unique=True, nullable=False),
        sa.Column('device_id', sa.String(255)),
        sa.Column('device_name', sa.String(255)),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('user_agent', sa.Text()),
        sa.Column('is_revoked', sa.Boolean(), default=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True)),
        sa.Column('last_activity', sa.String(255)),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Categories
    op.create_table(
        'categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name_vi', sa.String(100), nullable=False),
        sa.Column('name_en', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('description_vi', sa.Text()),
        sa.Column('description_en', sa.Text()),
        sa.Column('icon_url', sa.Text()),
        sa.Column('image_url', sa.Text()),
        sa.Column('color_hex', sa.String(7)),
        sa.Column('order_index', sa.Integer(), default=0),
        sa.Column('is_active', sa.Boolean(), default=True, index=True),
        sa.Column('recipes_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Ingredients
    op.create_table(
        'ingredients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name_vi', sa.String(255), nullable=False, index=True),
        sa.Column('name_en', sa.String(255), nullable=False, index=True),
        sa.Column('slug', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('description_vi', sa.Text()),
        sa.Column('description_en', sa.Text()),
        sa.Column('category', sa.String(100), index=True),
        sa.Column('image_url', sa.Text()),
        sa.Column('is_common', sa.Boolean(), default=False, index=True),
        sa.Column('usage_count', sa.Integer(), default=0),
        sa.Column('allergen_tags', postgresql.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Recipes
    op.create_table(
        'recipes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('categories.id', ondelete='SET NULL'), index=True),
        sa.Column('title_vi', sa.String(255), nullable=False, index=True),
        sa.Column('title_en', sa.String(255), nullable=False, index=True),
        sa.Column('slug', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('description_vi', sa.Text(), nullable=False),
        sa.Column('description_en', sa.Text(), nullable=False),
        sa.Column('thumbnail_url', sa.Text()),
        sa.Column('image_url', sa.Text()),
        sa.Column('video_url', sa.Text()),
        sa.Column('prep_time_minutes', sa.Integer(), nullable=False),
        sa.Column('cook_time_minutes', sa.Integer(), nullable=False),
        sa.Column('total_time_minutes', sa.Integer(), nullable=False),
        sa.Column('servings', sa.Integer(), nullable=False),
        sa.Column('difficulty', postgresql.ENUM('easy', 'medium', 'hard', name='difficulty_level'), nullable=False, index=True),
        sa.Column('is_vegetarian', sa.Boolean(), default=False, index=True),
        sa.Column('is_vegan', sa.Boolean(), default=False, index=True),
        sa.Column('is_gluten_free', sa.Boolean(), default=False),
        sa.Column('is_dairy_free', sa.Boolean(), default=False),
        sa.Column('allergens', postgresql.JSON),
        sa.Column('tips_vi', sa.Text()),
        sa.Column('tips_en', sa.Text()),
        sa.Column('views_count', sa.Integer(), default=0),
        sa.Column('favorites_count', sa.Integer(), default=0),
        sa.Column('ratings_count', sa.Integer(), default=0),
        sa.Column('average_rating', sa.Float(), default=0.0),
        sa.Column('comments_count', sa.Integer(), default=0),
        sa.Column('is_published', sa.Boolean(), default=True, index=True),
        sa.Column('is_featured', sa.Boolean(), default=False, index=True),
        sa.Column('embedding', sa.Text()),  # Deprecated, kept for backward compatibility
        sa.Column('extra_data', postgresql.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('published_at', sa.DateTime(timezone=True)),
    )

    # Recipe ingredients
    op.create_table(
        'recipe_ingredients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('ingredient_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(50), nullable=False),
        sa.Column('name_vi', sa.String(255)),
        sa.Column('name_en', sa.String(255)),
        sa.Column('notes_vi', sa.Text()),
        sa.Column('notes_en', sa.Text()),
        sa.Column('is_optional', sa.Boolean(), default=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
    )

    # Recipe steps
    op.create_table(
        'recipe_steps',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('step_number', sa.Integer(), nullable=False),
        sa.Column('title_vi', sa.String(255)),
        sa.Column('title_en', sa.String(255)),
        sa.Column('instruction_vi', sa.Text(), nullable=False),
        sa.Column('instruction_en', sa.Text(), nullable=False),
        sa.Column('image_url', sa.Text()),
        sa.Column('video_url', sa.Text()),
        sa.Column('duration_minutes', sa.Integer()),
        sa.Column('tips_vi', sa.Text()),
        sa.Column('tips_en', sa.Text()),
    )

    # Nutrition facts
    op.create_table(
        'nutrition_facts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, unique=True, index=True),
        sa.Column('calories', sa.Float(), nullable=False),
        sa.Column('protein_g', sa.Float(), nullable=False),
        sa.Column('carbs_g', sa.Float(), nullable=False),
        sa.Column('fat_g', sa.Float(), nullable=False),
        sa.Column('fiber_g', sa.Float()),
        sa.Column('sugar_g', sa.Float()),
        sa.Column('sodium_mg', sa.Float()),
        sa.Column('cholesterol_mg', sa.Float()),
        sa.Column('vitamin_a_percent', sa.Float()),
        sa.Column('vitamin_c_percent', sa.Float()),
        sa.Column('calcium_percent', sa.Float()),
        sa.Column('iron_percent', sa.Float()),
    )

    # Recipe embeddings (metadata for Qdrant)
    op.create_table(
        'recipe_embeddings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('content_type', sa.String(50), nullable=False, index=True),
        sa.Column('content_text', sa.Text(), nullable=False),
        sa.Column('qdrant_point_id', sa.String(100), nullable=False, unique=True),  # Reference to Qdrant, NOT vector column
        sa.Column('embedding_model', sa.String(100), default='text-embedding-3-small'),
        sa.Column('is_synced', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Ingredient embeddings (metadata for Qdrant)
    op.create_table(
        'ingredient_embeddings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('ingredient_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False, unique=True, index=True),
        sa.Column('content_text', sa.Text(), nullable=False),
        sa.Column('qdrant_point_id', sa.String(100), nullable=False, unique=True),  # Reference to Qdrant, NOT vector column
        sa.Column('embedding_model', sa.String(100), default='text-embedding-3-small'),
        sa.Column('is_synced', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Favorites
    op.create_table(
        'favorites',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_unique_constraint('uq_user_recipe_favorite', 'favorites', ['user_id', 'recipe_id'])

    # Ratings
    op.create_table(
        'ratings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('review', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_unique_constraint('uq_user_recipe_rating', 'ratings', ['user_id', 'recipe_id'])

    # Comments
    op.create_table(
        'comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('comments.id', ondelete='CASCADE'), index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_edited', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Cooking sessions
    op.create_table(
        'cooking_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recipe_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('servings', sa.Integer(), nullable=False),
        sa.Column('status', postgresql.ENUM('active', 'paused', 'completed', 'cancelled', name='cooking_session_status'), default='active', nullable=False),
        sa.Column('current_step', sa.Integer(), default=0),
        sa.Column('completed_steps', postgresql.JSON),
        sa.Column('notes', sa.Text()),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('paused_at', sa.DateTime(timezone=True)),
        sa.Column('resumed_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('cancelled_at', sa.DateTime(timezone=True)),
    )

    # Cooking timers
    op.create_table(
        'cooking_timers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('cooking_sessions.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('step_number', sa.Integer(), nullable=False),
        sa.Column('label', sa.String(255), nullable=False),
        sa.Column('duration_seconds', sa.Integer(), nullable=False),
        sa.Column('remaining_seconds', sa.Integer(), nullable=False),
        sa.Column('status', postgresql.ENUM('active', 'paused', 'completed', 'cancelled', name='timer_status'), default='active', nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('paused_at', sa.DateTime(timezone=True)),
        sa.Column('resumed_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
    )

    # Chats
    op.create_table(
        'chats',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Chat messages
    op.create_table(
        'chat_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('chat_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
    )

    # Recipe lists
    op.create_table(
        'recipe_lists',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_public', sa.Boolean(), default=False),
        sa.Column('recipe_ids', postgresql.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('recipe_lists')
    op.drop_table('chat_messages')
    op.drop_table('chats')
    op.drop_table('cooking_timers')
    op.drop_table('cooking_sessions')
    op.drop_table('comments')
    op.drop_table('ratings')
    op.drop_table('favorites')
    op.drop_table('ingredient_embeddings')
    op.drop_table('recipe_embeddings')
    op.drop_table('nutrition_facts')
    op.drop_table('recipe_steps')
    op.drop_table('recipe_ingredients')
    op.drop_table('recipes')
    op.drop_table('ingredients')
    op.drop_table('categories')
    op.drop_table('refresh_tokens')
    op.drop_table('oauth_accounts')
    op.drop_table('users')

    # Drop enum types
    op.execute("""
        DROP TYPE IF EXISTS timer_status;
        DROP TYPE IF EXISTS cooking_session_status;
        DROP TYPE IF EXISTS difficulty_level;
        DROP TYPE IF EXISTS ai_personality;
        DROP TYPE IF EXISTS user_role;
    """)
