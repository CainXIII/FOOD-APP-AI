"""
Generate cooking data: sessions and timers
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

def gen_timestamp(days_ago=0, hours_ago=0, minutes_ago=0):
    dt = BASE_TIME - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

recipe_ids = [r["id"] for r in recipes]
user_ids = [u["id"] for u in users]

print("="*70)
print(" Generating Cooking Data")
print("="*70)
print()

# ============================================================================
# 1. COOKING SESSIONS (30 sessions)
# ============================================================================
print("1. Generating cooking sessions...")

session_statuses = ["completed", "completed", "completed", "in_progress", "paused", "abandoned"]

cooking_sessions = []
for i in range(30):
    recipe = random.choice(recipes)
    status = random.choice(session_statuses)
    total_steps = len(recipe["steps"])
    
    if status == "completed":
        current_step = total_steps
        completed_steps = list(range(1, total_steps + 1))
    elif status == "in_progress":
        current_step = random.randint(1, total_steps - 1)
        completed_steps = list(range(1, current_step))
    else:
        current_step = random.randint(1, total_steps)
        completed_steps = list(range(1, current_step))
    
    session = {
        "id": gen_uuid("b50e8400"),
        "user_id": random.choice(user_ids),
        "recipe_id": recipe["id"],
        "status": status,
        "current_step": current_step,
        "total_steps": total_steps,
        "servings_adjusted": recipe["servings"] + random.choice([-1, 0, 0, 0, 1, 2]),
        "completed_steps": completed_steps,
        "active_timers": [] if status == "completed" else [1, 2] if status == "in_progress" else [],
        "notes": random.choice([
            None,
            "Đã giảm muối",
            "Tăng gấp đôi khẩu phần",
            "Bỏ ớt vì trẻ em",
            "Ngon lắm!"
        ]),
        "modifications": random.choice([
            {},
            {"muối": "giảm 50%"},
            {"ớt": "bỏ"},
            {"đường": "thay bằng mật ong"}
        ]),
        "ingredient_substitutions": {},
        "rating_given": random.choice([None, 4, 5]) if status == "completed" else None,
        "started_at": gen_timestamp(days_ago=random.randint(1, 90), hours_ago=random.randint(0, 23)),
        "completed_at": gen_timestamp(days_ago=random.randint(1, 90)) if status == "completed" else None,
        "created_at": gen_timestamp(days_ago=random.randint(1, 90)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 30))
    }
    cooking_sessions.append(session)

print(f"   ✅ Created {len(cooking_sessions)} cooking sessions")

# ============================================================================
# 2. COOKING TIMERS (40 timers)
# ============================================================================
print("2. Generating cooking timers...")

timer_labels = [
    ("Hầm nước dùng", "Simmer broth"),
    ("Ướp thịt", "Marinate meat"),
    ("Nấu cơm", "Cook rice"),
    ("Luộc trứng", "Boil eggs"),
    ("Chiên giòn", "Deep fry"),
    ("Rán", "Pan fry"),
    ("Nướng", "Bake"),
    ("Hấp", "Steam"),
    ("Kho", "Braise"),
    ("Nghỉ bột", "Rest dough"),
]

timer_statuses = ["completed", "completed", "completed", "running", "paused", "cancelled"]

cooking_timers = []
for i in range(40):
    session_id = random.choice([s["id"] for s in cooking_sessions])
    label_vi, label_en = random.choice(timer_labels)
    status = random.choice(timer_statuses)
    total_seconds = random.choice([300, 600, 900, 1200, 1800, 3600, 7200])  # 5min to 2hrs
    
    if status == "completed":
        remaining_seconds = 0
    elif status == "running":
        remaining_seconds = random.randint(60, total_seconds - 60)
    else:
        remaining_seconds = random.randint(0, total_seconds)
    
    timer = {
        "id": gen_uuid("c50e8400"),
        "cooking_session_id": session_id,
        "step_number": random.randint(1, 5),
        "label_vi": label_vi,
        "label_en": label_en,
        "total_seconds": total_seconds,
        "remaining_seconds": remaining_seconds,
        "status": status,
        "alert_sound": random.choice(["bell", "chime", "beep"]),
        "started_at": gen_timestamp(days_ago=random.randint(1, 60), hours_ago=random.randint(0, 23)),
        "completed_at": gen_timestamp(days_ago=random.randint(1, 60)) if status == "completed" else None,
        "created_at": gen_timestamp(days_ago=random.randint(1, 60)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 10))
    }
    cooking_timers.append(timer)

print(f"   ✅ Created {len(cooking_timers)} cooking timers")

# ============================================================================
# Save files
# ============================================================================
print()
print("="*70)
print(" Saving files...")
print("="*70)

with open("data/cooking-sessions_full.json", "w", encoding="utf-8") as f:
    json.dump({"cooking_sessions": cooking_sessions}, f, ensure_ascii=False, indent=2)
print("✅ Saved cooking-sessions_full.json")

with open("data/cooking-timers_full.json", "w", encoding="utf-8") as f:
    json.dump({"cooking_timers": cooking_timers}, f, ensure_ascii=False, indent=2)
print("✅ Saved cooking-timers_full.json")

print()
print(f"Total: {len(cooking_sessions)} sessions + {len(cooking_timers)} timers")
