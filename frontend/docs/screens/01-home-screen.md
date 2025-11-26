# 🏠 Home Screen - Design Specification

## Overview
Home Screen là điểm trung tâm của ứng dụng, cho phép users browse và discover recipes nhanh chóng với personalized experience.

---

## Visual Layout

```
┌─────────────────────────────────────────────┐
│ ┌─────┐                          ┌────┐    │
│ │ 👤  │  Xin chào, Minh!         │ 🔔 │    │ <- AppBar (sticky)
│ └─────┘                          └────┘    │    Height: 60px
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ 🔍  Tìm món ăn, nguyên liệu...  [🎙️]│  │ <- Search Bar
│  └──────────────────────────────────────┘  │    Height: 56px
│                                             │    Margin: 16px
├─────────────────────────────────────────────┤
│ ☰ Danh mục                                  │ <- Section Header
│                                             │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐           │
│ │ 🍜  │ │ 🍲  │ │ 🥘  │ │ 🍖  │ >>>       │ <- Category Carousel
│ │Món  │ │Món  │ │Món  │ │BBQ  │           │    Horizontal scroll
│ │Việt │ │Á    │ │Âu   │ │     │           │    Height: 100px
│ └─────┘ └─────┘ └─────┘ └─────┘           │
│                                             │
├─────────────────────────────────────────────┤
│ ⭐ Gợi ý cho bạn                             │ <- Section Header
│                                             │
│ ┌─────────────┐  ┌─────────────┐          │
│ │   [Image]   │  │   [Image]   │          │
│ │             │  │             │          │ <- Recipe Grid
│ │ Phở Bò Hà Nội│  │ Bún Chả HN  │          │    2 columns
│ │ ⭐ 4.8 • 45p │  │ ⭐ 4.6 • 30p │          │    Aspect ratio 3:4
│ └─────────────┘  └─────────────┘          │
│                                             │
│ ┌─────────────┐  ┌─────────────┐          │
│ │   [Image]   │  │   [Image]   │          │
│ │ Cơm Tấm SG  │  │ Bánh Mì     │          │
│ │ ⭐ 4.9 • 25p │  │ ⭐ 4.7 • 15p │          │
│ └─────────────┘  └─────────────┘          │
│                                             │
│         [Load more...]                      │
│                                             │
├─────────────────────────────────────────────┤
│ [🏠]  [🧭]  [💬]  [📷]  [👤]               │ <- Bottom Navigation
│ Home Explore Chat Camera Profile           │    Height: 70px
└─────────────────────────────────────────────┘
```

---

## Components Detail

