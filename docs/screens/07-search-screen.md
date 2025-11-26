# 🔍 Search Screen - Design Specification

## Overview
Search Screen cho phép users tìm kiếm recipes với nhiều tiêu chí: tên món, nguyên liệu, category, độ khó, thời gian nấu. Hỗ trợ filters nâng cao và suggestions thông minh.

**Access Point:** Explore Bottom Sheet → 🔍 Recipes

---

## Visual Layout

### Initial State (Before Typing)

```
┌─────────────────────────────────────┐
│ [←] ┌─────────────────────┐ [⋮]    │ <- AppBar
│     │ 🔍 Tìm kiếm...      │         │    Search input
│     └─────────────────────┘         │
├─────────────────────────────────────┤
│                                     │
│ 🕐 Tìm kiếm gần đây                 │ <- Recent searches
│ ┌─────────────────────────────────┐ │
│ │ • Phở bò                   [×]  │ │
│ │ • Bún chả                  [×]  │ │
│ │ • Món chay                 [×]  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Clear All]                         │
│                                     │
│ 🔥 Trending                         │ <- Trending keywords
│ [Bánh mì] [Gỏi cuốn] [Cơm tấm]    │
│ [Phở] [Bún bò Huế] [Chả giò]      │
│ [Canh chua] [Thịt kho]             │
│                                     │
│ 📂 Browse by Category               │ <- Quick shortcuts
│ [Món chính] [Món phụ] [Tráng miệng]│
│ [Món chay] [Món nước] [Món khô]    │
│                                     │
└─────────────────────────────────────┘
```

### While Typing (Autocomplete)

```
┌─────────────────────────────────────┐
│ [←] ┌─────────────────────┐ [⋮]    │
│     │ 🔍 phở              │         │
│     └─────────────────────┘         │
├─────────────────────────────────────┤
│                                     │
│ 💡 Gợi ý:                           │
│                                     │
│ 🍜 Phở bò                      (142)│ <- Recipe matches
│ 🍜 Phở gà                       (89)│
│ 🍜 Phở cuốn                     (34)│
│ 🍜 Phở xào                      (21)│
│                                     │
│ 🥘 Nguyên liệu:                     │ <- Ingredient matches
│ Thịt bò phở                     (12)│
│ Bánh phở khô                     (8)│
│                                     │
│ 👨‍🍳 Chef/Tác giả:                   │ <- Chef names
│ Chef Phở Việt                   (5) │
│                                     │
└─────────────────────────────────────┘
```

### Results View

```
┌─────────────────────────────────────┐
│ [←] ┌─────────────────────┐ [⋮]    │
│     │ 🔍 phở bò           │         │
│     └─────────────────────┘         │
├─────────────────────────────────────┤
│ 142 kết quả                    [⚙️] │ <- Results header
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Image]                         │ │
│ │                                 │ │
│ │ Phở Bò Hà Nội              [❤️] │ │
│ │ ⭐ 4.8  ⏱️ 60 min  🔥 Medium    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Image]                         │ │
│ │                                 │ │
│ │ Phở Bò Nam Bộ              [❤️] │ │
│ │ ⭐ 4.6  ⏱️ 45 min  🔥 Easy      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Image]                         │ │
│ │                                 │ │
│ │ Phở Bò Viên                [❤️] │ │
│ │ ⭐ 4.5  ⏱️ 50 min  🔥 Medium    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Load More]                         │
│                                     │
└─────────────────────────────────────┘
```

---

## Components Detail

### 1. AppBar

```
┌─────────────────────────────────────┐
│ [←] ┌─────────────────────┐ [⋮]    │
│     │ 🔍 Tìm kiếm...      │         │
│     └─────────────────────┘         │
└─────────────────────────────────────┘
```

**Back Button [←]:**
- Size: 40×40px
- Icon: Arrow left (24×24px, black)
- Position: Left
- Tap: Navigate back to Explore/Home

