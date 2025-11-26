# 📡 API Endpoints Specification - AI Cooking Assistant

Complete REST API documentation for the AI Cooking Assistant backend (FastAPI).

**Base URL**: `https://api.cooking.app/v1`

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Recipes](#recipes)
4. [Ingredients](#ingredients)
5. [Categories](#categories)
6. [Cooking Sessions](#cooking-sessions)
7. [AI Chat](#ai-chat)
8. [Search](#search)
9. [Social Features](#social-features)
10. [Analytics](#analytics)
11. [Error Handling](#error-handling)
12. [Rate Limiting](#rate-limiting)

---

## 🔐 Authentication

### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "Nguyen Van A",
  "language": "vi"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "full_name": "Nguyen Van A",
      "is_verified": false
    },
    "tokens": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "token_type": "bearer",
      "expires_in": 3600
    }
  }
}
```

**Errors:**
- `400`: Email already exists
- `422`: Validation error (weak password, invalid email)

---

### POST /auth/login
Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "full_name": "Nguyen Van A",
      "avatar_url": "https://...",
      "ai_personality": "friendly"
    },
    "tokens": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "token_type": "bearer",
      "expires_in": 3600
    }
  }
}
```

**Errors:**
- `401`: Invalid credentials
- `403`: Account not verified or disabled

---

### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

**Errors:**
- `401`: Invalid or expired refresh token

---

### POST /auth/logout
Logout and invalidate tokens.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### POST /auth/oauth/{provider}
OAuth login (Google, Facebook, Apple).

**Path Parameters:**
- `provider`: `google` | `facebook` | `apple`

**Request Body:**
```json
{
  "access_token": "oauth_provider_token"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user": { /* user object */ },
    "tokens": { /* tokens */ }
  }
}
```

---

### POST /auth/verify-email
Verify email with token sent to user's email.

**Request Body:**
```json
{
  "token": "verification_token_from_email"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

---

### POST /auth/forgot-password
Request password reset email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

---

### POST /auth/reset-password
Reset password with token.

**Request Body:**
```json
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

---

## 👤 Users

### GET /users/me
Get current user profile.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "Nguyen Van A",
    "display_name": "Chef A",
    "avatar_url": "https://...",
    "bio": "Đam mê nấu ăn...",
    "ai_personality": "friendly",
    "language": "vi",
    "dietary_preferences": ["vegetarian"],
    "allergies": ["peanuts"],
    "default_servings": 4,
    "voice_enabled": true,
    "wake_word_enabled": true,
    "notification_settings": { /* ... */ },
    "stats": {
      "total_recipes_cooked": 12,
      "total_cooking_time_seconds": 28800,
      "total_recipes_saved": 45
    },
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

---

### PATCH /users/me
Update current user profile.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "full_name": "Nguyen Van A Updated",
  "display_name": "Chef A Pro",
  "bio": "New bio...",
  "ai_personality": "humorous",
  "dietary_preferences": ["vegetarian", "gluten-free"],
  "allergies": ["peanuts", "shellfish"],
  "default_servings": 2
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": { /* updated user object */ }
}
```

---

### POST /users/me/avatar
Upload user avatar.

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
file: [image file]
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "avatar_url": "https://storage.cooking.app/avatars/profile/uuid.webp"
  }
}
```

**Errors:**
- `413`: File too large (max 5MB)
- `415`: Invalid file type (only images)

---

### GET /users/{user_id}
Get public user profile.

**Path Parameters:**
- `user_id`: User UUID

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "display_name": "Chef A",
    "avatar_url": "https://...",
    "bio": "...",
    "stats": {
      "total_recipes_cooked": 12,
      "total_recipes_saved": 45
    },
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Note:** Only returns public information (email, dietary info hidden).

---

### GET /users/{user_id}/recipes
Get recipes created by user.

**Path Parameters:**
- `user_id`: User UUID

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `sort`: `created_at` | `rating` | `views` (default: `created_at`)
- `order`: `asc` | `desc` (default: `desc`)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "recipes": [
      {
        "id": "uuid",
        "title_vi": "Phở Bò Hà Nội",
        "slug": "pho-bo-ha-noi",
        "image_url": "https://...",
        "prep_time_minutes": 30,
        "cook_time_minutes": 720,
        "difficulty": "hard",
        "rating_average": 4.8,
        "rating_count": 234,
        "created_at": "2025-01-15T10:30:00Z"
      }
      // ... more recipes
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "pages": 3
    }
  }
}
```

---

## 🍽️ Recipes

### GET /recipes
List recipes with filters.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `category`: Category slug or ID
- `difficulty`: `easy` | `medium` | `hard`
- `max_time`: Maximum total time in minutes
- `min_rating`: Minimum rating (0-5)
- `cuisine`: Cuisine type (e.g., `Vietnamese`)
- `meal_type`: `breakfast` | `lunch` | `dinner` | `snack` | `appetizer`
- `tags`: Comma-separated tags
- `is_vegetarian`: `true` | `false`
- `is_vegan`: `true` | `false`
- `is_gluten_free`: `true` | `false`
- `sort`: `created_at` | `rating` | `views` | `cooked_count` (default: `created_at`)
- `order`: `asc` | `desc` (default: `desc`)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "recipes": [
      {
        "id": "uuid",
        "title_vi": "Phở Bò Hà Nội",
        "title_en": "Hanoi Beef Pho",
        "slug": "pho-bo-ha-noi",
        "description_vi": "Món phở bò truyền thống...",
        "image_url": "https://...",
        "author": {
          "id": "uuid",
          "display_name": "Chef A",
          "avatar_url": "https://..."
        },
        "category": {
          "id": "uuid",
          "name_vi": "Món Việt",
          "slug": "vietnamese"
        },
        "prep_time_minutes": 30,
        "cook_time_minutes": 720,
        "total_time_minutes": 750,
        "servings": 4,
        "difficulty": "hard",
        "rating_average": 4.8,
        "rating_count": 234,
        "view_count": 15678,
        "favorite_count": 892,
        "cooked_count": 456,
        "is_featured": true,
        "created_at": "2025-01-15T10:30:00Z"
      }
      // ... more recipes
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "pages": 8
    },
    "filters_applied": {
      "category": "vietnamese",
      "difficulty": "medium"
    }
  }
}
```

---

### GET /recipes/{recipe_id}
Get recipe details by ID.

**Path Parameters:**
- `recipe_id`: Recipe UUID or slug

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title_vi": "Phở Bò Hà Nội",
    "title_en": "Hanoi Beef Pho",
    "slug": "pho-bo-ha-noi",
    "description_vi": "Món phở bò truyền thống...",
    "description_en": "Traditional Hanoi beef pho...",
    "author": {
      "id": "uuid",
      "display_name": "Chef A",
      "avatar_url": "https://..."
    },
    "category": {
      "id": "uuid",
      "name_vi": "Món Việt",
      "name_en": "Vietnamese"
    },
    "image_url": "https://...",
    "video_url": "https://...",
    "prep_time_minutes": 30,
    "cook_time_minutes": 720,
    "total_time_minutes": 750,
    "servings": 4,
    "difficulty": "hard",
    "cuisine": "Vietnamese",
    "meal_type": ["lunch", "dinner"],
    "tags": ["traditional", "comfort-food", "noodles", "soup"],
    "is_vegetarian": false,
    "is_vegan": false,
    "is_gluten_free": true,
    "allergens": [],
    "ingredients": [
      {
        "id": "uuid",
        "name_vi": "Xương bò",
        "name_en": "Beef bones",
        "quantity": 1,
        "unit": "kg",
        "image_url": "https://..."
      }
      // ... more ingredients
    ],
    "steps": [
      {
        "step_number": 1,
        "title_vi": "Chuẩn bị nguyên liệu",
        "title_en": "Prepare ingredients",
        "instruction_vi": "Rửa sạch xương bò...",
        "instruction_en": "Clean beef bones...",
        "image_url": "https://...",
        "video_url": null,
        "duration_minutes": 30,
        "timer": {
          "label_vi": "Ngâm xương",
          "label_en": "Soaking bones",
          "seconds": 1800,
          "alert_sound": "gentle_bell"
        },
        "tips": "Việc ngâm xương giúp nước dùng trong hơn..."
      }
      // ... more steps
    ],
    "nutrition_facts": {
      "serving_size": "1 tô",
      "calories": 450,
      "protein_g": 35,
      "carbs_g": 58,
      "fat_g": 8,
      "fiber_g": 3,
      "sugar_g": 5,
      "sodium_mg": 1800,
      "vitamins": {
        "vitamin_a_mcg": 120,
        "vitamin_c_mg": 15,
        "calcium_mg": 60,
        "iron_mg": 4.5
      }
    },
    "rating_average": 4.8,
    "rating_count": 234,
    "view_count": 15678,
    "favorite_count": 892,
    "cooked_count": 456,
    "share_count": 123,
    "is_featured": true,
    "is_published": true,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-20T14:00:00Z"
  }
}
```

**Errors:**
- `404`: Recipe not found

---

### POST /recipes
Create a new recipe.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title_vi": "Phở Bò Hà Nội",
  "title_en": "Hanoi Beef Pho",
  "description_vi": "Món phở bò truyền thống...",
  "description_en": "Traditional Hanoi beef pho...",
  "category_id": "uuid",
  "image_url": "https://...",
  "video_url": "https://...",
  "prep_time_minutes": 30,
  "cook_time_minutes": 720,
  "servings": 4,
  "difficulty": "hard",
  "cuisine": "Vietnamese",
  "meal_type": ["lunch", "dinner"],
  "tags": ["traditional", "comfort-food"],
  "is_vegetarian": false,
  "is_vegan": false,
  "is_gluten_free": true,
  "allergens": [],
  "ingredients": [
    {
      "ingredient_id": "uuid",
      "quantity": 1,
      "unit": "kg",
      "notes": "Fresh beef bones"
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "title_vi": "Chuẩn bị nguyên liệu",
      "title_en": "Prepare ingredients",
      "instruction_vi": "Rửa sạch xương bò...",
      "instruction_en": "Clean beef bones...",
      "duration_minutes": 30,
      "timer_seconds": 1800,
      "timer_label_vi": "Ngâm xương",
      "timer_label_en": "Soaking bones"
    }
  ],
  "nutrition_facts": {
    "calories": 450,
    "protein_g": 35,
    "carbs_g": 58,
    "fat_g": 8
  }
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "slug": "pho-bo-ha-noi",
    /* ... full recipe object ... */
  }
}
```

**Errors:**
- `401`: Unauthorized
- `422`: Validation error

---

### PATCH /recipes/{recipe_id}
Update recipe.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `recipe_id`: Recipe UUID

**Request Body:** (Same as POST, all fields optional)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": { /* updated recipe */ }
}
```

**Errors:**
- `401`: Unauthorized
- `403`: Not recipe owner
- `404`: Recipe not found

---

### DELETE /recipes/{recipe_id}
Delete recipe.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Recipe deleted successfully"
}
```

