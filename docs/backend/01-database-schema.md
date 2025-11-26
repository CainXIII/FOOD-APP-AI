# 🗄️ Database Schema Design - PostgreSQL + pgvector

## Overview
Database schema cho AI Cooking Assistant sử dụng PostgreSQL 15+ với pgvector extension để hỗ trợ vector embeddings cho RAG (Retrieval-Augmented Generation). Schema được tối ưu hóa cho performance, scalability, và data integrity.

**Tech Stack:**
- **PostgreSQL 15+**: Main database
- **pgvector**: Vector similarity search for RAG
- **UUID**: Primary keys for distributed systems
- **JSONB**: Flexible metadata storage
- **Full-text search**: PostgreSQL tsvector for Vietnamese text

---

## Entity Relationship Diagram (ERD)

### High-Level Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    Users    │────────>│   Recipes    │<────────│  Categories │
└─────────────┘         └──────────────┘         └─────────────┘
       │                       │                         │
       │                       │                         │
       ├──────────────────────┬┴────────────┐           │
       │                      │              │           │
       v                      v              v           v
┌─────────────┐      ┌──────────────┐  ┌─────────────┐ │
│  Favorites  │      │   Ratings    │  │RecipeSteps  │ │
└─────────────┘      └──────────────┘  └─────────────┘ │
       │                      │              │          │
       │                      │              │          │
       v                      v              v          v
┌─────────────┐      ┌──────────────┐  ┌─────────────┐ │
│Recipe Lists │      │   Comments   │  │Ingredients  │<┘
└─────────────┘      └──────────────┘  └─────────────┘
       │                                       │
       │                                       │
       v                                       v
┌─────────────┐                       ┌─────────────┐
│  Sessions   │                       │  Nutrition  │
│  (Cooking)  │                       │    Facts    │
└─────────────┘                       └─────────────┘
       │
       v
┌─────────────┐
│   Timers    │
└─────────────┘


┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│ AI Messages │<────────│   Chats      │────────>│    Users    │
└─────────────┘         └──────────────┘         └─────────────┘


┌─────────────┐         ┌──────────────┐
│   Recipe    │         │  Embedding   │
│ Embeddings  │<────────│    Cache     │
│ (pgvector)  │         │   (Redis)    │
└─────────────┘         └──────────────┘
```

---

## Core Tables

### 1. users

Quản lý user accounts, authentication, và preferences.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Authentication
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255), -- NULL for OAuth-only users
    
    -- Profile
    full_name VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,
    
    -- OAuth
    oauth_provider VARCHAR(50), -- 'google', 'facebook', 'apple', NULL
    oauth_id VARCHAR(255),
    
    -- Preferences
    ai_personality VARCHAR(50) DEFAULT 'friendly' CHECK (
        ai_personality IN ('professional', 'friendly', 'humorous', 'nutritionist', 'efficient')
    ),
    language VARCHAR(10) DEFAULT 'vi' CHECK (language IN ('vi', 'en')),
    dietary_preferences JSONB DEFAULT '[]'::jsonb,
    -- Example: ["vegetarian", "gluten-free", "lactose-intolerant"]
    
    allergies JSONB DEFAULT '[]'::jsonb,
    -- Example: ["peanuts", "shellfish"]
    
    default_servings INTEGER DEFAULT 2,
    
    -- Voice Settings
    voice_enabled BOOLEAN DEFAULT true,
    wake_word_enabled BOOLEAN DEFAULT false,
    tts_voice VARCHAR(50) DEFAULT 'vi-VN-Wavenet-A',
    
    -- Privacy
    profile_public BOOLEAN DEFAULT true,
    show_cooking_history BOOLEAN DEFAULT true,
    
    -- Notifications
    notification_settings JSONB DEFAULT '{
        "email": true,
        "push": true,
        "timer_complete": true,
        "new_recipes": false,
        "weekly_suggestions": true
    }'::jsonb,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    
    -- Stats (cached, updated via triggers)
    total_recipes_cooked INTEGER DEFAULT 0,
    total_cooking_time_seconds INTEGER DEFAULT 0,
    total_recipes_saved INTEGER DEFAULT 0,
    
    CONSTRAINT unique_oauth UNIQUE (oauth_provider, oauth_id)
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Full-text search on user profiles
CREATE INDEX idx_users_search ON users USING GIN (
    to_tsvector('simple', coalesce(full_name, '') || ' ' || coalesce(display_name, ''))
);
```

**Sample Data:**
```sql
INSERT INTO users (email, full_name, display_name, ai_personality, dietary_preferences, allergies) VALUES
('user@example.com', 'Nguyễn Văn A', 'Chef A', 'friendly', 
 '["vegetarian"]'::jsonb, '["peanuts"]'::jsonb);
```

---

### 2. categories

Danh mục recipes (Món chính, Món tráng miệng, etc.).

