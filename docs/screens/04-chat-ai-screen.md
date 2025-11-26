# 💬 Chat AI Screen - Design Specification

## Overview
Chat AI Screen là trợ lý nấu ăn thông minh với RAG (Retrieval-Augmented Generation), hỗ trợ voice input/output tiếng Việt, và Wake Word Detection cho hands-free experience.

---

## Visual Layout

```
┌─────────────────────────────────────┐
│ [←] Trợ lý AI              [⋮]     │ <- AppBar
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────┐      │
│  │ Chào bạn! Tôi là trợ lý  │      │ <- AI Message (left)
│  │ nấu ăn. Bạn muốn nấu món │      │    Gray bubble
│  │ gì hôm nay?              │      │
│  └──────────────────────────┘      │
│  10:30                              │ <- Timestamp
│                                     │
│         ┌──────────────────────┐   │
│         │ Tôi có gà, cà chua, │   │ <- User Message (right)
│         │ hành tây. Nấu món gì?│   │    Orange bubble
│         └──────────────────────┘   │
│                        10:31        │
│                                     │
│  ┌──────────────────────────┐      │
│  │ 🤔 Typing...             │      │ <- Typing indicator
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ Tuyệt! Với nguyên liệu này,  │  │ <- AI with embedded recipe
│  │ bạn có thể nấu:              │  │
│  │                              │  │
│  │ ╭──────────────────────╮     │  │
│  │ │ [Recipe Card]        │     │  │ <- Interactive card
│  │ │ Gà Sốt Cà Chua      │     │  │
│  │ │ ⭐ 4.7  ⏱️ 30p       │     │  │
│  │ ╰──────────────────────╯     │  │
│  │                              │  │
│  │ Bạn muốn xem công thức này? │  │
│  └──────────────────────────────┘  │
│                                     │
│                                     │
│  [Scroll for more messages...]     │
│                                     │
├─────────────────────────────────────┤
│ [📎] Nhập tin nhắn...  [🎙️] [📤]  │ <- Input bar (fixed)
└─────────────────────────────────────┘    Height: 56px
```

---

## Components Detail

### 1. AppBar

```
┌─────────────────────────────────────┐
│ [←]  Trợ lý AI               [⋮]   │
└─────────────────────────────────────┘
Height: 56px
Background: White (light) / Dark (#1E1E1E)
```

**Elements:**
- **Back button** (left, 40×40px):
  - Icon: Arrow left
  - Tap: Return to previous screen
- **Title:** "Trợ lý AI" (18px, bold)
- **Menu button** (right, 40×40px):
  - Icon: Three dots vertical (⋮)
  - Tap: Open menu

**Menu Options:**
```
┌─────────────────────────────────┐
│ Xóa lịch sử chat                │
│ Cài đặt voice                   │
│ Cài đặt Wake Word               │
│ Báo cáo vấn đề                  │
└─────────────────────────────────┘
```

---

### 2. Chat Messages Area

**Scroll Behavior:**
- Reverse list (oldest top, newest bottom)
- Auto-scroll to bottom on new message
- Pull-to-refresh loads older messages (20 more)
- Sticky date headers ("Hôm nay", "Hôm qua", date)

**Padding:**
- Top: 16px
- Bottom: 16px (+ input bar height)
- Horizontal: 16px

---

### 3. Message Bubbles

#### AI Message (Left-aligned)

```
┌─────────────────────────────────────┐
│ ┌─ 🤖 ─┐                            │
│ │ AI   │  ┌──────────────────────┐  │
│ └──────┘  │ Chào bạn! Tôi có thể│  │ <- Gray bubble
│           │ giúp gì cho bạn?    │  │    #F5F5F5
│           └──────────────────────┘  │
│ 10:30 AM                            │ <- Timestamp
└─────────────────────────────────────┘
```

**Avatar:**
- Size: 32×32px circle
- Icon: 🤖 or robot image
- Position: Top-left, aligned with first line
- Margin: 8px from bubble

