# 👨‍🍳 Cooking Mode Screen - Design Specification

## Overview
Cooking Mode là màn hình fullscreen, hands-free, step-by-step guide cho quá trình nấu ăn thực tế. Được tối ưu hóa cho việc sử dụng trong bếp với giọng nói, timers tích hợp, chữ lớn, và navigation dễ dàng ngay cả khi tay đang bận.

**Access Point:** Recipe Detail → Tap "▶️ Bắt đầu nấu" button

**Key Features:**
- Fullscreen immersive mode (hide status bar)
- Extra large text (easy to read from distance)
- Voice commands ("Next step", "Start timer", etc.)
- Integrated timers with notifications
- Hands-free navigation
- Screen always on (prevent sleep)
- Maximum brightness
- Background timer support
- Progress saving & resume

---

## Visual Layout

### Step View (Main Screen)

```
┌─────────────────────────────────────┐
│ [×]              Phở Bò        [⋮] │ <- Minimal header
│                                     │
├─────────────────────────────────────┤
│                                     │
│                                     │
│         Step 2 of 8                 │ <- Step indicator
│         ━━━━━━━░░░░░░░░░░           │    Progress bar
│                                     │
│                                     │
│    Luộc xương bò với gừng          │ <- Step title
│                                     │    (28px, bold)
│                                     │
│    Cho xương bò vào nồi nước       │ <- Instructions
│    sôi, thêm gừng đập dập.         │    (22px, spacious)
│    Luộc 5 phút rồi vớt ra rửa      │
│    sạch. Điều này giúp khử         │
│    mùi hôi xương.                  │
│                                     │
│                                     │
│    ⏱️ 5 minutes                     │ <- Timer component
│    [Start Timer]                   │
│                                     │
│                                     │
│    💡 Tip: Nước luộc xương nên     │ <- Tips (optional)
│    đổ đi, không dùng để nấu phở   │
│                                     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  [← Previous]        [Next →]      │ <- Fixed navigation
│                                     │
│                          [🎙️]      │ <- Voice FAB
└─────────────────────────────────────┘
```

---

### With Active Timer

```
┌─────────────────────────────────────┐
│ [×]              Phở Bò        [⋮] │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │  ⏱️ Timer Running               │ │ <- Sticky timer bar
│ │  04:37 remaining                │ │    (orange bg)
│ │  ━━━━━━━━━━━━━━░░░░░░            │ │
│ │  [⏸️ Pause] [+1 min] [⏹️ Stop]  │ │
│ └─────────────────────────────────┘ │
│                                     │
│         Step 2 of 8                 │
│         ━━━━━━━░░░░░░░░░░           │
│                                     │
│    Luộc xương bò với gừng          │
│                                     │
│    Cho xương bò vào nồi nước...    │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  [← Previous]        [Next →]      │
│                          [🎙️]      │
└─────────────────────────────────────┘
```

---

### Voice Command Overlay

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│         [🎙️ Waveform animation]     │ <- Audio visualization
│                                     │
│         Listening...                │
│                                     │
│         "Next step"                 │ <- Recognized text
│                                     │
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘

Overlay: Semi-transparent black (85%)
Waveform: Audio-reactive animation
Auto-dismiss: After command execution (2s)
Voice feedback: TTS confirms action
```

---

## Components Detail

### 1. Header (Minimal)

```
┌─────────────────────────────────────┐
│ [×]              Phở Bò        [⋮] │
└─────────────────────────────────────┘
```

**Exit Button [×]:**
- Size: 48×48px (large for easy tap)
- Icon: X mark (28×28px, white)
- Position: Top-left, 12px margin
- Background: Semi-transparent black circle (rgba(0,0,0,0.5))
- Tap: Show exit confirmation dialog

**Recipe Title:**
- Text: Recipe name (18px, bold, white)
- Position: Center
- Text shadow: 0 2px 6px rgba(0,0,0,0.9)
- Max width: 60% screen width
- Truncate: Ellipsis if too long

**Menu Button [⋮]:**
- Size: 48×48px
- Icon: Three dots vertical (28×28px, white)
- Position: Top-right, 12px margin
- Background: Semi-transparent black circle
- Tap: Open options menu

**Header Container:**
- Height: 64px
- Background: Linear gradient
  - Top: rgba(0,0,0,0.6)
  - Bottom: rgba(0,0,0,0)
- Position: Absolute, overlay
- Z-index: 100 (always on top)

---

### 2. Step Indicator

```
┌─────────────────────────────────────┐
│         Step 2 of 8                 │
│         ━━━━━━━░░░░░░░░░░           │
└─────────────────────────────────────┘
```

**Step Label:**
- Text: "Step [current] of [total]" (20px, bold, black)
- Position: Center, 40px from top
- Background: White pill shape
  - Padding: 10px 28px
  - Border radius: 24px
  - Shadow: Elevation 2
- Color: Black (high contrast)

**Progress Bar:**
- Width: 80% screen width (centered)
- Height: 6px
- Margin: 12px top
- Border radius: 3px
- Background (inactive): Light gray #E0E0E0
- Foreground (active): Orange #FF6F00
- Animation: Smooth transition on step change
- Progress calculation: (current_step / total_steps) × 100%

**Example:**
- Step 2 of 8 = 25% progress
- Step 5 of 8 = 62.5% progress

---

### 3. Step Content Area

**Step Title:**
```
┌─────────────────────────────────────┐
│    Luộc xương bò với gừng          │
└─────────────────────────────────────┘

Font: 28px, bold, black
Weight: 700
Alignment: Center
Margin: 32px top
Max lines: 2
Line height: 1.3
Letter spacing: 0.3px
```

**Instructions Text:**
```
┌─────────────────────────────────────┐
│    Cho xương bò vào nồi nước sôi,  │
│    thêm gừng đập dập. Luộc 5 phút  │
│    rồi vớt ra rửa sạch. Điều này   │
│    giúp khử mùi hôi xương.         │
└─────────────────────────────────────┘

