# 👤 Profile Screen - Design Specification

## Overview
Profile Screen là trung tâm quản lý tài khoản, preferences, favorites, và settings. Users có thể:
- Xem thông tin cá nhân
- Quản lý công thức đã lưu/yêu thích
- Xem lịch sử nấu ăn
- Cấu hình preferences (dietary, allergies, portion size)
- **Chọn AI Personality** (giọng điệu AI chat)
- Settings (voice, wake word, notifications, privacy)
- Đăng xuất/xóa tài khoản

---

## Visual Layout

```
┌─────────────────────────────────────┐
│                                     │
│   ┌────┐  John Doe                  │ <- Profile header
│   │👤  │  john@email.com            │    Avatar + Info
│   └────┘  [Edit Profile]            │    Edit button
│                                     │
├─────────────────────────────────────┤
│                                     │
│ 📊 Stats                            │ <- Stats cards
│ ┌─────┬─────┬─────┐                 │    3 columns
│ │ 24  │ 142 │ 8   │                 │
│ │Saved│Cooked│Lists│                 │
│ └─────┴─────┴─────┘                 │
│                                     │
├─────────────────────────────────────┤
│                                     │
│ ❤️  Công thức yêu thích      >      │ <- Menu options
│                                     │    Navigate to lists
│ 🍳 Lịch sử nấu ăn            >      │
│                                     │
│ 🥗 Preferences               >      │
│                                     │
│ ⚙️  Settings                 >      │
│                                     │
│ ❓  Help & Support           >      │
│                                     │
│ 🚪 Đăng xuất                        │
│                                     │
└─────────────────────────────────────┘
```

---

## Components Detail

### 1. Profile Header

```
┌─────────────────────────────────────┐
│  ┌─────┐                            │
│  │ 👤  │  John Doe                   │
│  │     │  john@email.com            │
│  └─────┘  Member since Jan 2024     │
│                                     │
│           [Edit Profile]            │
└─────────────────────────────────────┘
```

**Avatar:**
- Size: 80×80px circular
- Border: 2px white + shadow
- Default: Initials (JD) on orange background
- Tap: Upload new photo (camera/gallery)

**Name:**
- Font: 20px, bold
- Color: Black
- Tap: Edit name

**Email:**
- Font: 14px, regular
- Color: Gray #666
- Not editable (linked to account)

**Member Since:**
- Font: 12px, regular
- Color: Gray #999
- Format: "Member since [Month Year]"

**Edit Button:**
- Height: 40px
- Width: 120px
- Border: 1px solid orange
- Text: "Edit Profile"
- Tap: Navigate to Edit Profile screen

---

### 2. Stats Cards

```
┌─────────────────────────────────────┐
│ 📊 My Stats                         │
│                                     │
│ ┌───────┬───────┬───────┐           │
│ │  24   │  142  │   8   │           │
│ │ Saved │Cooked │ Lists │           │
│ └───────┴───────┴───────┘           │
└─────────────────────────────────────┘
```

**Container:**
- Background: White card
- Border radius: 16px
- Padding: 16px
- Shadow: Elevation 2
- Margin: 16px

**Individual Stat:**
```
┌─────────┐
│   24    │ <- Number (24px, bold, black)
│ Saved   │ <- Label (12px, regular, gray)
└─────────┘
Width: 33% each
Tap: Navigate to corresponding list
```

**Stats:**
1. **Saved:** Recipes marked as favorite (❤️)
2. **Cooked:** Recipes where user completed cooking
3. **Lists:** Custom collections (e.g., "Weeknight Dinners", "Kids Favorites")

**Tap Actions:**
- Saved → Navigate to Favorites list
- Cooked → Navigate to Cooking History
- Lists → Navigate to My Collections

---

### 3. Menu Options

#### Công thức yêu thích

```
┌─────────────────────────────────────┐
│ ❤️  Công thức yêu thích      >      │
└─────────────────────────────────────┘

Height: 56px
Background: White
Border bottom: 1px #F0F0F0
Icon: ❤️ (24×24px, red)
Text: 16px, regular, black
Chevron: > (20×20px, gray)
Tap: Navigate to Favorites screen
```

