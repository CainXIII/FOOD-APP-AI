# 📷 Camera Screen - Design Specification

## Overview
Camera Screen cho phép users chụp hoặc tải ảnh nguyên liệu để nhận diện (ingredient recognition) sử dụng AI Vision, sau đó gợi ý recipes phù hợp.

---

## Visual Layout

```
┌─────────────────────────────────────┐
│ [×]  Nhận diện nguyên liệu    [💡] │ <- AppBar (overlay)
├─────────────────────────────────────┤
│                                     │
│                                     │
│                                     │
│       [Camera Preview]              │ <- Live camera feed
│        Full screen                  │    Or selected image
│                                     │
│                                     │
│      [Overlay Guidelines]           │ <- Frame guide (optional)
│                                     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│ Đã nhận diện:                       │ <- Results panel (bottom)
│ ✓ Cà chua (3 quả)                   │    Expandable
│ ✓ Hành tây (2 củ)                   │    Editable
│ ✓ Tỏi (5 tép)                       │
│                                     │
├─────────────────────────────────────┤
│  [🖼️]     [📸]     [🔍]            │ <- Action buttons
│ Gallery  Capture  Search           │    Fixed bottom
└─────────────────────────────────────┘
```

---

## Screen Modes

### Mode 1: Camera Mode (Default)

```
┌─────────────────────────────────────┐
│ [×]                            [💡] │
│                                     │
│                                     │
│                                     │
│      ┌──────────────────┐           │ <- Frame overlay
│      │                  │           │    Dotted corners
│      │  [Live preview]  │           │    Guide user framing
│      │                  │           │
│      └──────────────────┘           │
│                                     │
│   Đặt nguyên liệu vào khung         │ <- Hint text
│                                     │
├─────────────────────────────────────┤
│  [🖼️]     [📸]     [⚡]            │
│ Gallery  Capture  Flash           │
└─────────────────────────────────────┘
```

**Camera Preview:**
- Full screen preview
- Aspect ratio: 4:3 or 16:9 (device dependent)
- Auto-focus enabled
- Exposure control

**Frame Overlay:**
- Dotted rectangle
- Color: White with 50% opacity
- Size: 80% of screen width × 70% height
- Animated corners (pulsing subtly)
- Purpose: Guide composition

**Hint Text:**
- Position: Bottom of frame
- Font: 14px, medium
- Color: White with shadow
- Background: Semi-transparent black pill
- Text: "Đặt nguyên liệu vào khung"

---

### Mode 2: Image Preview (After Capture/Select)

```
┌─────────────────────────────────────┐
│ [←]  Preview                   [⟳] │ <- Back & Retake
│                                     │
│                                     │
│                                     │
│      [Captured Image]               │ <- Static image
│       Full screen                   │    Zoomable
│                                     │
│                                     │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ ┌─ Analyzing... ─────────────────┐  │
│ │ 🔍 Đang nhận diện nguyên liệu  │  │ <- Loading state
│ │ [Progress bar 45%]             │  │
│ └────────────────────────────────┘  │
├─────────────────────────────────────┤
│           [✓ Xác nhận]              │ <- Confirm button
└─────────────────────────────────────┘
```

**AppBar:**
- **Back button** (left): Discard and return to camera
- **Retake button** (right): Take another photo
- Title: "Preview"

**Image:**
- Full screen display
- Pinch to zoom (1x - 3x)
- Pan when zoomed
- High quality preview

**Loading Overlay:**
```
┌─────────────────────────────────┐
│ 🔍 Đang nhận diện nguyên liệu   │
│                                 │
│ ━━━━━━━━━░░░░░░░                │ <- Progress bar
│ 45%                             │
│                                 │
│ Processing with AI...           │
└─────────────────────────────────┘

Position: Bottom third of screen
Background: White, rounded 16px
Shadow: Elevation 8
Padding: 20px
Progress: Indeterminate or percentage
```

---

### Mode 3: Results Display