**Errors:**
- `401`: Unauthorized
- `403`: Not recipe owner
- `404`: Recipe not found

---

### POST /recipes/{recipe_id}/favorite
Add recipe to favorites.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "notes": "Món ăn yêu thích của gia đình"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "favorite_id": "uuid",
    "recipe_id": "uuid",
    "notes": "Món ăn yêu thích của gia đình",
    "created_at": "2025-11-25T10:30:00Z"
  }
}
```

---

### DELETE /recipes/{recipe_id}/favorite
Remove recipe from favorites.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Removed from favorites"
}
```

---

### POST /recipes/{recipe_id}/rating
Rate and review a recipe.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "rating": 5,
  "review": "Công thức rất chi tiết và dễ làm theo!",
  "is_verified_cook": true
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "rating_id": "uuid",
    "recipe_id": "uuid",
    "rating": 5,
    "review": "...",
    "helpful_count": 0,
    "created_at": "2025-11-25T10:30:00Z"
  }
}
```

---

### POST /recipes/{recipe_id}/comment
Add comment to recipe.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "content": "Cho hỏi nếu không có xương bò...",
  "parent_id": null
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "comment_id": "uuid",
    "content": "...",
    "author": {
      "id": "uuid",
      "display_name": "Chef A",
      "avatar_url": "https://..."
    },
    "parent_id": null,
    "helpful_count": 0,
    "created_at": "2025-11-25T10:30:00Z"
  }
}
```

