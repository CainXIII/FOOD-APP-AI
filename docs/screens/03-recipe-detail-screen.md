# 📱 Recipe Detail Screen - Design Specification

## Overview
Recipe Detail Screen hiển thị đầy đủ thông tin công thức nấu ăn với hướng dẫn từng bước, hỗ trợ voice guidance và cooking mode.

---

## Visual Layout

```
┌─────────────────────────────────────┐
│ [←]                          [⭐💬📤]│ <- Floating AppBar (transparent)
├─────────────────────────────────────┤
│                                     │
│                                     │
│      [Hero Recipe Image]            │ <- Large image (Full width)
│         (Scrolls under)             │    Height: 300px
│                                     │    Parallax effect
│                                     │
├─────────────────────────────────────┤
│ ╭───────────────────────────────╮   │
│ │                               │   │
│ │  Phở Bò Hà Nội               │   │ <- Title card (overlaps image)
│ │  ⭐ 4.8 (124)  👥 4 người     │   │    Rounded, elevated
│ │  ⏱️ 45 phút    📊 Trung bình  │   │    White background
│ │                               │   │
│ ╰───────────────────────────────╯   │
│                                     │
│ ┌─ Tabs ─────────────────────────┐  │
│ │[Nguyên liệu][Cách làm][Dinh dưỡng]│ <- Tab bar
│ └─────────────────────────────────┘  │
│                                     │
│ ── Tab Content Area ──              │
│                                     │
│ (Scrollable content based on tab)   │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ [🎙️ Đọc hướng dẫn]  [▶️ Bắt đầu]   │ <- Fixed bottom actions
└─────────────────────────────────────┘    Height: 80px
```

---

## Components Detail

### 1. Hero Image Section

```
┌─────────────────────────────────────┐
│ [←]                     [⭐] [💬] [📤]│ <- Floating overlay
│                                     │
│                                     │
│       [Large Recipe Photo]          │ <- Height: 300-400px
│                                     │    Full bleed
│                                     │    Gradient overlay
│                                     │
└─────────────────────────────────────┘
```

**Dimensions:**
- Height: 300px (mobile), 400px (tablet+)
- Width: 100% screen width
- Aspect ratio: 16:9 or auto

**Image:**
- High quality, optimized
- Fit: Cover
- Loading: Progressive (LQIP blur-up)
- Cache: Aggressive

**Gradient Overlay:**
- Position: Bottom 40% of image
- Color: Linear gradient
  - Start: Transparent (top)
  - End: Black 50% opacity (bottom)
- Purpose: Ensure text readability

**Floating AppBar:**
- Position: Absolute, top
- Background: Transparent initially
- Padding: 16px horizontal, 8px vertical
- Height: 56px

**Back Button (Left):**
- Size: 40×40px circular button
- Background: White with shadow
- Icon: Arrow left (black, 24×24px)
- Shadow: 0 2px 8px rgba(0,0,0,0.2)
- Tap: Navigate back

**Action Buttons (Right):**
```
[⭐] [💬] [📤]
 ^    ^    ^
 |    |    Share
 |    Reviews (with count badge)
 Favorite (toggle)
```

**Each button:**
- Size: 40×40px circular
- Background: White with shadow
- Spacing: 8px gap between
- Icon: 24×24px
- Tap: Execute action

