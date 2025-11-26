# 🗺️ Navigation Flow - Tổng quan luồng điều hướng giữa các màn hình

## Overview
Tài liệu này mô tả chi tiết cách các màn hình kết nối với nhau, navigation patterns, deep linking, và user journeys trong ứng dụng AI Cooking Assistant.

---

## Architecture Overview

### Navigation Strategy
- **Pattern:** Nested Navigation với Bottom Navigation Bar
- **Router:** go_router 14.0 (declarative routing)
- **Deep Linking:** Hỗ trợ đầy đủ (web URLs, app links)
- **State Management:** Riverpod 2.x cho navigation state
- **Transition Animations:** Custom transitions cho mỗi route type

---

## Main Navigation Structure

```
App Root
│
├─ Bottom Navigation (Main Shell)
│  ├─ Home Tab (/)
│  ├─ Explore Tab (Bottom Sheet overlay)
│  ├─ Chat Tab (/chat)
│  ├─ Camera Tab (/camera)
│  └─ Profile Tab (/profile)
│
├─ Modal Screens (Full screen)
│  ├─ Recipe Detail (/recipe/:id)
│  ├─ Cooking Mode (/recipe/:id/cooking)
│  ├─ Search (/search)
│  └─ Categories (/categories)
│
└─ Overlays
   ├─ Explore Bottom Sheet
   ├─ Filter Bottom Sheet
   └─ Various dialogs/modals
```

---

## Complete Navigation Map

```
                        ┌─────────────────┐
                        │   App Launch    │
                        └────────┬────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Bottom Navigation Bar  │
                    │  (Persistent Shell)     │
                    └────────────┬────────────┘
                                 │
        ┌────────────┬───────────┼──────────┬────────────┐
        │            │           │          │            │
   ┌────▼────┐  ┌───▼───┐  ┌───▼───┐  ┌───▼────┐  ┌───▼─────┐
   │  HOME   │  │EXPLORE│  │ CHAT  │  │CAMERA  │  │ PROFILE │
   │ Screen  │  │ Sheet │  │   AI  │  │ Screen │  │ Screen  │
   └────┬────┘  └───┬───┘  └───┬───┘  └───┬────┘  └───┬─────┘
        │           │          │          │            │
        │      ┌────┴────┐     │          │            │
        │      │         │     │          │            │
        │  ┌───▼───┐ ┌──▼───┐ │          │            │
        │  │SEARCH │ │CATEG.│ │          │            │
        │  │Screen │ │Screen│ │          │            │
        │  └───┬───┘ └──┬───┘ │          │            │
        │      │        │     │          │            │
        └──────┴────────┴─────┴──────────┴────────────┘
                        │
                 ┌──────▼──────┐
                 │   RECIPE    │
                 │   DETAIL    │
                 │   Screen    │
                 └──────┬──────┘
                        │
                 ┌──────▼──────┐
                 │   COOKING   │
                 │     MODE    │
                 │   Screen    │
                 └─────────────┘
```

---

## Screen Relationships

### 01. Home Screen → Connections

**From Home Screen, users can navigate to:**

```
HOME SCREEN
│
├─ Tap Search Bar
│  └─> SEARCH SCREEN (/search)
│
├─ Tap Recipe Card
│  └─> RECIPE DETAIL (/recipe/:id)
│
├─ Tap Category in Carousel
│  └─> CATEGORIES SCREEN (/categories?selected=:id)
│
├─ Tap "Xem tất cả" (View all) in Category section
│  └─> CATEGORIES SCREEN (/categories)
│
├─ Tap Explore Button (Bottom Nav)
│  └─> EXPLORE BOTTOM SHEET (overlay)
│     ├─ Tap "Tìm kiếm recipes"
│     │  └─> SEARCH SCREEN (/search)
│     └─ Tap "Duyệt theo danh mục"
│        └─> CATEGORIES SCREEN (/categories)
│
├─ Tap Chat Button (Bottom Nav)
│  └─> CHAT AI SCREEN (/chat)
│
├─ Tap Camera Button (Bottom Nav)
│  └─> CAMERA SCREEN (/camera)
│
└─ Tap Profile Button (Bottom Nav)
   └─> PROFILE SCREEN (/profile)
```

**Route Configuration:**
```dart
GoRoute(
  path: '/',
  name: 'home',
  builder: (context, state) => HomeScreen(),
)
```

---

### 02. Explore Bottom Sheet → Connections

**From Explore Bottom Sheet:**