```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic Info
    name_vi VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description_vi TEXT,
    description_en TEXT,
    
    -- Visual
    icon_url TEXT,
    image_url TEXT,
    color_hex VARCHAR(7), -- Example: "#FF6F00"
    
    -- Hierarchy (for sub-categories)
    parent_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    
    -- Display Order
    sort_order INTEGER DEFAULT 0,
    
    -- Stats (cached)
    recipe_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Indexes
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_sort ON categories(sort_order);
```

**Sample Data:**
```sql
INSERT INTO categories (name_vi, name_en, slug, color_hex, sort_order) VALUES
('Món chính', 'Main Dishes', 'main-dishes', '#FF6F00', 1),
('Món khai vị', 'Appetizers', 'appetizers', '#4CAF50', 2),
('Món tráng miệng', 'Desserts', 'desserts', '#E91E63', 3),
('Món súp', 'Soups', 'soups', '#2196F3', 4),
('Đồ uống', 'Beverages', 'beverages', '#9C27B0', 5);
```

---

### 3. recipes

Core table cho cooking recipes.

```sql
CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic Info
    title_vi VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_vi TEXT,
    description_en TEXT,
    
    -- Author
    author_id UUID REFERENCES users(id) ON DELETE SET NULL,
    author_name VARCHAR(255), -- Cached for performance
    
    -- Category
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    
    -- Media
    image_url TEXT,
    video_url TEXT,
    thumbnail_url TEXT,
    
    -- Recipe Details
    servings INTEGER DEFAULT 2,
    prep_time_minutes INTEGER, -- Preparation time
    cook_time_minutes INTEGER, -- Cooking time
    total_time_minutes INTEGER GENERATED ALWAYS AS (prep_time_minutes + cook_time_minutes) STORED,
    
    difficulty VARCHAR(20) DEFAULT 'medium' CHECK (
        difficulty IN ('easy', 'medium', 'hard')
    ),
    
    cuisine VARCHAR(50), -- 'vietnamese', 'japanese', 'italian', etc.
    
    -- Instructions Summary (for preview)
    instructions_summary TEXT,
    
    -- Tags (for filtering)
    tags JSONB DEFAULT '[]'::jsonb,
    -- Example: ["quick", "healthy", "budget-friendly", "one-pot"]
    
    dietary_tags JSONB DEFAULT '[]'::jsonb,
    -- Example: ["vegetarian", "vegan", "gluten-free", "keto"]
    
    -- Stats (cached, updated via triggers)
    view_count INTEGER DEFAULT 0,
    save_count INTEGER DEFAULT 0,
    cook_count INTEGER DEFAULT 0,
    rating_average DECIMAL(3,2) DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    
    -- SEO
    meta_title VARCHAR(255),
    meta_description TEXT,
    meta_keywords TEXT[],
    
    -- Status
    status VARCHAR(20) DEFAULT 'draft' CHECK (
        status IN ('draft', 'published', 'archived')
    ),
    
    -- Moderation
    is_featured BOOLEAN DEFAULT false,
    is_verified BOOLEAN DEFAULT false, -- Verified by admin/chef
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP WITH TIME ZONE,
    
    -- Search Vector (for full-text search)
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('simple',
            coalesce(title_vi, '') || ' ' ||
            coalesce(title_en, '') || ' ' ||
            coalesce(description_vi, '') || ' ' ||
            coalesce(tags::text, '')
        )
    ) STORED
);

-- Indexes
CREATE INDEX idx_recipes_slug ON recipes(slug);
CREATE INDEX idx_recipes_author ON recipes(author_id);
CREATE INDEX idx_recipes_category ON recipes(category_id);
CREATE INDEX idx_recipes_status ON recipes(status) WHERE status = 'published';
CREATE INDEX idx_recipes_featured ON recipes(is_featured) WHERE is_featured = true;
CREATE INDEX idx_recipes_rating ON recipes(rating_average DESC);
CREATE INDEX idx_recipes_created ON recipes(created_at DESC);
CREATE INDEX idx_recipes_total_time ON recipes(total_time_minutes);
CREATE INDEX idx_recipes_difficulty ON recipes(difficulty);

-- Full-text search
CREATE INDEX idx_recipes_search ON recipes USING GIN (search_vector);

-- JSONB indexes for tag filtering
CREATE INDEX idx_recipes_tags ON recipes USING GIN (tags);
CREATE INDEX idx_recipes_dietary ON recipes USING GIN (dietary_tags);
```

**Sample Data:**
```sql
INSERT INTO recipes (
    title_vi, title_en, slug, description_vi, 
    category_id, servings, prep_time_minutes, cook_time_minutes,
    difficulty, cuisine, tags, dietary_tags, status, published_at
) VALUES (
    'Phở Bò Hà Nội', 'Hanoi Beef Pho', 'pho-bo-ha-noi',
    'Món phở bò truyền thống Hà Nội với nước dùng đậm đà từ xương hầm 12 tiếng',
    (SELECT id FROM categories WHERE slug = 'main-dishes'),
    4, 30, 180, 'medium', 'vietnamese',
    '["traditional", "comfort-food", "popular"]'::jsonb,
    '[]'::jsonb,
    'published', CURRENT_TIMESTAMP
);
```

