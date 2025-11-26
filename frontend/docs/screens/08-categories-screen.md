# 📂 Categories Screen - Design Specification

## Overview
Categories Screen hiển thị tất cả các danh mục món ăn (categories) dưới dạng grid view, cho phép users dễ dàng khám phá recipes theo từng loại. Mỗi category hiển thị thumbnail, tên, và số lượng recipes.

**Access Point:** Explore Bottom Sheet → 📂 Categories

---

## Visual Layout

```
┌─────────────────────────────────────┐
│ [←]  Categories                     │ <- AppBar
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────┬─────────────────┐   │
│ │   [Image]   │     [Image]     │   │
│ │   gradient  │     gradient    │   │
│ │             │                 │   │
│ │ Món chính   │    Món phụ      │   │
│ │ 342 recipes │   156 recipes   │   │
│ └─────────────┴─────────────────┘   │
│                                     │
│ ┌─────────────┬─────────────────┐   │
│ │   [Image]   │     [Image]     │   │
│ │   gradient  │     gradient    │   │
│ │             │                 │   │
│ │ Tráng miệng │    Món chay     │   │
│ │ 98 recipes  │   203 recipes   │   │
│ └─────────────┴─────────────────┘   │
│                                     │
│ ┌─────────────┬─────────────────┐   │
│ │   [Image]   │     [Image]     │   │
│ │   gradient  │     gradient    │   │
│ │             │                 │   │
│ │ Món nước    │    Món khô      │   │
│ │ 178 recipes │   145 recipes   │   │
│ └─────────────┴─────────────────┘   │
│                                     │
│ ┌─────────────┬─────────────────┐   │
│ │   [Image]   │     [Image]     │   │
│ │   gradient  │     gradient    │   │
│ │             │                 │   │
│ │ Bánh & Bột  │    Canh         │   │
│ │ 89 recipes  │   112 recipes   │   │
│ └─────────────┴─────────────────┘   │
│                                     │
│ ┌─────────────┬─────────────────┐   │
│ │   [Image]   │     [Image]     │   │
│ │   gradient  │     gradient    │   │
│ │             │                 │   │
│ │ Dim Sum     │    Cà ri        │   │
│ │ 67 recipes  │   54 recipes    │   │
│ └─────────────┴─────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

---

## Components Detail

### 1. AppBar

```
┌─────────────────────────────────────┐
│ [←]  Categories                     │
└─────────────────────────────────────┘
```

**Back Button [←]:**
- Size: 40×40px
- Icon: Arrow left (24×24px, black)
- Position: Left, 8px margin
- Tap: Navigate back to Explore/Home

**Title:**
- Text: "Categories" (20px, bold, black)
- Position: Left of center (after back button)
- Alignment: Left

**AppBar:**
- Height: 56px
- Background: White
- Elevation: 2 (subtle shadow)
- Padding: 0 16px
- Fixed: Stays at top when scrolling

---

### 2. Category Card

```
┌─────────────────────┐
│                     │
│   [Background       │ <- Image with gradient
│    Image with       │    overlay
│    gradient         │
│    overlay]         │
│                     │
│   🍖                │ <- Emoji icon (optional)
│   Món chính         │ <- Category name (white)
│   342 recipes       │ <- Recipe count (white)
└─────────────────────┘
```

**Card Container:**
- Width: `(screen_width - 48px) / 2` (2 columns)
- Aspect ratio: 4:3 (slightly portrait)
- Border radius: 16px
- Margin: 8px between cards
- Shadow: Elevation 2
- Overflow: Hidden (for image)

**Background Image:**
- Full card coverage
- Object-fit: Cover (crop to fill)
- Representative dish photo from category
- High quality: 600×450px minimum

**Gradient Overlay:**
```
Linear gradient (top to bottom):
- 0%: rgba(0,0,0,0) - Transparent top
- 50%: rgba(0,0,0,0.2) - Subtle middle
- 100%: rgba(0,0,0,0.7) - Dark bottom
```
Purpose: Ensure text readability over image

**Emoji Icon (Optional):**
- Size: 32×32px
- Position: Top-left or center-top
- Margin: 12px from edges
- Examples:
  - 🍖 Món chính
  - 🥗 Món phụ
  - 🍰 Tráng miệng
  - 🌱 Món chay

**Category Name:**
- Font: 18px, bold, white
- Position: Bottom-left
- Padding: 16px left, 36px bottom
- Text shadow: 0 2px 4px rgba(0,0,0,0.8)
- Max lines: 2
- Overflow: Ellipsis
- Letter spacing: 0.5px

**Recipe Count:**
- Font: 14px, regular, white
- Position: Below name
- Padding: 16px left, 16px bottom
- Text shadow: 0 2px 4px rgba(0,0,0,0.8)
- Format: "[number] recipes" or "[number] món"
- Opacity: 0.9

**Hover/Press State:**
- Scale: 0.97 on press
- Duration: 100ms ease-out
- Brightness: Increase 10%
- Haptic feedback: Light impact

---

### 3. Grid Layout

**Container:**
- Padding: 16px (all sides)
- Background: Light gray #F5F5F5

**Grid Configuration:**
```
Mobile (<600px):
- Columns: 2
- Gap: 16px (horizontal & vertical)
- Card width: (screen_width - 48px) / 2