```
EXPLORE BOTTOM SHEET (Overlay on current screen)
│
├─ Tap "🔍 Tìm kiếm recipes"
│  ├─ Dismiss sheet
│  └─> SEARCH SCREEN (/search)
│
└─ Tap "📂 Duyệt theo danh mục"
   ├─ Dismiss sheet
   └─> CATEGORIES SCREEN (/categories)
```

**Implementation:**
```dart
// Not a route, shown as BottomSheet modal
showModalBottomSheet(
  context: context,
  builder: (context) => ExploreBottomSheet(),
);
```

---

### 03. Recipe Detail Screen → Connections

**From Recipe Detail Screen:**

```
RECIPE DETAIL SCREEN (/recipe/:id)
│
├─ Tap "▶️ Bắt đầu nấu" (Start Cooking)
│  └─> COOKING MODE (/recipe/:id/cooking)
│
├─ Tap "🎙️ Đọc hướng dẫn" (Read Instructions)
│  └─> TEXT-TO-SPEECH (plays audio, stays on screen)
│
├─ Tap "💬 Hỏi AI về món này"
│  └─> CHAT AI SCREEN (/chat?context=recipe&id=:id)
│     [Chat pre-filled with recipe context]
│
├─ Tap Author/Chef Name
│  └─> CHEF PROFILE (/chef/:id) [Future feature]
│
├─ Tap Similar Recipe Card
│  └─> RECIPE DETAIL (/recipe/:other_id)
│
├─ Tap Category Tag
│  └─> CATEGORIES SCREEN (/categories?selected=:id)
│
├─ Tap Back Button / Swipe
│  └─> Previous Screen (Stack pop)
│
└─ Tap Share Button
   └─> SHARE SHEET (native dialog)
```

**Route Configuration:**
```dart
GoRoute(
  path: '/recipe/:id',
  name: 'recipe-detail',
  builder: (context, state) {
    final recipeId = state.pathParameters['id']!;
    return RecipeDetailScreen(recipeId: recipeId);
  },
  routes: [
    GoRoute(
      path: 'cooking',
      name: 'cooking-mode',
      builder: (context, state) {
        final recipeId = state.pathParameters['id']!;
        return CookingModeScreen(recipeId: recipeId);
      },
    ),
  ],
)
```

---

### 04. Chat AI Screen → Connections

**From Chat AI Screen:**

```
CHAT AI SCREEN (/chat)
│
├─ Tap Recipe Card in Chat Response
│  └─> RECIPE DETAIL (/recipe/:id)
│
├─ Tap "📸" Image Upload Button
│  ├─> CAMERA PICKER (native)
│  └─> Send image to chat (stay on screen)
│
├─ Tap Voice Button 🎙️
│  ├─> VOICE LISTENING (overlay)
│  └─> Convert to text (stay on screen)
│
├─ Wake Word "Hey Chef" / "Này Chef"
│  └─> AUTO ACTIVATE VOICE (overlay)
│
├─ Tap Suggested Question Chip
│  └─> Auto-fill input, send message (stay on screen)
│
├─ Tap "Xem công thức" (View Recipe) in AI response
│  └─> RECIPE DETAIL (/recipe/:id)
│
└─ Tap Home/Other Bottom Nav
   └─> Navigate to respective tab
```

**Route Configuration:**
```dart
GoRoute(
  path: '/chat',
  name: 'chat',
  builder: (context, state) {
    final context = state.queryParameters['context'];
    final contextId = state.queryParameters['id'];
    return ChatAIScreen(
      initialContext: context,
      contextId: contextId,
    );
  },
)
```

---

### 05. Camera Screen → Connections

**From Camera Screen:**

```
CAMERA SCREEN (/camera)
│
├─ Capture Photo
│  └─> PREVIEW MODE (same screen)
│     ├─ Tap "Retake"
│     │  └─> Back to CAMERA MODE
│     └─ Tap "Use Photo"
│        └─> RESULTS MODE (same screen)
│           ├─ Tap "Tìm recipes" (Find Recipes)
│           │  └─> SEARCH SCREEN (/search?ingredients=...)
│           │     [Pre-filled with detected ingredients]
│           ├─ Tap "Hỏi AI" (Ask AI)
│           │  └─> CHAT AI SCREEN (/chat?image=...)
│           │     [Pre-filled with image & ingredients]
│           └─ Tap "✓ Done"
│              └─> HOME SCREEN (/)
│
├─ Tap "📁 Gallery" Button
│  ├─> IMAGE PICKER (native)
│  └─> PREVIEW MODE (same screen)
│
└─ Tap Home/Other Bottom Nav
   └─> Navigate to respective tab
```