---

### 4. recipe_ingredients

Junction table giữa recipes và ingredients với quantities.

```sql
CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id UUID NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    
    -- Quantity
    quantity DECIMAL(10,2),
    unit VARCHAR(50), -- 'kg', 'g', 'ml', 'tbsp', 'tsp', 'cup', 'piece', etc.
    
    -- Optional specification
    preparation_note VARCHAR(255), -- "diced", "sliced thin", "minced", etc.
    
    -- Grouping (for recipe display)
    ingredient_group VARCHAR(100), -- "Main ingredients", "Seasoning", "Garnish"
    sort_order INTEGER DEFAULT 0,
    
    -- Optional/Substitution
    is_optional BOOLEAN DEFAULT false,
    substitutes JSONB DEFAULT '[]'::jsonb,
    -- Example: [{"ingredient_id": "uuid", "name": "ginger", "note": "same amount"}]
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_recipe_ingredient UNIQUE (recipe_id, ingredient_id)
);

-- Indexes
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);
CREATE INDEX idx_recipe_ingredients_sort ON recipe_ingredients(recipe_id, sort_order);
```

**Sample Data:**
```sql
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, ingredient_group, sort_order) VALUES
((SELECT id FROM recipes WHERE slug = 'pho-bo-ha-noi'),
 (SELECT id FROM ingredients WHERE name_en = 'beef bones'),
 1.0, 'kg', 'Main ingredients', 1);
```

---

### 5. ingredients

Master table cho tất cả ingredients.

```sql
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Names
    name_vi VARCHAR(255) NOT NULL,
    name_en VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    
    -- Alternative Names (for search)
    aliases_vi TEXT[], -- ['gừng tươi', 'củ gừng']
    aliases_en TEXT[], -- ['fresh ginger', 'ginger root']
    
    -- Category
    category VARCHAR(100), -- 'vegetables', 'meat', 'spices', 'dairy', etc.
    
    -- Image
    image_url TEXT,
    
    -- Nutritional Info (per 100g)
    calories DECIMAL(10,2),
    protein_g DECIMAL(10,2),
    carbs_g DECIMAL(10,2),
    fat_g DECIMAL(10,2),
    fiber_g DECIMAL(10,2),
    
    -- Dietary Flags
    is_vegetarian BOOLEAN DEFAULT true,
    is_vegan BOOLEAN DEFAULT true,
    is_gluten_free BOOLEAN DEFAULT true,
    is_dairy_free BOOLEAN DEFAULT true,
    
    -- Common allergens
    allergens TEXT[], -- ['gluten', 'dairy', 'nuts', 'shellfish', etc.]
    
    -- Storage & Shelf Life
    storage_tips_vi TEXT,
    storage_tips_en TEXT,
    shelf_life_days INTEGER,
    
    -- Usage Stats
    recipe_count INTEGER DEFAULT 0, -- How many recipes use this
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Search Vector
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('simple',
            coalesce(name_vi, '') || ' ' ||
            coalesce(name_en, '') || ' ' ||
            coalesce(array_to_string(aliases_vi, ' '), '') || ' ' ||
            coalesce(array_to_string(aliases_en, ' '), '')
        )
    ) STORED
);

-- Indexes
CREATE INDEX idx_ingredients_slug ON ingredients(slug);
CREATE INDEX idx_ingredients_category ON ingredients(category);
CREATE INDEX idx_ingredients_search ON ingredients USING GIN (search_vector);

-- Unique constraint on English name
CREATE UNIQUE INDEX idx_ingredients_name_en ON ingredients(LOWER(name_en));
```

**Sample Data:**
```sql
INSERT INTO ingredients (
    name_vi, name_en, slug, aliases_vi, aliases_en, category,
    calories, protein_g, carbs_g, fat_g,
    is_vegetarian, is_vegan
) VALUES
('Xương bò', 'Beef bones', 'beef-bones', 
 ARRAY['xương hầm', 'xương ống'], ARRAY['marrow bones'], 
 'meat', 150, 20, 0, 8, false, false),
('Gừng', 'Ginger', 'ginger',
 ARRAY['gừng tươi', 'củ gừng'], ARRAY['fresh ginger', 'ginger root'],
 'spices', 80, 1.8, 18, 0.8, true, true);
```

---

### 6. recipe_steps

Chi tiết từng bước nấu ăn.