**Favorites Screen:**
- Grid of saved recipes (same as Home)
- Filter: Date added, Name, Category
- Sort: Newest/Oldest/Name
- Batch actions: Remove, Add to list

---

#### Lịch sử nấu ăn

```
┌─────────────────────────────────────┐
│ 🍳 Lịch sử nấu ăn            >      │
└─────────────────────────────────────┘

Icon: 🍳 (24×24px)
Tap: Navigate to Cooking History
```

**Cooking History Screen:**
```
┌─────────────────────────────────────┐
│ [<] Lịch sử nấu ăn                  │
├─────────────────────────────────────┤
│ Hôm nay                             │
│ ┌─────────────────────────────────┐ │
│ │ [Thumb] Phở Bò         14:30    │ │
│ │ Completed ✓            Reorder  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Hôm qua                             │
│ ┌─────────────────────────────────┐ │
│ │ [Thumb] Bún Chả        19:00    │ │
│ │ Completed ✓            Reorder  │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

Features:
- Grouped by date (Today, Yesterday, This Week, etc.)
- Recipe thumbnail + name + time
- Completion badge (✓ Completed / ⏱️ In Progress)
- "Reorder" button → Quick add to shopping list
- Stats: Total cooked, Success rate
```

---

#### Preferences

```
┌─────────────────────────────────────┐
│ 🥗 Preferences               >      │
└─────────────────────────────────────┘

Icon: 🥗 (24×24px)
Tap: Navigate to Preferences screen
```

**Preferences Screen:**
```
┌─────────────────────────────────────┐
│ [<] Preferences                     │
├─────────────────────────────────────┤
│                                     │
│ 🍽️ Dietary Restrictions             │
│ ┌─────────────────────────────────┐ │
│ │ □ Vegetarian                    │ │
│ │ □ Vegan                         │ │
│ │ □ Gluten-Free                   │ │
│ │ □ Dairy-Free                    │ │
│ │ □ Halal                         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ⚠️  Allergies                       │
│ ┌─────────────────────────────────┐ │
│ │ • Peanuts                    [×]│ │
│ │ • Shellfish                  [×]│ │
│ │ [+ Add Allergy]                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 👥 Default Servings                 │
│ ┌─────────────────────────────────┐ │
│ │ [2] servings                    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 📏 Measurement Unit                 │
│ ┌─────────────────────────────────┐ │
│ │ ○ Metric (kg, g)                │ │
│ │ ● Imperial (lb, oz)             │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🌶️ Spice Level Preference          │
│ ┌─────────────────────────────────┐ │
│ │ Mild ━━━━○━━━━ Hot              │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

Features:
- Dietary checkboxes (multi-select)
- Allergy tags (add/remove)
- Default servings (number picker 1-10)
- Unit system (metric/imperial radio)
- Spice level slider (1-5)
- Auto-filter recipes based on preferences
- Show warning when recipe conflicts with allergy
```

---

#### Settings

```
┌─────────────────────────────────────┐
│ ⚙️  Settings                 >      │
└─────────────────────────────────────┘

Icon: ⚙️ (24×24px)
Tap: Navigate to Settings screen
```

