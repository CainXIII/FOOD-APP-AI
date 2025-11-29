"""
Generate chat data: conversations and messages with RAG metadata
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
print(" Generating Chat Data")
print("="*70)
print()

# ============================================================================
# 1. CHATS (15 conversations)
# ============================================================================
print("1. Generating chats...")

chat_contexts = [
    ("recipe", random.choice(recipe_ids)),
    ("recipe", random.choice(recipe_ids)),
    ("recipe", random.choice(recipe_ids)),
    ("recipe", random.choice(recipe_ids)),
    ("recipe", random.choice(recipe_ids)),
    ("general", None),
    ("general", None),
    ("general", None),
    ("general", None),
    ("general", None),
    ("recipe", random.choice(recipe_ids)),
    ("recipe", random.choice(recipe_ids)),
    ("general", None),
    ("general", None),
    ("general", None),
]

chats = []
for i, (context_type, context_id) in enumerate(chat_contexts):
    if context_type == "recipe":
        recipe = next(r for r in recipes if r["id"] == context_id)
        title = f"Chat về {recipe['title_vi']}"
    else:
        title = random.choice([
            "Hỏi về công thức nấu ăn",
            "Tư vấn món ăn",
            "Thay thế nguyên liệu",
            "Mẹo nấu ăn",
            "Meal planning"
        ])
    
    chat = {
        "id": gen_uuid("d50e8400"),
        "user_id": random.choice(user_ids),
        "title": title,
        "context_type": context_type,
        "context_id": context_id,
        "message_count": random.randint(3, 10),
        "created_at": gen_timestamp(days_ago=random.randint(1, 120)),
        "updated_at": gen_timestamp(days_ago=random.randint(0, 30)),
        "last_message_at": gen_timestamp(days_ago=random.randint(0, 30))
    }
    chats.append(chat)

print(f"   ✅ Created {len(chats)} chats")

# ============================================================================
# 2. CHAT MESSAGES (80 messages with RAG metadata)
# ============================================================================
print("2. Generating chat messages...")

# Vietnamese Q&A pairs
qa_pairs = [
    ("Làm sao để nấu phở ngon?", "Để nấu phở ngon, bạn cần chú ý vào nước dùng. Hầm xương bò ít nhất 8-12 tiếng với gừng và hành nướng. Gia vị quan trọng là hạt nêm, muối, đường và nước mắm. Nước dùng cần trong và ngọt tự nhiên từ xương."),
    ("Tôi có thể thay thế thịt bò bằng gì?", "Bạn có thể thay thế thịt bò bằng thịt gà, thịt heo, hoặc đậu phụ cho món chay. Thời gian nấu sẽ khác nhau tùy loại thịt."),
    ("Món này có thể làm bằng nồi áp suất không?", "Có thể! Nồi áp suất sẽ giảm thời gian nấu xuống còn 1/3. Nhưng cần chú ý điều chỉnh lượng nước và gia vị."),
    ("Cách bảo quản món ăn thế nào?", "Để trong hộp kín, bảo quản tủ lạnh 3-5 ngày. Có thể đông lạnh 1-2 tháng. Khi hâm nóng lại, thêm chút nước để giữ độ ẩm."),
    ("Món này ăn với gì?", "Món này ăn kèm với cơm trắng, rau sống, dưa muối, và nước chấm. Có thể thêm rau thơm như húng quế, ngò rí."),
    ("Có thể giảm lượng muối không?", "Được! Bạn có thể giảm 30-50% lượng muối, rồi nêm nếm và điều chỉnh theo khẩu vị gia đình."),
    ("Món này có cay không?", "Món này có độ cay vừa phải. Bạn có thể bỏ ớt hoặc giảm lượng ớt nếu không ăn cay."),
    ("Thời gian chuẩn bị bao lâu?", "Chuẩn bị mất khoảng 20-30 phút, nấu thêm 45-60 phút. Tổng cộng khoảng 1.5 giờ."),
    ("Món này phù hợp cho trẻ em không?", "Có! Món này phù hợp cho cả gia đình. Với trẻ em, bạn có thể giảm gia vị và bỏ ớt."),
    ("Tôi cần chuẩn bị gì trước?", "Bạn nên chuẩn bị: rửa sạch rau, ướp thịt trước 30 phút, chuẩn bị gia vị, và đọc kỹ công thức."),
]

user_messages = [
    "Làm sao để nấu phở ngon?",
    "Tôi có thể thay thế thịt bò bằng gì?",
    "Món này có thể làm bằng nồi áp suất không?",
    "Cách bảo quản món ăn thế nào?",
    "Món này ăn với gì?",
    "Có thể giảm lượng muối không?",
    "Món này có cay không?",
    "Thời gian chuẩn bị bao lâu?",
    "Món này phù hợp cho trẻ em không?",
    "Tôi cần chuẩn bị gì trước?",
    "Có thể làm chay được không?",
    "Nguyên liệu nào quan trọng nhất?",
    "Mẹo để món ngon hơn?",
    "Calo của món này là bao nhiêu?",
    "Có thể tăng gấp đôi khẩu phần không?",
]

assistant_responses = [
    "Để nấu phở ngon, bạn cần chú ý vào nước dùng. Hầm xương bò ít nhất 8-12 tiếng với gừng và hành nướng.",
    "Bạn có thể thay thế thịt bò bằng thịt gà, thịt heo, hoặc đậu phụ cho món chay.",
    "Có thể! Nồi áp suất sẽ giảm thời gian nấu xuống còn 1/3.",
    "Để trong hộp kín, bảo quản tủ lạnh 3-5 ngày. Có thể đông lạnh 1-2 tháng.",
    "Món này ăn kèm với cơm trắng, rau sống, dưa muối, và nước chấm.",
    "Được! Bạn có thể giảm 30-50% lượng muối, rồi nêm nếm và điều chỉnh.",
    "Món này có độ cay vừa phải. Bạn có thể bỏ ớt hoặc giảm lượng ớt.",
    "Chuẩn bị mất khoảng 20-30 phút, nấu thêm 45-60 phút.",
    "Có! Món này phù hợp cho cả gia đình. Với trẻ em, bạn có thể giảm gia vị.",
    "Bạn nên rửa sạch rau, ướp thịt trước 30 phút, và chuẩn bị gia vị.",
]

chat_messages = []
for chat in chats:
    num_messages = chat["message_count"]
    
    for msg_idx in range(num_messages):
        # Alternate between user and assistant
        if msg_idx % 2 == 0:  # User message
            message = {
                "id": gen_uuid("e50e8400"),
                "chat_id": chat["id"],
                "role": "user",
                "content": random.choice(user_messages),
                "metadata": {
                    "voice_input": random.random() > 0.7,
                    "wake_word_triggered": False,
                    "transcription_confidence": round(random.uniform(0.85, 0.99), 2) if random.random() > 0.7 else None
                },
                "created_at": gen_timestamp(
                    days_ago=random.randint(0, 90),
                    hours_ago=random.randint(0, 23),
                    minutes_ago=msg_idx * 2
                )
            }
        else:  # Assistant message
            message = {
                "id": gen_uuid("e50e8400"),
                "chat_id": chat["id"],
                "role": "assistant",
                "content": random.choice(assistant_responses),
                "metadata": {
                    "model": "gpt-4o-mini",
                    "tokens_used": random.randint(200, 800),
                    "rag_sources": [
                        {
                            "recipe_id": random.choice(recipe_ids),
                            "title": random.choice([r["title_vi"] for r in recipes[:5]]),
                            "similarity_score": round(random.uniform(0.6, 0.9), 2)
                        }
                        for _ in range(random.randint(2, 4))
                    ],
                    "response_time_ms": random.randint(800, 3000),
                    "tts_generated": random.random() > 0.6,
                    "tts_audio_url": f"https://storage.cooking.app/tts/{gen_uuid('audio')}.mp3" if random.random() > 0.6 else None
                },
                "created_at": gen_timestamp(
                    days_ago=random.randint(0, 90),
                    hours_ago=random.randint(0, 23),
                    minutes_ago=msg_idx * 2 + 1
                )
            }
        
        chat_messages.append(message)

print(f"   ✅ Created {len(chat_messages)} chat messages")

# ============================================================================
# Save files
# ============================================================================
print()
print("="*70)
print(" Saving files...")
print("="*70)

with open("data/chats_full.json", "w", encoding="utf-8") as f:
    json.dump({"chats": chats}, f, ensure_ascii=False, indent=2)
print("✅ Saved chats_full.json")

with open("data/chat-messages_full.json", "w", encoding="utf-8") as f:
    json.dump({"chat_messages": chat_messages}, f, ensure_ascii=False, indent=2)
print("✅ Saved chat-messages_full.json")

print()
print(f"Total: {len(chats)} chats + {len(chat_messages)} messages")