```sql
CREATE TABLE recipe_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Step Details
    step_number INTEGER NOT NULL,
    title_vi VARCHAR(255),
    title_en VARCHAR(255),
    instructions_vi TEXT NOT NULL,
    instructions_en TEXT,
    
    -- Media
    image_url TEXT,
    video_url TEXT,
    
    -- Timer (if applicable)
    has_timer BOOLEAN DEFAULT false,
    timer_duration_seconds INTEGER,
    timer_name VARCHAR(100), -- "Luộc xương", "Nấu nước dùng"
    
    -- Tips
    tip_vi TEXT,
    tip_en TEXT,
    
    -- Temperature (if applicable)
    temperature_celsius INTEGER,
    temperature_note VARCHAR(100), -- "medium heat", "high heat"
    
    -- Sort Order
    sort_order INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_recipe_step UNIQUE (recipe_id, step_number)
);

-- Indexes
CREATE INDEX idx_recipe_steps_recipe ON recipe_steps(recipe_id, step_number);
CREATE INDEX idx_recipe_steps_sort ON recipe_steps(recipe_id, sort_order);
```

**Sample Data:**
```sql
INSERT INTO recipe_steps (
    recipe_id, step_number, title_vi, instructions_vi,
    has_timer, timer_duration_seconds, timer_name, tip_vi
) VALUES (
    (SELECT id FROM recipes WHERE slug = 'pho-bo-ha-noi'),
    2, 'Luộc xương bò với gừng',
    'Cho xương bò vào nồi nước sôi, thêm gừng đập dập. Luộc 5 phút rồi vớt ra rửa sạch. Điều này giúp khử mùi hôi xương.',
    true, 300, 'Luộc xương',
    'Nước luộc xương nên đổ đi, không dùng để nấu phở'
);
```

---

### 7. nutrition_facts

Chi tiết dinh dưỡng cho mỗi recipe (calculated từ ingredients).

```sql
CREATE TABLE nutrition_facts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    recipe_id UUID UNIQUE NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Per serving
    serving_size VARCHAR(100), -- "1 bowl (500ml)"
    
    -- Macros (per serving)
    calories DECIMAL(10,2),
    protein_g DECIMAL(10,2),
    carbohydrates_g DECIMAL(10,2),
    fat_g DECIMAL(10,2),
    fiber_g DECIMAL(10,2),
    sugar_g DECIMAL(10,2),
    
    -- Micros
    sodium_mg DECIMAL(10,2),
    cholesterol_mg DECIMAL(10,2),
    vitamin_a_mcg DECIMAL(10,2),
    vitamin_c_mg DECIMAL(10,2),
    calcium_mg DECIMAL(10,2),
    iron_mg DECIMAL(10,2),
    
    -- Calculated
    is_calculated BOOLEAN DEFAULT true, -- true if auto-calculated
    last_calculated_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_nutrition_recipe ON nutrition_facts(recipe_id);
```

---

### 8. favorites

User saved/favorited recipes.

```sql
CREATE TABLE favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Optional organization
    list_id UUID REFERENCES recipe_lists(id) ON DELETE SET NULL,
    
    -- Notes
    personal_note TEXT,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_user_favorite UNIQUE (user_id, recipe_id)
);

-- Indexes
CREATE INDEX idx_favorites_user ON favorites(user_id, created_at DESC);
CREATE INDEX idx_favorites_recipe ON favorites(recipe_id);
CREATE INDEX idx_favorites_list ON favorites(list_id);
```

---

### 9. recipe_lists

User-created collections/lists of recipes.

```sql
CREATE TABLE recipe_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- List Info
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Privacy
    is_public BOOLEAN DEFAULT false,
    
    -- Visual
    cover_image_url TEXT,
    
    -- Stats
    recipe_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_recipe_lists_user ON recipe_lists(user_id);
CREATE INDEX idx_recipe_lists_public ON recipe_lists(is_public) WHERE is_public = true;
```

---

### 10. ratings

User ratings and reviews for recipes.

```sql
CREATE TABLE ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Rating
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    
    -- Review
    review_text TEXT,
    
    -- Cooking Context
    actual_difficulty VARCHAR(20) CHECK (actual_difficulty IN ('easy', 'medium', 'hard')),
    would_cook_again BOOLEAN,
    
    -- Media
    photos JSONB DEFAULT '[]'::jsonb, -- Array of image URLs
    
    -- Helpful votes
    helpful_count INTEGER DEFAULT 0,
    
    -- Moderation
    is_verified_cook BOOLEAN DEFAULT false, -- User actually cooked this
    is_flagged BOOLEAN DEFAULT false,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_user_rating UNIQUE (user_id, recipe_id)
);

-- Indexes
CREATE INDEX idx_ratings_recipe ON ratings(recipe_id, created_at DESC);
CREATE INDEX idx_ratings_user ON ratings(user_id);
CREATE INDEX idx_ratings_rating ON ratings(rating);
CREATE INDEX idx_ratings_verified ON ratings(is_verified_cook) WHERE is_verified_cook = true;
```

---

### 11. comments

Comments on recipes (optional discussion feature).

```sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Comment
    comment_text TEXT NOT NULL,
    
    -- Threading (replies)
    parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    
    -- Reactions
    like_count INTEGER DEFAULT 0,
    
    -- Moderation
    is_flagged BOOLEAN DEFAULT false,
    is_deleted BOOLEAN DEFAULT false,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_comments_recipe ON comments(recipe_id, created_at DESC);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_comments_parent ON comments(parent_id);
```

---

## Cooking Sessions & Progress Tracking

### 12. cooking_sessions

Track active và completed cooking sessions.

```sql
CREATE TABLE cooking_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Progress
    current_step INTEGER DEFAULT 1,
    total_steps INTEGER NOT NULL,
    completed_steps INTEGER[] DEFAULT ARRAY[]::INTEGER[],
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (
        status IN ('active', 'paused', 'completed', 'abandoned')
    ),
    
    -- Timings
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    paused_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    elapsed_time_seconds INTEGER DEFAULT 0,
    
    -- Session Data
    session_data JSONB DEFAULT '{}'::jsonb,
    -- Example: {"ingredients_checked": [1,2,3], "notes": "Added more salt"}
    
    -- Completion Data (if completed)
    completion_rating INTEGER CHECK (completion_rating >= 1 AND completion_rating <= 5),
    completion_notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Expiry (sessions older than 24 hours should be marked abandoned)
    expires_at TIMESTAMP WITH TIME ZONE GENERATED ALWAYS AS (
        started_at + INTERVAL '24 hours'
    ) STORED
);

-- Indexes
CREATE INDEX idx_cooking_sessions_user ON cooking_sessions(user_id);
CREATE INDEX idx_cooking_sessions_recipe ON cooking_sessions(recipe_id);
CREATE INDEX idx_cooking_sessions_status ON cooking_sessions(status);
CREATE INDEX idx_cooking_sessions_active ON cooking_sessions(user_id, status) 
    WHERE status IN ('active', 'paused');
CREATE INDEX idx_cooking_sessions_expires ON cooking_sessions(expires_at);
```

---

### 13. cooking_timers

Track timers within cooking sessions.

```sql
CREATE TABLE cooking_timers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    session_id UUID NOT NULL REFERENCES cooking_sessions(id) ON DELETE CASCADE,
    
    -- Timer Info
    name VARCHAR(255) NOT NULL,
    duration_seconds INTEGER NOT NULL,
    remaining_seconds INTEGER NOT NULL,
    
    -- Associated Step
    step_number INTEGER,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (
        status IN ('active', 'paused', 'completed', 'cancelled')
    ),
    
    -- Timings
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    paused_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Notification
    notification_sent BOOLEAN DEFAULT false,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_cooking_timers_session ON cooking_timers(session_id);
CREATE INDEX idx_cooking_timers_status ON cooking_timers(status);
CREATE INDEX idx_cooking_timers_active ON cooking_timers(session_id, status)
    WHERE status IN ('active', 'paused');
```

---

## AI & Chat Features

### 14. chats

User conversation threads with AI.

```sql
CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Chat Info
    title VARCHAR(255), -- Auto-generated or user-defined
    
    -- Context
    context_type VARCHAR(50), -- 'general', 'recipe', 'ingredient', null
    context_id UUID, -- Reference to recipe_id, ingredient_id, etc.
    
    -- AI Settings (at time of creation)
    ai_personality VARCHAR(50),
    ai_model VARCHAR(50) DEFAULT 'gpt-4o',
    
    -- Stats
    message_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_message_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_chats_user ON chats(user_id, last_message_at DESC);
CREATE INDEX idx_chats_context ON chats(context_type, context_id);
```

---

### 15. chat_messages

Individual messages in chat conversations.

```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    
    -- Message
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    
    -- Media (for user messages)
    media_urls JSONB DEFAULT '[]'::jsonb,
    -- Example: [{"type": "image", "url": "https://..."}]
    
    -- AI Metadata (for assistant messages)
    ai_model VARCHAR(50),
    completion_tokens INTEGER,
    prompt_tokens INTEGER,
    
    -- RAG Context (for assistant messages)
    retrieved_recipes JSONB DEFAULT '[]'::jsonb,
    -- Example: [{"recipe_id": "uuid", "score": 0.95, "reason": "..."}]
    
    -- Feedback
    user_feedback VARCHAR(20), -- 'helpful', 'not_helpful', null
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_chat_messages_chat ON chat_messages(chat_id, created_at);
CREATE INDEX idx_chat_messages_created ON chat_messages(created_at DESC);
```

---

## RAG & Vector Search

### 16. recipe_embeddings

Store vector embeddings for RAG (using pgvector).

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE recipe_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    recipe_id UUID UNIQUE NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    
    -- Embedding (OpenAI text-embedding-3-small = 1536 dimensions)
    embedding vector(1536) NOT NULL,
    
    -- Source text (for debugging)
    source_text TEXT,
    
    -- Metadata
    model VARCHAR(50) DEFAULT 'text-embedding-3-small',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vector similarity index (IVFFlat for fast approximate search)