---

### GET /recipes/{recipe_id}/comments
Get recipe comments.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `sort`: `created_at` | `helpful` (default: `created_at`)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "comments": [
      {
        "comment_id": "uuid",
        "content": "...",
        "author": { /* ... */ },
        "parent_id": null,
        "replies": [
          {
            "comment_id": "uuid",
            "content": "...",
            "author": { /* ... */ },
            "created_at": "..."
          }
        ],
        "helpful_count": 15,
        "created_at": "2025-11-25T10:30:00Z"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

---

## 🥕 Ingredients

### GET /ingredients
List all ingredients.

**Query Parameters:**
- `page`: Page number
- `limit`: Items per page
- `search`: Search query
- `category`: Filter by category
- `is_vegetarian`: Filter vegetarian
- `is_vegan`: Filter vegan
- `is_gluten_free`: Filter gluten-free

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "ingredients": [
      {
        "id": "uuid",
        "name_vi": "Xương bò",
        "name_en": "Beef bones",
        "slug": "beef-bones",
        "category": "meat",
        "image_url": "https://...",
        "calories": 150,
        "protein_g": 20,
        "is_vegetarian": false,
        "allergens": []
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

---

### GET /ingredients/{ingredient_id}
Get ingredient details.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name_vi": "Xương bò",
    "name_en": "Beef bones",
    "slug": "beef-bones",
    "aliases_vi": ["xương hầm", "xương ống"],
    "aliases_en": ["marrow bones"],
    "category": "meat",
    "image_url": "https://...",
    "calories": 150,
    "protein_g": 20,
    "carbs_g": 0,
    "fat_g": 8,
    "fiber_g": 0,
    "is_vegetarian": false,
    "is_vegan": false,
    "is_gluten_free": true,
    "allergens": []
  }
}
```

---

## 📂 Categories

### GET /categories
List all categories.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "id": "uuid",
        "name_vi": "Món chính",
        "name_en": "Main Dishes",
        "slug": "main-dishes",
        "description_vi": "...",
        "icon_url": "https://...",
        "image_url": "https://...",
        "color_hex": "#FF6F00",
        "recipe_count": 245,
        "sort_order": 1
      }
    ]
  }
}
```

---

### GET /categories/{category_id}/recipes
Get recipes in category.

**Query Parameters:** Same as `/recipes`

**Response:** Same as `/recipes`

---

## 👨‍🍳 Cooking Sessions

### POST /cooking-sessions
Start a new cooking session.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "recipe_id": "uuid",
  "servings_adjusted": 4
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "recipe_id": "uuid",
    "status": "in_progress",
    "current_step": 1,
    "servings_adjusted": 4,
    "started_at": "2025-11-25T10:30:00Z"
  }
}
```

---

### GET /cooking-sessions/{session_id}
Get cooking session details.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "recipe": { /* recipe summary */ },
    "status": "in_progress",
    "current_step": 3,
    "servings_adjusted": 4,
    "session_data": {
      "completed_steps": [1, 2],
      "active_timers": [
        {
          "timer_id": "uuid",
          "step_number": 3,
          "label": "Hầm nước phở",
          "total_seconds": 43200,
          "remaining_seconds": 21600,
          "started_at": "2025-11-25T08:00:00Z"
        }
      ],
      "notes": "Đã tăng lượng xương thêm 200g",
      "modifications": [],
      "ingredient_substitutions": []
    },
    "started_at": "2025-11-25T06:00:00Z"
  }
}
```