```
┌─────────────────────────────────────┐
│ [←]  Kết quả                   [⋮] │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  [Thumbnail of image]        │   │ <- Small preview
│  └──────────────────────────────┘   │    120px height
│                                     │
│ ✅ Đã nhận diện 5 nguyên liệu       │ <- Success header
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ✓ Cà chua (3 quả)         [×]  │ │ <- Ingredient list
│ │ ✓ Hành tây (2 củ)         [×]  │ │    Editable
│ │ ✓ Tỏi (5 tép)             [×]  │ │    Removable
│ │ ✓ Ớt (10 quả)             [×]  │ │
│ │ ✓ Gừng (1 củ)             [×]  │ │
│ │                                │ │
│ │ [+ Thêm nguyên liệu]           │ │ <- Add more
│ └─────────────────────────────────┘ │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ 🔍 Tìm công thức              │   │ <- Primary action
│ └───────────────────────────────┘   │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ 💬 Hỏi AI                     │   │ <- Secondary action
│ └───────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Image Thumbnail:**
- Height: 120px
- Width: 100% - 32px margin
- Border radius: 12px
- Tap: View fullscreen

**Success Header:**
- Icon: ✅ (20×20px, green)
- Text: "Đã nhận diện [N] nguyên liệu"
- Font: 16px, bold
- Color: Green (#4CAF50)

**Ingredient List:**
- Background: White card
- Border radius: 16px
- Padding: 16px
- Shadow: Elevation 2

**Ingredient Item:**
```
┌─────────────────────────────────┐
│ ✓  Cà chua (3 quả)        [×]  │
│ ^  ^                       ^    │
│ |  Text (16px)          Remove  │
│ Checkmark (green)               │
│                                 │
│ Height: 48px                    │
│ Tap: Edit quantity              │
└─────────────────────────────────┘

When tapped:
┌─────────────────────────────────┐
│ Cà chua                         │
│ ┌──────┐                        │
│ │ 3    │ quả   [✓] [×]         │ <- Edit mode
│ └──────┘                        │
│ Number input + unit + confirm   │
└─────────────────────────────────┘
```

**Add More Button:**
- Height: 48px
- Border: 1px dashed gray
- Text: "+ Thêm nguyên liệu"
- Color: Gray
- Tap: Manual input dialog

---

## Components Detail

### 1. AppBar (Overlay Mode)

```
┌─────────────────────────────────────┐
│ [×]  Nhận diện nguyên liệu    [💡] │
└─────────────────────────────────────┘
```

**Position:** Absolute, top of screen  
**Background:** Semi-transparent black (60%)  
**Height:** 56px  
**Padding:** 16px horizontal

**Close Button (×):**
- Size: 40×40px
- Icon: X (24×24px, white)
- Position: Left
- Tap: Exit to previous screen

**Title:**
- Text: "Nhận diện nguyên liệu"
- Font: 16px, medium
- Color: White

**Tips Button (💡):**
- Size: 40×40px
- Icon: Lightbulb (24×24px, white)
- Position: Right
- Tap: Show photography tips

**Tips Dialog:**
```
┌─────────────────────────────────┐
│ 💡 Mẹo chụp ảnh tốt             │
│                                 │
│ • Ánh sáng tốt, tránh ngược    │
│   sáng                          │
│ • Đặt nguyên liệu phẳng trên   │
│   bề mặt sạch                   │
│ • Tránh chồng chéo              │
│ • Chụp từ trên xuống           │
│ • Focus rõ nét                  │
│                                 │
│ [Đã hiểu]                       │
└─────────────────────────────────┘
```

---

### 2. Camera Controls

#### Bottom Action Bar

```
┌─────────────────────────────────────┐
│                                     │
│  [🖼️]     [📸]     [⚡]            │
│ Gallery  Capture  Flash           │
│                                     │
└─────────────────────────────────────┘
Height: 100px
Background: Semi-transparent black (80%)
Position: Fixed bottom
```

**Gallery Button:**
```
┌──────┐
│ 🖼️   │ <- 32×32px icon
│Gallery│    12px label
└──────┘
Size: 80×80px total
Background: Transparent
Tap: Open image picker
```

**Capture Button:**
```
┌──────┐
│  📸  │ <- Large circular button
│      │    White circle (70×70px)
│Capture│   Orange inner (60×60px)
└──────┘
Size: 80×80px
Animation: Scale down on press
Tap: Capture photo
```

**Flash Button:**
```
┌──────┐
│  ⚡  │ <- 32×32px icon
│Flash │    Auto/On/Off
└──────┘
Size: 80×80px
States:
- Auto: White (default)
- On: Yellow
- Off: Gray
Tap: Cycle through modes
```

---

#### Camera Flip Button (Front/Back)

```
Position: Top-right (below tips button)
┌──────┐
│  🔄  │ <- 40×40px circular
└──────┘
Background: Semi-transparent black
Icon: Camera flip (white)
Tap: Switch camera (front/back)
```

---

### 3. Frame Overlay Guide

```
┌─────────────────────────────────────┐
│                                     │
│    ╔═══════════════════╗            │ <- Dotted corners
│    ║                   ║            │    Animated
│    ║                   ║            │    White 50%
│    ║   [Frame area]    ║            │
│    ║                   ║            │
│    ║                   ║            │
│    ╚═══════════════════╝            │
│                                     │
│   Đặt nguyên liệu vào khung         │
└─────────────────────────────────────┘
```

**Frame Specs:**
- Border: 2px dashed white
- Opacity: 50%
- Corner radius: 16px
- Size: 80% width × 70% height
- Position: Centered

**Corner Animation:**
- Each corner: 20×20px L-shape
- Pulsing opacity: 30% ↔ 70%
- Duration: 2s infinite

**Hint Text:**
- Position: Below frame, centered
- Background: Black 60%, pill shape
- Padding: 8px 16px
- Text: 14px, white
- Shadow: 0 2px 4px rgba(0,0,0,0.5)

---

### 4. Results Panel (Expandable)

```
Collapsed state:
┌─────────────────────────────────────┐
│ Đã nhận diện: 3 nguyên liệu    [^] │ <- Tap to expand
└─────────────────────────────────────┘
Height: 48px