CREATE INDEX idx_recipe_embeddings_vector ON recipe_embeddings 
    USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 100);

-- Recipe lookup
CREATE INDEX idx_recipe_embeddings_recipe ON recipe_embeddings(recipe_id);
```

**Usage Example:**
```sql
-- Find similar recipes using cosine similarity
SELECT 
    r.id, r.title_vi, 
    1 - (e1.embedding <=> e2.embedding) as similarity
FROM recipe_embeddings e1
JOIN recipe_embeddings e2 ON e2.recipe_id = $1
JOIN recipes r ON r.id = e1.recipe_id
WHERE e1.recipe_id != $1
ORDER BY e1.embedding <=> e2.embedding
LIMIT 10;
```

---

### 17. ingredient_embeddings

Vector embeddings cho ingredients (for camera recognition improvement).

```sql
CREATE TABLE ingredient_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    ingredient_id UUID UNIQUE NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    
    -- Embedding
    embedding vector(1536) NOT NULL,
    
    -- Source
    source_text TEXT,
    model VARCHAR(50) DEFAULT 'text-embedding-3-small',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vector index
CREATE INDEX idx_ingredient_embeddings_vector ON ingredient_embeddings 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);
```

---

## Search & Discovery

### 18. search_queries

Log search queries for analytics và trending keywords.

```sql
CREATE TABLE search_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Query
    query TEXT NOT NULL,
    query_normalized TEXT, -- Lowercase, trimmed
    
    -- Context
    filters JSONB DEFAULT '{}'::jsonb,
    -- Example: {"category": "main-dishes", "difficulty": "easy"}
    
    -- Results
    result_count INTEGER DEFAULT 0,
    clicked_recipe_id UUID REFERENCES recipes(id) ON DELETE SET NULL,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    ip_address INET
);

-- Indexes
CREATE INDEX idx_search_queries_query ON search_queries(query_normalized);
CREATE INDEX idx_search_queries_user ON search_queries(user_id);
CREATE INDEX idx_search_queries_created ON search_queries(created_at DESC);

-- For trending queries
CREATE INDEX idx_search_queries_trending ON search_queries(created_at DESC)
    WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '7 days';
```

---

### 19. trending_keywords

Cached trending search terms (updated hourly via cron).

```sql
CREATE TABLE trending_keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    keyword VARCHAR(255) UNIQUE NOT NULL,
    search_count INTEGER DEFAULT 0,
    trend_score DECIMAL(10,4) DEFAULT 0, -- Weighted by recency
    
    -- Time window
    period VARCHAR(20) DEFAULT 'daily' CHECK (period IN ('hourly', 'daily', 'weekly')),
    
    -- Metadata
    first_seen_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_trending_keywords_score ON trending_keywords(trend_score DESC);
CREATE INDEX idx_trending_keywords_period ON trending_keywords(period, trend_score DESC);
```

---

## Activity & Analytics

### 20. user_activity

Track user actions for recommendations và analytics.

```sql
CREATE TABLE user_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Activity
    activity_type VARCHAR(50) NOT NULL,
    -- 'view_recipe', 'save_recipe', 'start_cooking', 'complete_cooking', 
    -- 'search', 'chat_message', 'rate_recipe', etc.
    
    -- Target
    target_type VARCHAR(50), -- 'recipe', 'category', 'ingredient', etc.
    target_id UUID,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_user_activity_user ON user_activity(user_id, created_at DESC);
CREATE INDEX idx_user_activity_type ON user_activity(activity_type, created_at DESC);
CREATE INDEX idx_user_activity_target ON user_activity(target_type, target_id);

-- Partitioning by month for scalability (optional)
-- CREATE TABLE user_activity_2024_11 PARTITION OF user_activity
--     FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
```

---

## Authentication & Security

### 21. refresh_tokens

Store JWT refresh tokens for authentication.

```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Token
    token_hash VARCHAR(255) UNIQUE NOT NULL, -- SHA-256 hash
    
    -- Device Info
    device_id VARCHAR(255),
    device_name VARCHAR(255),
    user_agent TEXT,
    ip_address INET,
    
    -- Expiry
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Status
    is_revoked BOOLEAN DEFAULT false,
    revoked_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at);
CREATE INDEX idx_refresh_tokens_active ON refresh_tokens(user_id, is_revoked)
    WHERE is_revoked = false;