**Route Configuration:**
```dart
GoRoute(
  path: '/camera',
  name: 'camera',
  builder: (context, state) => CameraScreen(),
)
```

---

### 06. Profile Screen → Connections

**From Profile Screen:**

```
PROFILE SCREEN (/profile)
│
├─ Tap "Saved Recipes" Card
│  └─> SAVED RECIPES LIST (/profile/saved)
│     └─ Tap Recipe → RECIPE DETAIL
│
├─ Tap "Cooked Recipes" Card
│  └─> COOKING HISTORY (/profile/history)
│     └─ Tap Recipe → RECIPE DETAIL
│
├─ Tap "My Lists" Card
│  └─> RECIPE LISTS (/profile/lists)
│     └─ Tap List → LIST DETAIL
│        └─ Tap Recipe → RECIPE DETAIL
│
├─ Tap "AI Personality" Section
│  └─> AI PERSONALITY SETTINGS (expand/collapse)
│     ├─ Tap Personality Option
│     │  └─> PERSONALITY PREVIEW SHEET (bottom sheet)
│     │     ├─ Tap "Try it"
│     │     │  └─> CHAT AI SCREEN (/chat?personality=...)
│     │     └─ Tap "Select"
│     │        └─> Save & close (stay on profile)
│     └─ Tap "Test in Chat"
│        └─> CHAT AI SCREEN (/chat)
│
├─ Tap "Dietary Preferences"
│  └─> PREFERENCES EDITOR (bottom sheet or inline)
│
├─ Tap "Voice Settings"
│  └─> VOICE SETTINGS SHEET (bottom sheet)
│
├─ Tap "Language"
│  └─> LANGUAGE SELECTOR (bottom sheet)
│
├─ Tap "Notifications"
│  └─> NOTIFICATION SETTINGS (/profile/notifications)
│
├─ Tap "Privacy & Security"
│  └─> PRIVACY SETTINGS (/profile/privacy)
│
├─ Tap "Help & Feedback"
│  └─> HELP CENTER (/help)
│
└─ Tap "Sign Out"
   └─> CONFIRMATION DIALOG
      └─ Confirm → LOGIN SCREEN (/login)
```

**Route Configuration:**
```dart
GoRoute(
  path: '/profile',
  name: 'profile',
  builder: (context, state) => ProfileScreen(),
  routes: [
    GoRoute(
      path: 'saved',
      name: 'saved-recipes',
      builder: (context, state) => SavedRecipesScreen(),
    ),
    GoRoute(
      path: 'history',
      name: 'cooking-history',
      builder: (context, state) => CookingHistoryScreen(),
    ),
    GoRoute(
      path: 'lists',
      name: 'recipe-lists',
      builder: (context, state) => RecipeListsScreen(),
    ),
    GoRoute(
      path: 'notifications',
      name: 'notifications-settings',
      builder: (context, state) => NotificationsSettingsScreen(),
    ),
    GoRoute(
      path: 'privacy',
      name: 'privacy-settings',
      builder: (context, state) => PrivacySettingsScreen(),
    ),
  ],
)
```

---

### 07. Search Screen → Connections

**From Search Screen:**

```
SEARCH SCREEN (/search)
│
├─ Tap Search Result (Recipe Card)
│  └─> RECIPE DETAIL (/recipe/:id)
│
├─ Tap Filter Button (🎛️)
│  └─> FILTER BOTTOM SHEET (overlay)
│     └─ Apply Filters → Refresh results (stay on search)
│
├─ Tap Category Filter Chip
│  └─> CATEGORIES SCREEN (/categories?selected=:id)
│
├─ Tap Recent Search Item
│  └─> Execute search (stay on screen, update query)
│
├─ Tap Trending Keyword
│  └─> Execute search (stay on screen, update query)
│
├─ Tap "Browse by Category"
│  └─> CATEGORIES SCREEN (/categories)
│
├─ Tap "💬 Ask AI Instead" (Empty State)
│  └─> CHAT AI SCREEN (/chat?query=...)
│
├─ Tap Voice Search Button (🎙️)
│  └─> VOICE LISTENING (overlay)
│     └─> Convert to text, execute search
│
└─ Tap Back Button
   └─> Previous Screen (Stack pop)
```

**Route Configuration:**
```dart
GoRoute(
  path: '/search',
  name: 'search',
  builder: (context, state) {
    final query = state.queryParameters['q'];
    final ingredients = state.queryParameters['ingredients'];
    return SearchScreen(
      initialQuery: query,
      initialIngredients: ingredients?.split(','),
    );
  },
)
```

