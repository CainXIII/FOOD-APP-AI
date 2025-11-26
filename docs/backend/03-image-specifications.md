# 📐 Image Specifications - AI Cooking Assistant

Tài liệu quy định kích thước, format và tối ưu hóa hình ảnh cho toàn bộ ứng dụng.

---

## 📐 Khuyến Nghị Kích Thước Hình Ảnh

### 🍽️ Recipe Images (Hình món ăn)
**`image_url` trong recipes**
- **Thumbnail/Card view**: 400x400px (1:1 square)
- **Detail view**: 1200x800px (3:2 landscape)
- **Hero image**: 1920x1080px (16:9 widescreen)
- **Format**: WebP (fallback JPEG)
- **Quality**: 80-85%
- **File size**: < 150KB (thumbnail), < 300KB (detail)

### 🥕 Ingredient Images
**`image_url` trong ingredients**
- **Size**: 300x300px (1:1 square)
- **Format**: WebP với transparent background (fallback PNG)
- **Quality**: 85%
- **File size**: < 50KB

### 👤 User Avatars
**`avatar_url` trong users**
- **Thumbnail**: 128x128px
- **Profile view**: 256x256px
- **Format**: WebP (fallback JPEG)
- **Shape**: Circular crop
- **File size**: < 30KB

### 📂 Category Images
**`image_url` trong categories**
- **Card size**: 600x400px (3:2)
- **Format**: WebP (fallback JPEG)
- **Quality**: 85%
- **File size**: < 100KB

**`icon_url` trong categories**
- **Size**: 64x64px (1:1)
- **Format**: SVG (vector, scalable) hoặc PNG
- **File size**: < 10KB

### 🎬 Recipe Step Images
**`image_url` trong recipe_steps**
- **Size**: 800x600px (4:3)
- **Format**: WebP (fallback JPEG)
- **Quality**: 80%
- **File size**: < 120KB

### 🎥 Video Thumbnails & Videos
**`video_url` trong recipes/steps**
- **Thumbnail**: 640x360px (16:9)
- **Video resolution**: 1280x720px (720p) hoặc 1920x1080px (1080p)
- **Format**: MP4 (H.264 codec)
- **Bitrate**: 2-5 Mbps
- **File size**: Tùy độ dài (aim for < 50MB)

---

## 📱 Responsive Strategy

### Mobile (< 768px)
- Recipe card: 360x240px
- Recipe detail hero: 360x240px
- Step images: 360x240px

### Tablet (768px - 1024px)
- Recipe card: 600x400px
- Recipe detail hero: 768x512px
- Step images: 600x450px

### Desktop (> 1024px)
- Recipe card: 400x400px (grid)
- Recipe detail hero: 1200x800px
- Step images: 800x600px

---

## 🎯 CDN & Storage Structure

```
https://storage.cooking.app/
├── recipes/
│   ├── thumbnails/      # 400x400px
│   ├── detail/          # 1200x800px
│   └── hero/            # 1920x1080px
├── ingredients/
│   └── icons/           # 300x300px
├── categories/
│   ├── images/          # 600x400px
│   └── icons/           # 64x64px (SVG)
├── avatars/
│   ├── thumb/           # 128x128px
│   └── profile/         # 256x256px
├── steps/               # 800x600px
└── videos/
    ├── thumbnails/      # 640x360px
    └── full/            # 720p/1080p MP4
```

---

## 🚀 Best Practices

### 1. Responsive Images (srcset)
```html
<img 
  src="recipe-400.webp"
  srcset="recipe-400.webp 400w,
          recipe-800.webp 800w,
          recipe-1200.webp 1200w"
  sizes="(max-width: 768px) 360px,
         (max-width: 1024px) 600px,
         400px"
  alt="Phở Bò Hà Nội"
/>
```

### 2. Lazy Loading
```html
<img loading="lazy" src="..." />
```

### 3. Progressive JPEG/WebP
- Load blurred low-quality placeholder first
- Then load full quality

### 4. Image Optimization Pipeline
```
Original (high-res) → 
Resize (multiple sizes) → 
Compress (WebP + JPEG) → 
Upload to CDN → 
Generate URLs
```

### 5. Compression Tools
- **ImageMagick**: CLI batch processing
- **Sharp** (Node.js): Fast image processing
- **Cloudinary/Imgix**: Automatic optimization CDN

---

## 💾 Storage Estimates