```

---

### 22. email_verifications

Email verification tokens.

```sql
CREATE TABLE email_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Token
    token VARCHAR(255) UNIQUE NOT NULL,
    
    -- Email
    email VARCHAR(255) NOT NULL,
    
    -- Status
    is_used BOOLEAN DEFAULT false,
    used_at TIMESTAMP WITH TIME ZONE,
    
    -- Expiry (24 hours)
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP + INTERVAL '24 hours'),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_email_verifications_token ON email_verifications(token);
CREATE INDEX idx_email_verifications_user ON email_verifications(user_id);
```

---

### 23. password_resets

Password reset tokens.

```sql
CREATE TABLE password_resets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    email VARCHAR(255) NOT NULL,
    
    -- Token
    token VARCHAR(255) UNIQUE NOT NULL,
    
    -- Status
    is_used BOOLEAN DEFAULT false,
    used_at TIMESTAMP WITH TIME ZONE,
    
    -- Expiry (1 hour)
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP + INTERVAL '1 hour'),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_password_resets_token ON password_resets(token);
CREATE INDEX idx_password_resets_email ON password_resets(email);
```

---

## Database Functions & Triggers

### Update `updated_at` Timestamp

```sql
-- Function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recipes_updated_at
    BEFORE UPDATE ON recipes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Repeat for other tables: categories, ingredients, recipe_steps, etc.
```

---

### Update Recipe Stats on Rating

```sql
-- Function to recalculate recipe rating average
CREATE OR REPLACE FUNCTION update_recipe_rating_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE recipes
    SET 
        rating_average = (
            SELECT ROUND(AVG(rating)::numeric, 2)
            FROM ratings
            WHERE recipe_id = NEW.recipe_id
        ),
        rating_count = (
            SELECT COUNT(*)
            FROM ratings
            WHERE recipe_id = NEW.recipe_id
        )
    WHERE id = NEW.recipe_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger on INSERT or UPDATE
CREATE TRIGGER update_recipe_rating_stats_trigger
    AFTER INSERT OR UPDATE ON ratings
    FOR EACH ROW
    EXECUTE FUNCTION update_recipe_rating_stats();
```

---

### Update User Stats

```sql
-- Update total_recipes_cooked when cooking_session completed
CREATE OR REPLACE FUNCTION update_user_cooking_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        UPDATE users
        SET 
            total_recipes_cooked = total_recipes_cooked + 1,
            total_cooking_time_seconds = total_cooking_time_seconds + NEW.elapsed_time_seconds
        WHERE id = NEW.user_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_cooking_stats_trigger
    AFTER UPDATE ON cooking_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_user_cooking_stats();
```

---

### Update Category Recipe Count

```sql
CREATE OR REPLACE FUNCTION update_category_recipe_count()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment for new recipe
    IF TG_OP = 'INSERT' AND NEW.category_id IS NOT NULL THEN
        UPDATE categories
        SET recipe_count = recipe_count + 1
        WHERE id = NEW.category_id;
    END IF;
    
    -- Handle category change
    IF TG_OP = 'UPDATE' AND NEW.category_id != OLD.category_id THEN
        IF OLD.category_id IS NOT NULL THEN
            UPDATE categories
            SET recipe_count = recipe_count - 1
            WHERE id = OLD.category_id;
        END IF;
        
        IF NEW.category_id IS NOT NULL THEN
            UPDATE categories
            SET recipe_count = recipe_count + 1
            WHERE id = NEW.category_id;
        END IF;
    END IF;
    
    -- Decrement for deleted recipe
    IF TG_OP = 'DELETE' AND OLD.category_id IS NOT NULL THEN
        UPDATE categories
        SET recipe_count = recipe_count - 1
        WHERE id = OLD.category_id;
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_category_recipe_count_trigger
    AFTER INSERT OR UPDATE OR DELETE ON recipes
    FOR EACH ROW
    EXECUTE FUNCTION update_category_recipe_count();
```

---

## Indexes Summary

### Performance-Critical Indexes

```sql
-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id);

-- Recipes (most queried)
CREATE INDEX idx_recipes_status_published ON recipes(status) WHERE status = 'published';
CREATE INDEX idx_recipes_featured ON recipes(is_featured) WHERE is_featured = true;
CREATE INDEX idx_recipes_rating_desc ON recipes(rating_average DESC);
CREATE INDEX idx_recipes_created_desc ON recipes(created_at DESC);
CREATE INDEX idx_recipes_category ON recipes(category_id);
CREATE INDEX idx_recipes_search_gin ON recipes USING GIN (search_vector);
CREATE INDEX idx_recipes_tags_gin ON recipes USING GIN (tags);

-- Favorites (user-specific queries)
CREATE INDEX idx_favorites_user_created ON favorites(user_id, created_at DESC);

-- Ratings (recipe detail page)
CREATE INDEX idx_ratings_recipe_created ON ratings(recipe_id, created_at DESC);

-- Cooking Sessions (active session lookup)
CREATE INDEX idx_cooking_sessions_active ON cooking_sessions(user_id, status)
    WHERE status IN ('active', 'paused');

-- Vector Search (RAG)
CREATE INDEX idx_recipe_embeddings_vector ON recipe_embeddings 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Search Queries (trending)
CREATE INDEX idx_search_queries_trending ON search_queries(created_at DESC)
    WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '7 days';
```

---

## Data Retention & Cleanup

### Auto-Cleanup Expired Sessions

```sql
-- Mark abandoned sessions (older than 24 hours)
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void AS $$
BEGIN
    UPDATE cooking_sessions
    SET status = 'abandoned'
    WHERE status IN ('active', 'paused')
        AND expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Run via cron job (every hour)