---

### 08. Categories Screen → Connections

**From Categories Screen:**

```
CATEGORIES SCREEN (/categories)
│
├─ Tap Category Card
│  └─> CATEGORY DETAIL VIEW (same screen, or push new route)
│     ├─ Tap Sort Menu
│     │  └─> SORT OPTIONS SHEET (bottom sheet)
│     │     └─> Apply sort (stay on screen)
│     ├─ Tap Filter Button
│     │  └─> FILTER BOTTOM SHEET (overlay)
│     │     └─> Apply filters (stay on screen)
│     ├─ Tap Recipe Card
│     │  └─> RECIPE DETAIL (/recipe/:id)
│     └─ Tap Back
│        └─> CATEGORIES GRID (same screen or pop)
│
├─ Tap Search Icon
│  └─> SEARCH SCREEN (/search)
│
└─ Tap Back Button
   └─> Previous Screen (Stack pop)
```

**Route Configuration:**
```dart
GoRoute(
  path: '/categories',
  name: 'categories',
  builder: (context, state) {
    final selectedId = state.queryParameters['selected'];
    return CategoriesScreen(selectedCategoryId: selectedId);
  },
)
```

---

### 09. Cooking Mode Screen → Connections

**From Cooking Mode Screen:**

```
COOKING MODE SCREEN (/recipe/:id/cooking)
│
├─ Tap [×] Exit Button
│  └─> EXIT CONFIRMATION DIALOG
│     ├─ Cancel → Stay in Cooking Mode
│     └─ Exit → RECIPE DETAIL (/recipe/:id)
│        [Progress saved, timers continue in background]
│
├─ Tap [⋮] Options Menu
│  └─> OPTIONS MENU SHEET
│     ├─ Tap "📋 View Ingredients"
│     │  └─> INGREDIENTS SHEET (bottom sheet)
│     │     └─ Close → Back to Cooking Mode
│     ├─ Tap "⏱️ Active Timers"
│     │  └─> TIMERS MANAGER SHEET (bottom sheet)
│     │     └─ Close → Back to Cooking Mode
│     ├─ Tap "🔄 Restart from Beginning"
│     │  └─> CONFIRMATION DIALOG
│     │     └─ Confirm → Reset to Step 1
│     ├─ Tap "📱 View Full Recipe"
│     │  └─> Exit to RECIPE DETAIL (/recipe/:id)
│     └─ Tap "❌ Exit Cooking Mode"
│        └─> EXIT CONFIRMATION DIALOG
│           └─ Exit → RECIPE DETAIL
│
├─ Complete All Steps → Tap [✓ Done]
│  └─> COMPLETION SCREEN (same route, completion view)
│     ├─ Tap Stars (Rating)
│     │  └─> Save rating (stay on completion)
│     ├─ Tap "📸 Share Your Creation"
│     │  └─> SHARE SHEET (native)
│     │     └─> Back to Completion Screen
│     ├─ Tap "🔙 Back to Recipe"
│     │  └─> RECIPE DETAIL (/recipe/:id)
│     │     [Shows "✓ Cooked" badge & rating]
│     └─ Tap "🔍 Find Similar Recipes"
│        └─> SEARCH SCREEN (/search?similar=:id)
│
└─ Background Behavior
   ├─ User exits app → Timers continue (foreground service)
   ├─ Timer completes → PUSH NOTIFICATION
   │  └─ Tap notification → COOKING MODE (resume)
   └─ User opens app later → Prompt to resume
```

**Route Configuration:**
```dart
GoRoute(
  path: 'cooking',
  name: 'cooking-mode',
  builder: (context, state) {
    final recipeId = state.pathParameters['id']!;
    final resumeSession = state.queryParameters['resume'] == 'true';
    return CookingModeScreen(
      recipeId: recipeId,
      resumeSession: resumeSession,
    );
  },
)
```

---

## Deep Linking & Web URLs

### Supported Deep Links

**Format:** `chef://` (app) or `https://cookingapp.com/` (web)

```
chef://                          → Home Screen
chef://recipe/001                → Recipe Detail
chef://recipe/001/cooking        → Start Cooking Mode
chef://search                    → Search Screen
chef://search?q=pho              → Search with query
chef://categories                → Categories Screen
chef://categories?selected=001   → Categories with pre-selected
chef://chat                      → Chat AI Screen
chef://chat?personality=chef     → Chat with specific personality
chef://camera                    → Camera Screen
chef://profile                   → Profile Screen
chef://profile/saved             → Saved Recipes
chef://profile/history           → Cooking History
```