**Settings Screen:**
```
┌─────────────────────────────────────┐
│ [<] Settings                        │
├─────────────────────────────────────┤
│                                     │
│ 🤖 AI Personality                   │
│ ┌─────────────────────────────────┐ │
│ │ ● Friendly Home Cook (Default)  │ │
│ │   "Thân thiện, động viên"       │ │
│ │                                 │ │
│ │ [Change Personality]            │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🎙️ Voice & Audio                    │
│ ┌─────────────────────────────────┐ │
│ │ Voice Guidance         [ON/OFF] │ │
│ │ Voice Language         [🇻🇳 VI]  │ │
│ │ Speech Speed           [1.0x  ] │ │
│ │ Wake Word Detection    [ON/OFF] │ │
│ │   • Activation phrase: "Hey Chef"│ │
│ │   • Sensitivity: High            │ │
│ │   • Auto-disable at: 20% battery│ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🔔 Notifications                    │
│ ┌─────────────────────────────────┐ │
│ │ Recipe Suggestions     [ON/OFF] │ │
│ │ Cooking Reminders      [ON/OFF] │ │
│ │ Timer Alerts           [ON/OFF] │ │
│ │ New Features           [ON/OFF] │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🌐 Language & Region                │
│ ┌─────────────────────────────────┐ │
│ │ App Language           [🇻🇳 VI]  │ │
│ │ Recipe Language        [🇻🇳 VI]  │ │
│ │ Region                 [Vietnam]│ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🔒 Privacy & Security               │
│ ┌─────────────────────────────────┐ │
│ │ On-device Processing   [ON/OFF] │ │
│ │ Save Search History    [ON/OFF] │ │
│ │ Usage Analytics        [ON/OFF] │ │
│ │ Change Password             >   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 💾 Data Management                  │
│ ┌─────────────────────────────────┐ │
│ │ Clear Cache            [48 MB]  │ │
│ │ Export My Data              >   │ │
│ │ Delete Account              >   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ℹ️ About                            │
│ ┌─────────────────────────────────┐ │
│ │ Version                1.0.0    │ │
│ │ Privacy Policy              >   │ │
│ │ Terms of Service            >   │ │
│ │ Open Source Licenses        >   │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 🤖 AI Personality Feature (NEW)

### Overview
Cho phép users tùy chỉnh giọng điệu và phong cách giao tiếp của AI chatbot để phù hợp với sở thích cá nhân.

---

### AI Personality Selection Screen

```
┌─────────────────────────────────────┐
│ [<] AI Personality                  │
├─────────────────────────────────────┤
│ Chọn phong cách AI phù hợp với bạn: │
│                                     │
│ ○ 👨‍🍳 Professional Chef             │
│   Chuyên nghiệp, chi tiết kỹ thuật │
│   [Preview]                         │
│                                     │
│ ● 🏠 Friendly Home Cook (Default)   │
│   Thân thiện, gần gũi, động viên   │
│   [Preview]                         │
│                                     │
│ ○ 😄 Humorous Foodie                │
│   Vui vẻ, hài hước, nhiều emoji    │
│   [Preview]                         │
│                                     │
│ ○ 🥗 Nutritionist                   │
│   Tập trung dinh dưỡng, sức khỏe   │
│   [Preview]                         │
│                                     │
│ ○ ⚡ Quick & Efficient              │
│   Ngắn gọn, súc tích, hiệu quả     │
│   [Preview]                         │
│                                     │
├─────────────────────────────────────┤
│         [Save Changes]              │
└─────────────────────────────────────┘
```

---

### Personality Options Detail

#### 1. 👨‍🍳 Professional Chef

**Đặc điểm:**
```
Giọng điệu: Trang trọng, chuyên nghiệp
Chi tiết:   Nhiệt độ chính xác, thời gian cụ thể
Thuật ngữ:  Sử dụng thuật ngữ ẩm thực chuyên môn
Cấu trúc:   Rõ ràng, logic, từng bước một
Emoji:      Ít hoặc không có
```

**Example responses:**
```
User: "Làm thế nào để caramel hóa hành tây?"

AI: "Để đạt độ caramel hóa hoàn hảo cho hành tây, 
bạn cần:

1. Nhiệt độ: Duy trì 150-160°C (lửa vừa thấp)
2. Thời gian: 25-30 phút
3. Kỹ thuật: Đảo đều mỗi 5 phút để tránh cháy

Quá trình này tạo ra phản ứng Maillard, biến 
đường tự nhiên thành caramel, tạo hương vị 
umami đặc trưng và độ ngọt phức hợp.

Lưu ý: Không vội vàng tăng nhiệt độ, điều này 
sẽ làm hành cháy thay vì caramel hóa."
```

---

#### 2. 🏠 Friendly Home Cook (DEFAULT)

**Đặc điểm:**
```
Giọng điệu: Thân thiện, ấm áp, động viên
Ngôn ngữ:   Đơn giản, dễ hiểu, gần gũi
Emoji:      Vừa phải (😊 🍳 ❤️ 👍)
Khuyến khích: "Bạn làm tốt lắm!", "Đừng lo!"
Tương tác:  Đặt câu hỏi, quan tâm user
```

**Example responses:**
```
User: "Hành tây của tôi bị cháy rồi!"