Tablet (600-1200px):
- Columns: 3
- Gap: 20px
- Card width: (screen_width - 64px) / 3

Desktop (>1200px):
- Columns: 4
- Gap: 24px
- Max width: 1200px (centered)
- Card max width: 280px
```

**Scroll Behavior:**
- Vertical scroll
- Smooth scrolling enabled
- Scroll to top: Tap status bar (iOS) or FAB (optional)

---

### 4. Category List (Full Set)

```
Main Categories:

1. 🍖 Món chính (Main Dishes)
   - Phở, Bún, Cơm, Mì
   - Recipe count: ~300-400

2. 🥗 Món phụ (Side Dishes)
   - Gỏi, Salad, Rau luộc
   - Recipe count: ~150-200

3. 🍰 Tráng miệng (Desserts)
   - Chè, Bánh ngọt, Hoa quả
   - Recipe count: ~80-120

4. 🌱 Món chay (Vegetarian)
   - All vegetarian/vegan dishes
   - Recipe count: ~200-250

5. 🍲 Món nước (Soups & Broths)
   - Canh, Súp, Lẩu
   - Recipe count: ~150-200

6. 🍗 Món khô (Dry Dishes)
   - Xào, Chiên, Nướng
   - Recipe count: ~150-180

7. 🍞 Bánh & Bột (Breads & Flour)
   - Bánh mì, Bánh bao, Bánh xèo
   - Recipe count: ~80-100

8. 🥣 Canh (Light Soups)
   - Canh chua, Canh rau
   - Recipe count: ~100-130

9. 🥟 Dim Sum & Snacks
   - Há cảo, Sủi cảo, Nem, Chả giò
   - Recipe count: ~60-80

10. 🍛 Cà ri & Stews
    - Cà ri gà, Bò kho
    - Recipe count: ~50-70

11. 🍚 Cơm (Rice Dishes)
    - Cơm rang, Cơm chiên, Cơm tấm
    - Recipe count: ~120-150

12. 🍜 Mì & Noodles
    - All noodle dishes
    - Recipe count: ~180-220

13. 🥤 Beverages
    - Nước uống, Sinh tố, Trà, Cà phê
    - Recipe count: ~40-60

14. 🌶️ Spicy Dishes
    - Món cay
    - Recipe count: ~100-130

15. 🎉 Party & Festive
    - Món ăn tiệc, ngày lễ
    - Recipe count: ~30-50

16. 🍢 Street Food
    - Món ăn vặt đường phố
    - Recipe count: ~80-100

Total: ~1500-2000 recipes across all categories
```

---

## Category Detail Screen

When user taps a category card:

```
┌─────────────────────────────────────┐
│ [←]  Món chính                 [⋮] │ <- AppBar
├─────────────────────────────────────┤
│                                     │
│ 342 recipes                    [⚙️] │ <- Results header
│                                     │
│ Sort: Popular                       │ <- Sort indicator
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Image 3:4]                     │ │
│ │                                 │ │
│ │                                 │ │
│ │ Phở Bò Hà Nội              [❤️] │ │
│ │ ⭐ 4.8  ⏱️ 60 min  🔥 Medium    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Image 3:4]                     │ │
│ │                                 │ │
│ │                                 │ │
│ │ Cơm Tấm Sài Gòn            [❤️] │ │
│ │ ⭐ 4.6  ⏱️ 45 min  🔥 Easy      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Image 3:4]                     │ │
│ │                                 │ │
│ │                                 │ │
│ │ Bún Chả Hà Nội             [❤️] │ │
│ │ ⭐ 4.7  ⏱️ 50 min  🔥 Medium    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Load More]                         │
│                                     │
└─────────────────────────────────────┘
```

**AppBar:**
- Back button [←]: Return to Categories screen
- Title: Category name (e.g., "Món chính")
- Menu [⋮]: Sort options

**Menu Options [⋮]:**
```
┌─────────────────────┐
│ Sort by:            │
│                     │
│ ● Popular           │ <- Default (most viewed/cooked)
│ ○ Highest Rated     │
│ ○ Newest            │
│ ○ Quickest          │ <- Shortest cooking time
│ ○ A-Z               │
│ ○ Z-A               │
└─────────────────────┘