**Web URL Examples:**
```
https://cookingapp.com/recipe/pho-bo-ha-noi
https://cookingapp.com/recipe/pho-bo-ha-noi/cooking
https://cookingapp.com/search?q=pho&category=soup
https://cookingapp.com/categories/vietnamese
https://cookingapp.com/chat
```

**Implementation:**
```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [...],
  redirect: (context, state) {
    // Handle authentication, onboarding, etc.
  },
  // Deep link handling
  urlPathStrategy: UrlPathStrategy.path,
);
```

---

## Navigation Patterns

### Pattern 1: Bottom Navigation (Main Tabs)

**Behavior:**
- 5 tabs: Home, Explore, Chat, Camera, Profile
- State preserved when switching tabs
- Tap active tab → Scroll to top
- Double tap active tab → Refresh content

**Implementation:**
```dart
BottomNavigationBar(
  currentIndex: selectedIndex,
  onTap: (index) {
    if (index == selectedIndex) {
      // Scroll to top or refresh
      _scrollToTop(index);
    } else {
      // Switch tab
      context.go(_getRouteForIndex(index));
    }
  },
  items: [
    BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
    BottomNavigationBarItem(icon: Icon(Icons.explore), label: 'Explore'),
    BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Chat'),
    BottomNavigationBarItem(icon: Icon(Icons.camera), label: 'Camera'),
    BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
  ],
)
```

---

### Pattern 2: Push Navigation (Modal Screens)

**Behavior:**
- Recipe Detail, Search, Categories pushed as full screens
- Hide bottom navigation bar
- Standard back gesture/button to pop
- Transition: Slide from right (iOS) or Fade+Scale (Android)

**Implementation:**
```dart
// Push new screen
context.push('/recipe/$recipeId');

// Replace current screen
context.go('/search');

// Pop back
context.pop();
```

---

### Pattern 3: Bottom Sheet (Contextual Actions)

**Behavior:**
- Explore, Filter, Options shown as bottom sheets
- Semi-transparent backdrop
- Swipe down or tap outside to dismiss
- Can be full-height or partial

**Types:**

**Modal Bottom Sheet:**
```dart
showModalBottomSheet(
  context: context,
  isScrollControlled: true,
  backgroundColor: Colors.transparent,
  builder: (context) => FilterBottomSheet(),
);
```

**Persistent Bottom Sheet:**
```dart
showBottomSheet(
  context: context,
  builder: (context) => IngredientsSheet(),
);
```

---

### Pattern 4: Dialog (Confirmations)

**Behavior:**
- Exit confirmations, destructive actions
- Block background interaction
- Two options: Cancel / Confirm

**Implementation:**
```dart
showDialog(
  context: context,
  barrierDismissible: false,
  builder: (context) => AlertDialog(
    title: Text('Exit Cooking Mode?'),
    content: Text('Your progress will be saved...'),
    actions: [
      TextButton(
        onPressed: () => Navigator.of(context).pop(false),
        child: Text('Cancel'),
      ),
      ElevatedButton(
        onPressed: () => Navigator.of(context).pop(true),
        child: Text('Exit'),
      ),
    ],
  ),
);
```

---

### Pattern 5: Overlay (Voice, Loading)

**Behavior:**
- Voice listening, loading indicators
- Full-screen semi-transparent overlay
- Auto-dismiss or manual close

**Implementation:**
```dart
showGeneralDialog(
  context: context,
  barrierDismissible: true,
  barrierColor: Colors.black.withOpacity(0.85),
  transitionDuration: Duration(milliseconds: 300),
  pageBuilder: (context, animation, secondaryAnimation) {
    return VoiceListeningOverlay();
  },
);
```

---

## Transition Animations

### Recipe Detail Entry
```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  // Slide from bottom with fade
  const begin = Offset(0.0, 0.1);
  const end = Offset.zero;
  const curve = Curves.easeOutCubic;
  
  var tween = Tween(begin: begin, end: end).chain(
    CurveTween(curve: curve),
  );
  var offsetAnimation = animation.drive(tween);
  var fadeAnimation = animation.drive(Tween(begin: 0.0, end: 1.0));
  
  return SlideTransition(
    position: offsetAnimation,
    child: FadeTransition(
      opacity: fadeAnimation,
      child: child,
    ),
  );
}
```

---

### Cooking Mode Entry
```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  // Fade in + scale up (immersive transition)
  var scaleAnimation = Tween(begin: 0.95, end: 1.0).animate(
    CurvedAnimation(parent: animation, curve: Curves.easeOutCubic),
  );
  var fadeAnimation = animation;
  
  return FadeTransition(
    opacity: fadeAnimation,
    child: ScaleTransition(
      scale: scaleAnimation,
      child: child,
    ),
  );
}
```