**Search Input:**
- Height: 48px
- Width: Flexible (screen width - 120px)
- Border radius: 24px
- Background: Light gray #F5F5F5
- Padding: 12px 16px 12px 48px
- Icon: 🔍 (20×20px, gray, left padding)
- Placeholder: "Tìm kiếm..." (gray #999)
- Font: 16px, regular
- Auto-focus: On screen load
- Clear button: [×] appears when typing (right side)

**Filter Button [⋮]:**
- Size: 40×40px
- Icon: Three dots vertical (24×24px, black)
- Position: Right
- Badge: Orange dot (8×8px) if filters active
- Tap: Open filter bottom sheet

---

### 2. Recent Searches Section

```
┌─────────────────────────────────────┐
│ 🕐 Tìm kiếm gần đây                 │
│ ┌─────────────────────────────────┐ │
│ │ • Phở bò                   [×]  │ │
│ │ • Bún chả                  [×]  │ │
│ │ • Món chay                 [×]  │ │
│ │ • Cơm tấm                  [×]  │ │
│ │ • Bánh xèo                 [×]  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Clear All]                         │
└─────────────────────────────────────┘
```

**Section Header:**
- Icon: 🕐 (20×20px)
- Text: "Tìm kiếm gần đây" (14px, medium, gray #666)
- Margin: 16px top, 12px bottom

**Recent Search Item:**
```
┌─────────────────────────────────┐
│ • Phở bò                   [×] │
└─────────────────────────────────┘

Height: 48px
Background: White
Border radius: 12px
Padding: 12px 16px
Margin: 4px 0
Border: 1px solid #F0F0F0

Bullet: • (gray #999, 16px)
Text: "Phở bò" (16px, black)
Remove button: [×] (32×32px, gray)

Tap on text: Execute search
Tap on [×]: Remove from history
```

**Clear All Button:**
```
┌─────────────┐
│ Clear All   │
└─────────────┘

Height: 40px
Width: Auto (padding 20px horizontal)
Background: Transparent
Border: 1px solid #F44336 (red)
Border radius: 20px
Text: "Clear All" (14px, red #F44336)
Margin: 12px top

Tap: Show confirmation dialog
```

**Clear All Confirmation:**
```
┌─────────────────────────────────┐
│ Clear search history?           │
├─────────────────────────────────┤
│ All recent searches will be     │
│ permanently deleted.            │
│                                 │
│ [Cancel]        [Clear]        │
└─────────────────────────────────┘
```

**Storage:**
- Max: 10 recent searches
- Persistence: Local storage (SQLite/SharedPreferences)
- Order: Most recent first
- Auto-save: After search execution

---

### 3. Trending Keywords Section

```
┌─────────────────────────────────────┐
│ 🔥 Trending                         │
│                                     │
│ [Bánh mì] [Gỏi cuốn] [Cơm tấm]    │
│ [Phở] [Bún bò Huế] [Chả giò]      │
│ [Canh chua] [Thịt kho]             │
└─────────────────────────────────────┘
```

**Section Header:**
- Icon: 🔥 (20×20px)
- Text: "Trending" (14px, medium, gray #666)
- Margin: 16px top, 12px bottom

**Trending Chip:**
```
┌─────────────┐
│ Bánh mì     │
└─────────────┘

Height: 36px
Padding: 8px 16px
Background: Light orange #FFF3E0
Border: 1px solid orange #FF6F00
Border radius: 18px
Text: 14px, medium, orange #FF6F00
Margin: 4px (between chips)

Tap: Execute search immediately
Animation: Scale down (0.95) on press
```

**Layout:**
- Wrap: Horizontal wrap, multiple rows
- Alignment: Left-aligned
- Spacing: 8px horizontal, 8px vertical
- Max visible: 12 keywords
- Update: Every hour (backend pre-computed)

**Trending Algorithm (Backend):**
```python
# Based on:
# - Search frequency (last 24h)
# - Recipe views
# - Social shares
# - Seasonal relevance
trending_score = (
    search_count * 3 +
    view_count * 2 +
    share_count * 5 +
    seasonal_boost * 1
)
```

---

### 4. Browse by Category Section

```
┌─────────────────────────────────────┐
│ 📂 Browse by Category               │
│                                     │
│ [Món chính] [Món phụ] [Tráng miệng]│
│ [Món chay] [Món nước] [Món khô]    │
└─────────────────────────────────────┘
```

**Section Header:**
- Icon: 📂 (20×20px)
- Text: "Browse by Category" (14px, medium, gray #666)
- Margin: 16px top, 12px bottom

**Category Chip:**
```
┌─────────────┐
│ Món chính   │
└─────────────┘

Height: 40px
Padding: 10px 20px
Background: White
Border: 1px solid gray #E0E0E0
Border radius: 20px
Text: 14px, medium, black
Icon: Optional emoji (left side)
Margin: 4px

Tap: Navigate to Category Detail screen
Animation: Background gray on press
```

**Layout:**
- Wrap: Horizontal wrap
- Spacing: 8px between chips
- Show: Top 6-8 categories
- Full list: "See all categories >" link at bottom

---

### 5. Autocomplete Suggestions

```
┌─────────────────────────────────────┐
│ 💡 Gợi ý:                           │
│                                     │
│ 🍜 Phở bò                      (142)│
│ 🍜 Phở gà                       (89)│
│ 🍜 Phở cuốn                     (34)│
│                                     │
│ 🥘 Nguyên liệu:                     │
│ Thịt bò phở                     (12)│
│                                     │
│ 👨‍🍳 Chef/Tác giả:                   │
│ Chef Phở Việt                   (5) │
└─────────────────────────────────────┘
```

**Section Header:**
- Icon: 💡 (20×20px)
- Text: "Gợi ý:" (14px, medium, gray)
- Margin: 16px top

**Suggestion Item:**
```
┌─────────────────────────────────┐
│ 🍜 Phở bò                  (142)│
└─────────────────────────────────┘

Height: 52px
Background: White
Padding: 12px 16px
Border bottom: 1px #F0F0F0

Icon: 24×24px (left)
  - 🍜 Recipe
  - 🥘 Ingredient
  - 👨‍🍳 Chef

Text: 16px, regular, black
  - Matching part: Bold
  - Example: "Phở" bold, "bò" regular
  
Count: (14px, gray, right)
  - Recipe count or result count

Tap: Execute search with this term
```

**Grouping:**
- **Recipes** (🍜): Max 4 items
- **Ingredients** (🥘): Max 2 items
- **Chefs** (👨‍🍳): Max 2 items

**"See more" link:**
```
If > max items:
┌─────────────────────────────────┐
│ See all 12 recipes >            │
└─────────────────────────────────┘
Text: 14px, orange, underline
Tap: Execute full search
```

**Highlighting:**
```
User types: "phở b"
Display: "Phở bò"
         ^^^^^ (bold matching part)
```

---

### 6. Search Results Header

```
┌─────────────────────────────────────┐
│ 142 kết quả                    [⚙️] │
└─────────────────────────────────────┘
```

**Container:**
- Height: 48px
- Padding: 12px 16px
- Background: White
- Border bottom: 1px solid #F0F0F0
- Sticky: Fixed at top when scrolling

**Results Count:**
- Text: "142 kết quả" (16px, bold, black)
- Position: Left
- Update: Real-time with filters

**Filter Button:**
- Icon: ⚙️ (24×24px, gray)
- Position: Right
- Badge: Orange dot (8×8px) if active
- Tap: Open filter bottom sheet

**Active Filters Display (Optional):**
```
┌─────────────────────────────────────┐
│ 142 kết quả                    [⚙️] │
│                                     │
│ [Under 30min ×] [Easy ×] [4★+ ×]  │ <- Filter chips
└─────────────────────────────────────┘

Chip: 
- Height: 28px
- Padding: 6px 12px
- Background: Orange #FFF3E0
- Border: 1px orange
- Text: 12px, orange
- [×] icon: Tap to remove filter
```

---

### 7. Recipe Cards (Results)

```
┌─────────────────────────────────┐
│ [Image 3:4 aspect ratio]        │
│                                 │
│                                 │
│ Phở Bò Hà Nội              [❤️] │
│ ⭐ 4.8  ⏱️ 60 min  🔥 Medium    │
└─────────────────────────────────┘
```

**Same design as Home Screen:**

**Image:**
- Aspect ratio: 3:4 (portrait)
- Width: 100% of card
- Border radius: 16px (top corners)
- Lazy load: Load when in viewport

**Favorite Button [❤️]:**
- Size: 36×36px
- Position: Absolute, top-right 12px
- Background: White 80% opacity, circular
- Icon: Heart (20×20px)
  - Unfilled: Gray outline
  - Filled: Red solid

**Title:**
- Text: Recipe name (16px, bold, black)
- Max lines: 2
- Overflow: Ellipsis

**Metadata Row:**
```
⭐ 4.8  ⏱️ 60 min  🔥 Medium

Rating: ⭐ 4.8 (14px, black)
Time: ⏱️ 60 min (14px, gray)
Difficulty: 🔥 Medium (14px, gray)
Separator: • (gray)
```

**Card Tap:** Navigate to Recipe Detail

---

### 8. Filter Bottom Sheet

```
┌─────────────────────────────────────┐
│ [×]  Filters                   [✓] │ <- Header
├─────────────────────────────────────┤
│                                     │
│ 🍽️ Category                         │
│ ┌─────────────────────────────────┐ │
│ │ ☑️ Món chính                     │ │
│ │ ☐ Món phụ                       │ │
│ │ ☐ Tráng miệng                   │ │
│ │ ☐ Món chay                      │ │
│ │ ☐ Món nước                      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ⏱️ Cooking Time                     │
│ ┌─────────────────────────────────┐ │
│ │ ○ Any                           │ │
│ │ ● Under 30 min                  │ │
│ │ ○ 30-60 min                     │ │
│ │ ○ Over 60 min                   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🔥 Difficulty                       │
│ ┌─────────────────────────────────┐ │
│ │ [Easy] [Medium] [Hard]          │ │
│ │   ●       ○        ○            │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ⭐ Rating                           │
│ ┌─────────────────────────────────┐ │
│ │ 4+ stars and above              │ │
│ │ ━━━━━●━━━━━                    │ │
│ │ 1.0        3.0        5.0       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 👥 Servings                         │
│ ┌─────────────────────────────────┐ │
│ │     [-]    [2]    [+]           │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🌱 Dietary                          │
│ ┌─────────────────────────────────┐ │
│ │ ☑️ Vegetarian                    │ │
│ │ ☐ Vegan                         │ │
│ │ ☐ Gluten-Free                   │ │
│ │ ☐ Dairy-Free                    │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Clear All]       [Apply (142)]    │
└─────────────────────────────────────┘
```

**Bottom Sheet:**
- Height: 80% screen (rounded top corners 24px)
- Background: White
- Shadow: Elevation 16
- Drag handle: Optional (6px line, centered top)

**Header:**
- Height: 56px
- Padding: 16px
- Border bottom: 1px #F0F0F0

- Close [×]: Left (40×40px)
- Title: "Filters" (18px, bold, center)
- Apply [✓]: Right (40×40px, orange)

**Filter Sections:**

**1. Category (Multi-select):**
```
☑️ Món chính
☐ Món phụ

Checkbox: 24×24px
  - Checked: Orange fill with white check
  - Unchecked: Gray border
Label: 16px, black
Tap area: Full row (48px height)
```

**2. Cooking Time (Radio):**
```
○ Any
● Under 30 min

Radio: 24×24px
  - Selected: Orange fill with white center
  - Unselected: Gray border
Label: 16px, black
Single select only
```

**3. Difficulty (Toggle chips):**
```
[Easy] [Medium] [Hard]
  ●       ○        ○

Chip height: 40px
Selected: Orange background, white text
Unselected: White background, gray border
Multi-select allowed
```

**4. Rating (Slider):**
```
━━━━━●━━━━━
1.0  3.0  5.0

Slider:
- Track: Gray #E0E0E0 (4px height)
- Active track: Orange #FF6F00
- Thumb: 24×24px circle, orange
- Range: 1.0 - 5.0
- Step: 0.5
- Default: 4.0
Label: "4+ stars and above" (14px, gray)
```

**5. Servings (Number picker):**
```
[-]  [2]  [+]

Button: 40×40px circular
  - Background: Light gray
  - Icon: - or + (20×20px)
Number: 20px, bold, center
Range: 1-10
Default: User's preference (or 2)
```

**6. Dietary (Multi-select):**
```
☑️ Vegetarian

Same as Category checkboxes
Auto-checked from user preferences
```

**Actions Bar:**
```
┌─────────────────────────────────┐
│ [Clear All]    [Apply (142)]   │
└─────────────────────────────────┘

Height: 72px
Padding: 12px 16px
Background: White
Border top: 1px #F0F0F0
Fixed at bottom

Clear All:
- Height: 48px
- Width: 40%
- Background: White
- Border: 1px gray
- Text: 14px, gray

Apply:
- Height: 48px
- Width: 55%
- Background: Orange
- Text: 16px, bold, white
- Shows updated count: "Apply (142)"
```

**Filter Logic:**
- AND between different filter types
- OR within same type (e.g., Easy OR Medium)
- Real-time count update in Apply button
- Persist filters across sessions

---

### 9. Empty State

```
┌─────────────────────────────────────┐
│ [←] ┌─────────────────────┐ [⋮]    │
│     │ 🔍 xyz abc 123      │         │
│     └─────────────────────┘         │
├─────────────────────────────────────┤
│                                     │
│                                     │
│             😕                      │
│                                     │
│     Không tìm thấy kết quả          │
│                                     │
│     Thử tìm kiếm với:               │
│     • Từ khóa khác                  │
│     • Tên món ăn phổ biến          │
│     • Nguyên liệu chính             │
│                                     │
│     Hoặc:                           │
│     ┌─────────────────────────┐     │
│     │ Browse Categories       │     │
│     └─────────────────────────┘     │
│                                     │
│     ┌─────────────────────────┐     │
│     │ 💬 Ask AI               │     │
│     └─────────────────────────┘     │
│                                     │
└─────────────────────────────────────┘

Icon: 😕 (80×80px, centered)
Heading: "Không tìm thấy kết quả" (18px, bold)
Suggestions: 14px, gray, bullet list
Buttons: 48px height, 80% width, 12px margin
```

**Browse Categories Button:**
- Background: White
- Border: 1px orange
- Text: Orange
- Tap: Navigate to Categories screen

**Ask AI Button:**
- Background: Orange
- Text: White
- Icon: 💬 (20×20px)
- Tap: Navigate to Chat AI with pre-filled query

---

### 10. Loading States

**Initial Search Loading:**
```
┌─────────────────────────────────────┐
│ 142 kết quả                    [⚙️] │
├─────────────────────────────────────┤
│ [Skeleton card]                     │
│ [Skeleton card]                     │
│ [Skeleton card]                     │
└─────────────────────────────────────┘

Skeleton: Shimmer animation (gray → light gray)
Duration: Show until data loads
```

**Load More Button:**
```
┌─────────────────────┐
│     Load More       │
└─────────────────────┘

Height: 48px
Width: 100% - 32px margin
Background: White
Border: 1px orange
Text: 16px, orange
Margin: 16px top

Tap: Load next 20 recipes
Loading state: Show spinner inside button
```

---

## User Flows

### Flow 1: Quick Search from Trending

```
User navigates to Search screen
  ↓
Initial state shows:
- Recent searches (if any)
- Trending keywords
- Categories
  ↓
User sees "Bánh mì" in trending
  ↓
Taps [Bánh mì] chip
  ↓
Search input auto-fills: "Bánh mì"
  ↓
Results load immediately
  ↓
Shows: "87 kết quả" + recipe grid
  ↓
"Bánh mì" saved to recent searches
  ↓
User scrolls, taps a recipe
  ↓
Navigate to Recipe Detail
```

---

### Flow 2: Type with Autocomplete

```
User taps search input
  ↓
Keyboard appears, cursor active
  ↓
User types: "p"
  ↓
After 300ms debounce, API call:
GET /api/v1/recipes/autocomplete?q=p
  ↓
Suggestions appear:
💡 Gợi ý:
🍜 Phở bò (142)
🍜 Phở gà (89)
  ↓
User continues typing: "ph"
  ↓
Suggestions update (cancels previous API call):
🍜 Phở bò (142)
🍜 Phở gà (89)
🍜 Phở cuốn (34)
  ↓
User types: "phở b"
  ↓
Suggestions narrow:
🍜 Phở bò (142)
🍜 Phở bò viên (28)
  ↓
User taps "Phở bò" suggestion
  ↓
Search executes immediately
  ↓
Results screen: "142 kết quả"
  ↓
Recipe grid displays
  ↓
"Phở bò" saved to recent searches
```

---

### Flow 3: Advanced Filtering

```
User searches "món chay"
  ↓
Results: "234 kết quả"
  ↓
Too many results, wants to narrow
  ↓
Taps filter icon [⚙️] or [⋮]
  ↓
Filter bottom sheet slides up
  ↓
User configures filters:
☑️ Category: Món chính
● Time: Under 30 min
● Difficulty: Easy
Rating slider: 4.0+
Dietary: ☑️ Vegetarian (auto from preferences)
  ↓
Apply button updates: "Apply (42)"
  ↓
Taps [Apply (42)]
  ↓
Bottom sheet closes with animation
  ↓
Results update: "42 kết quả"
  ↓
Filter chips appear:
[Under 30min ×] [Easy ×] [4★+ ×]
  ↓
Filter icon shows orange badge
  ↓
Recipe grid refreshes with filtered results
  ↓
User can tap [×] on chip to remove individual filter
```

---

### Flow 4: Recent Search Reuse

```
User returns to Search screen
  ↓
Sees recent searches:
• Phở bò
• Bún chả
• Món chay
  ↓
Taps "Bún chả" item
  ↓
Search executes immediately (no typing)
  ↓
Results load: "56 kết quả"
  ↓
Recipe grid displays

[Alternative: Remove from history]
  ↓
User taps [×] on "Món chay"
  ↓
Item removed from list (no confirmation)
  ↓
Local storage updated
  ↓
List re-renders without "Món chay"
```

---

### Flow 5: Clear All Recent Searches

```
User on Search screen
  ↓
Has 5+ recent searches
  ↓
Taps [Clear All] button
  ↓
Confirmation dialog appears:
┌─────────────────────────────┐
│ Clear search history?       │
│                             │
│ All recent searches will be │
│ permanently deleted.        │
│                             │
│ [Cancel]        [Clear]    │
└─────────────────────────────┘
  ↓
User taps [Clear]
  ↓
Dialog closes
  ↓
All recent searches removed
  ↓
Section hides (only trending + categories show)
  ↓
Toast: "Search history cleared"
```

---

### Flow 6: Empty Results → Ask AI

```
User searches "abc xyz 123" (invalid)
  ↓
API returns: 0 results
  ↓
Empty state displays:
😕 Không tìm thấy kết quả
  ↓
User taps [💬 Ask AI] button
  ↓
Navigate to Chat AI screen
  ↓
Message pre-filled:
"Tôi đang tìm món ăn liên quan đến 
'abc xyz 123'. Bạn có gợi ý gì không?"
  ↓
Auto-send or allow user to edit first
  ↓
AI responds with helpful suggestions:
"Có vẻ như không có món ăn với tên đó. 
Bạn có thể mô tả món ăn bạn muốn? 
Ví dụ: món chay, nhanh, cay..."
```

---

### Flow 7: Filter by Category Chip

```
User on Search screen (initial state)
  ↓
Sees "Browse by Category" section:
[Món chính] [Món phụ] [Tráng miệng]
  ↓
Taps [Món chính] chip
  ↓
Navigate to Category Detail screen
  ↓
Shows all recipes in "Món chính" category
  ↓
[Alternative in same Search screen]
  ↓
Opens filter bottom sheet with:
☑️ Món chính (pre-selected)
  ↓
User can add more filters
```

---

## Backend Integration

### Search API

**Endpoint:** `GET /api/v1/recipes/search`

**Query Parameters:**
```
?q=phở bò                    # Search query
&category=main_dish,soup     # Multiple categories
&time=under_30               # Time filter
&difficulty=easy,medium      # Multiple difficulties
&rating=4                    # Minimum rating
&servings=2                  # Servings count
&dietary=vegetarian,vegan    # Dietary restrictions
&page=1                      # Pagination
&limit=20                    # Results per page
```

**Request Example:**
```
GET /api/v1/recipes/search?q=phở&time=under_30&rating=4&page=1&limit=20
```

**Response:**
```json
{
  "success": true,
  "total": 142,
  "page": 1,
  "per_page": 20,
  "total_pages": 8,
  "results": [
    {
      "id": "recipe_001",
      "name": "Phở Bò Hà Nội",
      "slug": "pho-bo-ha-noi",
      "image": "https://cdn.example.com/recipes/pho-bo.jpg",
      "thumbnail": "https://cdn.example.com/recipes/pho-bo_thumb.jpg",
      "rating": 4.8,
      "rating_count": 1234,
      "time": 60,
      "difficulty": "medium",
      "servings": 4,
      "category": ["main_dish", "soup"],
      "dietary": ["none"],
      "is_favorited": false
    }
  ],
  "filters": {
    "available_categories": ["main_dish", "soup", "side_dish"],
    "time_ranges": ["under_30", "30_60", "over_60"],
    "difficulties": ["easy", "medium", "hard"],
    "dietary_options": ["vegetarian", "vegan", "gluten_free"]
  }
}
```

---

### Autocomplete API

**Endpoint:** `GET /api/v1/recipes/autocomplete`

**Query Parameters:**
```
?q=phở          # Search term (min 1 char)
&limit=10       # Max suggestions (default 10)
```

**Request Example:**
```
GET /api/v1/recipes/autocomplete?q=phở&limit=10
```

**Response:**
```json
{
  "success": true,
  "suggestions": {
    "recipes": [
      {
        "text": "Phở bò",
        "count": 142,
        "type": "recipe",
        "highlight": "Phở"
      },
      {
        "text": "Phở gà",
        "count": 89,
        "type": "recipe",
        "highlight": "Phở"
      },
      {
        "text": "Phở cuốn",
        "count": 34,
        "type": "recipe",
        "highlight": "Phở"
      }
    ],
    "ingredients": [
      {
        "text": "Thịt bò phở",
        "count": 12,
        "type": "ingredient",
        "highlight": "phở"
      }
    ],
    "chefs": [
      {
        "text": "Chef Phở Việt",
        "count": 5,
        "type": "chef",
        "highlight": "Phở"
      }
    ]
  }
}
```

**Debounce:** 300ms client-side before API call

---

### Trending Keywords API

**Endpoint:** `GET /api/v1/recipes/trending`

**Response:**
```json
{
  "success": true,
  "trending": [
    {"keyword": "Bánh mì", "score": 985},
    {"keyword": "Gỏi cuốn", "score": 876},
    {"keyword": "Cơm tấm", "score": 743},
    {"keyword": "Phở", "score": 701},
    {"keyword": "Bún bò Huế", "score": 654}
  ],
  "updated_at": "2024-11-25T14:00:00Z"
}
```

**Update Frequency:** Every hour  
**Cache:** Client caches for 1 hour

---

### Search Ranking Algorithm

**Backend ranking formula:**
```python
relevance_score = (
    name_exact_match * 100 +        # Exact match highest priority
    name_partial_match * 50 +       # Partial name match
    ingredient_match * 20 +         # Ingredient contains query
    description_match * 10 +        # Description keyword
    tag_match * 15 +                # Category/tag match
    rating * 5 +                    # Recipe rating (1-5)
    popularity * 3 +                # View/cook count
    recency * 2                     # Recently added bonus
)
```

**Example:**
```
Query: "phở bò"

Recipe A: "Phở Bò Hà Nội" (exact name match)
  - name_exact_match: 1.0
  - rating: 4.8
  - popularity: 1200 views
  → Score: 100 + 24 + 3.6 = 127.6

Recipe B: "Bún Bò Huế" (ingredient match only)
  - name_exact_match: 0
  - ingredient_match: 0.5 (has "bò")
  - rating: 4.5
  → Score: 10 + 22.5 = 32.5

Recipe A ranks higher ✓
```

---

## Performance Optimization

### Client-Side

**Debouncing:**
```javascript
// Autocomplete debounce
let debounceTimer;
function onSearchInput(query) {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchAutocomplete(query);
  }, 300); // Wait 300ms after user stops typing
}
```

**Request Cancellation:**
```javascript
// Cancel previous autocomplete request
let currentRequest = null;
function fetchAutocomplete(query) {
  if (currentRequest) {
    currentRequest.cancel(); // Abort previous request
  }
  currentRequest = api.get('/autocomplete', {query});
}
```

**Caching:**
- Recent searches: Local storage (persistent)
- Trending keywords: In-memory cache (1 hour TTL)
- Search results: In-memory cache (5 min TTL)

**Lazy Loading:**
- Load 20 recipes initially
- Load more on scroll (infinite scroll) or [Load More] button
- Images: Lazy load with placeholder

---

### Backend

**Database Indexing:**
```sql
CREATE INDEX idx_recipes_name ON recipes(name);
CREATE INDEX idx_recipes_search ON recipes USING gin(to_tsvector('english', name || ' ' || description));
CREATE INDEX idx_recipe_ingredients ON recipe_ingredients(ingredient_name);
```

**Full-Text Search:**
```python
# PostgreSQL full-text search
query = """
  SELECT *
  FROM recipes
  WHERE to_tsvector('english', name || ' ' || description) 
        @@ plainto_tsquery('english', %s)
  ORDER BY ts_rank(to_tsvector('english', name), plainto_tsquery('english', %s)) DESC
  LIMIT 20 OFFSET %s
"""
```

**Caching (Redis):**
- Trending keywords: 1 hour TTL
- Autocomplete results: 15 min TTL
- Popular searches: 30 min TTL

---

## Responsive Design

### Mobile (<600px)
- Search input: Full width - 120px
- Results: 1 column grid
- Filter sheet: 85% screen height
- Chips: Wrap to multiple rows
- Cards: Full width - 32px margin

### Tablet (600-1200px)
- Results: 2 column grid
- Filter sheet: 70% screen height
- More padding/margins
- Larger tap targets

### Desktop (>1200px)
```
┌─────────────────────────────────────────┐
│ [Search bar]                            │
├──────────────┬──────────────────────────┤
│ Filters      │  Results (3 columns)     │
│ (Sidebar)    │                          │
│              │  [Recipe] [Recipe] [Rec] │
│ [Category]   │  [Recipe] [Recipe] [Rec] │
│ [Time]       │  [Recipe] [Recipe] [Rec] │
│ [Difficulty] │                          │
│ [Rating]     │  [Load More]             │
│ [Servings]   │                          │
│ [Dietary]    │                          │
│              │                          │
│ [Clear] [Apply]                         │
└──────────────┴──────────────────────────┘

Left sidebar: 300px fixed width
Right content: Flexible, 3 column grid (max 1200px)
Filters always visible (no bottom sheet)
```

---

## Accessibility

### Screen Reader Announcements

**Elements:**
- Search input: "Search recipes, text field"
- Recent search: "Recent search: Phở bò, button, tap to search, remove button"
- Trending chip: "Trending keyword: Bánh mì, button"
- Category chip: "Browse category: Món chính, button"
- Suggestion: "Suggestion: Phở bò, 142 recipes, button"
- Filter button: "Filters, button, tap to open filter options"
- Results: "142 results found"
- Recipe card: "Recipe: Phở Bò Hà Nội, rating 4.8 stars, 60 minutes, medium difficulty, button"

**Live Regions:**
```html
<div aria-live="polite" aria-atomic="true">
  142 kết quả
</div>
```
Announces result count changes

---

### Keyboard Navigation

**Tab Order:**
1. Back button
2. Search input
3. Clear input button (if text present)
4. Filter button
5. Recent search items (if visible)
6. Trending chips
7. Category chips
8. Recipe cards
9. Load more button

**Shortcuts:**
- Enter: Execute search (in input field)
- Esc: Clear input / Close filter sheet
- Arrow Down/Up: Navigate suggestions (in autocomplete)
- Tab: Next focusable element
- Shift+Tab: Previous focusable element

---

### Focus Indicators

**All interactive elements:**
```css
button:focus, input:focus {
  outline: 2px solid #FF6F00; /* Orange outline */
  outline-offset: 2px;
}
```

**High contrast mode:**
- Ensure 4.5:1 contrast ratio for text
- Bold outlines on focus
- Clear visual separation between elements

---

## Edge Cases & Error Handling

### Network Errors

**API Timeout:**
```
┌─────────────────────────────────┐
│         ⚠️                      │
│                                 │
│  Lỗi kết nối                    │
│                                 │
│  Không thể tải kết quả.         │
│  Vui lòng kiểm tra kết nối.    │
│                                 │
│  [Thử lại]                      │
└─────────────────────────────────┘
```

**Slow Connection:**
- Show loading skeleton after 500ms
- Timeout after 30s
- Retry button on failure

---

### Invalid Input

**Special Characters:**
- Allow: Letters, numbers, spaces, hyphens, apostrophes
- Strip: SQL injection attempts, scripts
- Sanitize: Backend validation

**Empty Query:**
- Don't allow search with empty input
- Search button disabled if input empty

---

### No Recent Searches

**First-time users:**
- Hide "Recent Searches" section
- Show only Trending + Categories
- Populate after first search

---

### Filter Conflicts

**Example:** User selects:
- Time: Under 30 min
- Difficulty: Hard

If no results match:
```
Apply button: "Apply (0)"

On tap:
Toast: "No recipes match these filters. 
       Try adjusting your criteria."

Don't close bottom sheet
Allow user to modify filters
```

---

## Summary

**Search Screen Features:**
- ✅ Auto-focus search input on load
- ✅ Real-time autocomplete (300ms debounce)
- ✅ Grouped suggestions (recipes, ingredients, chefs)
- ✅ Recent searches (persistent, max 10)
- ✅ Clear all recent searches with confirmation
- ✅ Trending keywords (updated hourly)
- ✅ Browse by category shortcuts
- ✅ Advanced filters (7 types)
- ✅ Filter chips with remove option
- ✅ Filter badge indicator
- ✅ Results count with real-time updates
- ✅ Recipe grid (same as Home)
- ✅ Pagination/Load more
- ✅ Empty state with helpful actions
- ✅ "Ask AI" fallback
- ✅ Loading skeletons
- ✅ Error handling
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Full accessibility (screen reader, keyboard)
- ✅ Performance optimizations (caching, debounce, lazy load)

**Next:** Categories Screen
