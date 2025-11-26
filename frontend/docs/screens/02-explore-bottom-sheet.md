# 🧭 Explore Bottom Sheet - Design Specification

## Overview
Bottom sheet hiển thị khi user tap vào "Explore" trong bottom navigation, cung cấp 2 options: Search Recipes và Browse Categories.

---

## Visual Design

```
┌─────────────────────────────────────┐
│   ┌─────────────────────────────┐  │
│   │ 🔍  Recipes              ›  │  │ <- Option 1
│   └─────────────────────────────┘  │    Height: 56px
│                                     │
│   ┌─────────────────────────────┐  │
│   │ 📂  Categories           ›  │  │ <- Option 2
│   └─────────────────────────────┘  │    Height: 56px
│                                     │
└─────────────────────────────────────┘
```

---

## Design Specifications

### Bottom Sheet Container
**Dimensions:**
- Width: 100% (mobile)
- Height: 160px (auto-fit content)
- Max height: 90% screen height

**Visual:**
- Background: White (light) / Dark gray (#1E1E1E in dark mode)
- Border radius: 24px (top corners only)
- Shadow: Elevation 16 (0 -4px 16px rgba(0,0,0,0.15))

**Padding:**
- Top: 20px
- Horizontal: 20px
- Bottom: 20px
- **Calculation:** 20 + 56 + 8 + 56 + 20 = 160px total

**Position:**
- Anchored to bottom of screen
- Overlays all content
- Behind: Semi-transparent backdrop

---

### Option Items

**Structure:**
```
┌───────────────────────────────────────┐
│ [Icon] [Space] [Text]  [Space] [›]   │
│  24px   12px   Flex     Auto    16px  │
└───────────────────────────────────────┘
  ↑─16px padding                    16px─↑
```

**Dimensions:**
- Height: 56px
- Width: 100% of container (minus 40px padding)
- Border radius: 12px
- Margin bottom: 8px (between options)

**Icon:**
- Size: 24×24px
- Position: 16px from left edge
- Vertical: Centered

**Text:**
- Font size: 16px
- Weight: Medium (500)
- Color: Black (#212121) / White (dark mode)
- Position: 12px from icon
- Flex: Takes remaining space

**Chevron (›):**
- Size: 16×16px
- Color: Gray (#9E9E9E)
- Position: 16px from right edge
- Vertical: Centered

---

## States

### Default State
```
┌─────────────────────────────────┐
│ 🔍  Recipes              ›     │
└─────────────────────────────────┘
Background: Light gray (#F5F5F5)
Text: Black (#212121)
Chevron: Gray (#9E9E9E)
Border: None
```

### Pressed State
```
┌─────────────────────────────────┐
│ 🔍  Recipes              ›     │
└─────────────────────────────────┘
Background: Darker gray (#E0E0E0)
Text: Black
Chevron: Darker gray (#757575)
Scale: 0.98 (subtle feedback)
Duration: 100ms
```

### Hover State (Web/Desktop)
```
┌─────────────────────────────────┐
│ 🔍  Recipes              ›     │
└─────────────────────────────────┘
Background: Light orange (#FFF3E0)
Text: Orange (#FF6F00)
Chevron: Orange (#FF6F00)
Cursor: Pointer
Transition: 200ms ease-out
```

**Hover Animation (Optional):**
- Chevron moves right 2px (150ms)
- Returns on mouse leave (150ms)

---

## Backdrop

**Visual:**
- Color: Black (#000000)
- Opacity: 40% (0.4 alpha)
- Blur: 8px (optional, iOS-style)
- Full screen coverage

**Interaction:**
- Tap backdrop → Dismiss sheet
- Blocks interaction with content behind

**Animation:**
- Fade in: 200ms
- Fade out: 200ms

---

## Animations

### Opening Sequence
```
User taps "🧭 Explore" on bottom nav
  ↓
Haptic feedback (light impact)
  ↓
Backdrop fades in (200ms, black 40%)
  ↓
Sheet slides up from bottom (300ms ease-out curve)
  ↓
Options fade in with stagger
  - Option 1: 0ms delay
  - Option 2: 50ms delay
  - Duration: 200ms each
```

### Closing Sequence
```
User swipes down / taps backdrop / taps option
  ↓
Sheet slides down (250ms ease-in curve)
  ↓
Backdrop fades out (200ms)
  ↓
Sheet removed from UI tree
  ↓
If option tapped: Navigate to destination
```

---

## Interactions

### Dismiss Triggers
1. ✅ **Swipe down** anywhere on sheet
2. ✅ **Tap backdrop** (outside sheet)
3. ✅ **Tap any option** (auto-close then navigate)
4. ✅ **Back button** (Android/Web)
5. ✅ **Escape key** (Desktop)

### Swipe Gesture
**Without visible handle:**
```
User touches sheet and drags down
  ↓
Sheet follows finger with rubber band effect
  ↓
Threshold check:
- Distance > 50px AND velocity > threshold
  → Dismiss (continue slide down animation)
- Else
  → Spring back to original position (300ms)
```

**Touch zones for swipe:**
- Empty space between options (40px area)
- On top of option but swiping (cancels tap)
- Anywhere on sheet surface

---

## Navigation Flows

### Flow 1: Search Recipes
```
Home Screen
  ↓
User taps "🧭 Explore" bottom nav
  ↓
Bottom sheet slides up (300ms)
  ↓
User taps "🔍 Recipes" option
  ↓
Sheet slides down (250ms)
  ↓
Navigate to: Search Screen

┌─────────────────────────────────────┐
│ [←]  Tìm kiếm công thức             │
├─────────────────────────────────────┤
│ ┌────────────────────────────────┐  │
│ │ 🔍  Nhập từ khóa...      [🎙️] │  │ <- Auto-focused
│ └────────────────────────────────┘  │
├─────────────────────────────────────┤
│ 🔍 Filters                          │
│ [⏱️ Time] [📊 Difficulty] [🍽️ Type]│
├─────────────────────────────────────┤
│ Tìm kiếm gần đây:                   │
│ • Phở bò                            │
│ • Gà xào sả ớt                      │
└─────────────────────────────────────┘
```

### Flow 2: Browse Categories
```
Home Screen
  ↓
User taps "🧭 Explore" bottom nav
  ↓
Bottom sheet slides up
  ↓
User taps "📂 Categories" option
  ↓
Sheet slides down
  ↓
Navigate to: Categories Grid Screen

┌─────────────────────────────────────┐
│ [←]  Danh mục món ăn                │
├─────────────────────────────────────┤
│ ┌────────────────┐ ┌──────────────┐ │
│ │      🍜        │ │     🍲       │ │
│ │   Món Việt     │ │   Món Á      │ │
│ │   124 công thức│ │   89 công thức│ │
│ └────────────────┘ └──────────────┘ │
│ ┌────────────────┐ ┌──────────────┐ │
│ │      🥘        │ │     🍖       │ │
│ │   Món Âu       │ │   BBQ        │ │
│ └────────────────┘ └──────────────┘ │
└─────────────────────────────────────┘
```

---

## Responsive Behavior

### Mobile (<600px)
```
Sheet width: 100% screen width
Height: 160px (auto-sizes to content)
Position: Bottom-aligned
Rounded: Top corners only (24px)
Backdrop: Full screen
```

### Tablet (600-1200px)
```
Sheet width: 400px (fixed, centered horizontally)
Height: 160px
Position: Bottom-aligned, centered
Rounded: All 4 corners (16px)
Backdrop: Full screen
Shadow: More pronounced
```

### Desktop/Web (>1200px)
**Alternative Display: Dropdown Menu**
```
┌───────────────────────┐
│ 🔍  Recipes        ›  │ <- 48px height
├───────────────────────┤
│ 📂  Categories     ›  │
└───────────────────────┘
    ▼ (arrow pointing to Explore icon)

Position: Above Explore icon in bottom nav
No backdrop needed
Click outside to dismiss
Width: 240px
```

---

## Accessibility

### Screen Reader
**Sheet announcement:**
```
"Menu with 2 options"
```

**Focus order:**
```
1. Option 1: "Recipes, button, navigate to search recipes"
2. Option 2: "Categories, button, navigate to category browser"
```

**Backdrop:**
```
"Close menu, button"
```

**Chevron:**
- Aria-hidden: true (decorative only)
- Not announced by screen readers
- Navigation intent in button role + label

### Keyboard Navigation
- **Tab:** Focus first option (Recipes)
- **Tab again:** Focus second option (Categories)
- **Enter/Space:** Activate focused option
- **Escape:** Close sheet
- **Tab backwards:** Loop through options

**Focus indicators:**
```
When focused:
┌─────────────────────────────────┐
│ 🔍  Recipes              ›     │ <- 2px orange border
└─────────────────────────────────┘
Border: 2px solid #FF6F00
Border radius: 12px
Offset: 2px outside element
```

### Touch Targets
- Each option: 56px height (exceeds 48px minimum)
- Full width tappable
- Visual feedback on press
- Haptic feedback (light impact)

---

## State Management

### Sheet States
1. **Hidden** - Default, not visible
2. **Opening** - Animation in progress (300ms)
3. **Open** - Fully visible, interactive
4. **Closing** - Animation out (250ms)
5. **Closed** - Animation complete, removed

### Gesture States
- **Idle** - No touch
- **Touching** - Finger down
- **Dragging** - Moving vertically
- **Releasing** - Finger up (evaluate dismiss)

---

## Edge Cases

### Case 1: Rapid Taps
```
User taps Explore multiple times quickly
  ↓
Debounce: Only first tap registers
  ↓
Subsequent taps ignored until sheet fully open
  ↓
Prevents animation conflicts
```

### Case 2: Sheet Already Open
```
User taps Explore while sheet is open
  ↓
Toggle behavior: Close sheet
  ↓
No re-opening
  ↓
Same tap to open/close pattern
```

### Case 3: Navigation During Animation
```
User taps option while sheet is opening
  ↓
Wait for animation to complete (300ms)
  ↓
Then execute navigation
  ↓
Prevents janky transitions
```

### Case 4: System Back Button (Android)
```
Sheet is open
  ↓
User presses hardware back button
  ↓
Sheet closes (doesn't exit app)
  ↓
Back stack: Sheet dismissed, stays on Home
```

### Case 5: Accidental Swipe During Tap
```
User intends to tap option
But finger moves down slightly during press
  ↓
Gesture recognition:
- Vertical movement < 10px → Tap
- Vertical movement > 10px → Swipe
  ↓
Prevents false dismissal from fat-finger taps
```

---

## Performance

### Rendering
- Sheet lazy-rendered (only when triggered)
- Backdrop on separate layer (GPU acceleration)
- Animations use transform (not layout properties)

### Memory
- Sheet disposed when closed
- Backdrop image cached
- No persistent memory overhead

### Animation Performance
- Target: 60fps (16.67ms per frame)
- Transform + opacity only (no reflows)
- Hardware acceleration enabled

---

## Design Rationale

### Why Bottom Sheet?
1. **Mobile-first pattern** - Thumb-reachable zone
2. **Modern convention** - Instagram, Twitter use it
3. **Non-intrusive** - Doesn't block entire screen
4. **Natural gesture** - Swipe to dismiss familiar
5. **Contextual** - Appears from trigger point

### Why No Handle?
1. **Redundant** - Swipe works without visual cue
2. **Modern trend** - Material You minimizes chrome
3. **Space efficiency** - Saves 12-16px vertical
4. **Cleaner aesthetic** - Less UI noise
5. **Focus** - Directs attention to content

### Why No Title?
1. **Self-evident** - Icons + text explain options
2. **Context clear** - User just tapped "Explore"
3. **Speed** - Faster to scan without header
4. **Simplicity** - Reduces cognitive load

### Why Chevron?
1. **Visual affordance** - Indicates navigation
2. **Standard pattern** - iOS/Android convention
3. **Directional cue** - "Tap to go forward"
4. **Clean aesthetic** - Balanced, not cluttered

---

## Light & Dark Mode

### Light Mode
```
┌─────────────────────────────────────┐
│   ┌─────────────────────────────┐  │
│   │ 🔍  Recipes              ›  │  │
│   └─────────────────────────────┘  │
│   ┌─────────────────────────────┐  │
│   │ 📂  Categories           ›  │  │
│   └─────────────────────────────┘  │
└─────────────────────────────────────┘

Background: White (#FFFFFF)
Item bg: Light gray (#F5F5F5)
Text: Black (#212121)
Chevron: Gray (#9E9E9E)
Shadow: 0 -4px 16px rgba(0,0,0,0.1)
Backdrop: Black 40%
```

### Dark Mode
```
┌─────────────────────────────────────┐
│   ┌─────────────────────────────┐  │
│   │ 🔍  Recipes              ›  │  │
│   └─────────────────────────────┘  │
│   ┌─────────────────────────────┐  │
│   │ 📂  Categories           ›  │  │
│   └─────────────────────────────┘  │
└─────────────────────────────────────┘

Background: Dark gray (#1E1E1E)
Item bg: Darker gray (#2C2C2C)
Text: White (#FFFFFF)
Chevron: Light gray (#BDBDBD)
Shadow: 0 -4px 16px rgba(0,0,0,0.4)
Backdrop: Black 40%
```

---

## Implementation Notes

### Animation Curves
- **Ease-out** (opening): Starts fast, slows down - Natural lift
- **Ease-in** (closing): Starts slow, speeds up - Natural fall
- **Spring** (snap back): Overshoot + settle - Playful feel

### Touch Handling
- Touch events: `onTapDown`, `onTapUp`, `onTapCancel`
- Gesture: `DragGesture` with velocity tracking
- Haptics: `HapticFeedback.lightImpact()`

### Z-Index Layering
```
Layer 4: Sheet (elevation 16)
Layer 3: Backdrop (opacity 0.4)
Layer 2: Content (dimmed)
Layer 1: Bottom Nav (hidden/visible based on sheet)
```

---

## Testing Scenarios

- [ ] Open bottom sheet from Explore tap
- [ ] Close by tapping backdrop
- [ ] Close by swiping down
- [ ] Close by tapping option (then navigate)
- [ ] Rapid tap handling (debounce)
- [ ] Toggle open/close with same button
- [ ] Android back button closes sheet
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Screen reader announcements
- [ ] Animations smooth at 60fps
- [ ] Responsive on different screen sizes
- [ ] Dark mode styling correct
- [ ] Touch targets >= 48px
- [ ] Focus indicators visible

---

## Summary

**Bottom Sheet Design:**
- ✅ Minimal 2-option list (160px height)
- ✅ 56px tap targets (accessible)
- ✅ Chevron indicators (navigation cue)
- ✅ Swipe-to-dismiss (no handle needed)
- ✅ Backdrop for focus + dismiss
- ✅ Smooth animations (300ms open, 250ms close)
- ✅ Responsive across devices
- ✅ Full keyboard + screen reader support
- ✅ Light & dark mode compatible

**Navigation:**
- 🧭 Explore tap → Bottom sheet
- 🔍 Recipes → Search screen
- 📂 Categories → Category grid