---

### Bottom Sheet Slide Up
```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  const begin = Offset(0.0, 1.0);
  const end = Offset.zero;
  const curve = Curves.easeOutCubic;
  
  var tween = Tween(begin: begin, end: end).chain(
    CurveTween(curve: curve),
  );
  
  return SlideTransition(
    position: animation.drive(tween),
    child: child,
  );
}
```

---

## User Journey Examples

### Journey 1: Discover → Cook

```
1. User opens app
   └─> HOME SCREEN

2. Scrolls feed, sees "Phở Bò" recipe
   └─> Tap recipe card
   
3. Recipe Detail loads with hero animation
   └─> RECIPE DETAIL SCREEN
   
4. Reads ingredients, watches video
   └─> Scrolls to bottom
   
5. Ready to start cooking
   └─> Tap [▶️ Bắt đầu nấu]
   
6. Transition to fullscreen mode
   └─> COOKING MODE SCREEN
   
7. Follows steps, uses timers
   └─> Voice commands: "Next step", "Start timer"
   
8. Completes all steps
   └─> Tap [✓ Done]
   
9. Rates recipe 5 stars
   └─> COMPLETION SCREEN
   
10. Returns to recipe
    └─> Tap [🔙 Back to Recipe]
    
11. Recipe shows "✓ Cooked" badge
    └─> RECIPE DETAIL
```

**Timeline:** ~3-5 minutes browsing + cooking time

---

### Journey 2: Ask AI → Find Recipe

```
1. User has leftover ingredients
   └─> Tap Chat tab in bottom nav

2. Opens Chat AI
   └─> CHAT AI SCREEN

3. Says wake word: "Hey Chef"
   └─> Voice activates

4. Asks: "What can I make with chicken, tomatoes, and rice?"
   └─> AI processes question (RAG search)

5. AI suggests 3 recipes with reasoning
   └─> Chat displays recipe cards

6. User interested in "Cơm gà Hải Nam"
   └─> Tap recipe card in chat

7. Navigates to recipe detail
   └─> RECIPE DETAIL SCREEN

8. Saves recipe for later
   └─> Tap bookmark icon

9. Returns to home
   └─> Tap Home in bottom nav
```

**Timeline:** 2-3 minutes

---

### Journey 3: Camera → Search → Cook

```
1. User has mystery ingredient
   └─> Tap Camera tab in bottom nav

2. Opens camera view
   └─> CAMERA SCREEN

3. Points camera at ingredient
   └─> Tap capture button

4. Photo preview shows
   └─> Tap [Use Photo]

5. AI analyzes image (GPT-4V)
   └─> RESULTS MODE: "Detected: Ginger (Gừng)"

6. User confirms detection
   └─> Tap [Tìm recipes]

7. Navigates to search with pre-filled ingredients
   └─> SEARCH SCREEN (?ingredients=ginger)

8. Results show recipes using ginger
   └─> Scrolls results

9. Finds "Phở Bò"
   └─> Tap recipe card

10. Recipe detail loads
    └─> RECIPE DETAIL SCREEN

11. Starts cooking immediately
    └─> Tap [▶️ Bắt đầu nấu]

12. Enters cooking mode
    └─> COOKING MODE SCREEN
```

**Timeline:** 3-4 minutes

---

### Journey 4: Explore Categories

```
1. User wants specific cuisine type
   └─> Tap Explore button (bottom nav)

2. Explore bottom sheet appears
   └─> EXPLORE BOTTOM SHEET

3. Taps "Duyệt theo danh mục"
   └─> Sheet dismisses

4. Navigates to categories
   └─> CATEGORIES SCREEN (grid view)

5. Sees 15 categories displayed
   └─> Scrolls to find "Món Việt"

6. Taps "Món Việt" category
   └─> CATEGORY DETAIL VIEW (same screen)

7. Sees all Vietnamese recipes
   └─> Opens sort menu

8. Sorts by "Highest Rating"
   └─> Results reorder

9. Applies filter: "Under 30 minutes"
   └─> FILTER BOTTOM SHEET
   
10. Results filtered
    └─> CATEGORY DETAIL VIEW

11. Finds perfect recipe
    └─> Tap recipe card

12. Recipe detail opens
    └─> RECIPE DETAIL SCREEN
```

**Timeline:** 2-3 minutes

---

### Journey 5: Resume Cooking