Font: 22px, regular, dark gray (#333)
Weight: 400
Line height: 1.7 (extra spacious for readability)
Alignment: Left (easier to scan)
Padding: 32px horizontal, 24px top
Max width: 600px (centered container)
```

**Content Container:**
- Background: White
- Padding: 48px 32px
- Scroll: Vertical if content overflows
- Min height: Screen height - header - navigation (80px)

**Content Scrolling:**
- Smooth scroll
- Fade indicators at top/bottom if scrollable
- Scroll to top on step change

---

### 4. Timer Component

**Inactive State (Not Started):**
```
┌─────────────────────────────────────┐
│    ⏱️ 5 minutes                     │
│    [Start Timer]                   │
└─────────────────────────────────────┘

Container:
- Background: Light orange #FFF3E0
- Border: 2px solid orange #FF6F00
- Border radius: 16px
- Padding: 20px
- Margin: 24px horizontal, 24px top
- Center aligned

Icon & Text:
- Icon: ⏱️ (28×28px)
- Text: "5 minutes" (20px, orange #FF6F00)
- Gap: 8px

Start Button:
- Height: 56px
- Width: 200px
- Background: Orange #FF6F00
- Text: "Start Timer" (18px, white, bold)
- Border radius: 28px
- Shadow: Elevation 2
- Margin: 16px top
- Tap: Start countdown
```

---

**Active Timer Bar (Sticky Top):**
```
┌─────────────────────────────────────┐
│  ⏱️ Timer Running                   │
│  04:37 remaining                    │
│  ━━━━━━━━━━━━━━░░░░░░                │
│  [⏸️ Pause] [+1 min] [⏹️ Stop]     │
└─────────────────────────────────────┘

Container:
- Position: Sticky top (below header)
- Background: Orange #FF6F00
- Padding: 16px
- Z-index: 90
- Full width

Header Row:
- Icon: ⏱️ (20×20px, white)
- Text: "Timer Running" (14px, white, bold)

Time Remaining:
- Text: "04:37 remaining" (24px, white, bold)
- Format: MM:SS
- Margin: 4px top

Progress Bar:
- Height: 6px
- Margin: 12px top
- Active: White
- Inactive: rgba(255,255,255,0.3)
- Animation: Countdown visual
- Direction: Right to left (depleting)

Control Buttons:
- Layout: Horizontal row, 12px gap
- Margin: 12px top

Pause Button:
- Size: 40×40px
- Icon: ⏸️ (24×24px)
- Background: rgba(255,255,255,0.2)
- Border: 1px solid white
- Border radius: 20px
- Tap: Pause countdown

+1 Min Button:
- Height: 36px
- Padding: 8px 16px
- Background: rgba(255,255,255,0.2)
- Text: "+1 min" (14px, white)
- Border: 1px solid white
- Border radius: 18px
- Tap: Add 60 seconds

Stop Button:
- Size: 40×40px
- Icon: ⏹️ (24×24px)
- Background: rgba(255,255,255,0.2)
- Border: 1px solid white
- Border radius: 20px
- Tap: Cancel timer (with confirmation)
```

---

**Timer Complete Notification:**
```
┌─────────────────────────────────────┐
│          🔔                         │
│                                     │
│      Timer Complete!                │
│                                     │
│      Luộc xương bò                 │
│                                     │
│      [Dismiss]                      │
└─────────────────────────────────────┘

Overlay: Semi-transparent black (80%)
Card: White, centered
  - Width: 80% screen (max 400px)
  - Padding: 32px
  - Border radius: 20px
  - Shadow: Elevation 16

Icon: 🔔 (64×64px, centered)
Title: "Timer Complete!" (24px, bold)
Timer name: "Luộc xương bò" (18px, gray)
Button: "Dismiss" (56px height, orange)

Sound: Notification chime (3 beeps)
Vibration: 3 short pulses (200ms each)
Auto-dismiss: After 30 seconds
```

---

### 5. Tips Section (Optional)

```
┌─────────────────────────────────────┐
│ 💡 Tip: Nước luộc xương nên đổ    │
│ đi, không dùng để nấu phở          │
└─────────────────────────────────────┘

Container:
- Background: Light yellow #FFF9C4
- Border-left: 4px solid orange #FF6F00
- Border radius: 8px
- Padding: 16px
- Margin: 24px horizontal, 16px top

Icon: 💡 (20×20px, left)
Text: 16px, regular, dark gray (#555)
Line height: 1.5
Font style: Normal (not italic)
Max width: 600px
```

---

### 6. Navigation Buttons (Fixed Bottom)

```
┌─────────────────────────────────────┐
│  [← Previous]        [Next →]      │
└─────────────────────────────────────┘

Container:
- Position: Fixed bottom
- Height: 88px
- Background: White
- Shadow: 0 -4px 16px rgba(0,0,0,0.1) (top shadow)
- Padding: 16px horizontal
- Z-index: 95

Previous Button:
- Height: 56px
- Width: 45% screen width
- Background: White
- Border: 2px solid orange #FF6F00
- Text: "← Previous" (18px, orange, medium)
- Border radius: 28px
- Icon: ← (20×20px, left)
- Disabled state:
  - Border: 2px solid gray #E0E0E0
  - Text: Gray #999
  - Opacity: 0.5
  - Not tappable on first step

Next Button:
- Height: 56px
- Width: 45% screen width
- Background: Orange #FF6F00
- Text: "Next →" (18px, white, bold)
- Border radius: 28px
- Icon: → (20×20px, right)
- Shadow: Elevation 2

Gap: 16px between buttons

Done Button (Last Step):
- Background: Green #4CAF50
- Text: "✓ Done" or "✓ Hoàn thành"
- Icon: ✓ (20×20px)
- Tap: Navigate to completion screen
```

---

### 7. Voice Command FAB (Floating Action Button)

```
┌───────┐
│  🎙️   │
└───────┘

Position: Bottom-right corner
  - 20px from right edge
  - 120px from bottom (above nav buttons)
  
Size: 64×64px (circular)
Background: Orange #FF6F00
Icon: 🎙️ Microphone (32×32px, white)
Shadow: Elevation 6
Z-index: 100

States:

Inactive (default):
- Background: Orange
- Icon: Static microphone

Listening:
- Background: Pulsing animation
  - Orange → Light orange → Orange
  - Duration: 1.5s loop
- Icon: Animated waveform
- Outer ring: Expanding circle effect

Processing:
- Background: Orange
- Icon: Spinner overlay
- Text: "Processing..." (below button)

Tap: Activate voice listening
Hold: Continuous listening mode
Release: Stop and process

Voice activated (hands-free):
- Auto-activates on wake word "Hey Chef"
- Visual indicator: Pulsing animation
```

---

### 8. Options Menu [⋮]

```
┌─────────────────────────────────────┐
│ 🎙️ Voice Commands        [ON ✓]   │
│                                     │
│ 🔊 Read Steps Aloud      [OFF ○]  │
│                                     │
│ ☀️  Keep Screen On       [ON ✓]   │
│                                     │
│ 🔆 Max Brightness        [ON ✓]   │
│                                     │
│ ───────────────────────────────     │
│                                     │
│ 📋 View Ingredients            >   │
│                                     │
│ ⏱️ Active Timers (1)           >   │
│                                     │
│ 🔄 Restart from Beginning      >   │
│                                     │
│ 📱 View Full Recipe            >   │
│                                     │
│ ───────────────────────────────     │
│                                     │
│ ❌ Exit Cooking Mode               │
└─────────────────────────────────────┘

Dropdown Menu:
- Appear from: Top-right
- Background: White
- Border radius: 16px
- Shadow: Elevation 16
- Width: 320px
- Padding: 12px
- Max height: 80% screen (scrollable)

Menu Items:

Toggle Items:
- Height: 52px
- Padding: 12px 16px
- Icon: Left (24×24px)
- Label: Center-left (16px)
- Toggle switch: Right
  - ON: Green background, white checkmark
  - OFF: Gray background, gray circle
- Tap: Toggle state, save immediately

Action Items:
- Height: 52px
- Icon: Left (24×24px)
- Label: 16px, black
- Chevron: Right > (gray)
- Tap: Execute action or navigate

Separator:
- Height: 1px
- Color: Light gray #F0F0F0
- Margin: 8px vertical

Exit Item:
- Text color: Red #F44336
- No chevron
- Tap: Show exit confirmation
```

---

## Special Screens

### Completion Screen

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│             🎉                      │
│                                     │
│       Cooking Complete!             │
│                                     │
│     Phở Bò is ready to serve       │
│                                     │
│                                     │
│   How did it turn out?              │
│                                     │
│   ⭐ ⭐ ⭐ ⭐ ⭐                        │ <- Tap to rate
│                                     │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ 📸 Share Your Creation      │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ 🔙 Back to Recipe           │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ 🔍 Find Similar Recipes     │   │
│   └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘

Background: White
Padding: 32px

Icon: 🎉 (80×80px, centered)
Confetti animation: Optional (3s)

Heading: "Cooking Complete!" (28px, bold)
Subtext: "[Recipe name] is ready to serve" (18px, gray)
Margin: 16px between elements

Question: "How did it turn out?" (16px, medium)

Star Rating:
- Size: 48×48px per star
- Gap: 12px
- Inactive: Gray outline
- Active: Yellow filled
- Tap: Rate 1-5 stars
- Save: Immediate on tap

Buttons:
- Height: 56px
- Width: 100% - 32px margin
- Border radius: 28px
- Margin: 12px vertical
- Font: 18px, bold

Share Button:
- Background: Light blue #E3F2FD
- Text: Blue #2196F3
- Icon: 📸 (24×24px)

Back Button:
- Background: Light gray #F5F5F5
- Text: Black
- Icon: 🔙 (24×24px)

Find Similar Button:
- Background: Light orange #FFF3E0
- Text: Orange #FF6F00
- Icon: 🔍 (24×24px)
```

---

### Exit Confirmation Dialog

```
┌─────────────────────────────────────┐
│ Exit Cooking Mode?                  │
├─────────────────────────────────────┤
│ Your progress will be saved.        │
│                                     │
│ Active timers: 1                    │
│ • Luộc xương: 04:37 remaining      │
│                                     │
│ Timers will continue running in     │
│ the background. You'll receive      │
│ notifications when they complete.   │
│                                     │
│ [Cancel]             [Exit]        │
└─────────────────────────────────────┘

Modal Dialog:
- Width: 90% screen (max 420px)
- Background: White
- Border radius: 20px
- Padding: 24px
- Shadow: Elevation 24
- Centered

Title: "Exit Cooking Mode?" (20px, bold)
Message: 16px, gray, line-height 1.5

Timer Info:
- Background: Light orange #FFF3E0
- Padding: 12px
- Border radius: 8px
- Margin: 16px vertical
- List style: Bullet points

Buttons:
- Height: 52px
- Border radius: 26px
- Margin: 8px horizontal
- Gap: 16px

Cancel Button:
- Width: 40%
- Background: Light gray #F5F5F5
- Text: Black (16px, medium)

Exit Button:
- Width: 50%
- Background: Orange #FF6F00
- Text: White (16px, bold)

Tap outside: Close dialog (same as Cancel)
```

---

### Ingredients Quick View (Bottom Sheet)

```
┌─────────────────────────────────────┐
│ [×]  Ingredients                    │
├─────────────────────────────────────┤
│                                     │
│ Nguyên liệu chính:                  │
│                                     │
│ ☐ Xương bò (1 kg)                  │
│ ☑️ Gừng (3 củ)                      │
│ ☐ Hành khô (2 củ)                  │
│ ☐ Bánh phở (500g)                  │
│ ☐ Thịt bò (300g)                   │
│ ☐ Hành lá (1 bó)                   │
│                                     │
│ Gia vị:                             │
│                                     │
│ ☐ Muối (2 tsp)                     │
│ ☐ Đường (1 tsp)                    │
│ ☐ Nước mắm (3 tbsp)                │
│ ☐ Hạt nêm (1 tsp)                  │
│                                     │
└─────────────────────────────────────┘

Bottom Sheet:
- Height: 60% screen
- Background: White
- Border radius: 24px (top corners)
- Drag handle: 48px wide, 4px tall, gray
- Shadow: Elevation 16
- Scrollable content

Header:
- Height: 56px
- Close button [×]: Left (40×40px)
- Title: "Ingredients" (18px, bold, center)
- Padding: 16px

Content:
- Padding: 0 24px 24px 24px
- Scroll: Vertical

Section Headers:
- Text: 16px, bold, orange
- Margin: 20px top, 12px bottom

Ingredient Items:
- Height: 48px
- Checkbox: 24×24px (left)
  - Unchecked: Gray border
  - Checked: Orange fill with white check
- Text: 16px, black
- Quantity: Gray, right side
- Tap area: Full row
- Tap: Toggle checkbox

Checked state persists during cooking session
Auto-scroll to unchecked items
```

---

## Voice Commands

### Supported Commands (Vietnamese + English)

**Navigation:**
```
Vietnamese:
- "Bước tiếp theo" → Next step
- "Bước kế tiếp" → Next step
- "Bước trước" → Previous step
- "Quay lại" → Previous step
- "Đọc lại" → Repeat current step
- "Nhảy đến bước [số]" → Go to specific step

English:
- "Next step" → Next step
- "Next" → Next step
- "Previous step" → Previous step
- "Previous" → Previous step
- "Go back" → Previous step
- "Repeat" → Repeat current step
- "Read step" → Read current step aloud
- "Go to step [number]" → Jump to specific step
```

---

**Timer Commands:**
```
Vietnamese:
- "Bắt đầu hẹn giờ" → Start timer
- "Hẹn giờ 5 phút" → Set 5 min timer
- "Dừng hẹn giờ" → Pause timer
- "Tiếp tục hẹn giờ" → Resume timer
- "Hủy hẹn giờ" → Cancel timer
- "Thêm 1 phút" → Add 1 minute
- "Còn bao nhiêu thời gian" → Announce time left

English:
- "Start timer" → Start timer
- "Set timer 5 minutes" → Custom timer
- "Set timer for [duration]" → Custom timer
- "Pause timer" → Pause timer
- "Resume timer" → Resume timer
- "Stop timer" → Cancel timer
- "Cancel timer" → Cancel timer
- "Add one minute" → Extend by 1 min
- "Add [number] minutes" → Extend by X min
- "How much time left?" → Announce remaining
- "Time remaining?" → Announce remaining
```

---

**Information Commands:**
```
Vietnamese:
- "Bước này là gì" → Read step title
- "Hiện nguyên liệu" → Show ingredients
- "Đóng nguyên liệu" → Close ingredients
- "Trợ giúp" → Show help
- "Các lệnh" → List commands

English:
- "What's this step?" → Read step title
- "What step am I on?" → Announce current step
- "Show ingredients" → Open ingredients sheet
- "Hide ingredients" → Close ingredients
- "Help" → Show available commands
- "What can I say?" → List commands
```

---

**Action Commands:**
```
Vietnamese:
- "Bỏ qua bước này" → Skip step (with confirm)
- "Khởi động lại" → Restart from beginning
- "Thoát" → Exit cooking mode

English:
- "Skip this step" → Skip (with confirmation)
- "Skip step" → Skip (with confirmation)
- "Restart" → Restart from beginning
- "Start over" → Restart from beginning
- "Exit cooking mode" → Exit (with confirmation)
- "Exit" → Exit (with confirmation)
```

---

### Voice Feedback Examples

**Navigation:**
```
User: "Next step"
AI: "Step 3 of 8: Nấu nước dùng phở"

User: "Bước trước"
AI: "Bước 2: Luộc xương bò với gừng"

User: "Đọc lại"
AI: "Cho xương bò vào nồi nước sôi, thêm gừng đập dập..."
```

---

**Timer:**
```
User: "Start timer"
AI: "Timer started. 5 minutes."

User: "Bắt đầu hẹn giờ"
AI: "Đã bắt đầu hẹn giờ. 5 phút."

User: "How much time left?"
AI: "4 minutes and 37 seconds remaining."

User: "Add one minute"
AI: "Added 1 minute. 5 minutes and 37 seconds remaining."

User: "Stop timer"
AI: "Timer stopped."
```

---

**Information:**
```
User: "What's this step?"
AI: "Step 2: Luộc xương bò với gừng"

User: "Show ingredients"
AI: "Opening ingredients list"
[Sheet slides up]

User: "What step am I on?"
AI: "You're on step 2 of 8"
```

---

### Wake Word Detection

**Wake Phrases:**
- "Hey Chef" (English)
- "Này Chef" (Vietnamese)

**Flow:**
```
User cooking, hands busy
  ↓
Says: "Hey Chef"
  ↓
System: Chime sound (acknowledgment)
  ↓
Voice overlay appears (listening)
  ↓
User: "Next step"
  ↓
Command processed
  ↓
AI: "Step 3 of 8: Nấu nước dùng"
  ↓
Advances to next step
  ↓
Auto-dismiss overlay
```

**Settings:**
- Always listening: ON/OFF toggle
- Wake word sensitivity: Low/Medium/High
- Confirmation sound: Beep/Voice/None
- Auto-disable at battery: 20% (configurable)

---

## User Flows

### Flow 1: Start Cooking Mode

```
User on Recipe Detail screen
  ↓
Scrolls to bottom action bar
  ↓
Sees buttons:
[🎙️ Đọc hướng dẫn] [▶️ Bắt đầu nấu]
  ↓
Taps [▶️ Bắt đầu nấu]
  ↓
Transition animation (fade + slide up)
  ↓
Cooking Mode activates:
- Fullscreen (hide status bar & nav bar)
- Screen brightness: Maximum
- Keep screen on: Enabled
- Orientation: Lock portrait (mobile)
  ↓
Shows Step 1 of 8:
┌─────────────────────────────┐
│ Step 1 of 8                 │
│ ━━░░░░░░░░░░░░░░            │
│                             │
│ Chuẩn bị nguyên liệu        │
│                             │
│ Rửa sạch xương bò, ngâm     │
│ nước muối 30 phút...        │
└─────────────────────────────┘
  ↓
User reads instructions
  ↓
Taps [Next →]
  ↓
Advance to Step 2
  ↓
Progress bar updates: ━━━━░░░░░░░░░░░░
```

---

### Flow 2: Use Timer

```
User on Step 2: "Luộc xương bò"
  ↓
Reads instruction: "Luộc 5 phút"
  ↓
Sees timer component:
┌─────────────────────────────┐
│ ⏱️ 5 minutes                 │
│ [Start Timer]               │
└─────────────────────────────┘
  ↓
Taps [Start Timer]
  ↓
Timer bar appears at top (sticky):
┌─────────────────────────────┐
│ ⏱️ Timer Running            │
│ 05:00 remaining             │
│ ━━━━━━━━━━━━━━━━━━━━        │
│ [⏸️] [+1 min] [⏹️]         │
└─────────────────────────────┘
  ↓
Countdown begins: 04:59... 04:58...
  ↓
User continues reading or moves to next step
  ↓
Timer keeps running (sticky at top)
  ↓
[After 5 minutes]
  ↓
Timer reaches 00:00
  ↓
Notification triggers:
- Sound: 3 beeps (ding-ding-ding)
- Vibration: 3 short pulses
- Overlay appears:
┌─────────────────────────────┐
│        🔔                   │
│                             │
│  Timer Complete!            │
│                             │
│  Luộc xương bò             │
│                             │
│  [Dismiss]                  │
└─────────────────────────────┘
  ↓
User taps [Dismiss]
  ↓
Overlay closes
  ↓
Timer bar disappears
  ↓
Continue cooking
```

---

### Flow 3: Voice Commands (Hands-Free)

```
User on Step 2
  ↓
Hands are wet/busy with ingredients
  ↓
Says: "Hey Chef" (wake word)
  ↓
System plays acknowledgment chime
  ↓
Voice overlay appears:
┌─────────────────────────────┐
│  [🎙️ Waveform animation]    │
│  Listening...               │
└─────────────────────────────┘
  ↓
User says: "Start timer"
  ↓
Overlay updates:
"Start timer" (recognized text)
  ↓
AI responds (audio): "Timer started. 5 minutes."
  ↓
Timer begins countdown
  ↓
Overlay dismisses after 2s
  ↓
[3 minutes later]
  ↓
User says: "Hey Chef, how much time left?"
  ↓
Voice activates
  ↓
AI responds: "2 minutes and 15 seconds remaining."
  ↓
[After timer completes]
  ↓
User says: "Hey Chef, next step"
  ↓
Voice activates
  ↓
Recognizes: "Next step"
  ↓
AI responds: "Step 3 of 8: Nấu nước dùng phở"
  ↓
Screen advances to Step 3
  ↓
Overlay dismisses
```

---

### Flow 4: View Ingredients Mid-Cooking

```
User on Step 5
  ↓
Forgets exact amount of seasoning
  ↓
Taps menu [⋮] in header
  ↓
Menu appears with options
  ↓
Taps "📋 View Ingredients >"
  ↓
Bottom sheet slides up:
┌─────────────────────────────┐
│ [×] Ingredients             │
├─────────────────────────────┤
│ ☑️ Xương bò (1 kg)         │
│ ☑️ Gừng (3 củ)             │
│ ☐ Muối (2 tsp)             │ <- Looking for this
│ ☐ Đường (1 tsp)            │
└─────────────────────────────┘
  ↓
User sees: Muối (2 tsp)
  ↓
Taps checkbox to mark as used
  ↓
Checkbox: ☐ → ☑️
  ↓
[Alternative: Voice command]
Says: "Hey Chef, show ingredients"
  ↓
Sheet opens automatically
  ↓
User done checking
  ↓
Swipes down or taps [×]
  ↓
Sheet dismisses
  ↓
Returns to Step 5
```

---

### Flow 5: Pause & Resume Cooking

```
User on Step 5
  ↓
Active timer: 15:30 remaining
  ↓
Phone rings / needs to step away
  ↓
Taps [×] exit button
  ↓
Confirmation dialog appears:
┌─────────────────────────────┐
│ Exit Cooking Mode?          │
│                             │
│ Progress will be saved.     │
│ Active timers: 1            │
│ • Nấu nước dùng: 15:30     │
│                             │
│ [Cancel] [Exit]            │
└─────────────────────────────┘
  ↓
Taps [Exit]
  ↓
Cooking Mode exits
  ↓
Returns to Recipe Detail screen
  ↓
Timer continues in background
  ↓
Cooking session saved:
{
  recipe_id: "recipe_001",
  current_step: 5,
  total_steps: 8,
  timers: [{...}]
}
  ↓
[15 minutes later, timer completes]
  ↓
Push notification:
"🔔 Timer complete: Nấu nước dùng"
  ↓
[User returns to app later]
  ↓
On Recipe Detail, sees:
[🔄 Resume Cooking (Step 5/8)]
  ↓
Taps [Resume]
  ↓
Cooking Mode reopens at Step 5
  ↓
Progress restored
  ↓
Completed timer shows in history
  ↓
User continues from where they left off
```

---

### Flow 6: Complete Cooking

```
User progresses through steps
  ↓
Reaches Step 8 (final step):
"Múc phở ra tô, thêm hành và ngò"
  ↓
Navigation button changes:
[← Previous]  [✓ Done]
  ↓
User completes final step
  ↓
Taps [✓ Done]
  ↓
Completion screen appears:
┌─────────────────────────────┐
│        🎉                   │
│  Cooking Complete!          │
│  Phở Bò is ready            │
│                             │
│  How did it turn out?       │
│  ⭐ ⭐ ⭐ ⭐ ⭐              │
└─────────────────────────────┘
  ↓
Optional confetti animation (3s)
  ↓
User taps 5 stars ⭐⭐⭐⭐⭐
  ↓
Stars fill with yellow
  ↓
API call: POST /api/v1/recipes/:id/rate
{
  rating: 5,
  cooking_session_id: "session_123"
}
  ↓
Toast: "Thanks for your feedback! ❤️"
  ↓
Cooking marked as complete in history
  ↓
Options available:
- [📸 Share Your Creation]
- [🔙 Back to Recipe]
- [🔍 Find Similar Recipes]
  ↓
User taps [Back to Recipe]
  ↓
Exit Cooking Mode
  ↓
Return to Recipe Detail screen
  ↓
Recipe shows:
- "✓ Cooked on Nov 25" badge
- "Your rating: ⭐⭐⭐⭐⭐"
- Updated stats
```

---

### Flow 7: Multiple Timers

```
User on Step 3
  ↓
Instruction: "Nấu nước dùng 2 giờ"
  ↓
Taps [Start Timer] for 120 minutes
  ↓
Timer 1 starts at top
  ↓
User advances to Step 4
  ↓
Step 4 has different timer: "Luộc thịt bò 15 phút"
  ↓
Taps [Start Timer]
  ↓
Timer 2 starts
  ↓
Now has 2 active timers
  ↓
Taps menu [⋮]
  ↓
Sees: "⏱️ Active Timers (2) >"
  ↓
Taps to view:
┌─────────────────────────────┐
│ Active Timers (2)           │
├─────────────────────────────┤
│ ⏱️ Nấu nước dùng           │
│ 01:45:22 remaining          │
│ ━━━━━━━━━░░░░░░░            │
│ [⏸️] [+1] [⏹️]             │
│                             │
│ ⏱️ Luộc thịt bò            │
│ 00:14:08 remaining          │
│ ━━━━━━━━━━━━━━━━━           │
│ [⏸️] [+1] [⏹️]             │
└─────────────────────────────┘
  ↓
Can control each timer individually
  ↓
When timer completes, notification shows
  ↓
Other timers continue running
```

---

## Backend Integration

### Save Cooking Session

**Endpoint:** `POST /api/v1/cooking-sessions`

**Request:**
```json
{
  "recipe_id": "recipe_001",
  "current_step": 5,
  "total_steps": 8,
  "started_at": "2024-11-25T14:30:00Z",
  "active_timers": [
    {
      "id": "timer_1",
      "name": "Nấu nước dùng",
      "duration": 7200,
      "remaining": 5430,
      "step": 5,
      "started_at": "2024-11-25T14:35:00Z"
    }
  ],
  "completed_steps": [1, 2, 3, 4],
  "ingredients_used": ["ing_001", "ing_002"]
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "session_12345",
  "can_resume": true,
  "expires_at": "2024-11-25T20:30:00Z"
}
```

**Session Expiry:** 6 hours from creation

---

### Resume Cooking Session

**Endpoint:** `GET /api/v1/cooking-sessions/:recipe_id/active`

**Response:**
```json
{
  "success": true,
  "has_active_session": true,
  "session": {
    "session_id": "session_12345",
    "recipe_id": "recipe_001",
    "recipe_name": "Phở Bò",
    "current_step": 5,
    "total_steps": 8,
    "started_at": "2024-11-25T14:30:00Z",
    "paused_at": "2024-11-25T15:00:00Z",
    "elapsed_time": 1800,
    "active_timers": [
      {
        "id": "timer_1",
        "name": "Nấu nước dùng",
        "remaining": 5430,
        "paused": true
      }
    ],
    "completed_steps": [1, 2, 3, 4]
  }
}
```

---

### Complete Cooking

**Endpoint:** `POST /api/v1/recipes/:id/complete`

**Request:**
```json
{
  "session_id": "session_12345",
  "completed_at": "2024-11-25T16:30:00Z",
  "total_time": 7200,
  "rating": 5,
  "notes": "Rất ngon! Nước dùng đậm đà",
  "difficulty_actual": "medium",
  "would_cook_again": true
}
```

**Response:**
```json
{
  "success": true,
  "cooking_history_id": "history_789",
  "achievement_unlocked": {
    "id": "ach_001",
    "name": "First Phở Master!",
    "icon": "🍜",
    "description": "Completed your first Phở recipe"
  },
  "stats": {
    "total_recipes_cooked": 15,
    "total_cooking_time": 43200,
    "favorite_category": "Món chính"
  }
}
```

---

## Technical Implementation

### Screen Management

**Keep Screen On:**
```dart
import 'package:wakelock/wakelock.dart';

class CookingModeScreen extends StatefulWidget {
  @override
  void initState() {
    super.initState();
    _enterCookingMode();
  }
  
  void _enterCookingMode() {
    // Keep screen awake
    Wakelock.enable();
    
    // Hide system UI (fullscreen)
    SystemChrome.setEnabledSystemUIMode(
      SystemUiMode.immersive,
    );
    
    // Set max brightness
    ScreenBrightness().setScreenBrightness(1.0);
    
    // Lock orientation (portrait on mobile)
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
  }
  
  @override
  void dispose() {
    _exitCookingMode();
    super.dispose();
  }
  
  void _exitCookingMode() {
    // Re-enable screen sleep
    Wakelock.disable();
    
    // Restore system UI
    SystemChrome.setEnabledSystemUIMode(
      SystemUiMode.edgeToEdge,
    );
    
    // Restore original brightness
    ScreenBrightness().resetScreenBrightness();
    
    // Unlock orientation
    SystemChrome.setPreferredOrientations([]);
  }
}
```

---

### Voice Recognition

**Speech-to-Text:**
```dart
import 'package:speech_to_text/speech_to_text.dart' as stt;

class VoiceController {
  final stt.SpeechToText _speech = stt.SpeechToText();
  
  Future<void> initialize() async {
    bool available = await _speech.initialize(
      onStatus: (status) => print('Status: $status'),
      onError: (error) => print('Error: $error'),
    );
    
    if (!available) {
      throw Exception('Speech recognition not available');
    }
  }
  
  Future<void> startListening(Function(String) onResult) async {
    await _speech.listen(
      onResult: (result) {
        if (result.finalResult) {
          String command = result.recognizedWords.toLowerCase();
          onResult(command);
        }
      },
      localeId: 'vi_VN', // Vietnamese
      listenFor: Duration(seconds: 10),
      pauseFor: Duration(seconds: 3),
      cancelOnError: false,
      partialResults: true,
    );
  }
  
  void stopListening() {
    _speech.stop();
  }
}
```

---

**Command Processing:**
```dart
void processVoiceCommand(String command) {
  // Normalize
  command = command.toLowerCase().trim();
  
  // Navigation commands
  if (command.contains('next') || 
      command.contains('tiếp theo') ||
      command.contains('kế tiếp')) {
    _goToNextStep();
    _speak('Step ${currentStep + 1} of $totalSteps');
  }
  else if (command.contains('previous') || 
           command.contains('trước') ||
           command.contains('quay lại')) {
    _goToPreviousStep();
    _speak('Step ${currentStep - 1} of $totalSteps');
  }
  
  // Timer commands
  else if (command.contains('start timer') ||
           command.contains('bắt đầu hẹn giờ')) {
    _startTimer();
    _speak('Timer started. ${timerDuration} minutes.');
  }
  else if (command.contains('stop timer') ||
           command.contains('dừng hẹn giờ')) {
    _stopTimer();
    _speak('Timer stopped.');
  }
  
  // Add 1 minute
  else if (command.contains('add one minute') ||
           command.contains('thêm một phút')) {
    _addTimeToTimer(60);
    _speak('Added 1 minute.');
  }
  
  // Time remaining
  else if (command.contains('how much time') ||
           command.contains('time left') ||
           command.contains('còn bao nhiêu')) {
    int remaining = _getTimerRemaining();
    _speak('${remaining ~/ 60} minutes and ${remaining % 60} seconds remaining.');
  }
  
  // Unknown command
  else {
    _speak('Sorry, I didn\'t understand. Say "help" for available commands.');
  }
}
```

---

### Timer Implementation

**Timer Model:**
```dart
class CookingTimer {
  String id;
  String name;
  int durationSeconds;
  int remainingSeconds;
  bool isActive;
  bool isPaused;
  Timer? _timer;
  
  void start() {
    isActive = true;
    isPaused = false;
    
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (!isPaused && remainingSeconds > 0) {
        remainingSeconds--;
        
        if (remainingSeconds == 0) {
          _onComplete();
          timer.cancel();
        }
      }
    });
  }
  
  void pause() {
    isPaused = true;
  }
  
  void resume() {
    isPaused = false;
  }
  
  void stop() {
    _timer?.cancel();
    isActive = false;
  }
  
  void addTime(int seconds) {
    remainingSeconds += seconds;
  }
  
  void _onComplete() {
    // Play sound
    AudioPlayer().play(AssetSource('sounds/timer_complete.mp3'));
    
    // Vibrate
    Vibration.vibrate(
      pattern: [0, 200, 100, 200, 100, 200],
      intensities: [0, 128, 0, 128, 0, 128],
    );
    
    // Show notification
    _showTimerCompleteNotification();
    
    isActive = false;
  }
  
  void _showTimerCompleteNotification() {
    // Local notification (even if app backgrounded)
    FlutterLocalNotificationsPlugin().show(
      id.hashCode,
      'Timer Complete! 🔔',
      name,
      NotificationDetails(
        android: AndroidNotificationDetails(
          'cooking_timers',
          'Cooking Timers',
          importance: Importance.high,
          priority: Priority.high,
          sound: RawResourceAndroidNotificationSound('timer_complete'),
        ),
        iOS: DarwinNotificationDetails(
          sound: 'timer_complete.aiff',
        ),
      ),
    );
  }
}
```

---

### Background Timer Service

**Android (Foreground Service):**
```dart
import 'package:flutter_foreground_task/flutter_foreground_task.dart';

void startForegroundService() {
  FlutterForegroundTask.init(
    androidNotificationOptions: AndroidNotificationOptions(
      channelId: 'cooking_mode',
      channelName: 'Cooking Mode',
      channelDescription: 'Active cooking timers',
      channelImportance: NotificationChannelImportance.LOW,
      priority: NotificationPriority.LOW,
      iconData: NotificationIconData(
        resType: ResourceType.mipmap,
        resPrefix: ResourcePrefix.ic,
        name: 'launcher',
      ),
    ),
  );
  
  FlutterForegroundTask.startService(
    notificationTitle: 'Cooking Phở Bò',
    notificationText: 'Timer: 15:30 remaining',
  );
}
```

---

## Performance Optimization

### Text-to-Speech (TTS)

**Implementation:**
```dart
import 'package:flutter_tts/flutter_tts.dart';

class TTSController {
  final FlutterTts _tts = FlutterTts();
  
  Future<void> initialize() async {
    await _tts.setLanguage('vi-VN'); // Vietnamese
    await _tts.setSpeechRate(0.5); // Normal speed
    await _tts.setVolume(1.0);
    await _tts.setPitch(1.0);
  }
  
  Future<void> speak(String text) async {
    await _tts.speak(text);
  }
  
  Future<void> stop() async {
    await _tts.stop();
  }
}
```

---

### State Management

**Riverpod Providers:**
```dart
// Current step
final currentStepProvider = StateProvider<int>((ref) => 0);

// Active timers
final activeTimersProvider = StateNotifierProvider<TimersNotifier, List<CookingTimer>>(
  (ref) => TimersNotifier(),
);

// Voice listening state
final voiceListeningProvider = StateProvider<bool>((ref) => false);

// Settings
final cookingSettingsProvider = StateProvider<CookingSettings>((ref) {
  return CookingSettings(
    voiceCommandsEnabled: true,
    autoReadSteps: false,
    keepScreenOn: true,
    maxBrightness: true,
  );
});
```

---

## Responsive Design

### Mobile Portrait (Primary)

```
┌──────────────┐
│ [×] Phở [⋮] │ 64px header
├──────────────┤
│              │
│ Step 2 of 8  │ Step indicator
│ ━━━━░░░░░░░  │ Progress
│              │
│ Title        │ Large text
│              │ optimized
│ Instructions │ for reading
│              │ from distance
│              │
│ [Timer]      │ Timer component
│              │
│ 💡 Tip       │ Optional tip
│              │
│              │ Scrollable
│              │ content
├──────────────┤
│ [Prev][Next] │ 88px nav
│          [🎙️]│ Voice FAB
└──────────────┘

Text sizes:
- Title: 28px
- Instructions: 22px
- Buttons: 18px

Padding: 32px horizontal
Max width: 100% (no constraint)
```

---

### Tablet Landscape

```
┌─────────────────────────────────────┐
│ [×] Phở Bò [⋮]                      │
├─────────────────────────────────────┤
│                                     │
│ Step 2 of 8   │  [Optional step    │
│ ━━━━░░░░░░░   │   photo or video]  │
│               │                    │
│ Title         │  [Timer component] │
│               │                    │
│ Instructions  │  💡 Tips          │
│ (even larger  │                    │
│  32px text)   │  [Ingredient      │
│               │   quick view]      │
│               │                    │
├─────────────────────────────────────┤
│     [Previous]      [Next]          │
│                             [🎙️]   │
└─────────────────────────────────────┘

Split layout:
- Left: Main content (60%)
- Right: Auxiliary info (40%)
- Text sizes increased: 32px title, 24px body
- Larger buttons: 64px height
- More whitespace
```

---

## Accessibility

### Screen Reader Support

**Semantic Labels:**
```dart
Semantics(
  label: 'Step 2 of 8. Luộc xương bò với gừng',
  child: Text('Step 2 of 8'),
);

Semantics(
  label: 'Next step button. Double tap to go to step 3',
  button: true,
  enabled: currentStep < totalSteps,
  child: ElevatedButton(...),
);

Semantics(
  label: 'Timer: 5 minutes. Double tap to start countdown',
  button: true,
  child: TimerButton(...),
);
```

---

**Live Regions:**
```dart
Semantics(
  liveRegion: true,
  child: Text('Timer: ${remaining.inMinutes}:${remaining.inSeconds % 60}'),
);

Semantics(
  liveRegion: true,
  child: Text('Step ${currentStep + 1} of $totalSteps'),
);
```

---

### Keyboard Navigation

**Focus Order:**
1. Exit button [×]
2. Menu button [⋮]
3. Timer start button (if present)
4. Previous button
5. Next button
6. Voice FAB

**Shortcuts:**
- Space/Enter: Activate focused button
- Esc: Exit cooking mode (with confirmation)
- Arrow Left: Previous step
- Arrow Right: Next step
- T: Start/stop timer
- V: Activate voice command

---

### High Contrast Mode

**Color Adjustments:**
```dart
if (MediaQuery.of(context).highContrast) {
  return Theme(
    data: ThemeData(
      textTheme: TextTheme(
        bodyLarge: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.black,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.black,
          foregroundColor: Colors.white,
          side: BorderSide(width: 2, color: Colors.white),
        ),
      ),
    ),
    child: child,
  );
}
```

---

## Summary

**Cooking Mode Screen Features:**
- ✅ Fullscreen immersive mode (hide status/nav bars)
- ✅ Extra large, readable text (22-28px)
- ✅ Step-by-step navigation with progress bar
- ✅ Integrated countdown timers
- ✅ Multiple simultaneous timers support
- ✅ Timer notifications (sound + vibration)
- ✅ Background timer continuation
- ✅ Voice commands (Vietnamese + English)
- ✅ Wake word detection ("Hey Chef")
- ✅ Hands-free operation
- ✅ Voice feedback (TTS)
- ✅ Keep screen on + max brightness
- ✅ Pause & resume cooking session
- ✅ Progress auto-save
- ✅ Quick ingredients view (bottom sheet)
- ✅ Optional tips per step
- ✅ Completion screen with rating
- ✅ Exit confirmation
- ✅ Responsive (portrait/landscape)
- ✅ Full accessibility (screen reader, keyboard, high contrast)
- ✅ Settings menu (voice, brightness, etc.)
- ✅ Achievement unlock on completion

---

**🎉 PHASE 2 COMPLETE!**

Tất cả 9 màn hình frontend đã được thiết kế:
1. ✅ Home Screen
2. ✅ Explore Bottom Sheet
3. ✅ Recipe Detail Screen
4. ✅ Chat AI Screen (RAG + Voice + Wake Word)
5. ✅ Camera Screen (AI Ingredient Recognition)
6. ✅ Profile Screen (AI Personality)
7. ✅ Search Screen
8. ✅ Categories Screen
9. ✅ **Cooking Mode Screen** ⭐

**Sẵn sàng chuyển sang Phase 3: Backend Design & Database Schema!**