Radio buttons: Single select
Close menu after selection
Results refresh with new sort
```

**Results Header:**
- Count: "342 recipes" (16px, bold, black)
- Filter icon: [⚙️] (24×24px, tap to open filter)
- Sort label: "Sort: Popular" (14px, gray)
- Padding: 16px
- Background: White
- Border bottom: 1px #F0F0F0

**Recipe Cards:**
- Same design as Home/Search screens
- Full width - 32px margin
- Image aspect ratio: 3:4
- Tap: Navigate to Recipe Detail

**Pagination:**
- Load: 20 recipes initially
- [Load More] button: Load next 20
- Or: Infinite scroll (auto-load on scroll bottom)

---

## User Flows

### Flow 1: Browse All Categories

```
User on Home screen
  ↓
Taps Explore button (bottom nav)
  ↓
Explore bottom sheet appears:
┌─────────────────────────────┐
│ [🔍 Recipes]                │
│ [📂 Categories]             │
└─────────────────────────────┘
  ↓
Taps [📂 Categories]
  ↓
Navigate to Categories screen
  ↓
Grid loads with all categories:
- Món chính (342 recipes)
- Món phụ (156 recipes)
- Tráng miệng (98 recipes)
- ... (12+ more)
  ↓
User scrolls to browse options
  ↓
Sees appealing category image
```

---

### Flow 2: Select Category & View Recipes

```
User on Categories screen
  ↓
Scrolls through grid
  ↓
Sees "Món chay" with vibrant veggie image
  ↓
Taps "Món chay" card
  ↓
Card scales down (press animation)
  ↓
Navigate to Category Detail screen
  ↓
AppBar shows: "[←] Món chay [⋮]"
Results header: "203 recipes [⚙️]"
Sort: "Popular" (default)
  ↓
Recipe grid loads (first 20 recipes)
  ↓
User scrolls through recipes
  ↓
Finds "Đậu hũ sốt cà chua"
  ↓
Taps recipe card
  ↓
Navigate to Recipe Detail screen
```

---

### Flow 3: Change Sort Order

```
User on Category Detail (Món chính)
  ↓
Current sort: Popular
  ↓
Wants to see highest rated first
  ↓
Taps menu [⋮] in AppBar
  ↓
Menu dropdown appears:
● Popular
○ Highest Rated
○ Newest
○ Quickest
○ A-Z
  ↓
Taps "Highest Rated"
  ↓
Radio button updates: ● Highest Rated
Menu closes
  ↓
Sort label updates: "Sort: Highest Rated"
  ↓
Recipes re-sort (5.0★ → 3.0★)
  ↓
Grid refreshes with new order
  ↓
Top recipes now show highest ratings:
- Recipe A: ⭐ 5.0
- Recipe B: ⭐ 4.9
- Recipe C: ⭐ 4.8
```

---

### Flow 4: Filter Within Category

```
User on Category Detail (Món chính)
  ↓
Results: 342 recipes
  ↓
Wants only quick meals (<30 min)
  ↓
Taps filter icon [⚙️]
  ↓
Filter bottom sheet opens (same as Search)
  ↓
User configures:
⏱️ Cooking Time: ● Under 30 min
🔥 Difficulty: [Easy] selected
  ↓
Apply button: "Apply (87)"
  ↓
Taps [Apply (87)]
  ↓
Bottom sheet closes
  ↓
Results update: "87 recipes"
  ↓
Filter chips appear:
[Under 30min ×] [Easy ×]
  ↓
Grid refreshes with filtered results
  ↓
All recipes now show ⏱️ ≤30 min
```

---

### Flow 5: Remove Filter Chip

```
User on filtered Category Detail
  ↓
Active filters:
[Under 30min ×] [Easy ×]
  ↓
Results: 87 recipes
  ↓
Wants to see all easy recipes (any time)
  ↓
Taps [×] on "Under 30min" chip
  ↓