AI: "Ối đừng lo nhé! 😊 Lần đầu ai cũng vậy mà. 
Caramel hành tây đúng là hơi khó một chút.

Mẹo nhỏ của mình:
• Lửa vừa thôi (không quá to)
• Đảo thường xuyên (5 phút một lần)
• Nếu thấy khét, thêm chút nước

Bạn thử lại lần nữa nhé, lần này chắc chắn 
sẽ thành công! 💪 Mình tin bạn! Cần mình 
hướng dẫn chi tiết hơn không?"
```

---

#### 3. 😄 Humorous Foodie

**Đặc điểm:**
```
Giọng điệu: Hài hước, năng động, thoải mái
Emoji:      Nhiều (🤣 😋 🔥 👨‍🍳 💯)
Biệt ngữ:   Slang, meme ẩm thực
Câu đùa:    Xen kẽ trong hướng dẫn
Phong cách: Casual, như bạn bè
```

**Example responses:**
```
User: "Làm sao để không khóc khi thái hành?"

AI: "Ahaha classic problem! 🤣 Hành tây là ninja 
của bếp, làm người ta khóc mà không cần lý do!

Các trick của hội pro:
🥽 Level 1: Đeo kính bơi (serious mode ON)
🧊 Level 2: Ngậm thìa hoặc để hành vào tủ lạnh
⚔️  Level 3: Dao siêu sắc = ít tế bào bị vỡ

Hoặc... embrace the tears và blame the onions 
như bao chef khác 😭👨‍🍳

Btw, caramel hành = god-tier flavor! Worth it! 
Let's goooo 🔥💯"
```

---

#### 4. 🥗 Nutritionist

**Đặc điểm:**
```
Giọng điệu: Chuyên môn về sức khỏe
Tập trung:  Giá trị dinh dưỡng, calories, macro
Gợi ý:      Thay thế lành mạnh, cân bằng
Lưu ý:      Allergies, dietary restrictions
Giải thích: Lợi ích sức khỏe của từng thành phần
```

**Example responses:**
```
User: "Hành tây có tốt cho sức khỏe không?"

AI: "Hành tây là superfood ẩn giấu! 🥗

Thông tin dinh dưỡng (100g):
• Calories: 40 kcal (rất thấp)
• Vitamin C: 7.4mg (tăng miễn dịch)
• Quercetin: Chất chống oxy hóa mạnh
• Prebiotic fiber: Tốt cho đường ruột

Lợi ích sức khỏe:
✓ Chống viêm, giảm cholesterol
✓ Hỗ trợ sức khỏe tim mạch
✓ Kiểm soát đường huyết

Gợi ý nấu ăn:
• Ăn sống → Giữ tối đa vitamin C
• Caramel hóa → Tăng chất chống oxy hóa
• Kết hợp với tỏi → Tăng hiệu quả chống viêm

Lưu ý: Người bị IBS nên hạn chế do FODMAP cao."
```

---

#### 5. ⚡ Quick & Efficient

**Đặc điểm:**
```
Giọng điệu: Súc tích, đi thẳng vào vấn đề
Format:     Bullet points, ngắn gọn
Emoji:      Không hoặc rất ít
Tối ưu:     Tiết kiệm thời gian
Ngôn ngữ:   Trực tiếp, không lan man
```

**Example responses:**
```
User: "Cách caramel hóa hành tây?"

AI: "Caramelizing onions:

Setup:
• Heat: Medium-low
• Oil/butter: 1-2 tbsp

Process:
• Time: 25-30 min
• Stir: Every 5 min
• Add water if burning

Done when: Golden brown, soft

Tips:
- Don't rush heat
- Thin slices = faster
- Salt draws moisture