### Per Recipe (complete with images)
- 1 hero image (1920x1080): ~250KB
- 1 detail image (1200x800): ~180KB
- 1 thumbnail (400x400): ~60KB
- 8 step images (800x600 each): ~800KB
- 1 video (3 min, 720p): ~30MB

**Total per recipe**: ~31.3MB

### Database
- 1000 recipes × 31.3MB = ~31.3GB
- + User avatars (10K users × 30KB) = ~300MB
- + Ingredients (500 × 50KB) = ~25MB
- + Categories (50 × 100KB) = ~5MB

**Total estimate**: ~32GB for 1000 recipes

---

## 🔧 Implementation Tips

### 1. Upload & Process (Python)
```python
from PIL import Image
from io import BytesIO
import boto3

def process_recipe_image(original_file, recipe_id):
    """
    Process and upload recipe image in multiple sizes
    """
    img = Image.open(original_file)
    
    sizes = {
        'thumbnail': (400, 400),
        'detail': (1200, 800),
        'hero': (1920, 1080)
    }
    
    urls = {}
    s3_client = boto3.client('s3')
    
    for size_name, (width, height) in sizes.items():
        # Resize maintaining aspect ratio
        img_resized = img.copy()
        img_resized.thumbnail((width, height), Image.LANCZOS)
        
        # Save as WebP
        buffer = BytesIO()
        img_resized.save(buffer, format='WEBP', quality=85)
        buffer.seek(0)
        
        # Upload to S3
        key = f"recipes/{size_name}/{recipe_id}.webp"
        s3_client.upload_fileobj(
            buffer,
            'cooking-app-storage',
            key,
            ExtraArgs={
                'ContentType': 'image/webp',
                'CacheControl': 'max-age=31536000'
            }
        )
        
        urls[size_name] = f"https://storage.cooking.app/{key}"
    
    return urls

# Usage
urls = process_recipe_image('pho-bo-original.jpg', 'recipe-uuid')
# Returns:
# {
#   'thumbnail': 'https://storage.cooking.app/recipes/thumbnails/recipe-uuid.webp',
#   'detail': 'https://storage.cooking.app/recipes/detail/recipe-uuid.webp',
#   'hero': 'https://storage.cooking.app/recipes/hero/recipe-uuid.webp'
# }
```

### 2. Dynamic Resizing (với CDN)

#### Cloudinary
```
https://res.cloudinary.com/cooking-app/image/upload/
  w_400,h_400,c_fill,q_auto,f_auto/recipes/pho-bo.jpg
```

**Parameters:**
- `w_400,h_400` - Width & height
- `c_fill` - Crop mode (fill, fit, scale, etc.)
- `q_auto` - Automatic quality optimization
- `f_auto` - Automatic format (WebP for supported browsers)

#### Imgix
```
https://cooking-app.imgix.net/recipes/pho-bo.jpg?
  w=400&h=400&fit=crop&auto=format,compress
```

**Parameters:**
- `w=400&h=400` - Dimensions
- `fit=crop` - Crop mode
- `auto=format,compress` - Auto format & compression

### 3. Image Processing Service (FastAPI)

```python
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io

app = FastAPI()

@app.post("/api/images/upload")
async def upload_image(
    file: UploadFile = File(...),
    entity_type: str = "recipe",
    entity_id: str = None
):
    """
    Upload and process image
    """
    # Read uploaded file
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    
    # Process based on entity type
    if entity_type == "recipe":
        urls = process_recipe_image(img, entity_id)
    elif entity_type == "ingredient":
        urls = process_ingredient_image(img, entity_id)
    elif entity_type == "avatar":
        urls = process_avatar_image(img, entity_id)
    
    return {
        "success": True,
        "urls": urls
    }
```

---

## 📊 Image URL Naming Convention

### Recipes
```
# Thumbnail
https://storage.cooking.app/recipes/thumbnails/{recipe_id}.webp

# Detail
https://storage.cooking.app/recipes/detail/{recipe_id}.webp

# Hero
https://storage.cooking.app/recipes/hero/{recipe_id}.webp

# Steps
https://storage.cooking.app/recipes/steps/{recipe_id}_step{step_number}.webp
```

### Ingredients
```
https://storage.cooking.app/ingredients/icons/{ingredient_id}.webp
```

### Categories
```
# Images
https://storage.cooking.app/categories/images/{category_slug}.webp

# Icons (SVG)
https://storage.cooking.app/categories/icons/{category_slug}.svg
```