**Favorite Button:**
- Icon: Heart outline (default) / Filled heart (favorited)
- Color: Red (#F44336)
- Tap: Toggle favorite (optimistic update)

**Reviews Button:**
- Icon: Chat bubble
- Color: Gray (#757575)
- Badge: Orange circle with count (if > 0)
- Tap: Scroll to reviews section

**Share Button:**
- Icon: Share arrow
- Color: Gray (#757575)
- Tap: System share sheet
  - Recipe URL
  - Image thumbnail
  - Title

---

### Scroll Behavior: Parallax Effect

```
Scroll position 0px:
┌─────────────────────────────────────┐
│ [←]                     [⭐💬📤]     │ <- Transparent AppBar
│                                     │
│       [Image at top]                │
│                                     │
└─────────────────────────────────────┘

Scroll position 100px:
┌─────────────────────────────────────┐
│ [←]                     [⭐💬📤]     │ <- Semi-transparent
│   [Image scrolled 50px]             │    Parallax (half speed)
│                                     │
└─────────────────────────────────────┘

Scroll position 300px+:
┌─────────────────────────────────────┐
│ [←] Phở Bò Hà Nội       [⭐💬📤]     │ <- Opaque white + title
└─────────────────────────────────────┘
[Image completely off screen]

Parallax: Image scrolls at 0.5x speed
AppBar transition: 200ms ease-out
Title fade in: 0% → 100% opacity
```

---

### 2. Title Card (Overlapping)

```
┌─────────────────────────────────────┐
│         [Image area]                │
│                                     │
│   ╭─────────────────────────────╮   │ <- Overlaps image by 40px
│   │                             │   │
│   │  Phở Bò Hà Nội             │   │    White card
│   │                             │   │    Rounded: 24px
│   │  ⭐ 4.8 (124 đánh giá)      │   │    Shadow: Elevation 8
│   │  👥 4 người                 │   │
│   │  ⏱️ 45 phút                 │   │    Padding: 20px
│   │  📊 Trung bình              │   │
│   │                             │   │
│   ╰─────────────────────────────╯   │
│                                     │
└─────────────────────────────────────┘
```

**Dimensions:**
- Width: Screen width - 32px (16px margin each side)
- Height: Auto (min 140px)
- Position: Overlaps image bottom by 40px
- Border radius: 24px
- Shadow: 0 4px 16px rgba(0,0,0,0.15)
- Background: White (light) / Dark gray (#1E1E1E in dark)

**Content Layout:**
```
╭──────────────────────────────────╮
│ [Title - 20px, bold]             │ <- Phở Bò Hà Nội
│                                  │    2 lines max
│ ┌─ Metadata Row 1 ──────────────┐│
│ │ ⭐ 4.8 (124)       👥 4 người  ││
│ └────────────────────────────────┘│
│                                  │
│ ┌─ Metadata Row 2 ──────────────┐│
│ │ ⏱️ 45 phút         📊 Trung bình││
│ └────────────────────────────────┘│
╰──────────────────────────────────╯

Padding: 20px all sides
Gap between rows: 12px
```

**Metadata Items:**
- **Font size:** 14px
- **Icon size:** 16×16px
- **Layout:** 2x2 grid
- **Gap:** 12px vertical, 16px horizontal

**Metadata Details:**
1. **Rating:**
   - Icon: Gold star (⭐)
   - Text: "4.8 (124 đánh giá)"
   - Color: Black (number), Gray (count)

2. **Servings:**
   - Icon: Person group (👥)
   - Text: "4 người"
   - Color: Gray (#616161)

3. **Time:**
   - Icon: Clock (⏱️)
   - Text: "45 phút"
   - Color: Gray

4. **Difficulty:**
   - Icon: Chart (📊)
   - Text: "Trung bình" (Easy/Medium/Hard)
   - Color: 
     - Easy: Green (#4CAF50)
     - Medium: Orange (#FF9800)
     - Hard: Red (#F44336)

---

### 3. Tab Navigation

```
┌─────────────────────────────────────┐
│ ┌───────────────────────────────┐   │
│ │ Nguyên liệu │ Cách làm │ Dinh dưỡng│ <- 3 tabs
│ │      ▔▔▔▔▔▔▔▔                  │   │    Active: Orange underline
│ └───────────────────────────────┘   │    Height: 48px
└─────────────────────────────────────┘
```

**Tab Bar Specs:**
- Height: 48px
- Background: White
- Border bottom: 1px solid #E0E0E0
- Padding: 0 (tabs fill width)

**Tab Item:**
- Width: 33.33% (3 equal tabs)
- Height: 48px
- Padding: 12px vertical
- Tap target: Full area

**Tab States:**

**Active Tab:**
```
Nguyên liệu
▔▔▔▔▔▔▔▔▔▔▔▔
Text: Orange (#FF6F00)
Weight: Bold (600)
Underline: 3px thick, Orange
Position: Bottom of tab
```

**Inactive Tab:**
```
Cách làm

Text: Gray (#757575)
Weight: Medium (500)
No underline
```

**Interaction:**
- Tap tab: Switch content (crossfade 200ms)
- Underline animates to new position (300ms ease-out)
- Haptic feedback on tap
- Scroll to top of content area

---

### 4. Tab Content: Nguyên Liệu (Ingredients)

```
┌─────────────────────────────────────┐
│ Nguyên liệu chính                   │ <- Section header (16px, bold)
│                                     │
│ ☐ 500g thịt bò nạm                  │ <- Checkbox items
│ ☐ 300g bánh phở tươi                │    Height: 48px each
│ ☐ 2L nước dùng                      │
│ ☐ 2 củ hành tây                     │
│                                     │
│ Gia vị                              │ <- Section header
│                                     │
│ ☐ 3 tbsp nước mắm                   │
│ ☐ 2 tbsp đường                      │
│ ☐ 1 tbsp muối                       │
│ ☐ Hạt tiêu, gừng, hành              │
│                                     │
│ Rau ăn kèm                          │
│                                     │
│ ☐ Hành lá, ngò gai                  │
│ ☐ Giá đỗ, húng quế                  │
│ ☐ Chanh, ớt                         │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🛒 Thêm vào giỏ hàng            │ │ <- Action button
│ └─────────────────────────────────┘ │    (Future feature)
└─────────────────────────────────────┘
```

**Section Header:**
- Font: 16px, bold
- Color: Black
- Margin: 16px top, 8px bottom
- Padding: 0 16px

**Ingredient Item:**
```
┌─────────────────────────────────────┐
│ ☐  500g thịt bò nạm                │ <- Unchecked
│    ^   ^                            │
│    |   Text (16px, regular)         │
│    Checkbox (24×24px)               │
│                                     │
│ Height: 48px                        │
│ Padding: 0 16px                     │
│ Tap area: Full width                │
└─────────────────────────────────────┘

When checked:
┌─────────────────────────────────────┐
│ ☑  500g thịt bò nạm                │ <- Checked
│    ^   ^                            │    Green checkmark
│    |   Strikethrough, gray, 60%    │
│    Green (#4CAF50)                  │
└─────────────────────────────────────┘
```

**Checkbox:**
- Size: 24×24px
- Border: 2px solid gray (unchecked)
- Background: Green (checked)
- Icon: White checkmark (checked)
- Animation: Scale 1.2 → 1.0 (200ms)

**Progress Indicator:**
```
Top of list:
┌─────────────────────────────────────┐
│ 5/12 nguyên liệu ✓                  │ <- Progress text
│ ━━━━━━━━━░░░░░░░░░░░                │ <- Progress bar
└─────────────────────────────────────┘

Height: 40px
Background: Light orange (#FFF3E0)
Text: 14px, orange
Bar: 4px height, orange filled
```

**Action Button:**
- Height: 48px
- Margin: 16px all sides
- Border radius: 24px
- Background: White
- Border: 2px solid orange
- Text: 16px, orange
- Icon: 🛒 (20×20px)
- Tap: Add all ingredients to shopping list

---

### 5. Tab Content: Cách Làm (Instructions)

```
┌─────────────────────────────────────┐
│ Chuẩn bị (10 phút)                  │ <- Phase header
│                                     │
│ ┌─ Step 1 ─────────────────────┐   │
│ │ ①                            │   │
│ │ Rửa sạch thịt bò, cắt miếng  │   │
│ │ vừa ăn. Ngâm với nước muối   │   │ <- Step card
│ │ 10 phút rồi rửa lại.         │   │    Numbered
│ │                              │   │    Height: Auto
│ │ [  Thumbnail image  ]        │   │    Optional image
│ │                              │   │
│ │ ⏱️ 10 phút          ☑ Xong   │   │    Timer + Done
│ └──────────────────────────────┘   │
│                                     │
│ ┌─ Step 2 ─────────────────────┐   │
│ │ ②                            │   │
│ │ Hành tây bổ múi cau, rang    │   │
│ │ qua lửa cho thơm.            │   │
│ │                              │   │
│ │ ⏱️ 5 phút           ☐ Xong   │   │
│ └──────────────────────────────┘   │
│                                     │
│ Nấu (30 phút)                       │ <- Next phase
│                                     │
│ ┌─ Step 3 ─────────────────────┐   │
│ │ ③                            │   │
│ │ Cho nước vào nồi, thêm xương │   │
│ │ và thịt. Đun sôi rồi hạ lửa. │   │
└─────────────────────────────────────┘
```

**Phase Header:**
- Text: "[Phase name] ([time])"
- Font: 18px, bold
- Color: Orange (#FF6F00)
- Margin: 24px top, 12px bottom

**Step Card:**
```
╭──────────────────────────────────╮
│ ① [Step number - 32px circle]   │ <- Orange circle, white text
│                                  │
│ [Instruction text - 16px]        │ <- Multi-line, 20px line height
│ Lorem ipsum dolor sit amet...    │    Black text
│                                  │
│ ┌────────────────────────────┐   │
│ │   [Optional step image]    │   │ <- 100px height, rounded 12px
│ └────────────────────────────┘   │    Tap to fullscreen
│                                  │
│ ⏱️ 10 phút              ☐ Xong  │ <- Footer with timer + checkbox
│   ^                      ^      │
│   Timer button          Done    │
╰──────────────────────────────────╯

Background: White
Border: 1px solid #E0E0E0
Rounded: 16px
Padding: 16px
Margin: 12px between steps
Shadow: 0 2px 4px rgba(0,0,0,0.06)
```

**Step Number Circle:**
- Size: 32×32px
- Font: 16px, bold
- States:
  - **Not started:** Gray (#BDBDBD)
  - **Current:** Orange (#FF6F00) + pulsing animation
  - **Completed:** Green (#4CAF50) + checkmark icon

**Instruction Text:**
- Font: 16px, regular
- Line height: 24px (1.5)
- Color: Black
- Max lines: None (full text visible)

**Timer Button:**
- Size: Auto width × 32px height
- Background: Light gray (#F5F5F5)
- Text: "⏱️ 10 phút"
- Border radius: 16px
- Tap: Start countdown timer
- Active state: Orange background, white text

**Done Checkbox:**
- Size: 24×24px
- Unchecked: White bg, gray border
- Checked: Green bg, white checkmark
- Tap: Mark step complete
- Animation: Checkmark scales in

**Step Image (Optional):**
- Height: 100px
- Width: 100% of card
- Margin: 12px top & bottom
- Border radius: 12px
- Tap: Open fullscreen lightbox

---

### 6. Tab Content: Dinh Dưỡng (Nutrition)

```
┌─────────────────────────────────────┐
│ Thông tin dinh dưỡng                │
│ (Trên 1 khẩu phần)                  │
│                                     │
│ ┌───────────────────────────────┐   │
│ │      450                      │   │ <- Large calorie card
│ │    Calories                   │   │    Center-aligned
│ └───────────────────────────────┘   │    120px height
│                                     │
│ ┌─────────────┐ ┌───────────────┐   │
│ │ Protein     │ │ Carbs         │   │ <- 2-column grid
│ │   32g       │ │   45g         │   │    Small cards
│ └─────────────┘ └───────────────┘   │    80px height each
│                                     │
│ ┌─────────────┐ ┌───────────────┐   │
│ │ Fat         │ │ Fiber         │   │
│ │   18g       │ │   4g          │   │
│ └─────────────┘ └───────────────┘   │
│                                     │
│ ── Chi tiết ──                      │ <- Expandable section
│                                     │
│ Vitamin A         15% RDA          │ <- List
│ Vitamin C         25% RDA          │
│ Iron              20% RDA          │
│ Calcium           10% RDA          │
│                                     │
│ ── Allergens ──                     │
│                                     │
│ ⚠️ Chứa: Gluten, Đậu nành          │
└─────────────────────────────────────┘
```

**Large Calorie Card:**
- Height: 120px
- Width: 100% - 32px margin
- Background: Light orange gradient
- Number: 60px, bold
- Label: 14px, gray
- Border radius: 16px
- Shadow: Elevation 2

**Macro Cards (2×2 Grid):**
- Each card: (50% width - 8px gap) × 80px
- Background: Light gray (#F5F5F5)
- Border radius: 12px
- Padding: 12px
- Label: 12px, gray (top)
- Value: 24px, bold, black (center)

**Detail Section:**
- Expandable accordion
- Header: "── Chi tiết ──" (tap to expand)
- List items:
  - Name (left): 14px, black
  - Value (right): 14px, gray
  - Height: 36px each
  - Divider: 1px gray line

**Allergen Warning:**
- Background: Light red (#FFEBEE)
- Icon: ⚠️ (20×20px)
- Text: 14px, red (#D32F2F)
- Border radius: 8px
- Padding: 12px
- Margin: 16px

---

### 7. Fixed Bottom Action Bar

```
┌─────────────────────────────────────┐
│ ┌──────────────┐  ┌──────────────┐  │
│ │              │  │              │  │
│ │ 🎙️ Đọc      │  │ ▶️ Bắt đầu  │  │ <- 2 buttons
│ │   hướng dẫn │  │    nấu       │  │    Height: 56px each
│ │              │  │              │  │
│ └──────────────┘  └──────────────┘  │
└─────────────────────────────────────┘
Container height: 80px (56 + 12 top/bottom padding)
Background: White with top shadow
Position: Fixed (always visible)
Safe area: Respects bottom notch
```

**Button 1: Đọc hướng dẫn (Voice Guidance)**
```
┌──────────────────┐
│ 🎙️  Đọc hướng dẫn │
└──────────────────┘
Background: White
Border: 2px solid Orange (#FF6F00)
Text: Orange, 16px, medium
Icon: 20×20px
Width: 48% (with 4% gap)
Height: 56px
Border radius: 28px (pill)
Shadow: None
```

**Button 2: Bắt đầu nấu (Start Cooking)**
```
┌──────────────────┐
│ ▶️  Bắt đầu nấu   │
└──────────────────┘
Background: Orange gradient (#FF6F00 → #FF8F00)
Text: White, 16px, bold
Icon: 20×20px
Width: 48%
Height: 56px
Border radius: 28px
Shadow: 0 4px 12px rgba(255,111,0,0.3)
```

**Container:**
- Padding: 12px top/bottom, 16px horizontal
- Background: White (light) / Dark (#1E1E1E)
- Top border: 1px solid #E0E0E0
- Shadow: 0 -2px 8px rgba(0,0,0,0.08)
- Z-index: 10 (above content)

**Actions:**
- **Đọc hướng dẫn:** 
  - Start Vietnamese TTS
  - Reads current visible step (or all steps)
  - Pause/resume controls appear
- **Bắt đầu nấu:**
  - Navigate to Cooking Mode screen
  - Fullscreen step-by-step
  - Hands-free interface

---

## User Flows

### Flow 1: Browse Recipe Details
```
User on Home → Taps recipe card
  ↓
Hero animation (image expands, 300ms)
  ↓
Recipe Detail opens
  ↓
User scrolls down (parallax effect)
  ↓
Views title card metadata
  ↓
Switches tabs: Ingredients → Instructions → Nutrition
  ↓
Scrolls through content
  ↓
Decides: Start cooking or go back
```

### Flow 2: Check Off Ingredients
```
On Recipe Detail → Ingredients tab
  ↓
User taps checkbox for "500g thịt bò"
  ↓
Haptic feedback (light)
  ↓
Checkbox animates to checked (green, scale)
  ↓
Text strikes through, grays out
  ↓
Progress updates: "1/12 nguyên liệu ✓"
  ↓
Progress bar fills proportionally
  ↓
User continues checking items
  ↓
When all checked: "12/12 Sẵn sàng nấu! 🎉"
```

### Flow 3: Follow Cooking Steps
```
On Recipe Detail → Instructions tab
  ↓
User scrolls to Step 1
  ↓
Reads instruction
  ↓
Taps timer button "⏱️ 10 phút"
  ↓
Timer starts countdown (overlay/notification)
  ↓
User follows step
  ↓
Taps "✓ Xong" when done
  ↓
Step 1 number turns green (completed)
  ↓
Step 2 number pulses orange (current)
  ↓
User scrolls to Step 2
  ↓
Repeat process
```

### Flow 4: Start Cooking Mode
```
On Recipe Detail → User ready to cook
  ↓
Taps "▶️ Bắt đầu nấu" button
  ↓
Haptic feedback (medium)
  ↓
Navigate to Cooking Mode screen
  ↓
Fullscreen step-by-step interface:
- Large text (24px)
- Huge step number
- Voice guidance auto-enabled
- Timer controls prominent
- Next/Previous buttons
- Hands-free commands supported
```

### Flow 5: Voice Guidance
```
On Recipe Detail → Instructions tab
  ↓
Taps "🎙️ Đọc hướng dẫn" button
  ↓
TTS starts reading current visible step
  ↓
Overlay appears with controls:
┌─────────────────────────────────┐
│ 🔊 Đang đọc Bước 2...           │
│                                 │
│ [⏸️ Pause] [⏭️ Next] [❌ Stop] │
└─────────────────────────────────┘
  ↓
User can:
- Pause/Resume
- Skip to next step
- Stop reading
  ↓
Voice command support (if wake word enabled):
- "Tiếp theo" → Next step
- "Lặp lại" → Repeat current
- "Dừng" → Stop
```

### Flow 6: Share Recipe
```
On Recipe Detail
  ↓
Taps Share icon (📤) in AppBar
  ↓
System share sheet appears:
- WhatsApp
- Messenger
- Email
- Copy link
- More...
  ↓
Shares:
- Recipe URL
- Image thumbnail
- Title + brief description
```

---

## Responsive Design

### Mobile (<600px)
- Image height: 300px
- Title card: Full width - 32px margin
- Tabs: 3 equal width (33.33% each)
- Bottom buttons: 2 columns (48% + 4% gap + 48%)
- Step cards: Full width - 32px margin

### Tablet (600-1200px)
- Image height: 400px
- Title card: Max width 600px, centered
- Tabs: Content max width 600px
- Bottom buttons: Max width 600px, centered
- Step cards: Max width 600px

### Desktop (>1200px)
**Split Layout:**
```
┌─────────────────────────────────────┐
│ [Image + Title]  │  [Tabs + Content]│
│      50%         │       50%        │
│                  │                  │
│                  │  [Bottom buttons]│
└─────────────────────────────────────┘

Left side: Image + title card fixed
Right side: Scrollable tabs + content
Max width: 1200px, centered
```

---

## Accessibility

### Screen Reader
- Hero image: "Recipe photo: [Recipe name]"
- AppBar buttons:
  - "Back, button"
  - "Favorite, toggle button, currently [favorited/not favorited]"
  - "Reviews, button, 124 reviews"
  - "Share, button"
- Title card: "Recipe name, rated 4.8 stars by 124 people, serves 4, cooking time 45 minutes, difficulty medium"
- Tabs: "Ingredients tab, [selected/not selected]"
- Ingredients: "500 grams beef, checkbox, [checked/unchecked]"
- Steps: "Step 1 of 8, [instruction text], timer 10 minutes, mark done checkbox"

### Keyboard Navigation
- Tab order: Back → Actions → Tabs → Content → Bottom buttons
- Arrow keys: Switch tabs (when focused)
- Space: Check/uncheck items, mark steps done
- Enter: Activate buttons

### Voice Commands (Cooking Mode)
- "Bước tiếp theo" / "Next" → Next step
- "Lặp lại" / "Repeat" → Repeat current step
- "Hẹn giờ [X] phút" → Set timer
- "Tạm dừng" / "Pause" → Pause timer
- "Tiếp tục" / "Resume" → Resume timer

---

## Performance

### Image Loading
- Hero image: High priority, load first
- Step images: Lazy load (viewport-based)
- Thumbnail blur-up (progressive JPEG)
- Cache: Memory + disk, aggressive

### Tab Content
- Lazy render inactive tabs
- Keep active tab in memory
- Pre-fetch adjacent tab (user might switch)
- Dispose when navigating away

### Animations
- Use GPU acceleration (transform, opacity)
- Avoid layout thrashing
- 60fps target
- Reduce motion for accessibility settings

### Scroll Performance
- Virtual scrolling for long step lists (>20)
- Debounce parallax calculations
- Throttle scroll events

---

## Edge Cases

### No Ingredients
```
Empty ingredients list:
┌─────────────────────────────────┐
│ 📝 Chưa có thông tin nguyên liệu│
│                                 │
│ [Báo cáo thiếu thông tin]       │
└─────────────────────────────────┘
```

### No Instructions
```
Empty steps:
┌─────────────────────────────────┐
│ 📖 Hướng dẫn đang được cập nhật │
│                                 │
│ [Xem video thay thế] (if available)
└─────────────────────────────────┘
```

### Long Recipe (50+ steps)
- Virtual scrolling enabled
- "Jump to step" dropdown menu
- Progress indicator: "Step 15/52"
- Collapse completed steps option

### Offline Mode
```
Recipe detail page cached:
- Images cached
- Content available
- Favorite/share may not work
- Banner: "Offline mode"
```

---

## Design Tokens

### Colors
```
Primary: #FF6F00 (Orange)
Success: #4CAF50 (Green)
Error: #F44336 (Red)
Warning: #FF9800 (Amber)
Info: #2196F3 (Blue)
```

### Typography
```
Hero Title: 20px, Bold
Section Header: 18px, Bold
Tab Label: 14px, Medium
Body Text: 16px, Regular
Metadata: 14px, Regular
Small Text: 12px, Regular
```

### Spacing
```
Card overlap: 40px
Card margin: 16px
Section gap: 24px
Item gap: 12px
```

---

## Summary

**Recipe Detail Screen:**
- ✅ Hero image with parallax scroll
- ✅ Floating AppBar with actions
- ✅ Overlapping title card with metadata
- ✅ 3 tabs: Ingredients, Instructions, Nutrition
- ✅ Interactive checkboxes for ingredients
- ✅ Step-by-step with timers
- ✅ Voice guidance support
- ✅ Cooking mode transition
- ✅ Share functionality
- ✅ Responsive across devices
- ✅ Full accessibility support