**Bubble:**
- Max width: 75% screen width
- Background: Light gray (#F5F5F5)
- Text color: Black (#212121)
- Border radius: 18px
- Padding: 12px horizontal, 10px vertical
- Tail: Small triangle pointing left (optional)
- Shadow: None

**Timestamp:**
- Font: 12px, regular
- Color: Gray (#9E9E9E)
- Position: Below bubble, left-aligned
- Margin: 4px top

---

#### User Message (Right-aligned)

```
┌─────────────────────────────────────┐
│                  ┌──────────────────┐│
│                  │ Tôi có gà, cà   ││ <- Orange bubble
│                  │ chua, hành tây  ││    #FF6F00
│                  └──────────────────┘│
│                            10:31 AM  │ <- Timestamp
└─────────────────────────────────────┘
```

**Bubble:**
- Max width: 75% screen width
- Background: Orange (#FF6F00)
- Text color: White (#FFFFFF)
- Border radius: 18px
- Padding: 12px horizontal, 10px vertical
- Alignment: Right
- No avatar (user identity implied)

**Timestamp:**
- Font: 12px, regular
- Color: Gray (#9E9E9E)
- Position: Below bubble, right-aligned
- Margin: 4px top

---

### 4. Special Message Types

#### Typing Indicator

```
┌─────────────────────────────────────┐
│ ┌─ 🤖 ─┐                            │
│ └──────┘  ┌────────────┐            │
│           │ ●●● ...    │            │ <- Animated dots
│           └────────────┘            │    Gray bubble
└─────────────────────────────────────┘
```

**Animation:**
- 3 dots: ● ● ●
- Bounce sequentially
- Cycle duration: 500ms
- Infinite loop while typing

**Appearance:**
- Shows when AI is processing
- Replaces with actual message when ready
- Same styling as AI bubble

---

#### Recipe Card Embedded

```
┌─────────────────────────────────────┐
│ ┌─ 🤖 ─┐                            │
│ └──────┘  ┌────────────────────┐    │
│           │ Với nguyên liệu    │    │ <- Text message
│           │ này, bạn có thể:   │    │
│           │                    │    │
│           │ ╭────────────────╮ │    │
│           │ │ [Image] 80×80  │ │    │ <- Recipe card
│           │ │ Gà Sốt Cà Chua │ │    │    White bg
│           │ │ ⭐ 4.7 ⏱️ 30p  │ │    │    Rounded 12px
│           │ │ [Xem chi tiết] │ │    │    Tappable
│           │ ╰────────────────╯ │    │
│           │                    │    │
│           │ Bạn muốn xem công  │    │
│           │ thức chi tiết?     │    │
│           └────────────────────┘    │
└─────────────────────────────────────┘
```

**Recipe Card Specs:**
- Width: 100% of bubble (minus padding)
- Height: Auto (min 120px)
- Background: White
- Border radius: 12px
- Padding: 12px
- Shadow: 0 2px 4px rgba(0,0,0,0.1)
- Margin: 8px vertical (within bubble)

**Components:**
- **Thumbnail:** 80×80px, left-aligned, rounded 8px
- **Title:** 14px, bold, 2 lines max
- **Metadata:** Rating (⭐ 4.7) + Time (⏱️ 30p), 12px
- **Button:** "Xem chi tiết" (outline, 32px height)

**Action:**
- Tap card → Navigate to Recipe Detail screen
- Hero animation from thumbnail

---

#### Multiple Recipe Carousel

```
┌─────────────────────────────────────┐
│ ┌─ 🤖 ─┐                            │
│ └──────┘  ┌────────────────────┐    │
│           │ Tôi tìm thấy 3 món:│    │
│           │                    │    │
│           │ ╭──────╮ ╭──────╮ │ >> │ <- Horizontal scroll
│           │ │Recipe│ │Recipe│ │    │    Snap pagination
│           │ │  1   │ │  2   │ │    │    3 cards
│           │ ╰──────╯ ╰──────╯ │    │
│           │   ● ○ ○            │    │ <- Page indicators
│           └────────────────────┘    │
└─────────────────────────────────────┘
```

**Carousel:**
- Horizontal scroll with snap
- Card size: 140×180px each
- Gap: 8px between cards
- Page indicators: Dots below (8px circles)
- Swipe left/right to navigate

---

#### Quick Reply Suggestions

```
┌─────────────────────────────────────┐
│ ┌─ 🤖 ─┐                            │
│ └──────┘  ┌────────────────────┐    │
│           │ Bạn muốn biết gì?  │    │
│           └────────────────────┘    │
│                                     │
│  ┌─────────────┐ ┌──────────────┐   │
│  │ Cách nấu    │ │ Thay thế     │   │ <- Suggestion chips
│  │ thế nào?    │ │ nguyên liệu  │   │    Tap to send
│  └─────────────┘ └──────────────┘   │
│                                     │
│  ┌─────────────┐ ┌──────────────┐   │
│  │ Lưu ý gì?   │ │ Món khác     │   │
│  └─────────────┘ └──────────────┘   │
└─────────────────────────────────────┘
```

**Suggestion Chip:**
- Height: 36px
- Padding: 8px 16px
- Border: 1px solid #E0E0E0
- Background: White
- Text: 14px, gray
- Border radius: 20px (pill)
- Margin: 4px gap

**Action:**
- Tap chip → Send as user message
- Chip disappears after tap
- New AI response generated

---

### 5. Input Bar (Fixed Bottom)

```
┌─────────────────────────────────────┐
│ [📎]  [Text Input Area...]  [🎙️] [📤]│
│  ^           ^                ^   ^  │
│  |           |                |   |  │
│  Attach   Multi-line       Voice Send│
└─────────────────────────────────────┘
```

**Dimensions:**
- Height: 56px (auto-expands to 120px max)
- Background: White (light) / Dark (#1E1E1E)
- Top border: 1px solid #E0E0E0
- Shadow: 0 -2px 8px rgba(0,0,0,0.08)
- Padding: 8px horizontal

---

#### Attach Button (📎)

```
[📎] 24×24px icon, gray
Tap: Opens attachment menu
```

**Attachment Menu:**
```
┌─────────────────────────────────┐
│ 📷 Camera                       │ <- Take photo
│ 🖼️ Gallery                      │ <- Choose image
│ 🧾 Recipe URL                   │ <- Paste link
└─────────────────────────────────┘
```

**Actions:**
- **Camera:** Open camera, take photo of ingredients
- **Gallery:** Pick image from library
- **URL:** Paste recipe link to parse

---

#### Text Input

```
┌────────────────────────────────┐
│ Nhập tin nhắn...               │ <- Placeholder (gray)
└────────────────────────────────┘
```

**Specs:**
- Font: 16px, regular
- Padding: 12px vertical, 8px horizontal
- Border: None (borderless)
- Background: Transparent
- Placeholder color: Gray (#9E9E9E)
- Auto-expand: 1-4 lines (max 120px height)
- Scroll: When exceeds 4 lines

**Behavior:**
- Tap: Focus, show keyboard
- Type: Real-time input
- Enter (mobile): New line (Shift+Enter on desktop: send)
- Empty: Disable send button

---

#### Voice Button (🎙️)

```
[🎙️] 40×40px circular button
```

**States:**

**Default (Idle):**
- Background: White
- Border: 1px solid gray
- Icon: Mic (gray, 20×20px)

**Recording:**
- Background: Orange (#FF6F00)
- Border: None
- Icon: Mic (white, pulsing animation)
- Size: Scale 1.1 (breathing effect)

**Processing:**
- Background: Orange
- Icon: Loading spinner (white)

**Interaction:**
```
Tap mic button
  ↓
Haptic feedback + sound cue
  ↓
Button turns orange, pulsing
  ↓
"Listening..." text appears above input
  ↓
User speaks (Vietnamese)
  ↓
Release or tap again to stop
  ↓
"Processing..." (spinner)
  ↓
STT result appears in text input
  ↓
User can edit or send directly
```

---

#### Send Button (📤)

```
[📤] 40×40px circular button
```

**States:**

**Disabled (Input empty):**
- Background: Gray (#E0E0E0)
- Icon: Send arrow (gray, 50% opacity)
- Not tappable

**Enabled (Has text):**
- Background: Orange (#FF6F00)
- Icon: Send arrow (white, 20×20px)
- Shadow: 0 2px 4px rgba(255,111,0,0.3)

**Pressed:**
- Scale: 0.95
- Shadow: Reduced
- Duration: 100ms

**Action:**
- Tap: Send message
- Clear input field
- Scroll to bottom
- Show typing indicator

---

## Voice Features

### Voice Input (STT)

#### Activation Methods

**Method 1: Button Press**
```
Tap mic button → Immediate recording
Release or tap again → Stop and process
```

**Method 2: Hold-to-Talk**
```
Long press mic → Record while holding
Release → Auto-process and send
```

#### Visual Feedback

**Recording Overlay:**
```
┌─────────────────────────────────────┐
│                                     │
│     🎙️  Listening...                │
│                                     │
│     ╭───────────────────╮           │
│     │ ▂▃▅▇▅▃▂          │           │ <- Waveform animation
│     ╰───────────────────╯           │    Real-time visualization
│                                     │
│     Tap to stop                     │ <- Hint text
│                                     │
└─────────────────────────────────────┘
```

**Overlay Specs:**
- Position: Center of screen
- Background: Semi-transparent white (90%)
- Border radius: 24px
- Padding: 40px
- Shadow: Elevation 16

**Waveform:**
- Height: 60px
- Width: 200px
- Bars: 20 vertical bars
- Animation: Responds to audio amplitude
- Color: Orange gradient

**Language:** Vietnamese (vi-VN)

**Backend Processing:**
- Audio recorded as WAV/MP3
- Sent to FastAPI backend
- OpenAI Whisper API transcription
- Returns text to display

---

### Voice Output (TTS)

#### Trigger Options

**Option 1: Manual (Per Message)**
```
Each AI message has "🎙️ Đọc to" button
Tap to play that specific message
```

**Option 2: Auto-play (Setting)**
```
Settings → Voice → Auto-read responses: ON
Every AI response auto-plays TTS
```

#### Audio Controls

```
┌─────────────────────────────────────┐
│ ┌─ 🤖 ─┐                            │
│ └──────┘  ┌────────────────────┐    │
│           │ [Message content]  │    │
│           └────────────────────┘    │
│                                     │
│ [🎙️ Đọc to] [⏸️ Pause] [⏭️ Skip]   │ <- Audio controls
└─────────────────────────────────────┘
```

**Controls appear when TTS active:**
- **🎙️ Đọc to:** Start playback
- **⏸️ Pause:** Pause/Resume
- **⏭️ Skip:** Stop and move to next

**Settings:**
```
Voice Settings:
- Speed: 0.75x - 1.5x (slider)
- Voice type: Male / Female (dropdown)
- Auto-read: On / Off (toggle)
- Volume: System volume control
```

**Backend:**
- Text sent to FastAPI
- OpenAI TTS API generates audio
- Returns audio bytes (MP3)
- Play using audio player

---

### Wake Word Detection

#### Concept
- Wake word: "Hey Chef" (English) / "Này Chef" (Vietnamese)
- Always-listening mode (optional)
- Hands-free activation

#### Activation Modes

**Mode 1: Always Listening (Background)**
```
App in foreground
  ↓
Wake word detection runs continuously
  ↓
User says: "Hey Chef"
  ↓
System recognizes wake word
  ↓
Mic activates automatically
  ↓
Waiting for command...
  ↓
User: "Tìm món gà kho"
  ↓
Process and respond
```

**Visual Indicator:**
```
┌─────────────────────────────────────┐
│ [←] Trợ lý AI              [⋮]     │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ● Listening for "Hey Chef"      │ │ <- Status bar
│ └─────────────────────────────────┘ │    Green pulsing dot
│                                     │    Dismissible
│ [Chat messages...]                  │
└─────────────────────────────────────┘
```

**Status Bar Specs:**
- Height: 32px
- Background: Light green (#E8F5E9)
- Text: 12px, green (#4CAF50)
- Dot: 8×8px, pulsing (1s cycle)
- Close button: X (right side)

---

**Mode 2: Manual Toggle**

```
Input bar with wake word button:
┌─────────────────────────────────────┐
│ [📎] [Text Input] [🎙️] [👂] [📤]  │
│                         ^           │
│                    Wake Word Toggle │
└─────────────────────────────────────┘
```

**Button States:**

**OFF:**
- Icon: Ear (👂), gray
- Background: White
- Border: 1px gray
- Size: 40×40px

**ON:**
- Icon: Ear (👂), white
- Background: Green (#4CAF50)
- Pulsing animation (subtle)
- Size: 40×40px

**Tap:** Toggle on/off

---

#### Wake Word Flow

```
User: "Hey Chef"
  ↓
┌─────────────────────────────────────┐
│ 🎙️  I'm listening...                │ <- Full screen overlay
│                                     │    500ms after wake word
│     ╭───────────────────╮           │
│     │ ▂▃▅▇▅▃▂          │           │ <- Waveform
│     ╰───────────────────╯           │
│                                     │
│     Speak now...                    │
└─────────────────────────────────────┘
  ↓
User: "Tìm món ăn từ gà"
  ↓
(3 seconds silence OR max 10s timeout)
  ↓
┌─────────────────────────────────────┐
│     Processing...                   │ <- Processing state
│         ⏳                          │
└─────────────────────────────────────┘
  ↓
Voice converted to text
  ↓
Sent as message to AI
  ↓
AI responds (text + optional TTS)
  ↓
Wake word detection resumes (if enabled)
```

---

#### Wake Word Settings

```
┌─────────────────────────────────────┐
│ Voice & Wake Word Settings          │
├─────────────────────────────────────┤
│                                     │
│ Wake Word Detection                 │
│ ○ Off                               │
│ ● Always On                         │
│ ○ Manual Toggle                     │
│                                     │
│ Wake Word                           │
│ ┌─────────────────────────────────┐ │
│ │ Hey Chef          [Customize >] │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Sensitivity                         │
│ Low ━━●━━━━━━━━ High               │ <- Slider
│                                     │
│ Timeout after Wake Word             │
│ 10 seconds                          │
│                                     │
│ [×] Haptic feedback on activation   │
│ [×] Sound confirmation              │
│ [×] Show visual indicator           │
│                                     │
│ Privacy                             │
│ ○ On-device only                    │
│ ● On-device + Cloud (More accurate) │
│                                     │
└─────────────────────────────────────┘
```

**Wake Word Options:**
- **English:** "Hey Chef" (default), "Ok Chef", "Hey Cooking"
- **Vietnamese:** "Này Chef" (default), "Ê Chef", "Chef ơi"
- **Custom:** User can train custom phrase (advanced)

**Sensitivity:**
- Low: Fewer false positives, may miss some
- High: More responsive, more false positives
- Default: Medium

**Timeout:**
- Duration to wait for command after wake word
- Options: 5s, 10s (default), 15s, 20s

---

#### Audio Feedback

**Wake Word Detected Sound:**

**Option 1: Chime (Default)**
- Sound: "Ding" (200ms)
- Volume: Medium
- Pitch: Rising (C to E)

**Option 2: Voice Confirmation**
- TTS: "Vâng?" (Vietnamese) / "Yes?" (English)
- Duration: 500ms

**Option 3: Beep**
- Sound: Single beep (100ms)
- Frequency: 800Hz
- Volume: Low

**Haptic Feedback:**
- Pattern: Light → Medium → Light
- Duration: 300ms
- Purpose: Physical confirmation

---

#### Privacy & Battery

**Privacy Controls:**
```
Wake Word Processing:
○ On-device only (Private, less accurate)
● On-device + Cloud (Accurate, recommended)

[×] Process audio locally first
[×] Delete voice data after session
[ ] Keep voice data for improvement

Microphone Access:
Only when app is open (not background)
```

**On-device:**
- Lightweight ML model (TensorFlow Lite)
- ~5-10MB model size
- No audio to server until wake word
- Lower accuracy but private

**Hybrid (Recommended):**
- On-device for wake word detection
- Cloud STT for command transcription
- Best balance

**Battery Management:**
```
Always On mode: ~3-7% battery/hour
Manual Toggle: Only when enabled
Smart mode: Auto-disable at 20% battery

⚠️ Low Battery (20%):
"Wake word paused to save battery"
[Keep Enabled] [Ok]

Auto-disable at 10%
```

---

## Conversation Flows

### Flow 1: Basic Q&A
```
User: "Cách luộc trứng lòng đào?"
  ↓
AI: Typing indicator (2s)
  ↓
AI: "Để luộc trứng lòng đào:
     1. Đun sôi nước
     2. Cho trứng vào
     3. Luộc 6-7 phút
     4. Ngâm nước lạnh
     
     Bạn muốn xem video hướng dẫn không?"
  ↓
Quick replies: [Có] [Không] [Mẹo khác?]
```

### Flow 2: Ingredient Search (RAG)
```
User: "Tôi có gà, khoai tây, cà rốt"
  ↓
AI: Typing (3s, RAG query to vector DB)
  ↓
AI: "Tuyệt! Tôi tìm thấy 5 món với nguyên liệu này:"
     [Recipe Card 1: Gà Kho Khoai Tây] ⭐ 4.8
     [Recipe Card 2: Gà Nướng] ⭐ 4.6
     >>> (horizontal scroll for more)
  ↓
User taps Recipe Card 1
  ↓
Navigate to Recipe Detail screen
```

### Flow 3: Substitution Question
```
User: "Thay nước mắm bằng gì?"
  ↓
AI: "Bạn có thể thay nước mắm bằng:
     • Nước tương (1:1 ratio)
     • Muối + đường (1 tsp mỗi thứ)
     • Soy sauce (ít mặn hơn)
     
     Bạn đang nấu món gì?"
  ↓
User: "Phở"
  ↓
AI: "Với phở, tôi khuyên dùng nước tương + 
     chút đường để giữ vị ngọt thanh."
     
← Context-aware (remembers "phở" from previous message)
```

### Flow 4: Voice Input
```
User: Taps 🎙️ button
  ↓
Mic activates (orange, pulsing)
  ↓
User speaks: "Tìm món ăn vặt dễ làm"
  ↓
STT converts (2s processing)
  ↓
Text appears in input field (editable)
  ↓
User taps send (or auto-send if configured)
  ↓
AI responds with snack recipe suggestions
```

### Flow 5: Image Upload
```
User: Taps 📎 → Camera
  ↓
Takes photo of fridge ingredients
  ↓
Image appears in chat as user message
  ↓
AI: "Đang nhận diện nguyên liệu..." (loading)
  ↓
Vision API processes (OpenAI GPT-4V)
  ↓
AI: "Tôi thấy trong ảnh có:
     ✓ Cà chua (3 quả)
     ✓ Hành tây (2 củ)
     ✓ Trứng (6 quả)
     
     Bạn muốn tôi gợi ý món ăn?"
  ↓
Quick replies: [Có] [Sửa nguyên liệu]
```

### Flow 6: Wake Word Hands-Free
```
User cooking (hands busy/wet)
  ↓
User: "Hey Chef"
  ↓
Wake word detected (500ms)
  ↓
Overlay: "I'm listening..."
  ↓
User: "Bước tiếp theo là gì?"
  ↓
AI: Reads next cooking step via TTS
  ↓
User: "Hey Chef"
  ↓
User: "Hẹn giờ 10 phút"
  ↓
AI: "Timer set for 10 minutes" + starts timer
```

---

## Context Awareness & Multi-turn

### Session Memory
- Last 10 messages kept in context
- User preferences remembered:
  - Dietary restrictions (vegetarian, no pork, etc.)
  - Spice level preference
  - Cooking skill level
- Recipe history influences suggestions

### Example Multi-turn:
```
User: "Phở cần nguyên liệu gì?"
AI: [Lists phở ingredients]

User: "Thịt bò nên mua phần nào?"
AI: "Với phở, nên dùng thịt bò nạm hoặc gân..."
     ← Remembers talking about phở

User: "Còn món khác không?"
AI: "Ngoài phở, với thịt bò bạn có thể nấu..."
     ← Still in beef context
```

---

## Smart Suggestions

### Time-based
```
Morning (6-10 AM):
AI: "Chào buổi sáng! Bạn muốn nấu gì cho bữa sáng?"
Suggestions: [Phở] [Bánh mì] [Cháo]

Afternoon (15-17 PM):
AI: "Bạn cần gợi ý món cho bữa tối không?"

Evening (20-22 PM):
AI: "Muốn làm món tráng miệng?"
```

### Trending
```
AI: "Món đang hot hôm nay: 🔥 Gà Popcorn Hàn Quốc
     124 người đã nấu tuần này!"
     [Xem công thức]
```

### Weather-based
```
Rainy day:
AI: "Hôm nay trời mưa, nấu lẩu ấm áp nhé!"

Hot day:
AI: "Trời nóng, thử món salad mát lành?"
```

---

## Error Handling

### No Results Found
```
User: "Món ăn từ sao Hỏa"
  ↓
AI: "Xin lỗi, tôi không tìm thấy món ăn này 😅
     
     Bạn có thể thử:
     • Mô tả nguyên liệu bạn có
     • Hỏi về kỹ thuật nấu ăn
     • Yêu cầu gợi ý món ăn"
```

### Ambiguous Query
```
User: "Gà"
  ↓
AI: "Bạn muốn:
     • Tìm công thức món gà?
     • Hỏi về cách chế biến gà?
     • Xem tips chọn gà tươi?
     
     Hoặc cho tôi biết thêm chi tiết!"
```

### Network Error
```
AI: "⚠️ Mất kết nối internet
     
     Vui lòng kiểm tra kết nối và thử lại
     
     [Thử lại]"
```

### STT Failed
```
Voice input unclear
  ↓
Show in input: "[Không nghe rõ]"
  ↓
User can retry or type manually
```

---

## Responsive Design

### Mobile (<600px)
- Single column chat
- Bubbles max 75% width
- Input bar full width
- Voice button 40×40px

### Tablet (600-1200px)
- Chat area max 600px, centered
- Wider bubbles (80% max width)
- Side margins for readability
- Larger tap targets

### Desktop (>1200px)
```
┌─────────────────────────────────────┐
│ [Sidebar]  │  [Chat Area]           │
│            │                        │
│ Recent     │  Messages              │
│ Chats      │                        │
│ (Future)   │                        │
│            │  Input bar             │
└─────────────────────────────────────┘

Split view:
- Left: Conversation history (200px)
- Right: Active chat (max 800px)
```

---

## Accessibility

### Screen Reader
- AI message: "AI assistant says: [content]"
- User message: "You said: [content]"
- Recipe card: "[Recipe name], rated [X] stars, cooking time [Y] minutes, tap to view details"
- Voice button: "Record voice message, button, tap to start recording"
- Send button: "Send message, button, [enabled/disabled]"
- Wake word: "Wake word detection [on/off]"

### Keyboard Navigation
- Tab to input field
- Enter to send message (Shift+Enter for new line on desktop)
- Arrow keys to scroll messages
- Escape to cancel voice recording

### Visual
- High contrast mode support
- Text scaling (up to 200%)
- Color-blind friendly
- Focus indicators visible

---

## Performance

### Message Loading
- Initial: 20 messages
- Pull-to-refresh: +20 older messages
- Virtualized list for 100+ messages
- Message disposal off-screen

### Image Optimization
- Recipe thumbnails: 80×80px, compressed WebP
- Lazy load images in scroll viewport
- Cache aggressively

### Network
- Debounce typing indicator (user typing → 1s delay)
- Retry failed messages with exponential backoff
- Offline queue (send when reconnected)
- WebSocket for real-time (optional)

---

## Design Tokens

### Colors
```
AI Bubble: #F5F5F5
User Bubble: #FF6F00
Timestamp: #9E9E9E
Quick Reply: White with #E0E0E0 border
```

### Typography
```
Message text: 16px, Regular
Timestamp: 12px, Regular
Quick reply: 14px, Medium
```

### Spacing
```
Bubble padding: 12px H × 10px V
Message gap: 12px
Bubble-timestamp gap: 4px
```

---

## Summary

**Chat AI Screen:**
- ✅ Conversational UI (bubble style)
- ✅ RAG-powered responses (recipe search from vector DB)
- ✅ Embedded recipe cards (tappable, navigate to detail)
- ✅ Voice input (Vietnamese STT)
- ✅ Voice output (Vietnamese TTS with controls)
- ✅ Wake Word Detection ("Hey Chef" / "Này Chef")
  - Always listening mode
  - Manual toggle mode
  - Privacy controls
  - Battery management
- ✅ Image upload (ingredient recognition via GPT-4V)
- ✅ Context-aware (multi-turn memory)
- ✅ Smart suggestions (time, trending, weather)
- ✅ Error handling (no results, network, ambiguous)
- ✅ Responsive design
- ✅ Full accessibility support