Chip animates out (fade + slide)
  ↓
Results update: "145 recipes"
  ↓
Grid refreshes
  ↓
Only [Easy ×] chip remains
  ↓
Recipes now include all easy dishes
```

---

### Flow 6: Load More Recipes

```
User on Category Detail
  ↓
First 20 recipes loaded
  ↓
Scrolls to bottom
  ↓
Sees [Load More] button
  ↓
Taps [Load More]
  ↓
Button shows loading spinner
  ↓
API call: GET /api/v1/recipes/categories/mon-chinh?page=2
  ↓
Next 20 recipes load
  ↓
Append to grid (no page refresh)
  ↓
Button reappears if more pages exist
  ↓
User continues scrolling
```

---

## Backend Integration

### Categories List API

**Endpoint:** `GET /api/v1/recipes/categories`

**Request:**
```
GET /api/v1/recipes/categories
```

**Response:**
```json
{
  "success": true,
  "categories": [
    {
      "id": "cat_001",
      "name": "Món chính",
      "name_en": "Main Dishes",
      "slug": "mon-chinh",
      "description": "Các món ăn chính như phở, cơm, bún, mì...",
      "image": "https://cdn.example.com/categories/mon-chinh.jpg",
      "thumbnail": "https://cdn.example.com/categories/mon-chinh_thumb.jpg",
      "icon": "🍖",
      "recipe_count": 342,
      "order": 1,
      "color": "#FF6F00"
    },
    {
      "id": "cat_002",
      "name": "Món phụ",
      "name_en": "Side Dishes",
      "slug": "mon-phu",
      "description": "Các món ăn kèm như gỏi, nộm, salad...",
      "image": "https://cdn.example.com/categories/mon-phu.jpg",
      "thumbnail": "https://cdn.example.com/categories/mon-phu_thumb.jpg",
      "icon": "🥗",
      "recipe_count": 156,
      "order": 2,
      "color": "#4CAF50"
    },
    {
      "id": "cat_003",
      "name": "Tráng miệng",
      "name_en": "Desserts",
      "slug": "trang-mieng",
      "description": "Các món tráng miệng như chè, bánh ngọt...",
      "image": "https://cdn.example.com/categories/trang-mieng.jpg",
      "thumbnail": "https://cdn.example.com/categories/trang-mieng_thumb.jpg",
      "icon": "🍰",
      "recipe_count": 98,
      "order": 3,
      "color": "#E91E63"
    }
  ],
  "total": 16
}
```

**Caching:**
- Client: Cache for 1 hour
- CDN: Cache images indefinitely (versioned URLs)
- Server: Update recipe counts every 15 minutes

---

### Category Detail API

**Endpoint:** `GET /api/v1/recipes/categories/:slug`

**Example:** `GET /api/v1/recipes/categories/mon-chinh`

**Query Parameters:**
```
?sort=popular         # Sort: popular, rating, newest, time, name
&page=1              # Pagination (default: 1)
&limit=20            # Results per page (default: 20)
&time=under_30       # Filter: cooking time
&difficulty=easy     # Filter: difficulty
&rating=4            # Filter: minimum rating
&dietary=vegetarian  # Filter: dietary restrictions
```

**Request Example:**
```
GET /api/v1/recipes/categories/mon-chinh?sort=rating&page=1&limit=20&time=under_30
```

**Response:**
```json
{
  "success": true,
  "category": {
    "id": "cat_001",
    "name": "Món chính",
    "name_en": "Main Dishes",
    "slug": "mon-chinh",
    "description": "Các món ăn chính như phở, cơm, bún, mì...",
    "image": "https://cdn.example.com/categories/mon-chinh.jpg",
    "recipe_count": 342,
    "icon": "🍖"
  },
  "total": 87,
  "filtered_count": 87,
  "page": 1,
  "per_page": 20,
  "total_pages": 5,
  "sort": "rating",
  "active_filters": {
    "time": "under_30",
    "difficulty": null,
    "rating": null,
    "dietary": []
  },
  "recipes": [
    {
      "id": "recipe_045",
      "name": "Cơm Chiên Dương Châu",
      "slug": "com-chien-duong-chau",
      "image": "https://cdn.example.com/recipes/com-chien.jpg",
      "thumbnail": "https://cdn.example.com/recipes/com-chien_thumb.jpg",
      "rating": 4.9,
      "rating_count": 567,
      "time": 25,
      "difficulty": "easy",
      "servings": 2,
      "category": ["main_dish", "rice"],
      "dietary": [],
      "is_favorited": false
    },
    {
      "id": "recipe_089",
      "name": "Mì Xào Bò",
      "slug": "mi-xao-bo",
      "image": "https://cdn.example.com/recipes/mi-xao-bo.jpg",
      "thumbnail": "https://cdn.example.com/recipes/mi-xao-bo_thumb.jpg",
      "rating": 4.8,
      "rating_count": 423,
      "time": 20,
      "difficulty": "easy",
      "servings": 2,
      "category": ["main_dish", "noodles"],
      "dietary": [],
      "is_favorited": true
    }
  ]
}
```

---

### Sort Options

**Backend Implementation:**

```python
# Sort mapping
SORT_OPTIONS = {
    "popular": "view_count DESC, cook_count DESC",
    "rating": "rating DESC, rating_count DESC",
    "newest": "created_at DESC",
    "time": "cooking_time ASC",  # Quickest first
    "name": "name ASC",
    "name_desc": "name DESC"
}