Time-saving: Instant Pot 15 min high pressure."
```

---

### Preview Dialog

Khi user tap **[Preview]** button:

```
┌─────────────────────────────────────┐
│ Preview: Friendly Home Cook         │
├─────────────────────────────────────┤
│ Hỏi mẫu: "Làm sao để chiên trứng    │
│          ngon?"                     │
│                                     │
│ 🤖 AI Response:                     │
│ ┌─────────────────────────────────┐ │
│ │ Ối dễ mà bạn! 🍳              │ │
│ │                                 │ │
│ │ Bí quyết vàng:                  │ │
│ │ • Chảo nóng + chút bơ           │ │
│ │ • Lửa nhỏ để lòng đỏ mềm        │ │
│ │ • Nêm muối tiêu vừa đủ          │ │
│ │                                 │ │
│ │ Lòng đỏ còn lòng là ngon nhất   │ │
│ │ nè! Bạn thử xem, chắc thích     │ │
│ │ lắm đó 😊                       │ │
│ │                                 │ │
│ │ Cần mình hướng dẫn chi tiết     │ │
│ │ hơn không? ❤️                   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Try Another Question]              │
│                                     │
├─────────────────────────────────────┤
│ [Cancel]          [Select This]    │
└─────────────────────────────────────┘

Modal dialog
Width: 90% screen (max 500px)
Height: Auto
Background: White
Border radius: 20px
Shadow: Elevation 16
```

**Preview Features:**
- Show sample question & response
- [Try Another Question] → Rotate through 5 sample Q&As
- Real-time demonstration of personality style
- Compare side-by-side option (optional)

---

### Personality Comparison (Optional Feature)

```
┌─────────────────────────────────────┐
│ [<] Compare Personalities           │
├─────────────────────────────────────┤
│ Question: "Cách làm phở ngon?"      │
│                                     │
│ ┌─────────────┬─────────────────┐   │
│ │ 🏠 Friendly  │ 👨‍🍳 Professional│   │
│ ├─────────────┼─────────────────┤   │
│ │"Phở là món  │"Phở yêu cầu     │   │
│ │ ăn quốc hồn │ nước dùng ninh  │   │
│ │ quốc tuý    │ xương bò 8-12h  │   │
│ │ nè! 😋      │ ở 95°C, sử dụng │   │
│ │             │ gia vị gồm..."  │   │
│ │ Mẹo: Nước   │                 │   │
│ │ dùng phải   │ Tỷ lệ xương:    │   │
│ │ trong..."   │ nước = 1:3..."  │   │
│ └─────────────┴─────────────────┘   │
│                                     │
│ [Select Left] [Select Right]       │
└─────────────────────────────────────┘
```

---

## User Flows

### Flow 1: Change AI Personality

```
User on Profile screen
  ↓
Taps "⚙️ Settings"
  ↓
Settings screen loads
  ↓
Sees "🤖 AI Personality" section (top):
┌─────────────────────────────────┐
│ 🤖 AI Personality               │
│ ┌─────────────────────────────┐ │
│ │ ● Friendly Home Cook        │ │
│ │   "Thân thiện, động viên"   │ │
│ │                             │ │
│ │ [Change Personality]        │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
  ↓
Taps [Change Personality]
  ↓
Navigate to AI Personality Selection screen
  ↓
Shows 5 personality options with descriptions
  ↓
User taps "😄 Humorous Foodie" radio button
  ↓
Taps [Preview] to see sample response
  ↓
Preview dialog appears with sample conversation
  ↓
User likes it, taps [Select This]
  ↓
Dialog closes, returns to selection screen
  ↓
Radio button now selected: ● Humorous Foodie
  ↓
Taps [Save Changes]
  ↓
Loading spinner appears
  ↓
API: PATCH /api/v1/users/me/settings
{
  "ai_personality": "humorous_foodie"
}
  ↓
Success toast: "AI Personality updated! 🎉"
  ↓
Navigate back to Settings
  ↓
Settings now shows:
┌─────────────────────────────────┐
│ 🤖 AI Personality               │
│ ┌─────────────────────────────┐ │
│ │ ● Humorous Foodie           │ │
│ │   "Vui vẻ, hài hước"        │ │
│ │                             │ │
│ │ [Change Personality]        │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
  ↓
User goes to Chat AI screen
  ↓
AI now responds with humorous tone:
"Hey hey! 🔥 Sẵn sàng nấu nướng chưa nào! 
Hôm nay bạn muốn làm món gì? 👨‍🍳😎"
```

---

### Flow 2: Preview Multiple Personalities

```
User on AI Personality Selection screen
  ↓
Curious about "👨‍🍳 Professional Chef"
  ↓
Taps [Preview] button
  ↓