---

### PATCH /cooking-sessions/{session_id}
Update cooking session.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "current_step": 4,
  "completed_steps": [1, 2, 3],
  "notes": "Additional notes...",
  "modifications": [
    {
      "step": 3,
      "change": "Increased cooking time"
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": { /* updated session */ }
}
```

---

### POST /cooking-sessions/{session_id}/complete
Complete cooking session.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "rating": 5,
  "notes": "Rất ngon!"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "status": "completed",
    "completed_at": "2025-11-25T14:30:00Z",
    "total_cooking_time_seconds": 28800
  }
}
```

---

### POST /cooking-sessions/{session_id}/timers
Start a timer for a step.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "step_number": 3,
  "label_vi": "Hầm nước phở",
  "label_en": "Simmering broth",
  "total_seconds": 43200,
  "alert_sound": "cooking_bell"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "timer_id": "uuid",
    "step_number": 3,
    "label_vi": "Hầm nước phở",
    "total_seconds": 43200,
    "remaining_seconds": 43200,
    "status": "running",
    "started_at": "2025-11-25T08:00:00Z"
  }
}
```

---

### GET /cooking-sessions/{session_id}/timers/{timer_id}
Get timer status.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "timer_id": "uuid",
    "remaining_seconds": 21600,
    "status": "running",
    "started_at": "2025-11-25T08:00:00Z"
  }
}
```

---

### POST /cooking-sessions/{session_id}/timers/{timer_id}/pause
Pause timer.

**Response:** `200 OK`

---

### POST /cooking-sessions/{session_id}/timers/{timer_id}/resume
Resume timer.

**Response:** `200 OK`

---

### DELETE /cooking-sessions/{session_id}/timers/{timer_id}
Cancel timer.

**Response:** `200 OK`

---

## 🤖 AI Chat

