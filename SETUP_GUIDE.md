# Food App AI - Setup Guide

## 📋 Mục lục
- [1. Setup Backend Environment](#1-setup-backend-environment)
- [2. Setup Docker](#2-setup-docker)  
- [3. Thư mục lưu ảnh](#3-thư-mục-lưu-ảnh)
- [4. Chạy scripts generate data](#4-chạy-scripts-generate-data)
- [5. Import data vào PostgreSQL](#5-import-data-vào-postgresql)

---

## 1. Setup Backend Environment

### 1.1 Tạo môi trường Virtual Environment

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Trên Windows
venv\Scripts\activate

# Trên macOS/Linux  
source venv/bin/activate

# Xác nhận đã kích hoạt (sẽ thấy (venv) ở đầu dòng terminal)
```

### 1.2 Cài đặt Dependencies

```bash
# Đảm bảo đã kích hoạt venv
# Nâng cấp pip lên phiên bản mới nhất
python -m pip install --upgrade pip

# Cài đặt requirements
pip install -r requirements.txt

# Xác nhận cài đặt thành công
pip list
```

### 1.3 Cấu hình Environment Variables

Tạo file `.env` trong thư mục `backend/`:

```env
# Database
DATABASE_URL=postgresql://admin:secure_pass_123@localhost:5432/food_app_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=secure_pass_123
POSTGRES_DB=food_app_db

# Qdrant Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=recipe_embeddings

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_V1_PREFIX=/api/v1
DEBUG=true

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB
```

---

## 2. Setup Docker

### 2.1 Cài đặt Docker Desktop

- **Windows**: Download từ [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **macOS**: Download từ [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux**: Làm theo hướng dẫn [Docker Engine for Linux](https://docs.docker.com/engine/install/)

### 2.2 Chạy Services với Docker Compose

```bash
# Từ thư mục root của project
cd /path/to/FOOD-APP-AI-app_v0_1

# Khởi động tất cả services
docker-compose -f docker-compose.postergresql.yml -f docker-compose.qdrant.yml up -d

# Xem logs
docker-compose logs -f

# Kiểm tra trạng thái services
docker-compose ps
```

### 2.3 Docker Services

File `docker-compose.postgresql.yml` và `docker-compose.qdrant.yml` sẽ khởi động:

- **PostgreSQL Database**: `localhost:5432`
- **Qdrant Vector Database**: `localhost:6333`
- **pgAdmin** (optional): `localhost:5050`

### 2.4 Kiểm tra Services

```bash
# Kiểm tra PostgreSQL
$env:PGPASSWORD="secure_pass_123"; psql -h localhost -p 5432 -U admin -d food_app_db -c "SELECT version();"

# Kiểm tra Qdrant
curl http://localhost:6333/collections

# Truy cập pgAdmin (nếu có)
# Mở browser: http://localhost:5050
# Email: admin@admin.com
# Password: admin
```

---

## 3. Thư mục lưu ảnh

### 3.1 Cấu trúc thư mục

Tạo các thư mục sau để lưu ảnh:

```
backend/
├── uploads/
│   ├── recipes/
│   │   ├── thumbnails/     # Ảnh thumbnail công thức
│   │   ├── steps/          # Ảnh các bước làm
│   │   └── full/           # Ảnh full size
│   ├── users/
│   │   ├── avatars/        # Avatar người dùng
│   │   └── covers/         # Ảnh bìa profile
│   ├── categories/         # Ảnh danh mục
│   └── temp/               # Ảnh tạm thời
data/
├── images/
│   ├── recipes/
│   │   ├── vietnamese/     # Ảnh công thức Việt Nam
│   │   ├── asian/          # Ảnh công thức châu Á
│   │   ├── western/        # Ảnh công thức phương Tây
│   │   └── desserts/       # Ảnh món tráng miệng
│   ├── ingredients/        # Ảnh nguyên liệu
│   └── categories/         # Ảnh danh mục
```

### 3.2 Tạo thư mục bằng script

```bash
# Chạy từ thư mục root
mkdir -p backend/uploads/{recipes/{thumbnails,steps,full},users/{avatars,covers},categories,temp}
mkdir -p data/images/{recipes/{vietnamese,asian,western,desserts},ingredients,categories}
```

### 3.3 Permissions (Linux/macOS)

```bash
# Cấp quyền ghi cho thư mục uploads
chmod -R 755 backend/uploads
chown -R $USER:$USER backend/uploads
```

---

## 4. Chạy scripts generate data

### 4.1 Chuẩn bị scripts

Kiểm tra các script trong thư mục `data/scripts/`:

```
data/scripts/
├── generate_all_data.py       # Tạo tất cả data
├── generate_recipes.py        # Tạo công thức
├── generate_nutrition.py      # Tạo thông tin dinh dưỡng
├── generate_social.py         # Tạo data tương tác xã hội
├── generate_chat.py           # Tạo data chat
├── generate_cooking.py        # Tạo data nấu ăn
├── generate_analytics.py      # Tạo data thống kê
├── generate_embeddings.py     # Tạo vector embeddings
├── import_simple.py           # Import đơn giản
├── import_to_postgresql.py    # Import vào PostgreSQL
└── import_to_qdrant.py        # Import vào Qdrant
```

### 4.2 Chạy scripts tạo data

```bash
# Kích hoạt virtual environment
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Tạo database schema
alembic upgrade head

# Về thư mục root để chạy scripts
cd ..

# Chạy script tạo tất cả data
python data/scripts/generate_all_data.py

# Hoặc chạy từng script riêng lẻ:
python data/scripts/generate_recipes.py
python data/scripts/generate_nutrition.py
python data/scripts/generate_social.py

# Tạo embeddings cho recipes
python data/scripts/generate_embeddings.py
```

### 4.3 Script generate từng loại data

```bash
# Generate data part 1 (users, categories, ingredients)
python data/scripts/generate_data_part1.py

# Generate recipes
python data/scripts/generate_recipes.py

# Generate nutrition facts
python data/scripts/generate_nutrition.py

# Generate social interactions (favorites, ratings, comments)
python data/scripts/generate_social.py

# Generate chat sessions
python data/scripts/generate_chat.py

# Generate cooking sessions và timers
python data/scripts/generate_cooking.py

# Generate analytics data
python data/scripts/generate_analytics.py
```

### 4.4 Kiểm tra data đã tạo

```bash
# Khởi động backend server
uvicorn app.main:app --reload

# Kiểm tra APIs
curl http://localhost:8000/api/v1/recipes/
curl http://localhost:8000/api/v1/users/
curl http://localhost:8000/collections  # Qdrant
```

---

## 5. Import data vào PostgreSQL

### 5.1 Import từ JSON files

Sử dụng data có sẵn trong thư mục `data/` và scripts trong `data/scripts/`:

```bash
# Import đơn giản (tất cả data cùng lúc)
python data/scripts/import_simple.py

# Import vào PostgreSQL
python data/scripts/import_to_postgresql.py

# Import vào Qdrant (vector embeddings)
python data/scripts/import_to_qdrant.py

# Hoặc import từng file JSON riêng lẻ:
# python data/scripts/import_categories.py data/categories_full.json
# python data/scripts/import_ingredients.py data/ingredients_full.json
# python data/scripts/import_recipes.py data/recipes_full.json
```

### 5.2 Import sử dụng SQL

```bash
# Connect to PostgreSQL
psql -h localhost -p 5432 -U postgres -d food_app

# Import SQL files (nếu có)
\i backend/sql/sample_data.sql
\i backend/sql/categories.sql  
\i backend/sql/recipes.sql
```

### 5.3 Backup và Restore

```bash
# Backup database
pg_dump -h localhost -p 5432 -U postgres -d food_app > backup.sql

# Restore database
psql -h localhost -p 5432 -U postgres -d food_app < backup.sql

# Backup specific tables
pg_dump -h localhost -p 5432 -U postgres -d food_app -t recipes -t users > recipes_users.sql
```

### 5.4 Verify data imported

```bash
# Kiểm tra tables và record counts
psql -h localhost -p 5432 -U postgres -d food_app -c "
SELECT 
  schemaname,
  tablename,
  n_tup_ins as \"Rows\"
FROM pg_stat_user_tables 
ORDER BY n_tup_ins DESC;
"

# Kiểm tra sample data
psql -h localhost -p 5432 -U postgres -d food_app -c "
SELECT COUNT(*) as recipe_count FROM recipes;
SELECT COUNT(*) as user_count FROM users;
SELECT COUNT(*) as category_count FROM categories;
"
```

---

## 🚀 Quick Start Commands

### Setup toàn bộ environment

```bash
# 1. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Setup Docker
docker-compose up -d

# 3. Tạo thư mục images
mkdir -p uploads/{recipes/{thumbnails,steps,full},users/{avatars,covers},categories,temp}

# 4. Setup database
alembic upgrade head

# 5. Generate sample data
python data/scripts/generate_all_data.py
python data/scripts/generate_embeddings.py

# 6. Start server
uvicorn app.main:app --reload
```

### Kiểm tra setup

```bash
# Backend health check
curl http://localhost:8000/health

# Database check
psql -h localhost -p 5432 -U postgres -d food_app -c "SELECT version();"

# Qdrant check  
curl http://localhost:6333/collections

# Sample API calls
curl http://localhost:8000/api/v1/recipes/ | jq
curl http://localhost:8000/api/v1/categories/ | jq
```

---

## 🛠️ Troubleshooting

### Lỗi thường gặp

**1. PostgreSQL connection error**
```bash
# Kiểm tra service đang chạy
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres
```

**2. Virtual environment không hoạt động**
```bash
# Xóa và tạo lại venv
rmdir /s venv  # Windows
rm -rf venv    # macOS/Linux

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**3. Qdrant connection error**
```bash
# Restart Qdrant
docker-compose restart qdrant

# Check logs
docker-compose logs qdrant
```

**4. Permission denied on uploads folder**
```bash
# Windows: Run as Administrator
# Linux/macOS:
sudo chown -R $USER:$USER backend/uploads
chmod -R 755 backend/uploads
```

---

## 📝 Notes

- Đảm bảo Docker Desktop đang chạy trước khi start services
- File `.env` cần có đúng cấu hình database
- Scripts generate data có thể chạy nhiều lần để tạo thêm data
- Backup database thường xuyên trước khi test
- Qdrant embeddings sẽ được tạo tự động khi import recipes