# SQL Query example
query = f"""
    SELECT * FROM recipes
    WHERE category_id = %s
    ORDER BY {SORT_OPTIONS[sort_by]}
    LIMIT %s OFFSET %s
"""
```

---

## Performance Optimization

### Image Loading

**Strategy:**
- Lazy load: Load images when cards enter viewport
- Progressive: Load low-quality placeholder → full quality
- Sizes:
  - Thumbnail: 400×300px (mobile)
  - Full: 800×600px (desktop)
- Format: WebP with JPEG fallback
- CDN: Use content delivery network

**Placeholder:**
```
While loading:
┌─────────────────────┐
│                     │
│    [Gray box        │
│     with            │
│     shimmer         │
│     animation]      │
│                     │
│   Category Name     │
│   ### recipes       │
└─────────────────────┘
```

---

### Data Caching

**Client-Side (Flutter):**
```dart
// Cache categories list
final cachedCategories = await cacheManager.getFile(
  'categories.json',
  maxAge: Duration(hours: 1)
);

// Cache category images
CachedNetworkImage(
  imageUrl: category.image,
  cacheKey: 'cat_${category.id}',
  memCacheWidth: 400,
  memCacheHeight: 300,
);
```

**Server-Side (Redis):**
```python
# Cache categories list
redis.setex('categories:list', 3600, json.dumps(categories))

# Cache recipe counts (update every 15 min)
redis.setex(f'category:{slug}:count', 900, recipe_count)
```

---

### Pagination

**Infinite Scroll (Optional):**
```dart
ScrollController _scrollController = ScrollController();

void initState() {
  _scrollController.addListener(() {
    if (_scrollController.position.pixels >= 
        _scrollController.position.maxScrollExtent - 200) {
      // Load more when 200px from bottom
      _loadMoreRecipes();
    }
  });
}
```

**Load More Button (Recommended):**
- More control for users
- Better performance (user triggers load)
- Clear indication of more content

---

## Responsive Design

### Mobile (<600px)

```
┌─────────────────────────────────┐
│ [←] Categories                  │
├─────────────────────────────────┤
│ Padding: 16px                   │
│                                 │
│ ┌───────┬───────┐               │
│ │ Card  │ Card  │ Gap: 16px     │
│ │ 165px │ 165px │               │
│ └───────┴───────┘               │
│                                 │
│ ┌───────┬───────┐               │
│ │ Card  │ Card  │               │
│ └───────┴───────┘               │
│                                 │
└─────────────────────────────────┘

Grid: 2 columns
Card width: (screen_width - 48px) / 2
Gap: 16px
Aspect: 4:3
```

---

### Tablet (600-1200px)

```
┌─────────────────────────────────────┐
│ [←] Categories                      │
├─────────────────────────────────────┤
│ Padding: 24px                       │
│                                     │
│ ┌──────┬──────┬──────┐              │
│ │ Card │ Card │ Card │ Gap: 20px    │
│ │      │      │      │              │
│ └──────┴──────┴──────┘              │
│                                     │
│ ┌──────┬──────┬──────┐              │
│ │ Card │ Card │ Card │              │
│ └──────┴──────┴──────┘              │
│                                     │
└─────────────────────────────────────┘