Preview dialog opens with sample:
┌─────────────────────────────────┐
│ Preview: Professional Chef      │
│                                 │
│ Q: "Làm sao để chiên trứng     │
│     ngon?"                      │
│                                 │
│ A: "Để đạt độ chín hoàn hảo    │
│     cho trứng chiên:            │
│     1. Nhiệt độ chảo: 160°C    │
│     2. Thời gian: 3-4 phút     │
│     3. Kỹ thuật: Basted eggs..."│
└─────────────────────────────────┘
  ↓
User taps [Try Another Question]
  ↓
New sample question/answer loads:
"Q: Cách làm nước dùng phở?"
  ↓
User reads, not satisfied
  ↓
Taps [Cancel] to return
  ↓
Tries "🥗 Nutritionist" [Preview]
  ↓
Preview dialog shows nutritionist style
  ↓
User compares mentally
  ↓
Decides on "🏠 Friendly Home Cook"
  ↓
Selects and saves
```

---

### Flow 3: Edit Profile

```
User on Profile screen
  ↓
Taps [Edit Profile] button
  ↓
Navigate to Edit Profile screen:
┌─────────────────────────────────┐
│ [<] Edit Profile           [✓] │
├─────────────────────────────────┤
│   ┌─────┐                      │
│   │👤   │ [Change Photo]       │
│   └─────┘                      │
│                                │
│ Full Name:                     │
│ ┌─────────────────────────┐    │
│ │ John Doe                │    │
│ └─────────────────────────┘    │
│                                │
│ Email: (cannot edit)           │
│ john@email.com                 │
│                                │
│ Phone (optional):              │
│ ┌─────────────────────────┐    │
│ │ +84 123 456 789         │    │
│ └─────────────────────────┘    │
│                                │
│ Bio (optional):                │
│ ┌─────────────────────────┐    │
│ │ Home cook enthusiast... │    │
│ └─────────────────────────┘    │
└─────────────────────────────────┘
  ↓
User edits fields
  ↓
Taps [✓] save button (AppBar)
  ↓
Show saving spinner
  ↓
API: PUT /api/v1/users/me
  ↓
Success: Navigate back to Profile
  ↓
Profile updated with new info
```

---

### Flow 4: Manage Dietary Preferences

```
User on Profile screen
  ↓
Taps "🥗 Preferences"
  ↓
Preferences screen loads
  ↓
User checks "Vegetarian" checkbox
  ↓
Immediately saved (no save button)
  ↓
API: PATCH /api/v1/users/me/preferences
{
  "dietary_restrictions": ["vegetarian"]
}
  ↓
Confirmation toast: "Preferences updated"
  ↓
Recipe recommendations updated
  ↓
Filters applied to search/explore
```

---

### Flow 5: Add Allergy

```
User on Preferences screen
  ↓
Scrolls to "⚠️ Allergies" section
  ↓
Taps [+ Add Allergy]
  ↓
Dialog appears:
┌─────────────────────────────┐
│ Add Allergy                 │
│ ┌─────────────────────────┐ │
│ │ [Text input]            │ │
│ └─────────────────────────┘ │
│                             │
│ Common allergies:           │
│ [Peanuts] [Shellfish]       │
│ [Eggs] [Milk] [Soy]        │
│                             │
│ [Cancel]        [Add]      │
└─────────────────────────────┘
  ↓
User types "Peanuts" or taps button
  ↓
Taps [Add]
  ↓
New allergy tag appears:
┌─────────────────────────────┐
│ • Peanuts              [×]  │
└─────────────────────────────┘
  ↓
API: POST /api/v1/users/me/allergies
  ↓
Recipes with peanuts now show warning:
⚠️ "Contains allergen: Peanuts"
```

---

### Flow 6: Configure Wake Word

```
User on Profile screen
  ↓
Taps "⚙️ Settings"
  ↓
Settings screen loads
  ↓
In "🎙️ Voice & Audio" section
  ↓
Toggles "Wake Word Detection" ON
  ↓
