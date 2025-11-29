"""
Generate social data: ratings, favorites, comments, recipe lists
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
print(" Generating Social Data")
print("="*70)
print()

# ============================================================================
# 1. RATINGS (100 ratings)
# ============================================================================
print("1. Generating ratings...")

rating_comments_vi = [
    "Món này rất ngon! Gia đình tôi rất thích.",
    "Công thức dễ làm, phù hợp cho người mới học nấu ăn.",
    "Nước dùng thơm ngon, đúng vị truyền thống.",
    "Đã làm theo và rất thành công, cảm ơn!",
    "Món ăn ngon nhưng hơi mất thời gian.",
    "Rất tuyệt vời! Sẽ làm lại nhiều lần.",
    "Vị hơi nhạt, tôi đã tăng gia vị thêm.",
    "Công thức chi tiết, dễ hiểu.",
    "Món này ổn nhưng chưa đặc sắc lắm.",
    "Tuyệt vời! Ngon hơn ngoài hàng.",
]

ratings = []
for i in range(100):
    rating = {
        "id": gen_uuid("950e8400"),
        "recipe_id": random.choice(recipe_ids),
        "user_id": random.choice(user_ids),
        "rating": random.choice([3, 4, 4, 4, 5, 5, 5]),  # Biased toward high ratings
        "review": random.choice(rating_comments_vi) if random.random() > 0.3 else None,
        "images": [f"https://storage.cooking.app/reviews/{gen_uuid('img')}.jpg"] if random.random() > 0.8 else [],
        "helpful_count": random.randint(0, 25),
        "is_verified_cook": random.random() > 0.5,
        "created_at": gen_timestamp(days_ago=random.randint(1, 180)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 30))
    }
    ratings.append(rating)

print(f"   ✅ Created {len(ratings)} ratings")

# ============================================================================
# 2. FAVORITES (60 favorites)
# ============================================================================
print("2. Generating favorites...")

favorites = []
for i in range(60):
    favorite = {
        "id": gen_uuid("a50e8400"),
        "user_id": random.choice(user_ids),
        "recipe_id": random.choice(recipe_ids),
        "notes": random.choice([None, "Làm cho bữa tối cuối tuần", "Món ưa thích của gia đình", "Dễ làm"]),
        "created_at": gen_timestamp(days_ago=random.randint(1, 180))
    }
    favorites.append(favorite)

print(f"   ✅ Created {len(favorites)} favorites")

# ============================================================================
# 3. COMMENTS (80 comments with threading)
# ============================================================================
print("3. Generating comments...")

comment_texts = [
    "Cảm ơn công thức tuyệt vời này!",
    "Tôi có thể thay thế nguyên liệu X bằng Y được không?",
    "Món này có thể làm bằng nồi áp suất không?",
    "Rất chi tiết và dễ hiểu!",
    "Đã làm thành công, gia đình rất thích!",
    "Bước 3 hơi khó, có thể giải thích rõ hơn không?",
    "Tuyệt vời! Cảm ơn bạn đã chia sẻ.",
    "Có thể giảm lượng đường được không?",
    "Món này phù hợp cho trẻ em không?",
    "Đã bookmark để làm sau!",
]

comments = []
parent_comments = []

# Create 50 parent comments
for i in range(50):
    comment = {
        "id": gen_uuid("j50e8400"),
        "recipe_id": random.choice(recipe_ids),
        "user_id": random.choice(user_ids),
        "parent_id": None,
        "content": random.choice(comment_texts),
        "helpful_count": random.randint(0, 15),
        "created_at": gen_timestamp(days_ago=random.randint(1, 180)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 30))
    }
    comments.append(comment)
    parent_comments.append(comment)

# Create 30 reply comments
reply_texts = [
    "Cảm ơn bạn! Rất vui vì món ăn phù hợp với bạn.",
    "Có thể thay thế được, nhưng vị sẽ khác một chút.",
    "Được đấy, thời gian nấu sẽ giảm xuống.",
    "Cảm ơn bạn đã theo dõi!",
    "Bạn có thể điều chỉnh theo khẩu vị nhé.",
]

for i in range(30):
    parent = random.choice(parent_comments)
    comment = {
        "id": gen_uuid("j50e8400"),
        "recipe_id": parent["recipe_id"],
        "user_id": random.choice(user_ids),
        "parent_id": parent["id"],
        "content": random.choice(reply_texts),
        "helpful_count": random.randint(0, 5),
        "created_at": gen_timestamp(days_ago=random.randint(1, 150)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 20))
    }
    comments.append(comment)

print(f"   ✅ Created {len(comments)} comments (50 parent + 30 replies)")

# ============================================================================
# 4. RECIPE LISTS (15 curated lists)
# ============================================================================
print("4. Generating recipe lists...")

list_data = [
    ("Món ăn cuối tuần", "Các món dễ làm cho bữa ăn gia đình cuối tuần", True),
    ("Healthy & Diet", "Món ăn healthy, ít calo", True),
    ("Món nhanh 30 phút", "Các món có thể hoàn thành trong 30 phút", True),
    ("Món truyền thống Việt Nam", "Những món ăn truyền thống đặc sắc", True),
    ("Món ăn sáng yêu thích", "Bữa sáng ngon và dinh dưỡng", True),
    ("Món cho người mới học nấu ăn", "Công thức đơn giản, dễ làm", True),
    ("Món ăn chay", "Các món chay thanh đạm", True),
    ("Ăn vặt & Snacks", "Món ăn nhẹ, ăn vặt", False),
    ("Món mùa hè", "Món ăn mát lạnh cho mùa hè", True),
    ("Món đãi tiệc", "Các món ăn sang trọng cho tiệc", False),
    ("Meal Prep cho tuần", "Món có thể chuẩn bị trước", True),
    ("Món ngọt & Tráng miệng", "Các loại chè, bánh ngọt", True),
    ("Comfort Food", "Món ăn gia đình ấm cúng", True),
    ("Món nướng BBQ", "Các món nướng thơm ngon", True),
    ("Đồ uống giải khát", "Nước uống, sinh tố", True),
]

recipe_lists = []
for i, (name, desc, is_public) in enumerate(list_data):
    # Select 5-10 random recipes for each list
    selected_recipes = random.sample(recipe_ids, random.randint(5, 10))
    
    recipe_list = {
        "id": gen_uuid("i50e8400"),
        "user_id": random.choice(user_ids),
        "name": name,
        "description": desc,
        "is_public": is_public,
        "recipe_ids": selected_recipes,
        "recipe_count": len(selected_recipes),
        "follower_count": random.randint(0, 100) if is_public else 0,
        "created_at": gen_timestamp(days_ago=random.randint(1, 180)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 30))
    }
    recipe_lists.append(recipe_list)

print(f"   ✅ Created {len(recipe_lists)} recipe lists")

# ============================================================================
# Save all files
# ============================================================================
print()
print("="*70)
print(" Saving files...")
print("="*70)

with open("data/ratings_full.json", "w", encoding="utf-8") as f:
    json.dump({"ratings": ratings}, f, ensure_ascii=False, indent=2)
print("✅ Saved ratings_full.json")

with open("data/favorites_full.json", "w", encoding="utf-8") as f:
    json.dump({"favorites": favorites}, f, ensure_ascii=False, indent=2)
print("✅ Saved favorites_full.json")

with open("data/comments_full.json", "w", encoding="utf-8") as f:
    json.dump({"comments": comments}, f, ensure_ascii=False, indent=2)
print("✅ Saved comments_full.json")

with open("data/recipe-lists_full.json", "w", encoding="utf-8") as f:
    json.dump({"recipe_lists": recipe_lists}, f, ensure_ascii=False, indent=2)
print("✅ Saved recipe-lists_full.json")

print()
print(f"Total: {len(ratings)} ratings + {len(favorites)} favorites + {len(comments)} comments + {len(recipe_lists)} lists")
