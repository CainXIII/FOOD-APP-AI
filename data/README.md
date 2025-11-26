# 📦 JSON Sample Data - AI Cooking Assistant

Thư mục này chứa tất cả dữ liệu mẫu dưới dạng JSON để phục vụ cho việc phát triển và testing ứng dụng AI Cooking Assistant.

## 📋 Danh Sách Files

### 1. Core Data

#### `categories.json` - Danh Mục Món Ăn
- **Số lượng**: 15 categories
- **Nội dung**: Món chính, Món khai vị, Món tráng miệng, Món súp, Đồ uống, Món ăn sáng, Món salad, Món nướng, Món chiên, Món hấp, Món xào, Món hầm, Bánh mì & Sandwich, Món chay, Món Việt
- **Thuộc tính**: id, name_vi, name_en, slug, description, icon_url, image_url, color_hex, parent_id, sort_order, is_active

#### `ingredients.json` - Nguyên Liệu
- **Số lượng**: 30 ingredients
- **Phân loại**: 
  - Proteins: Xương bò, Thịt bò, Thịt gà, Thịt heo, Tôm, Cá, Trứng gà, Đậu phụ
  - Vegetables: Gừng, Hành tây, Tỏi, Cà chua, Cà rốt, Khoai tây, Rau muống, Rau ngót, Hành lá
  - Noodles/Grains: Bánh phở, Gạo, Bún, Mì
  - Seasonings: Muối, Đường, Nước mắm, Dầu ăn, Xì dầu, Hạt nêm, Tiêu, Ớt, Ngò rí
- **Thuộc tính**: id, name_vi, name_en, slug, aliases, category, image_url, nutrition (calories, protein, carbs, fat, fiber), dietary flags (vegetarian, vegan, gluten_free, dairy_free), allergens

#### `users.json` - Người Dùng
- **Số lượng**: 5 users (1 admin + 4 regular users)
- **Thuộc tính**: id, email, password_hash, full_name, display_name, avatar_url, bio, oauth_provider, oauth_id, ai_personality, language, dietary_preferences, allergies, default_servings, voice_enabled, wake_word_enabled, tts_voice, notification_settings, cooking stats

#### `recipes.json` - Công Thức Món Ăn
- **Số lượng**: 3 complete recipes
  - **Phở Bò Hà Nội** (8 steps, 750 phút, khó)
  - **Cơm Gà Hải Nam** (4 steps, 60 phút, trung bình)
  - **Gỏi Cuốn Tôm Thịt** (4 steps, 40 phút, dễ)
- **Thuộc tính**: id, title_vi/en, slug, description, author_id, category_id, images, videos, prep_time, cook_time, servings, difficulty, cuisine, meal_type, tags, dietary flags, allergens, ingredients_summary, steps (với timer details), nutrition_facts, rating_average, stats (views, favorites, cooked, shares), is_featured, is_published

### 2. Social Features

#### `ratings.json` - Đánh Giá & Reviews
- **Số lượng**: 4 ratings
- **Thuộc tính**: id, recipe_id, user_id, rating (1-5), review, helpful_count, is_verified_cook

#### `favorites.json` - Món Ăn Yêu Thích
- **Số lượng**: 5 favorites
- **Thuộc tính**: id, user_id, recipe_id, notes

#### `comments.json` - Bình Luận
- **Số lượng**: 6 comments (including replies)
- **Thuộc tính**: id, recipe_id, user_id, parent_id (for threading), content, helpful_count

#### `recipe-lists.json` - Danh Sách Công Thức
- **Số lượng**: 3 lists
- **Ví dụ**: "Món ăn cuối tuần", "Healthy Meal Prep", "Món ăn nhanh 30 phút"
- **Thuộc tính**: id, user_id, name, description, is_public, recipe_ids[]

### 3. Cooking Features

#### `cooking-sessions.json` - Phiên Nấu Ăn
- **Số lượng**: 2 sessions (1 in_progress, 1 completed)
- **Thuộc tính**: id, user_id, recipe_id, status, current_step, servings_adjusted, session_data (completed_steps, active_timers, notes, modifications, ingredient_substitutions), rating_given, completed_at

#### `cooking-timers.json` - Timer Nấu Ăn
- **Số lượng**: 2 timers (1 running, 1 completed)
- **Thuộc tính**: id, cooking_session_id, step_number, label_vi/en, total_seconds, remaining_seconds, status, alert_sound, started_at, completed_at

### 4. AI Chat & RAG

#### `chats.json` - Cuộc Hội Thoại
- **Số lượng**: 2 chats
- **Thuộc tính**: id, user_id, title, context_type (recipe/general), context_id, last_message_at

#### `chat-messages.json` - Tin Nhắn Chat
- **Số lượng**: 6 messages (user + assistant)
- **Ví dụ**: 
  - Q: "Tôi có thể dùng nồi áp suất để hầm xương phở được không?"
  - Q: "Can you suggest a healthy meal plan for someone with gluten allergy?"
- **Thuộc tính**: id, chat_id, role (user/assistant), content, metadata (voice_input, wake_word_triggered, transcription_confidence, model, tokens_used, rag_sources, response_time_ms, tts_generated, tts_audio_url)

#### `recipe-embeddings.json` - Vector Embeddings cho Recipes
- **Số lượng**: 3 embeddings
- **Thuộc tính**: id, recipe_id, content_type, content_text, embedding (1536-dimensional vector - null in JSON), embedding_model

#### `ingredient-embeddings.json` - Vector Embeddings cho Ingredients
- **Số lượng**: 5 embeddings
- **Thuộc tính**: id, ingredient_id, content_text, embedding (null in JSON), embedding_model