### POST /chat/conversations
Create a new chat conversation.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "context_type": "recipe",
  "context_id": "uuid",
  "title": "Hỏi về món phở"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "conversation_id": "uuid",
    "title": "Hỏi về món phở",
    "context_type": "recipe",
    "context_id": "uuid",
    "created_at": "2025-11-25T10:30:00Z"
  }
}
```

---

### GET /chat/conversations
List user's conversations.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page`: Page number
- `limit`: Items per page

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "conversation_id": "uuid",
        "title": "Hỏi về món phở",
        "context_type": "recipe",
        "last_message": {
          "content": "Chắc chắn rồi! Bạn có thể...",
          "created_at": "2025-11-25T14:30:00Z"
        },
        "message_count": 4,
        "created_at": "2025-11-25T10:30:00Z"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

---

### POST /chat/conversations/{conversation_id}/messages
Send a message to AI.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "content": "Tôi có thể dùng nồi áp suất để hầm xương phở được không?",
  "voice_input": false,
  "wake_word_triggered": false
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_message": {
      "message_id": "uuid",
      "role": "user",
      "content": "...",
      "created_at": "2025-11-25T14:30:00Z"
    },
    "assistant_message": {
      "message_id": "uuid",
      "role": "assistant",
      "content": "Chắc chắn rồi! Bạn có thể dùng nồi áp suất...",
      "metadata": {
        "model": "gpt-4o",
        "tokens_used": 245,
        "rag_sources": [
          {
            "type": "recipe_step",
            "recipe_id": "uuid",
            "step_number": 3,
            "similarity_score": 0.92
          }
        ],
        "response_time_ms": 1850
      },
      "created_at": "2025-11-25T14:30:02Z"
    }
  }
}
```

---

### GET /chat/conversations/{conversation_id}/messages
Get conversation messages.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page`: Page number
- `limit`: Items per page

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "message_id": "uuid",
        "role": "user",
        "content": "...",
        "created_at": "2025-11-25T14:30:00Z"
      },
      {
        "message_id": "uuid",
        "role": "assistant",
        "content": "...",
        "metadata": { /* ... */ },
        "created_at": "2025-11-25T14:30:02Z"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

---

### POST /chat/voice/transcribe
Transcribe voice to text (STT).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
audio: [audio file - mp3, wav, m4a]
language: vi
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "text": "Tôi có thể dùng nồi áp suất để hầm xương phở được không?",
    "confidence": 0.95,
    "language": "vi",
    "duration_seconds": 4.2
  }
}
```

---

### POST /chat/voice/synthesize
Synthesize text to speech (TTS).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "text": "Chắc chắn rồi! Bạn có thể dùng nồi áp suất...",
  "language": "vi",
  "voice": "vi-VN-Wavenet-A"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "audio_url": "https://storage.cooking.app/tts/audio_uuid.mp3",
    "duration_seconds": 12.5
  }
}
```

---

## 🔍 Search

### GET /search/recipes
Search recipes with full-text and semantic search.

**Query Parameters:**
- `q`: Search query (required)
- `page`: Page number
- `limit`: Items per page
- Plus all filters from `/recipes`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "query": "món phở bò",
    "recipes": [ /* ... */ ],
    "pagination": { /* ... */ },
    "search_metadata": {
      "search_type": "hybrid",
      "full_text_matches": 45,
      "semantic_matches": 12,
      "search_time_ms": 125
    }
  }
}
```

---

### GET /search/ingredients
Search ingredients.

**Query Parameters:**
- `q`: Search query

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "ingredients": [ /* ... */ ]
  }
}
```

---

### GET /search/suggestions
Get search suggestions (autocomplete).

**Query Parameters:**
- `q`: Partial search query
- `limit`: Max suggestions (default: 10)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "suggestions": [
      {
        "text": "món phở bò",
        "type": "recipe",
        "count": 45
      },
      {
        "text": "phở gà",
        "type": "recipe",
        "count": 23
      }
    ]
  }
}
```

---

### GET /search/trending
Get trending keywords.

**Query Parameters:**
- `language`: `vi` | `en`
- `limit`: Max items (default: 10)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "keywords": [
      {
        "keyword": "phở",
        "search_count": 1245,
        "trend_score": 0.95
      }
    ]
  }
}
```

---

## ❤️ Social Features

