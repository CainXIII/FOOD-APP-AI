"""
Generate analytics data: search queries, trending keywords, user activities
"""
import json
import random
from datetime import datetime, timedelta

# Load existing data
with open("data/recipes_full.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)["recipes"]

with open("data/users_full.json", "r", encoding="utf-8") as f:
    users = json.load(f)["users"]

BASE_TIME = datetime(2025, 1, 1, 0, 0, 0)

def gen_uuid(prefix):
    import uuid
    base = str(uuid.uuid4())
    return f"{prefix}{base[8:]}"

def gen_timestamp(days_ago=0, hours_ago=0):
    dt = BASE_TIME - timedelta(days=days_ago, hours=hours_ago)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

recipe_ids = [r["id"] for r in recipes]
user_ids = [u["id"] for u in users]

print("="*70)
print(" Generating Analytics Data")
print("="*70)
print()

# ============================================================================
# 1. SEARCH QUERIES (50 queries)
# ============================================================================
print("1. Generating search queries...")

search_keywords = [
    "phở bò", "bún chả", "cơm tấm", "bánh mì", "gỏi cuốn",
    "món chay", "món ăn sáng", "món nhanh", "healthy",
    "cách nấu phở", "công thức bánh xèo", "làm bún bò huế",
    "món ăn truyền thống", "món Việt Nam", "món nướng",
    "cơm chiên", "canh chua", "thịt kho", "cá kho tộ",
    "món tráng miệng", "chè", "sinh tố", "đồ uống",
    "món cho trẻ em", "meal prep", "ăn kiêng", "low carb",
    "món ngon", "dễ làm", "30 phút", "nồi áp suất",
]

search_queries = []
for i in range(50):
    query_text = random.choice(search_keywords)
    
    query = {
        "id": gen_uuid("f50e8400"),
        "user_id": random.choice(user_ids + [None]),  # Some anonymous searches
        "query_text": query_text,
        "filters": random.choice([
            {},
            {"difficulty": "easy"},
            {"max_time": 30},
            {"category": "vietnamese"},
            {"dietary": ["vegetarian"]},
            {"difficulty": "easy", "max_time": 45}
        ]),
        "results_count": random.randint(5, 50),
        "clicked_recipe_ids": random.sample(recipe_ids, random.randint(1, 3)),
        "created_at": gen_timestamp(days_ago=random.randint(1, 90))
    }
    search_queries.append(query)

print(f"   ✅ Created {len(search_queries)} search queries")

# ============================================================================
# 2. TRENDING KEYWORDS (30 keywords)
# ============================================================================
print("2. Generating trending keywords...")

trending_data = [
    ("phở", "vi", 0.95),
    ("phở bò", "vi", 0.92),
    ("bún chả", "vi", 0.88),
    ("cơm tấm", "vi", 0.85),
    ("bánh mì", "vi", 0.83),
    ("gỏi cuốn", "vi", 0.80),
    ("món chay", "vi", 0.78),
    ("healthy recipes", "en", 0.75),
    ("quick meals", "en", 0.72),
    ("vietnamese food", "en", 0.70),
    ("bánh xèo", "vi", 0.68),
    ("bún bò huế", "vi", 0.65),
    ("cơm chiên", "vi", 0.63),
    ("canh chua", "vi", 0.60),
    ("thịt kho", "vi", 0.58),
    ("món nướng", "vi", 0.55),
    ("breakfast", "en", 0.52),
    ("desserts", "en", 0.50),
    ("vegetarian", "en", 0.48),
    ("meal prep", "en", 0.45),
    ("30 minutes", "en", 0.43),
    ("easy cooking", "en", 0.40),
    ("chè", "vi", 0.38),
    ("bánh", "vi", 0.35),
    ("lẩu", "vi", 0.33),
    ("món hầm", "vi", 0.30),
    ("cá kho", "vi", 0.28),
    ("gà nướng", "vi", 0.25),
    ("salad", "vi", 0.22),
    ("sinh tố", "vi", 0.20),
]

trending_keywords = []
for keyword, lang, score in trending_data:
    trending = {
        "id": gen_uuid("g50e8400"),
        "keyword": keyword,
        "search_count": int(score * 1000),
        "language": lang,
        "trend_score": score,
        "period_start": gen_timestamp(days_ago=30),
        "period_end": gen_timestamp(days_ago=0),
        "created_at": gen_timestamp(days_ago=30),
        "updated_at": gen_timestamp(days_ago=0)
    }
    trending_keywords.append(trending)

print(f"   ✅ Created {len(trending_keywords)} trending keywords")

# ============================================================================
# 3. USER ACTIVITIES (200 activities)
# ============================================================================
print("3. Generating user activities...")

activity_types = [
    "recipe_view",
    "recipe_favorite",
    "recipe_unfavorite",
    "cooking_start",
    "cooking_complete",
    "recipe_rating",
    "chat_message",
    "recipe_share",
    "search",
    "comment",
]

user_activities = []
for i in range(200):
    activity_type = random.choice(activity_types)
    user_id = random.choice(user_ids)
    
    # Generate appropriate target_id based on activity type
    if activity_type in ["recipe_view", "recipe_favorite", "recipe_unfavorite", "recipe_rating", "recipe_share"]:
        target_id = random.choice(recipe_ids)
        metadata = {"recipe_title": random.choice([r["title_vi"] for r in recipes[:10]])}
    elif activity_type in ["cooking_start", "cooking_complete"]:
        target_id = random.choice(recipe_ids)
        metadata = {"duration_minutes": random.randint(30, 180)}
    elif activity_type == "chat_message":
        target_id = gen_uuid("d50e8400")
        metadata = {"message_length": random.randint(10, 200)}
    elif activity_type == "search":
        target_id = None
        metadata = {"query": random.choice(search_keywords), "results": random.randint(5, 50)}
    elif activity_type == "comment":
        target_id = random.choice(recipe_ids)
        metadata = {"comment_length": random.randint(20, 300)}
    else:
        target_id = None
        metadata = {}
    
    activity = {
        "id": gen_uuid("h50e8400"),
        "user_id": user_id,
        "activity_type": activity_type,
        "target_id": target_id,
        "metadata": metadata,
        "ip_address": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "created_at": gen_timestamp(days_ago=random.randint(1, 180))
    }
    user_activities.append(activity)

# Sort by timestamp
user_activities.sort(key=lambda x: x["created_at"], reverse=True)

print(f"   ✅ Created {len(user_activities)} user activities")

# ============================================================================
# Save files
# ============================================================================
print()
print("="*70)
print(" Saving files...")
print("="*70)

with open("data/search-queries_full.json", "w", encoding="utf-8") as f:
    json.dump({"search_queries": search_queries}, f, ensure_ascii=False, indent=2)
print("✅ Saved search-queries_full.json")

with open("data/trending-keywords_full.json", "w", encoding="utf-8") as f:
    json.dump({"trending_keywords": trending_keywords}, f, ensure_ascii=False, indent=2)
print("✅ Saved trending-keywords_full.json")

with open("data/user-activity_full.json", "w", encoding="utf-8") as f:
    json.dump({"user_activities": user_activities}, f, ensure_ascii=False, indent=2)
print("✅ Saved user-activity_full.json")

print()
print(f"Total: {len(search_queries)} searches + {len(trending_keywords)} keywords + {len(user_activities)} activities")
print()
print("="*70)
print(" 🎉 ALL DATA GENERATION COMPLETE!")
print("="*70)