Expanded state:
┌─────────────────────────────────────┐
│ Đã nhận diện:                  [v] │ <- Tap to collapse
│                                     │
│ ✓ Cà chua (3 quả)             [×]  │
│ ✓ Hành tây (2 củ)             [×]  │
│ ✓ Tỏi (5 tép)                 [×]  │
│                                     │
│ [+ Thêm]                            │
└─────────────────────────────────────┘
Height: Auto (max 40% screen)
```

**Panel Specs:**
- Position: Bottom of screen (above actions)
- Background: White
- Border radius: 24px (top corners)
- Shadow: Elevation 16
- Padding: 16px

**Header:**
- Text: "Đã nhận diện: [N] nguyên liệu"
- Font: 14px, medium
- Expand/collapse icon: Chevron (up/down)

**Scroll:**
- If items > 5, enable vertical scroll
- Max height: 40% screen

---

### 5. Recognition Results

#### Ingredient Item (Editable)

```
Default state:
┌─────────────────────────────────┐
│ ✓  Cà chua (3 quả)        [×]  │
└─────────────────────────────────┘

Tap to edit:
┌─────────────────────────────────┐
│ Cà chua                         │
│ ┌──────┐ quả  [✓] [×]          │
│ │  3   │                        │ <- Number input
│ └──────┘                        │
└─────────────────────────────────┘

Edit mode:
- Number input: 60px width
- Unit dropdown: "quả", "củ", "kg", "g"
- Confirm: Green check
- Cancel: Gray X
```

**Checkmark:**
- Size: 20×20px
- Color: Green (#4CAF50)
- Icon: Filled circle with check

**Text:**
- Name: 16px, regular, black
- Quantity: 16px, medium, black
- Parentheses: Gray

**Remove Button [×]:**
- Size: 32×32px
- Icon: X (16×16px, gray)
- Tap: Remove from list with animation

---

#### Add Ingredient Button

```
┌─────────────────────────────────┐
│     + Thêm nguyên liệu          │
└─────────────────────────────────┘

Height: 48px
Border: 1px dashed #E0E0E0
Border radius: 12px
Text: 14px, gray
Icon: + (16×16px)
Tap: Open manual input dialog
```

**Manual Input Dialog:**
```
┌─────────────────────────────────┐
│ Thêm nguyên liệu                │
├─────────────────────────────────┤
│ Tên nguyên liệu:                │
│ ┌─────────────────────────────┐ │
│ │ [Text input]                │ │
│ └─────────────────────────────┘ │
│                                 │
│ Số lượng:                       │
│ ┌───────┐  ┌──────────────┐    │
│ │ [Num] │  │ [Unit: quả]  │    │
│ └───────┘  └──────────────┘    │
│                                 │
│ [Hủy]              [Thêm]      │
└─────────────────────────────────┘