-- SELECT cron.schedule('cleanup-sessions', '0 * * * *', 'SELECT cleanup_expired_sessions()');
```

---

### Archive Old User Activity

```sql
-- Archive activity older than 90 days to separate table
CREATE TABLE user_activity_archive (LIKE user_activity INCLUDING ALL);

CREATE OR REPLACE FUNCTION archive_old_activity()
RETURNS void AS $$
BEGIN
    INSERT INTO user_activity_archive
    SELECT * FROM user_activity
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '90 days';
    
    DELETE FROM user_activity
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '90 days';
END;
$$ LANGUAGE plpgsql;

-- Run monthly
-- SELECT cron.schedule('archive-activity', '0 0 1 * *', 'SELECT archive_old_activity()');
```

---

## Database Size Estimates

### Initial Data (MVP)

```
users:                    1,000 rows    ~200 KB
categories:                  20 rows      ~5 KB
recipes:                  1,000 rows   ~2 MB
recipe_ingredients:       5,000 rows   ~500 KB
ingredients:              1,000 rows   ~200 KB
recipe_steps:             8,000 rows   ~4 MB
nutrition_facts:          1,000 rows   ~100 KB
favorites:                5,000 rows   ~500 KB
ratings:                  3,000 rows   ~1 MB
cooking_sessions:         2,000 rows   ~500 KB
cooking_timers:           3,000 rows   ~300 KB
chats:                    2,000 rows   ~200 KB
chat_messages:           20,000 rows   ~10 MB
recipe_embeddings:        1,000 rows   ~12 MB (1536 dimensions × 4 bytes × 1000)
user_activity:           50,000 rows   ~10 MB

TOTAL (estimated):                     ~41 MB
```

### After 1 Year (Projected)

```
users:                   50,000 rows   ~10 MB
recipes:                 10,000 rows   ~20 MB
recipe_embeddings:       10,000 rows  ~120 MB
favorites:              200,000 rows   ~20 MB
ratings:                100,000 rows   ~30 MB
cooking_sessions:       500,000 rows  ~100 MB
chat_messages:        1,000,000 rows  ~500 MB
user_activity:       10,000,000 rows    ~2 GB
search_queries:       5,000,000 rows    ~1 GB

TOTAL (estimated):                    ~3.8 GB
```

**Note:** With proper indexing, partitioning, and archiving, database will remain performant up to 10GB+.

---

## Backup Strategy

### Daily Backups
```bash
# Full database dump
pg_dump -Fc cooking_assistant > backup_$(date +%Y%m%d).dump

# Backup to S3/cloud storage
aws s3 cp backup_$(date +%Y%m%d).dump s3://backups/postgres/
```

### Point-in-Time Recovery
```sql
-- Enable WAL archiving in postgresql.conf
archive_mode = on
archive_command = 'cp %p /archive/%f'
wal_level = replica
```

---

## Summary

### Total Tables: 23

**Core Tables (10):**
1. users
2. categories
3. recipes
4. recipe_ingredients
5. ingredients
6. recipe_steps
7. nutrition_facts
8. favorites
9. recipe_lists
10. ratings

**Cooking & Progress (2):**
11. cooking_sessions
12. cooking_timers

**AI & Chat (2):**
13. chats
14. chat_messages

**RAG & Vectors (2):**
15. recipe_embeddings
16. ingredient_embeddings

**Search & Discovery (2):**
17. search_queries
18. trending_keywords

**Activity & Analytics (1):**
19. user_activity

**Authentication (3):**
20. refresh_tokens
21. email_verifications
22. password_resets

**Optional (1):**
23. comments

---

### Key Features

✅ **UUID Primary Keys** - Distributed-friendly, no collisions  
✅ **JSONB Flexibility** - Dynamic metadata without schema changes  
✅ **Full-Text Search** - Native PostgreSQL tsvector (Vietnamese support)  
✅ **Vector Search** - pgvector for RAG similarity search  
✅ **Soft Deletes** - is_active, is_deleted flags  
✅ **Audit Trail** - created_at, updated_at timestamps  
✅ **Stats Caching** - Denormalized counts for performance  
✅ **Triggers & Functions** - Auto-update stats, timestamps  
✅ **Proper Indexing** - Optimized for common queries  
✅ **Data Integrity** - Foreign keys, constraints, check constraints  

---

**✅ Database Schema Design Complete!**

Schema này support đầy đủ tất cả features của app:
- Recipe management với ingredients, steps, nutrition
- User authentication (email + OAuth)
- Cooking sessions với progress tracking và timers
- AI chat với RAG (vector embeddings)
- Search, favorites, ratings, comments
- Analytics và activity tracking
- Security (refresh tokens, email verification)

Sẵn sàng cho phần tiếp theo: **API Endpoints Specification**! 🚀