Sub-settings expand:
┌─────────────────────────────┐
│ Wake Word Detection   [ON]  │
│                             │
│ Activation phrase:          │
│ ○ "Hey Chef"                │
│ ● "Này Chef" (Vietnamese)   │
│                             │
│ Sensitivity:                │
│ Low ━━━●━━ High             │
│                             │
│ Auto-disable at:            │
│ [20%] battery               │
│                             │
│ [Test Wake Word]            │
└─────────────────────────────┘
  ↓
User changes phrase to "Này Chef"
  ↓
Taps [Test Wake Word]
  ↓
Listening indicator appears
  ↓
User says "Này Chef"
  ↓
Success: "✓ Wake word detected!"
  ↓
Settings saved automatically
```

---

### Flow 7: View Cooking History

```
User on Profile screen
  ↓
Taps "🍳 Lịch sử nấu ăn"
  ↓
Cooking History screen loads
  ↓
Shows grouped list:
- Hôm nay (Today): 1 recipe
- Hôm qua (Yesterday): 2 recipes
- Tuần này (This week): 8 recipes
  ↓
User taps recipe "Phở Bò"
  ↓
Navigate to Recipe Detail screen
  ↓
Shows cooking completion stats:
┌─────────────────────────────┐
│ Your last cook: Nov 25, 14:30│
│ Time taken: 42 minutes      │
│ ⭐⭐⭐⭐⭐ (You rated 5/5)      │
└─────────────────────────────┘
  ↓
Option to cook again or rate
```

---

### Flow 8: Delete Account

```
User on Settings screen
  ↓
Scrolls to "💾 Data Management"
  ↓
Taps "Delete Account"
  ↓
Warning dialog appears:
┌─────────────────────────────────┐
│ ⚠️ Delete Account               │
├─────────────────────────────────┤
│ This action cannot be undone.   │
│                                 │
│ All your data will be           │
│ permanently deleted:            │
│ • Saved recipes                 │
│ • Cooking history               │
│ • Preferences                   │
│ • Account information           │
│                                 │
│ Type "DELETE" to confirm:       │
│ ┌─────────────────────────┐     │
│ │ [Text input]            │     │
│ └─────────────────────────┘     │
│                                 │
│ [Cancel]        [Delete]       │
└─────────────────────────────────┘
  ↓
User types "DELETE"
  ↓
[Delete] button enables (red)
  ↓
Taps [Delete]
  ↓
Show loading spinner
  ↓
API: DELETE /api/v1/users/me
  ↓
Success: Clear local data
  ↓
Navigate to Welcome/Login screen
  ↓
Toast: "Account deleted successfully"
```

---

## Backend Integration

### AI Personality API

**Endpoint:** `PATCH /api/v1/users/me/settings`

**Request:**
```json
{
  "ai_personality": "humorous_foodie"
}
```

**Supported Values:**
```
- "professional_chef"
- "friendly_home_cook" (default)
- "humorous_foodie"
- "nutritionist"
- "quick_efficient"
```

**Response:**
```json
{
  "success": true,
  "settings": {
    "ai_personality": "humorous_foodie",
    "updated_at": "2024-11-25T14:30:00Z"
  }
}
```

---

### System Prompt Generation

Backend dynamically generates OpenAI system prompts based on personality:

**Example for "Humorous Foodie":**
```python
system_prompts = {
    "humorous_foodie": """
You are a fun, enthusiastic cooking assistant with a humorous personality.

Communication style:
- Use casual, friendly language
- Include emojis frequently (🔥 😋 👨‍🍳 🤣)
- Make cooking jokes and puns
- Use food slang and memes
- Keep energy high and encouraging
- Make cooking feel like an adventure

Tone: Upbeat, humorous, relatable
Example: "Ahaha! 🤣 That's the spirit! Let's turn you into a master chef! 👨‍🍳🔥"

Always maintain enthusiasm while providing accurate cooking information.
"""
}
```

**API Chat Completion:**
```python
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompts[user.ai_personality]},
        {"role": "user", "content": user_message}
    ]
)
```

---

## Responsive Design

### Mobile (<600px)
- Full width layout
- Stats cards: 3 columns (tight)
- Menu items: Full width, 56px height
- Personality list: Full width cards
- Preview dialog: 90% width

### Tablet (600-1200px)
- Max width: 600px, centered
- Stats cards: More padding
- Menu items: Slightly larger fonts
- Personality cards: 2 columns

### Desktop (>1200px)
```
┌─────────────────────────────────────────┐
│ [Profile Header]   [Stats]              │
│                                         │
│ [Menu Grid - 2 columns]                 │
│ ❤️ Favorites        🍳 History           │
│ 🥗 Preferences      ⚙️ Settings          │
│ ❓ Help             🚪 Logout            │
└─────────────────────────────────────────┘