Modal dialog, centered
Width: 90% screen (max 400px)
Height: Auto
```

---

### 6. Action Buttons (Results Screen)

#### Primary: Tìm Công Thức

```
┌───────────────────────────────┐
│ 🔍 Tìm công thức              │
└───────────────────────────────┘

Height: 56px
Width: 100% - 32px margin
Background: Orange (#FF6F00)
Text: White, 16px, bold
Icon: 🔍 (20×20px)
Border radius: 28px
Shadow: Elevation 4
```

**Action:**
- Tap: Navigate to Search Results
- Query: Recipes matching ingredients
- Loading: Button shows spinner

---

#### Secondary: Hỏi AI

```
┌───────────────────────────────┐
│ 💬 Hỏi AI                     │
└───────────────────────────────┘

Height: 56px
Width: 100% - 32px margin
Background: White
Border: 2px solid Orange
Text: Orange, 16px, medium
Icon: 💬 (20×20px)
Border radius: 28px
```

**Action:**
- Tap: Navigate to Chat AI
- Pre-fill message: "Tôi có [ingredient list], nấu món gì?"
- Automatic RAG query

---

## User Flows

### Flow 1: Capture & Recognize

```
User taps Camera from bottom nav
  ↓
Camera Screen opens (live preview)
  ↓
User positions ingredients in frame
  ↓
Taps Capture button (📸)
  ↓
Shutter animation + sound
  ↓
Navigate to Preview mode
  ↓
Image displayed with loading overlay
  ↓
Upload to backend (FastAPI)
  ↓
Backend calls OpenAI Vision API (GPT-4V)
  ↓
Progress: "Analyzing... 45%"
  ↓
API returns ingredient list with confidence
  ↓
Display Results screen
  ↓
User reviews, edits if needed
  ↓
Taps "🔍 Tìm công thức"
  ↓
Navigate to Search Results (filtered by ingredients)
```

---

### Flow 2: Pick from Gallery

```
User on Camera Screen
  ↓
Taps Gallery button (🖼️)
  ↓
System image picker opens
  ↓
User selects photo from library
  ↓
Image loads in Preview mode
  ↓
[Same recognition flow as Flow 1]
```

---

### Flow 3: Edit Recognition Results

```
Results displayed:
✓ Cà chua (3 quả)
✓ Hành tây (2 củ)
✓ Tỏi (5 tép)
  ↓
User taps "Hành tây" item
  ↓
Edit mode activates:
┌─────────────────────────────┐
│ Hành tây                    │
│ ┌────┐ củ  [✓] [×]         │
│ │ 2  │ ← Number editable    │
│ └────┘                      │
└─────────────────────────────┘
  ↓
User changes 2 → 3
  ↓
Taps [✓] confirm
  ↓
Item updates: "Hành tây (3 củ)"
  ↓
Exit edit mode
```

---

### Flow 4: Remove Ingredient

```
Results list displayed
  ↓
User taps [×] on "Tỏi (5 tép)"
  ↓
Confirmation (optional):
"Xóa Tỏi khỏi danh sách?"
[Hủy] [Xóa]
  ↓
Item animates out (slide left + fade)
  ↓
List updates: "Đã nhận diện: 2 nguyên liệu"
```

---

### Flow 5: Add Manual Ingredient

```
User on Results screen
  ↓
Taps "+ Thêm nguyên liệu"
  ↓
Dialog appears:
┌─────────────────────────┐
│ Thêm nguyên liệu        │
│ Tên: [________]         │
│ SL:  [___] [quả▼]      │
│ [Hủy]        [Thêm]    │
└─────────────────────────┘
  ↓
User types "Ớt"
  ↓
Enters quantity: 10
  ↓
Selects unit: "quả"
  ↓
Taps [Thêm]
  ↓
Dialog closes
  ↓
New item added: "✓ Ớt (10 quả)"
  ↓
List updates: "Đã nhận diện: 3 nguyên liệu"
```

---

### Flow 6: Ask AI about Ingredients

```
User on Results screen
  ↓
Reviews recognized ingredients:
- Cà chua (3 quả)
- Hành tây (2 củ)
- Tỏi (5 tép)
  ↓
Taps "💬 Hỏi AI" button
  ↓
Navigate to Chat AI screen
  ↓
Message pre-filled in input:
"Tôi có cà chua, hành tây, tỏi. 
 Nấu món gì ngon?"
  ↓
Auto-sends or user can edit first
  ↓
AI responds with recipe suggestions
```

---

### Flow 7: Retake Photo

```
User on Preview screen (after capture)
  ↓
Image not clear / missing items
  ↓
Taps Retake button (⟳) in AppBar
  ↓
Return to Camera mode (live preview)
  ↓
Previous photo discarded
  ↓
User can capture again
```

---

## Recognition Logic

### API Communication

**Endpoint:** `POST /api/v1/vision/recognize-ingredients`

**Request:**
- Image: Base64 encoded string
- Language: "vi" (Vietnamese)
- Max size: 5MB
- Format: JPEG/PNG

**Processing:**
- Backend receives image
- Calls OpenAI Vision API (GPT-4V)
- Prompt: "Identify food ingredients in Vietnamese with quantity and unit"
- Returns structured JSON

**Response Format:**
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "Cà chua",
      "quantity": 3,
      "unit": "quả",
      "confidence": 0.95
    },
    {
      "name": "Hành tây",
      "quantity": 2,
      "unit": "củ",
      "confidence": 0.92
    }
  ],
  "processing_time": 2.3
}
```

---

### Confidence Handling

**High Confidence (>0.9):**
- Add to list with checkmark (✓)
- No warning

**Medium Confidence (0.7-0.9):**
- Add to list with checkmark
- Yellow dot indicator (⚠️)
- User should verify

**Low Confidence (<0.7):**
- Add to list with question mark (?)
- Orange warning
- Suggest manual confirmation

**Display:**
```
✓ Cà chua (3 quả)           ← High confidence
⚠️ Hành tây (2 củ)          ← Medium
? Tỏi (5 tép)               ← Low (user verify)
```

---

## Error Handling

### No Ingredients Detected

```
┌─────────────────────────────────┐
│         😕                      │
│                                 │
│ Không nhận diện được nguyên liệu│
│                                 │
│ Thử lại với:                    │
│ • Ánh sáng tốt hơn             │
│ • Đặt nguyên liệu rõ ràng      │
│ • Chụp từ trên xuống           │
│                                 │
│ [Chụp lại]  [Thêm thủ công]    │
└─────────────────────────────────┘
```

---

### API Error

```
┌─────────────────────────────────┐
│         ⚠️                      │
│                                 │
│ Lỗi kết nối                     │
│                                 │
│ Không thể phân tích ảnh.        │
│ Vui lòng kiểm tra internet.    │
│                                 │
│ [Thử lại]  [Hủy]               │
└─────────────────────────────────┘
```

---

### Poor Image Quality

```
┌─────────────────────────────────┐
│         📷                      │
│                                 │
│ Ảnh không rõ                    │
│                                 │
│ Vui lòng chụp ảnh rõ nét hơn    │
│ để nhận diện tốt hơn            │
│                                 │
│ [Chụp lại]  [Tiếp tục]         │
└─────────────────────────────────┘
```

---

### Camera Permission Denied

```
┌─────────────────────────────────┐
│         🔒                      │
│                                 │
│ Cần quyền truy cập camera       │
│                                 │
│ Vui lòng cho phép trong         │
│ Settings để sử dụng tính năng   │
│ nhận diện nguyên liệu           │
│                                 │
│ [Mở Settings]  [Hủy]           │
└─────────────────────────────────┘
```

---

## Photography Tips

### Best Practices

**Lighting:**
- Natural light preferred
- Avoid harsh shadows
- No backlight (window behind)
- Even illumination

**Composition:**
- Flat surface (table, cutting board)
- White or neutral background
- Top-down angle (bird's eye)
- No overlapping items

**Focus:**
- Clear focus on all items
- No motion blur
- Proper exposure (not too dark/bright)
- Fill frame (ingredients prominent)

**Examples (Visual Guide in App):**
```
✓ GOOD                    ✗ BAD
┌──────────┐             ┌──────────┐
│ Well-lit │             │ Dark/    │
│ Top-down │             │ Blurry   │
│ Clear    │             │ Overlap  │
└──────────┘             └──────────┘
```

---

## Responsive Design

### Mobile (<600px)
- Camera: Full screen
- Action buttons: 3 columns (even width)
- Results panel: 40% max height
- Image preview: Full width

### Tablet (600-1200px)
- Camera: Centered, max 800px width
- Action buttons: Larger (100px each)
- Results panel: Side-by-side with preview
- More whitespace

### Desktop (>1200px)
```
┌─────────────────────────────────┐
│ [Image]      │  [Results]       │
│              │  ✓ Cà chua       │
│              │  ✓ Hành tây      │
│              │                  │
│              │  [Actions]       │
└─────────────────────────────────┘

Split view:
- Left: Camera/Preview (60%)
- Right: Results + Actions (40%)
```

---

## Accessibility

### Screen Reader
- Camera preview: "Camera preview, point at ingredients"
- Capture button: "Capture photo, button"
- Gallery button: "Choose from gallery, button"
- Flash button: "Flash [mode], tap to change"
- Ingredient item: "[Name], [quantity] [unit], tap to edit, button"
- Remove button: "Remove [name] from list, button"

### Visual
- High contrast mode support
- Large tap targets (min 48×48px)
- Clear labels on all buttons
- Focus indicators visible

### Alternative Input
- Voice command: "Chụp ảnh" → Capture
- Keyboard: Space → Capture (when focused)
- External camera button support

---

## Performance

### Camera
- Preview: 30fps minimum
- Focus: Auto-focus with tap-to-focus
- Exposure: Auto-exposure compensation
- Resolution: High quality (1920×1080+)

### Image Processing
- Compression: 80% quality JPEG
- Max file size: 5MB
- Resize if > 2000px (any dimension)
- Upload timeout: 30s

### Recognition
- API call: Async, non-blocking
- Progress updates: Real-time
- Timeout: 30s
- Retry: 3 attempts with exponential backoff

---

## Privacy & Storage

### Image Handling
- Captured images: Temporary storage only
- Auto-delete after processing
- Option: Save to gallery (user permission)
- No server-side storage (unless user saves recipe)

### Permissions
- Camera: Required for capture
- Gallery: Required for image picker
- Storage: Required for save-to-gallery (optional)

**Permission Request:**
```
┌─────────────────────────────────┐
│ Quyền truy cập Camera           │
│                                 │
│ Ứng dụng cần quyền camera để   │
│ chụp ảnh nguyên liệu và nhận    │
│ diện tự động                    │
│                                 │
│ [Từ chối]     [Cho phép]       │
└─────────────────────────────────┘
```

---

## Design Tokens

### Colors
```
Overlay: Black 60%
Frame guide: White 50%
Success: Green #4CAF50
Warning: Orange #FF9800
Error: Red #F44336
```

### Typography
```
Hint text: 14px, Medium
Ingredient name: 16px, Regular
Quantity: 16px, Medium
Header: 16px, Bold
```

### Spacing
```
Camera padding: 16px
Action button gap: 16px
Ingredient item height: 48px
Panel padding: 16px
```

---

## Edge Cases

### Multiple Similar Items
```
Detected:
✓ Cà chua (3 quả)
✓ Cà chua cherry (5 quả)

AI distinguishes varieties
User can merge if needed
```

### Packaged Ingredients
```
Detected:
✓ Gói mì gói
✓ Lon cà chua

Recognizes packaging
Suggests "opened" quantity
```

### Non-Food Items
```
Detected:
? Bát sứ
? Dao

Low confidence
Auto-filtered or marked
User can remove
```

---

## Summary

**Camera Screen:**
- ✅ Live camera preview with frame guide
- ✅ Capture or pick from gallery
- ✅ AI ingredient recognition (OpenAI Vision API)
- ✅ Editable results (quantity, unit, add/remove)
- ✅ Confidence indicators (high/medium/low)
- ✅ Search recipes by ingredients
- ✅ Ask AI about ingredients
- ✅ Photography tips dialog
- ✅ Error handling (no results, API error, poor quality)
- ✅ Privacy-focused (no permanent storage)
- ✅ Responsive design
- ✅ Full accessibility support

**Next Action Options:**
1. 🔍 **Tìm công thức** → Search Results (filtered by detected ingredients)
2. 💬 **Hỏi AI** → Chat AI (pre-filled with ingredient query)