```
1. User cooked yesterday, left at Step 5
   [Background: Session saved in DB]

2. Opens app today
   └─> HOME SCREEN

3. Sees "Resume Cooking" card at top
   └─> Card shows: "Phở Bò - Step 5/8"

4. Taps resume card
   └─> RECIPE DETAIL SCREEN
   
5. Action bar shows special button
   └─> [🔄 Resume Cooking (Step 5/8)]

6. Taps resume button
   └─> COOKING MODE SCREEN
   
7. Loads directly to Step 5
   └─> Progress bar shows: ━━━━━━░░░

8. Completed timers shown in history
   └─> Tap [⋮] → "Active Timers"

9. Continues from where left off
   └─> Voice: "Next step"

10. Completes remaining steps
    └─> Tap [✓ Done]

11. Rates and completes
    └─> COMPLETION SCREEN
```

**Timeline:** Instant resume, no re-navigation needed

---

## State Persistence

### Navigation Stack State

**Preserved:**
- Bottom navigation tab indices
- Scroll positions in lists
- Search queries and filters
- Chat conversation history
- Camera captured images
- Cooking mode progress (with session_id)

**Not Preserved (Cleared on app restart):**
- Modal overlays (bottom sheets, dialogs)
- Voice listening state
- Temporary selections
- Form input (draft states)

**Implementation:**
```dart
// Save navigation state
class NavigationState {
  int currentTab;
  String? searchQuery;
  Map<String, double> scrollPositions;
  String? activeCookingSession;
}

final navigationProvider = StateNotifierProvider<NavigationNotifier, NavigationState>(
  (ref) => NavigationNotifier(),
);

// Persist to SharedPreferences
await prefs.setString('nav_state', jsonEncode(state.toJson()));
```

---

### Cooking Session Persistence

**Auto-save triggers:**
- User exits Cooking Mode
- App backgrounded
- Timer state changes
- Step navigation

**Session data:**
```json
{
  "session_id": "session_12345",
  "recipe_id": "recipe_001",
  "current_step": 5,
  "started_at": "2024-11-25T14:30:00Z",
  "last_updated": "2024-11-25T15:00:00Z",
  "active_timers": [...],
  "completed_steps": [1, 2, 3, 4]
}
```

**Resume flow:**
```dart
// On app launch
final session = await api.getActiveCookingSession();
if (session != null) {
  // Show resume option in Home or Recipe Detail
  showResumePrompt(session);
}
```

---

## Error Handling & Edge Cases

### Network Errors

**Scenario:** User loses connection while navigating

**Handling:**
```
User taps recipe card
  └─> Show loading indicator
     └─> API call fails (timeout/no connection)
        └─> Show error snackbar: "No connection. Try again."
           └─> Stay on current screen
              └─> Recipe Detail not pushed to stack
```

**Retry Options:**
- Snackbar with "Retry" button
- Pull-to-refresh on list screens
- Cached content shown when available

---

### Deep Link to Invalid Recipe

**Scenario:** User opens `chef://recipe/999999` (non-existent)

**Handling:**
```
Deep link opens
  └─> App launches
     └─> Navigate to /recipe/999999
        └─> API call: GET /recipes/999999
           └─> Response: 404 Not Found
              └─> Show error screen:
                 "Recipe not found"
                 [Go to Home] button
                    └─> Redirect to HOME SCREEN
```

---

### Cooking Mode Interrupted

**Scenario:** User exits app with active timers

**Handling:**
```
User exits Cooking Mode
  └─> Session saved to backend
     └─> Timers continue in foreground service
        └─> Timer completes
           └─> Push notification sent
              └─> User taps notification
                 └─> Deep link: chef://recipe/:id/cooking?resume=true
                    └─> App opens to COOKING MODE
                       └─> Resume at last step
```

**Foreground Service:**
- Persistent notification: "Cooking Phở Bò - Timer: 15:30"
- Tap to return to Cooking Mode
- Actions: Pause Timer, Stop Timer

---

### Back Button Behavior

**Different contexts:**

1. **Recipe Detail (from Home):**
   - Back → HOME SCREEN (pop)

2. **Recipe Detail (from Search):**
   - Back → SEARCH SCREEN (pop)

3. **Cooking Mode:**
   - Back → EXIT CONFIRMATION
      - Cancel → Stay in Cooking Mode
      - Exit → RECIPE DETAIL (pop + save session)

4. **Search (from Explore):**
   - Back → HOME SCREEN (pop)

5. **Chat (direct tab):**
   - Back → Does nothing (main tab)
   - Home button → HOME SCREEN