Grid: 3 columns
Card width: (screen_width - 88px) / 3
Gap: 20px
Larger cards
```

---

### Desktop (>1200px)

```
┌─────────────────────────────────────────┐
│ [←] Categories                          │
├─────────────────────────────────────────┤
│        Max width: 1200px (centered)     │
│                                         │
│  ┌─────┬─────┬─────┬─────┐             │
│  │ Cat │ Cat │ Cat │ Cat │ Gap: 24px   │
│  │ 280 │ 280 │ 280 │ 280 │             │
│  └─────┴─────┴─────┴─────┘             │
│                                         │
│  ┌─────┬─────┬─────┬─────┐             │
│  │ Cat │ Cat │ Cat │ Cat │             │
│  └─────┴─────┴─────┴─────┘             │
│                                         │
└─────────────────────────────────────────┘

Grid: 4 columns
Card: Max 280px width, fixed
Gap: 24px
Centered layout
```

---

## Accessibility

### Screen Reader

**Announcements:**
- Category grid: "Categories grid, 16 items"
- Category card: "Món chính category, 342 recipes, button"
- Tap hint: "Double tap to view recipes in this category"
- Sort menu: "Sort by Popular, selected"
- Filter active: "2 filters active"

**Live Regions:**
```html
<div aria-live="polite">
  87 recipes found
</div>
```
Announces when results update

---

### Keyboard Navigation

**Tab Order:**
1. Back button
2. Category cards (row by row, left to right)
3. Sort menu (on detail screen)
4. Filter button
5. Recipe cards
6. Load more button

**Shortcuts:**
- Enter: Select category/recipe
- Esc: Close menu/filter
- Arrow keys: Navigate grid (optional)

---

### Focus Indicators

```css
.category-card:focus {
  outline: 3px solid #FF6F00;
  outline-offset: 4px;
}

.category-card:focus-visible {
  box-shadow: 0 0 0 4px rgba(255, 111, 0, 0.3);
}
```

**High Contrast:**
- Increase border thickness
- Brighter focus outlines
- Bold text weights

---

### Touch Targets

**Minimum sizes:**
- Category card: 48px minimum tap area
- Back button: 44×44px
- Menu items: 48px height
- Filter chips: 36px height (acceptable for secondary)

---

## Edge Cases & Error Handling

### Empty Category

```
┌─────────────────────────────────────┐
│ [←] Món fusion                 [⋮] │
├─────────────────────────────────────┤
│                                     │
│             🍽️                      │
│                                     │
│      No recipes yet                 │
│                                     │
│   This category is coming soon.     │
│   Check back later!                 │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Browse Other Categories     │   │
│   └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘

Icon: 🍽️ (60×60px)
Heading: 18px, bold
Description: 14px, gray
Button: Navigate back to Categories
```

---

### Loading State

**Initial load:**
```
┌─────────────────────────────────┐
│ [←] Categories                  │
├─────────────────────────────────┤
│                                 │
│ [Skeleton card] [Skeleton card] │
│ [Skeleton card] [Skeleton card] │
│ [Skeleton card] [Skeleton card] │
│                                 │
└─────────────────────────────────┘

Skeleton: Gray boxes with shimmer
Animation: Left-to-right shimmer
Duration: Until data loads
```

---

### Network Error

```
┌─────────────────────────────────┐
│ [←] Categories                  │
├─────────────────────────────────┤
│                                 │
│            ⚠️                   │
│                                 │
│      Failed to load             │
│      categories                 │
│                                 │
│   Please check your internet    │
│   connection and try again.     │
│                                 │
│   ┌─────────────────────────┐   │
│   │ Retry                   │   │
│   └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

---

### Image Load Failure

```
┌─────────────────────┐
│                     │
│    [Fallback        │
│     solid color     │
│     background      │
│     #FF6F00]        │
│                     │
│   🍖                │
│   Món chính         │
│   342 recipes       │
└─────────────────────┘

Use category color as fallback
Show emoji icon (larger, centered)
Text remains readable
```

---

## Summary

**Categories Screen Features:**
- ✅ Grid layout (2/3/4 columns responsive)
- ✅ Category cards with images, names, counts
- ✅ Gradient overlays for text readability
- ✅ Emoji icons for visual identity
- ✅ Tap to navigate to category detail
- ✅ Category detail with recipe list
- ✅ Sort options (6 types)
- ✅ Filter support (same as Search)
- ✅ Active filter chips
- ✅ Pagination (Load More button)
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Lazy image loading
- ✅ Client & server caching
- ✅ Loading skeletons
- ✅ Error handling (empty, network, images)
- ✅ Full accessibility (screen reader, keyboard, focus)
- ✅ Touch targets optimized
- ✅ Performance optimizations