Max width: 1200px, centered
Grid: 2 columns for menu items
Larger stats cards
Personality selection: Side-by-side preview
```

---

## Accessibility

**Screen Reader:**
- "Profile section, [Name], [Email]"
- "Edit profile, button"
- "24 saved recipes, button"
- "Favorites, button, navigate"
- "AI Personality: Friendly Home Cook, button"
- "Change personality, button"
- "Logout, button, requires confirmation"

**Visual:**
- High contrast mode support
- Focus indicators on all interactive elements
- Large tap targets (min 48×48px)
- Clear radio button states

**Keyboard:**
- Tab navigation through all options
- Enter to activate buttons
- Arrow keys for sliders
- Space to toggle radio buttons

---

## Performance

**Data Loading:**
- Profile info: Cached, load on app start
- Stats: Async, show placeholders while loading
- Images: Lazy load, compress avatars to 200×200px
- AI Personality: Loaded with settings, no separate call

**Optimization:**
- Preferences saved immediately (optimistic UI)
- Stats update in background
- Cache avatar locally
- Personality previews: Pre-generated responses (cached)

---

## Privacy & Data

**AI Personality Storage:**
- Stored in user settings table
- Not shared with third parties
- Used only for chat prompt generation
- Can be changed anytime

**Data Handling:**
- Personality preference synced to backend
- Chat history respects privacy settings
- Preview responses: Static, not logged
- No personality data sold or shared

---

## Summary

**Profile Screen Features:**
- ✅ Profile header (avatar, name, email, edit)
- ✅ Stats cards (Saved, Cooked, Lists) - tap to navigate
- ✅ Favorites list access
- ✅ Cooking history with timeline
- ✅ Dietary preferences (vegetarian, vegan, etc.)
- ✅ Allergy management (add/remove)
- ✅ Default servings & measurement units
- ✅ **AI Personality selection (5 options)** ⭐ NEW
- ✅ **Preview personality with sample responses** ⭐ NEW
- ✅ Voice settings (language, speed, wake word)
- ✅ Notifications preferences
- ✅ Privacy controls (on-device processing, analytics)
- ✅ Data management (cache, export, delete account)
- ✅ Help & support (FAQs, contact, feedback)
- ✅ Logout with confirmation

---

## AI Personality Summary

| Personality | Tone | Emoji Use | Detail Level | Use Case |
|------------|------|-----------|--------------|----------|
| **Professional Chef** | Formal, Technical | Minimal | High | Serious cooks, culinary students |
| **Friendly Home Cook** | Warm, Encouraging | Moderate | Medium | Default, general users |
| **Humorous Foodie** | Fun, Casual | Heavy | Medium | Entertainment, stress-free cooking |
| **Nutritionist** | Health-focused | Minimal | High | Health-conscious, dietary restrictions |
| **Quick & Efficient** | Direct, Brief | Minimal | Low | Busy users, quick answers |

---

Với việc hoàn thành **Profile Screen với AI Personality feature**, chúng ta đã thiết kế xong **TẤT CẢ 5 màn chính** trong bottom navigation:

1. ✅ **Home Screen** - Khám phá & gợi ý recipes
2. ✅ **Explore Bottom Sheet** - Tìm kiếm & danh mục
3. ✅ **Chat AI Screen** - Trợ lý AI với RAG + Voice + Wake Word
4. ✅ **Camera Screen** - Nhận diện nguyên liệu bằng AI Vision
5. ✅ **Profile Screen** - Quản lý tài khoản & preferences + **AI Personality** ⭐

**Còn lại các màn phụ:** Search Screen, Categories Screen, Recipe Detail (đã có), Cooking Mode.

Bạn muốn tiếp tục thiết kế các màn phụ này, hay chuyển sang **Phase 3: Backend Design & Database Schema**?