### GET /users/me/favorites
Get user's favorite recipes.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page`: Page number
- `limit`: Items per page

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "favorites": [
      {
        "favorite_id": "uuid",
        "recipe": { /* recipe summary */ },
        "notes": "Món ăn yêu thích...",
        "created_at": "2025-11-25T10:30:00Z"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

---

### GET /users/me/cooking-history
Get user's cooking history.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "session_id": "uuid",
        "recipe": { /* recipe summary */ },
        "status": "completed",
        "rating_given": 5,
        "started_at": "2025-11-24T10:00:00Z",
        "completed_at": "2025-11-24T18:30:00Z"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

---

### GET /users/me/recipe-lists
Get user's recipe lists/collections.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "lists": [
      {
        "list_id": "uuid",
        "name": "Món ăn cuối tuần",
        "description": "...",
        "recipe_count": 12,
        "is_public": true,
        "created_at": "2025-11-25T10:30:00Z"
      }
    ]
  }
}
```

---

### POST /recipe-lists
Create a new recipe list.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Món ăn cuối tuần",
  "description": "Các món ăn yêu thích nấu vào cuối tuần",
  "is_public": true
}
```

**Response:** `201 Created`

---

### POST /recipe-lists/{list_id}/recipes
Add recipe to list.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "recipe_id": "uuid"
}
```

**Response:** `200 OK`

---

## 📊 Analytics

### POST /analytics/events
Track user events.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "event_type": "recipe_view",
  "target_id": "uuid",
  "metadata": {
    "source": "search",
    "time_spent_seconds": 245
  }
}
```

**Response:** `200 OK`

**Event Types:**
- `recipe_view`
- `recipe_favorite`
- `recipe_share`
- `cooking_start`
- `cooking_complete`
- `search`
- `chat_message`

---

### GET /analytics/dashboard
Get user analytics dashboard (admin only).

**Headers:**
```
Authorization: Bearer {admin_access_token}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "total_users": 10500,
    "active_users_7d": 3450,
    "total_recipes": 2345,
    "total_cooking_sessions": 45678,
    "top_recipes": [ /* ... */ ],
    "trending_searches": [ /* ... */ ]
  }
}
```

---

## ⚠️ Error Handling

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### Standard HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created
- `204 No Content`: Successful with no response body
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate)
- `413 Payload Too Large`: File/request too large
- `415 Unsupported Media Type`: Invalid file type
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

### Error Codes

```
AUTH_001: Invalid credentials
AUTH_002: Token expired
AUTH_003: Account not verified
AUTH_004: Account disabled

USER_001: User not found
USER_002: Email already exists
USER_003: Invalid user data

RECIPE_001: Recipe not found
RECIPE_002: Unauthorized to modify recipe
RECIPE_003: Invalid recipe data

RATE_LIMIT_001: Too many requests
RATE_LIMIT_002: API quota exceeded

SERVER_001: Internal server error
SERVER_002: Database error
SERVER_003: External service error
```

---

## 🚦 Rate Limiting

### Rate Limits by Endpoint Type

| Endpoint Type | Authenticated | Anonymous |
|--------------|---------------|-----------|
| Read (GET) | 1000/hour | 100/hour |
| Write (POST/PATCH) | 200/hour | 20/hour |
| Delete | 100/hour | N/A |
| Chat/AI | 100/hour | N/A |
| Search | 500/hour | 50/hour |
| Upload | 50/hour | N/A |

### Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1700000000
```

### Rate Limit Error Response

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_001",
    "message": "Rate limit exceeded. Try again in 15 minutes.",
    "details": {
      "limit": 1000,
      "reset_at": "2025-11-25T15:00:00Z"
    }
  }
}
```

---

## 🔐 Authentication

### Bearer Token

All authenticated endpoints require:

```
Authorization: Bearer {access_token}
```

### Token Expiration

- Access token: 1 hour
- Refresh token: 30 days

### Token Refresh Flow

1. Call `/auth/refresh` with refresh token
2. Get new access token + refresh token
3. Update stored tokens
4. Retry original request

---

## 📱 API Versioning

Current version: `v1`

Base URL: `https://api.cooking.app/v1`

Version included in URL path for clear version management.

---

## 🌍 Internationalization

### Language Header

```
Accept-Language: vi-VN
```

Supported: `vi-VN`, `en-US`

### Response Format

All text fields have both Vietnamese and English:
- `title_vi` / `title_en`
- `description_vi` / `description_en`
- `name_vi` / `name_en`

Client displays based on user's language preference.

---

## 📄 Pagination

Standard pagination format:

```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

**Total Endpoints**: 60+ endpoints covering all features

**Next Steps**:
- ✅ API Endpoints Specification completed
- ⏳ RAG Pipeline Architecture (next)
- ⏳ Authentication & Authorization details
- ⏳ Caching Strategy