6. **Root screens (bottom nav):**
   - Back → Exit app (show exit confirmation)

**Implementation:**
```dart
WillPopScope(
  onWillPop: () async {
    if (currentScreen is CookingModeScreen) {
      final shouldExit = await showExitConfirmation();
      return shouldExit;
    }
    return true; // Allow normal pop
  },
  child: child,
)
```

---

## Navigation Analytics

### Tracked Events

**Screen Views:**
```dart
analytics.logScreenView(
  screenName: 'recipe_detail',
  screenClass: 'RecipeDetailScreen',
  parameters: {
    'recipe_id': recipeId,
    'source': 'home_feed', // or 'search', 'chat', etc.
  },
);
```

**Navigation Paths:**
```dart
analytics.logEvent(
  name: 'navigation_path',
  parameters: {
    'from': 'home',
    'to': 'recipe_detail',
    'action': 'tap_recipe_card',
    'recipe_id': recipeId,
  },
);
```

**User Journey Tracking:**
```dart
// Track complete journey
analytics.logEvent(
  name: 'cooking_journey_complete',
  parameters: {
    'path': 'home -> recipe_detail -> cooking_mode -> completion',
    'duration_seconds': 3600,
    'recipe_id': recipeId,
  },
);
```

---

## Performance Considerations

### Route Preloading

**Strategy:** Preload likely next screens

```dart
// On Recipe Detail, preload Cooking Mode
Future.delayed(Duration(seconds: 2), () {
  precacheImage(AssetImage('assets/cooking_bg.png'), context);
  // Warm up cooking session API
  ref.read(cookingSessionProvider).prepare(recipeId);
});
```

---

### Navigation Stack Optimization

**Limit stack depth:**
```dart
// Replace instead of push for search results
if (navigationStack.length > 10) {
  context.go(route); // Replace
} else {
  context.push(route); // Push
}
```

**Clear stack on home:**
```dart
void goToHome() {
  // Clear entire stack, go to root
  context.go('/');
}
```

---

### Lazy Loading

**Bottom Nav tabs:**
```dart
IndexedStack(
  index: currentIndex,
  children: [
    HomeScreen(),              // Loaded immediately
    Container(),               // Explore (no screen, just bottom sheet)
    currentIndex == 2 ? ChatAIScreen() : Container(), // Lazy
    currentIndex == 3 ? CameraScreen() : Container(), // Lazy
    currentIndex == 4 ? ProfileScreen() : Container(), // Lazy
  ],
)
```

---

## Summary

### Complete Screen Inventory

| # | Screen Name | Route | Access From | Type |
|---|-------------|-------|-------------|------|
| 01 | Home Screen | `/` | App Launch | Tab (Bottom Nav) |
| 02 | Explore Bottom Sheet | N/A (Modal) | Explore Button | Bottom Sheet Overlay |
| 03 | Recipe Detail | `/recipe/:id` | Home, Search, Chat, Camera | Full Screen (Push) |
| 04 | Chat AI Screen | `/chat` | Bottom Nav, Recipe Detail | Tab (Bottom Nav) |
| 05 | Camera Screen | `/camera` | Bottom Nav | Tab (Bottom Nav) |
| 06 | Profile Screen | `/profile` | Bottom Nav | Tab (Bottom Nav) |
| 07 | Search Screen | `/search` | Home, Explore, Categories | Full Screen (Push) |
| 08 | Categories Screen | `/categories` | Home, Explore, Recipe Detail | Full Screen (Push) |
| 09 | Cooking Mode Screen | `/recipe/:id/cooking` | Recipe Detail | Full Screen (Immersive) |

**Total Primary Screens:** 9  
**Total Routes (including sub-routes):** 15+  
**Bottom Sheet Overlays:** 5+ (Explore, Filter, Options, Ingredients, Timers)

---

### Navigation Principles

1. **Simplicity:** Max 2 taps to reach any primary function
2. **Context Preservation:** Back button always logical and predictable
3. **State Persistence:** Resume from exactly where user left off
4. **Progressive Disclosure:** Show advanced options only when needed
5. **Accessibility:** Keyboard navigation, screen reader support
6. **Performance:** Lazy loading, route preloading, optimized transitions
7. **Deep Linking:** Every screen accessible via URL/deep link
8. **Analytics:** Full navigation path tracking for UX optimization

---

**✅ Navigation Flow Documentation Complete!**

Tài liệu này cung cấp blueprint đầy đủ cho việc implement navigation trong Flutter app với go_router. Mỗi connection, transition, và edge case đều được document chi tiết.