### 1. AppBar
**Height:** 60px  
**Background:** White (light mode) / Dark (#1E1E1E in dark mode)  
**Padding:** 16px horizontal, 8px vertical

**Elements:**
- **Avatar** (left): 48×48px circle
  - User profile image
  - Green online status dot (12×12px, bottom-right)
  - Tap: Navigate to Profile
- **Greeting Text** (center-left):
  - Top line: Time-based greeting (12px, gray)
    - "Chào buổi sáng" (< 12h)
    - "Chào buổi chiều" (12h-18h)
    - "Chào buổi tối" (> 18h)
  - Bottom line: User name (16px, bold)
- **Notification Bell** (right):
  - Icon: 24×24px
  - Badge: Red circle with count (if > 0)
  - Tap: Navigate to Notifications

---

### 2. Search Bar
**Height:** 56px  
**Margin:** 16px horizontal, 12px vertical  
**Border Radius:** 28px (pill shape)  
**Background:** Light gray (#F5F5F5)  
**Shadow:** Subtle (0 2px 8px rgba(0,0,0,0.05))

**Elements:**
- **Search Icon** (left): 24×24px, gray, 20px from edge
- **Placeholder Text**: "Tìm món ăn, nguyên liệu..." (16px, gray #616161)
- **Voice Button** (right):
  - 40×40px circular button
  - Orange background (#FF6F00)
  - White mic icon (20×20px)
  - 8px margin from right edge

**Behavior:**
- **Tap anywhere**: Navigate to full Search Screen
- **Tap mic**: Start voice search immediately
- **Non-editable** on Home (prevents keyboard disruption)

---

### 3. Category Carousel
**Section Header:**
- Title: "Danh mục" (18px, bold)
- "Xem tất cả" link (14px, orange)
- Padding: 16px horizontal, 8px vertical

**Carousel:**
- **Height:** 100px
- **Scroll:** Horizontal, momentum
- **Padding:** 12px horizontal

**Category Card:**
- **Size:** 80×100px
- **Margin:** 4px between cards
- **Border Radius:** 16px
- **Border:** 2px solid

**States:**
- **Unselected:**
  - Background: White
  - Border: Gray (#E0E0E0)
  - Text: Black
- **Selected:**
  - Background: Orange (#FF6F00)
  - Border: Orange
  - Text: White
  - Shadow: 0 4px 8px rgba(255,111,0,0.3)

**Content:**
- Emoji: 32px (top, centered)
- Label: 12px, bold, 2 lines max (bottom)

**Default Categories:**
```
🍽️ Tất cả
🍜 Món Việt
🍲 Món Á
🥘 Món Âu
🍖 BBQ
🍰 Tráng miệng
🥗 Món chay
⚡ Nhanh
```

**Interaction:**
- Tap category → Filter recipe grid
- Visual feedback: Instant state change
- Auto-scroll recipe grid into view

---

### 4. Recipe Grid
**Section Header:**
- Title: "Gợi ý cho bạn" (or selected category name)
- 18px, bold
- Padding: 16px horizontal

**Grid Layout:**
- **Columns:** 2 (mobile)
- **Gap:** 16px (horizontal & vertical)
- **Padding:** 16px all sides
- **Child Aspect Ratio:** 0.75 (3:4)

**Loading States:**
- Shimmer effect for placeholders
- Skeleton cards during fetch

---

### 5. Recipe Card
**Dimensions:**
- Width: (Screen width - 48px) / 2
- Height: Width / 0.75
- Border Radius: 16px
- Shadow: 0 4px 12px rgba(0,0,0,0.08)

**Structure:**
```
┌─────────────────┐
│                 │ <- Image (75% height)
│   [Image]       │    Hero animation tag
│                 │
│─────────────────│
│ Title           │ <- Info (25% height)
│ ⭐ 4.8  ⏱️ 45p │    Metadata
└─────────────────┘
```

**Image Section (75%):**
- **Image:**
  - Full width
  - Fit: Cover
  - Border radius: Top 16px only
  - Lazy loading with cache
  - Placeholder: Shimmer effect
- **Difficulty Badge** (top-right, 8px margin):
  - Padding: 8px horizontal, 4px vertical
  - Border radius: 12px
  - Font: 10px, bold, white
  - Colors:
    - Easy: Green (#4CAF50)
    - Medium: Orange (#FF9800)
    - Hard: Red (#F44336)
- **Favorite Button** (top-left, 8px margin):
  - 32×32px circular button
  - White background
  - Icon: Heart (20×20px)
    - Filled red (if favorited)
    - Outlined red (if not)
  - Tap: Toggle favorite (optimistic update)

**Info Section (25%):**
- **Padding:** 12px all sides
- **Title:**
  - Font: 14px, bold
  - Max lines: 2
  - Overflow: Ellipsis
  - Color: Black (#212121)
- **Metadata Row:**
  - Icon + text pairs
  - Font: 12px
  - Gap: 8px between pairs
  - **Rating:**
    - Star icon: 14×14px, amber
    - Text: "4.8" (black)
  - **Time:**
    - Clock icon: 14×14px, gray
    - Text: "45p" (gray #757575)

**Interactions:**
- **Tap card:** Navigate to Recipe Detail (Hero animation)
- **Tap heart:** Toggle favorite
- **Press state:** Scale 0.98, shadow increase

---

### 6. Bottom Navigation
**Height:** 70px  
**Background:** White with top shadow  
**Fixed:** Always visible (overlays content)

**Items (5):**
```
┌──────┬──────┬──────┬──────┬──────┐
│  🏠  │  🧭  │  💬  │  📷  │  👤  │
│ Home │Explore│ Chat │Camera│Profile│
└──────┴──────┴──────┴──────┴──────┘
```

**Item Specs:**
- Width: 20% each (equal distribution)
- Height: 70px
- Tap target: Full item area

**Icon:**
- Size: 24×24px
- Colors:
  - Active: Orange (#FF6F00)
  - Inactive: Gray (#9E9E9E)

**Label:**
- Font: 11px
- Position: Below icon (4px gap)
- Colors:
  - Active: Orange, bold
  - Inactive: Gray, medium

**Active Indicator:**
- None (color change only)

**Items Detail:**
1. **🏠 Home** - Current screen
2. **🧭 Explore** - Opens bottom sheet (2 options)
3. **💬 Chat** - Navigate to AI Chat
4. **📷 Camera** - Navigate to Camera/Scan
5. **👤 Profile** - Navigate to Profile

---

## User Flows

### Flow 1: Browse Recipes
```
User lands on Home
  ↓
Sees personalized greeting
  ↓
Scrolls through categories
  ↓
Taps "Món Việt"
  ↓
Recipe grid updates (filtered)
  ↓
Taps recipe card
  ↓
Navigate to Recipe Detail (Hero animation)
```

### Flow 2: Voice Search
```
User on Home
  ↓
Taps mic icon on search bar
  ↓
Voice recording starts (waveform animation)
  ↓
User says: "Tìm món ăn từ gà"
  ↓
STT converts to text
  ↓
Navigate to Search screen with query
  ↓
Shows filtered results
```

### Flow 3: Toggle Favorite
```
User browsing recipe grid
  ↓
Taps heart icon on recipe card
  ↓
Optimistic update (UI changes immediately)
  ↓
API call in background
  ↓
If success: Keep state
If fail: Revert + show snackbar error
```

### Flow 4: Category Filtering
```
User on Home (default: "Tất cả")
  ↓
Horizontal scrolls category carousel
  ↓
Taps "BBQ" category
  ↓
Category card state changes (orange bg + shadow)
  ↓
Recipe grid animates (fade out old, fade in new)
  ↓
Scroll view auto-scrolls to recipe grid
  ↓
Recipes filtered to BBQ category only
```

---

## Responsive Design

### Mobile (<600px)
- Recipe grid: 2 columns
- Category carousel: 3-4 visible
- Search bar: Full width - 32px margin
- Bottom nav: Fixed, 5 items

### Tablet (600-1200px)
- Recipe grid: 3 columns
- Category carousel: 5-6 visible
- Search bar: Max width 600px, centered
- Bottom nav: Fixed, 5 items

### Desktop (>1200px)
- Recipe grid: 4 columns
- Category carousel: All visible (no scroll)
- Search bar: Max width 800px, centered
- Bottom nav: Replaced by side rail

---

## Performance Optimizations

### Image Loading
1. **Lazy Loading:** Only load images in viewport
2. **Progressive Loading:** LQIP (blur-up technique)
3. **Caching:** Aggressive memory + disk cache
4. **Compression:** WebP format, optimized sizes

### List Performance
1. **Pagination:** Load 20 recipes initially
2. **Infinite Scroll:** Load +20 when 80% scrolled
3. **Virtual Scrolling:** Recycle off-screen cards
4. **Debouncing:** Category selection (300ms)

### State Management
1. **Category Filter:** Instant local state update
2. **Favorites:** Optimistic updates
3. **Recipe Cache:** Keep last 3 category results

---

## Accessibility

### Screen Reader
- Avatar: "User profile, [Name]"
- Search bar: "Search recipes, button"
- Voice button: "Voice search, button"
- Category: "Vietnamese food, button, selected"
- Recipe card: "[Name], rated 4.8 stars, 45 minutes cooking time"
- Bottom nav: "Home, active" / "Explore, button"

### Keyboard Navigation
- Tab through: Avatar → Search → Categories → Recipes → Bottom Nav
- Arrow keys: Navigate category carousel
- Enter/Space: Activate focused element

### Visual
- High contrast mode support
- Min tap targets: 48×48px
- Color not sole indicator (text + icons)
- Focus indicators: 2px orange outline

---

## Edge Cases

### No Internet
```
Show cached recipes (if available)
Display banner: "Offline mode - Showing cached recipes"
Disable: Category filtering, Search, Voice
Enable: View cached recipe details
```

### Empty Category
```
User selects category with 0 recipes
  ↓
Show empty state:
┌─────────────────────────────────┐
│        🍽️                       │
│  Chưa có món ăn nào              │
│  trong danh mục này              │
│                                  │
│  [Xem danh mục khác]            │
└─────────────────────────────────┘
```

### API Error
```
Recipe fetch fails
  ↓
Show error widget:
┌─────────────────────────────────┐
│        ⚠️                        │
│  Không thể tải công thức         │
│                                  │
│  [Thử lại]                       │
└─────────────────────────────────┘
```

### Slow Network
```
Show skeleton screens during load
Progress indicator in AppBar
Timeout: 30 seconds
Fallback: Show cached + error message
```

---

## State Management (Riverpod)

### Providers
```dart
// Selected category
final selectedCategoryProvider = StateProvider<String>((ref) => 'all');

// Recipes by category
final recipesByCategoryProvider = FutureProvider.family<List<Recipe>, String>(
  (ref, categoryId) async {
    final repository = ref.read(recipeRepositoryProvider);
    return repository.getRecipesByCategory(categoryId);
  },
);

// User profile
final userProvider = StreamProvider<User>((ref) {
  final repository = ref.read(userRepositoryProvider);
  return repository.getUserStream();
});

// Notification count
final notificationCountProvider = StreamProvider<int>((ref) {
  final repository = ref.read(notificationRepositoryProvider);
  return repository.getUnreadCountStream();
});

// Favorites
final favoriteProvider = StateNotifierProvider<FavoriteNotifier, Set<String>>(
  (ref) => FavoriteNotifier(ref.read(recipeRepositoryProvider)),
);
```

---

## Design Tokens

### Colors
```
Primary: #FF6F00 (Orange)
Primary Dark: #E65100
Secondary: #4CAF50 (Green)
Background: #FFFFFF (Light) / #121212 (Dark)
Surface: #FFFFFF (Light) / #1E1E1E (Dark)
Error: #F44336
Text Primary: #212121 (Light) / #FFFFFF (Dark)
Text Secondary: #757575 (Light) / #BDBDBD (Dark)
Divider: #E0E0E0 (Light) / #424242 (Dark)
```

### Typography
```
Title Large: 20px, Bold (Poppins/Montserrat)
Title Medium: 18px, Bold
Title Small: 16px, Bold
Body Large: 16px, Medium (Roboto/Inter)
Body Medium: 14px, Medium
Body Small: 12px, Regular
Label: 11px, Medium
```

### Spacing
```
xs: 4px
sm: 8px
md: 12px
lg: 16px
xl: 20px
2xl: 24px
3xl: 32px
```

### Border Radius
```
Small: 8px
Medium: 12px
Large: 16px
XLarge: 24px
Pill: 28px (half of height)
Circle: 50%
```

### Elevation
```
Level 0: None
Level 2: 0 2px 4px rgba(0,0,0,0.08)
Level 4: 0 4px 8px rgba(0,0,0,0.12)
Level 8: 0 4px 12px rgba(0,0,0,0.15)
Level 16: 0 8px 24px rgba(0,0,0,0.2)
```

---

## Notes
- Home screen is the default landing after authentication
- Pull-to-refresh supported for recipe grid
- Haptic feedback on button taps (light impact)
- Smooth animations: 200-300ms ease-out curves
- Content personalized based on user history & preferences