### Avatars
```
# Thumbnail
https://storage.cooking.app/avatars/thumb/{user_id}.webp

# Profile
https://storage.cooking.app/avatars/profile/{user_id}.webp
```

### Videos
```
# Thumbnail
https://storage.cooking.app/videos/thumbnails/{video_id}.webp

# Full video
https://storage.cooking.app/videos/full/{video_id}.mp4
```

---

## 🔒 Security & Access Control

### Public Images
- Recipe images (thumbnails, detail, hero)
- Category images/icons
- Ingredient icons
- Video thumbnails

**Access**: Public read, signed upload

### Private Images
- User avatars (profile pictures)

**Access**: Authenticated read, signed upload

### Upload Security
```python
# Generate presigned upload URL (AWS S3)
def generate_upload_url(user_id, file_type):
    s3_client = boto3.client('s3')
    
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'cooking-app-storage',
            'Key': f'uploads/{user_id}/{uuid.uuid4()}.{file_type}',
            'ContentType': f'image/{file_type}'
        },
        ExpiresIn=3600  # 1 hour
    )
    
    return presigned_url
```

---

## ⚡ Performance Optimization

### 1. Image Caching Headers
```
Cache-Control: max-age=31536000, immutable
```

### 2. CDN Configuration
- Enable Gzip/Brotli compression
- Set proper CORS headers
- Enable HTTP/2
- Use edge caching

### 3. Lazy Loading Strategy
```javascript
// Intersection Observer for lazy loading
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      imageObserver.unobserve(img);
    }
  });
});

document.querySelectorAll('img.lazy').forEach(img => {
  imageObserver.observe(img);
});
```

### 4. Progressive Image Loading
```javascript
// Load placeholder → low quality → full quality
<img 
  src="placeholder.svg"
  data-lowsrc="recipe-low.webp"
  data-src="recipe-full.webp"
  class="progressive-image"
/>
```

---

## 📝 Image Metadata

### Store in Database
```json
{
  "image_url": "https://storage.cooking.app/recipes/detail/uuid.webp",
  "image_metadata": {
    "width": 1200,
    "height": 800,
    "format": "webp",
    "size_bytes": 245632,
    "blurhash": "LGF5?xYk^6#M@-5c,1J5@[or[Q6.",
    "dominant_color": "#FF6B35",
    "uploaded_at": "2025-11-25T10:30:00Z"
  }
}
```

### BlurHash for Placeholders
```python
import blurhash

# Generate blurhash
hash_string = blurhash.encode('path/to/image.jpg', x_components=4, y_components=3)
# Output: "LGF5?xYk^6#M@-5c,1J5@[or[Q6."

# Decode to placeholder
placeholder = blurhash.decode(hash_string, width=32, height=32)
```

---

## 🧪 Testing & Validation

### Image Quality Checks
- Resolution matches specifications
- File size within limits
- Format is WebP (or fallback)
- Aspect ratio preserved
- No artifacts or distortion

### Performance Checks
- Load time < 2 seconds on 3G
- Lighthouse image optimization score > 90
- CDN cache hit rate > 95%
- Bandwidth usage per user < 5MB/session

---

## 📚 Tools & Libraries

### Backend (Python)
- **Pillow (PIL)**: Image processing
- **boto3**: AWS S3 upload
- **blurhash**: Placeholder generation
- **ffmpeg-python**: Video processing

### Frontend (Flutter)
- **cached_network_image**: Image caching
- **flutter_blurhash**: BlurHash placeholder
- **photo_view**: Zoomable images
- **image_picker**: Upload from device

---

## 🎯 Summary

| Image Type | Size | Format | Max Size | Priority |
|------------|------|--------|----------|----------|
| Recipe Thumbnail | 400x400 | WebP | 150KB | High |
| Recipe Detail | 1200x800 | WebP | 300KB | High |
| Recipe Hero | 1920x1080 | WebP | 400KB | Medium |
| Recipe Step | 800x600 | WebP | 120KB | High |
| Ingredient Icon | 300x300 | WebP/PNG | 50KB | Medium |
| Category Image | 600x400 | WebP | 100KB | Medium |
| Category Icon | 64x64 | SVG | 10KB | Low |
| User Avatar | 128/256 | WebP | 30KB | Low |
| Video Thumbnail | 640x360 | WebP | 80KB | Medium |
| Video Full | 720p/1080p | MP4 | 50MB | Low |

---

**Next Steps:**
- Setup CDN (Cloudinary/AWS CloudFront)
- Implement image processing pipeline
- Create upload API endpoints
- Test with real images