### 5. Search & Analytics

#### `search-queries.json` - Lịch Sử Tìm Kiếm
- **Số lượng**: 5 queries
- **Ví dụ**: "món phở bò", "món ăn chay", "quick dinner recipes"
- **Thuộc tính**: id, user_id, query_text, filters (category, difficulty, max_time, dietary), results_count

#### `trending-keywords.json` - Từ Khóa Xu Hướng
- **Số lượng**: 10 keywords
- **Top keywords**: phở (0.95), món chay (0.87), healthy recipes (0.82)
- **Thuộc tính**: id, keyword, search_count, language (vi/en), trend_score

#### `user-activity.json` - Hoạt Động Người Dùng
- **Số lượng**: 8 activities
- **Activity types**: recipe_view, recipe_favorite, cooking_start, cooking_complete, recipe_rating, chat_message, recipe_share, search
- **Thuộc tính**: id, user_id, activity_type, target_id, metadata

### 6. Nutrition

#### `nutrition-facts.json` - Thông Tin Dinh Dưỡng
- **Số lượng**: 3 nutrition facts (one per recipe)
- **Thuộc tính**: id, recipe_id, serving_size, calories, macros (protein, carbs, fat, fiber, sugar), micronutrients (sodium, cholesterol, saturated_fat, trans_fat), vitamins (A, C, D, calcium, iron)

## 🎯 Mục Đích Sử Dụng

### Development
- Import vào database để testing
- Mock data cho API development
- UI/UX testing với dữ liệu thực tế

### Testing
- Unit tests với sample data
- Integration tests
- Load testing với data seed

### Documentation
- API examples với real data
- User stories demonstration
- Feature documentation

## 📝 Lưu Ý Quan Trọng

### UUIDs
Tất cả IDs sử dụng UUID v4 format. Prefix patterns:
- `550e8400-*`: categories
- `650e8400-*`: ingredients  
- `750e8400-*`: users
- `850e8400-*`: recipes
- `950e8400-*`: ratings
- `a50e8400-*`: favorites
- `b50e8400-*`: cooking_sessions
- `c50e8400-*`: cooking_timers
- `d50e8400-*`: chats
- `e50e8400-*`: chat_messages
- `f50e8400-*`: search_queries
- `g50e8400-*`: trending_keywords
- `h50e8400-*`: user_activity
- `i50e8400-*`: recipe_lists
- `j50e8400-*`: comments
- `k50e8400-*`: nutrition_facts
- `l50e8400-*`: recipe_embeddings
- `m50e8400-*`: ingredient_embeddings

### Timestamps
- Format: ISO 8601 (UTC)
- Example: `"2025-11-25T14:30:00Z"`
- Các trường: created_at, updated_at, last_message_at, started_at, completed_at

### Password Hashes
- Algorithm: bcrypt ($2b$12$...)
- Sample password: `password123` (for testing only)
- **NEVER** use these hashes in production

### Vector Embeddings
- Model: `text-embedding-3-small`
- Dimensions: 1536
- Trong JSON files: `embedding: null` (để tiết kiệm dung lượng)
- Thực tế: Generate từ OpenAI API khi import vào database

### Multilingual Support
- Vietnamese (vi): name_vi, description_vi, instruction_vi
- English (en): name_en, description_en, instruction_en
- Default language trong app settings

## 🔄 Import vào Database

### Sử dụng Python Script
```python
import json
import psycopg2

# Load JSON data
with open('data/categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)['categories']

# Insert into database
conn = psycopg2.connect(...)
cursor = conn.cursor()

for cat in categories:
    cursor.execute("""
        INSERT INTO categories (id, name_vi, name_en, slug, ...)
        VALUES (%(id)s, %(name_vi)s, %(name_en)s, %(slug)s, ...)
    """, cat)

conn.commit()
```

### Thứ Tự Import (Quan Trọng!)
1. `categories.json`
2. `ingredients.json`
3. `users.json`
4. `recipes.json`
5. `nutrition-facts.json`
6. `ratings.json`
7. `favorites.json`
8. `comments.json`
9. `recipe-lists.json`
10. `cooking-sessions.json`
11. `cooking-timers.json`
12. `chats.json`
13. `chat-messages.json`
14. `search-queries.json`
15. `trending-keywords.json`
16. `user-activity.json`
17. `recipe-embeddings.json` (generate embeddings first)
18. `ingredient-embeddings.json` (generate embeddings first)

### Generate Vector Embeddings
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# For each recipe/ingredient
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=content_text
)

embedding = response.data[0].embedding  # 1536-dimensional vector
```

## 📊 Thống Kê Dữ Liệu

- **Tổng số files**: 18 JSON files
- **Tổng số records**: ~150+ records
- **Kích thước**: ~45KB (without embeddings)
- **Ngôn ngữ**: Vietnamese (primary), English (secondary)
- **Recipes**: 3 complete Vietnamese recipes với 16 steps tổng cộng
- **Ingredients**: 30 common Vietnamese ingredients
- **Users**: 5 test users với different personas
- **AI Messages**: 6 sample conversations với RAG metadata

## 🚀 Next Steps

Sau khi có sample data, tiếp tục Phase 3:

1. ✅ Database Schema Design
2. ✅ Sample Data Formats (JSON)
3. ⏳ **API Endpoints Specification** (next)
4. ⏳ RAG Pipeline Architecture
5. ⏳ Authentication & Authorization
6. ⏳ Caching Strategy

---

**Note**: Đây là dữ liệu mẫu cho development và testing. Production data cần được validate, sanitize và có proper security measures.
