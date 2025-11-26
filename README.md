# 🍳 AI Cooking Assistant

Trợ lý nấu ăn AI thông minh với khả năng trò chuyện bằng giọng nói, đề xuất công thức cá nhân hóa và tìm kiếm công thức bằng trí tuệ nhân tạo.

## ✨ Tính năng chính

- 🤖 **Chat AI** - Trò chuyện bằng giọng nói với trợ lý nấu ăn
- 🔍 **Tìm kiếm thông minh** - Tìm công thức bằng ngôn ngữ tự nhiên với RAG
- 📱 **Ứng dụng di động** - Giao diện Flutter đẹp mắt và thân thiện
- 🎯 **Đề xuất cá nhân** - Công thức được cá nhân hóa dựa trên sở thích
- 🌍 **Đa ngôn ngữ** - Hỗ trợ tiếng Việt và tiếng Anh
- 🔒 **Xác thực** - Hệ thống đăng nhập/đăng ký an toàn

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flutter App   │    │   FastAPI       │    │   SQLite        │
│   (Frontend)    │◄──►│   Backend       │◄──►│   Database      │
│                 │    │                 │    │                 │
│ - Voice Chat    │    │ - RAG System    │    │ - Recipes       │
│ - Recipe Search │    │ - OpenAI API    │    │ - Embeddings    │
│ - User Profile  │    │ - Authentication │    │ - Users         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Caching)     │
                       └─────────────────┘
```

## 🚀 Công nghệ sử dụng

### Backend
- **FastAPI** - Web framework Python hiện đại
- **SQLite** - Database file-based nhẹ nhàng
- **Redis** - Caching và session management
- **OpenAI** - AI chat và embeddings
- **SQLAlchemy** - ORM database
- **LangChain** - RAG pipeline

### Frontend
- **Flutter** - Framework cross-platform
- **Riverpod** - State management
- **Cached Network Image** - Image caching
- **HTTP** - API communication

## 📋 Yêu cầu hệ thống

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **RAM**: 4GB
- **Storage**: 2GB free space

### Development Requirements
- **Python**: 3.11+
- **Flutter**: 3.16+
- **Redis**: 7+ (tùy chọn cho caching)
- **Git**

## 🛠️ Hướng dẫn cài đặt

### 1. Cài đặt Backend

#### Yêu cầu tiên quyết
- Python 3.11+
- Redis 7+ (tùy chọn cho caching)

#### Cài đặt dependencies

```bash
cd backend

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Cài đặt dependencies
pip install -r requirements.txt
```

#### Cấu hình Database

**SQLite sẽ được tạo tự động** khi chạy ứng dụng lần đầu. Không cần setup database riêng.

**Tùy chọn: Cài đặt Redis cho caching**

```bash
# Sử dụng Docker (khuyến nghị)
docker run -d -p 6379:6379 --name redis redis:7.2-alpine

# Hoặc cài đặt local Redis
# Windows: https://redis.io/download
# macOS: brew install redis
# Ubuntu: sudo apt install redis-server
```

#### Cấu hình Environment Variables

```bash
# Copy file template
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn
# OPENAI_API_KEY=your_openai_api_key
# DATABASE_URL=sqlite:///./cooking_assistant.db
# REDIS_URL=redis://localhost:6379
```

#### Khởi tạo Database

```bash
# Tạo tables và chạy migrations
alembic upgrade head

# Seed dữ liệu mẫu (tùy chọn)
python scripts/seed_data.py
```

Database SQLite sẽ được tạo tự động tại `cooking_assistant.db`.

### 3. Cài đặt Frontend

#### Yêu cầu tiên quyết
- Flutter 3.16+
- Android Studio / Xcode (cho mobile development)

#### Cài đặt dependencies

```bash
cd frontend

# Cài đặt Flutter dependencies
flutter pub get

# Kiểm tra thiết bị
flutter devices

# Chạy trên emulator/simulator
flutter run
```

#### Cấu hình API Endpoint

Mở file `lib/core/config/api_config.dart` và cập nhật:

```dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000'; // Thay đổi nếu cần
}
```

## 🚀 Chạy dự án

### Chạy Backend

```bash
cd backend

# Activate virtual environment
.venv\Scripts\activate

# Chạy development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# API documentation: http://localhost:8000/docs
```

### Chạy Frontend

```bash
cd frontend

# Chạy trên Android emulator
flutter run

# Chạy trên iOS simulator (macOS only)
flutter run --device-id <ios-simulator-id>

# Chạy trên web
flutter run -d chrome
```

## 📱 Screenshots

*Screenshots sẽ được thêm vào sau*

## 📚 API Documentation

Khi backend đang chạy, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Main Endpoints

- `POST /api/v1/auth/login` - Đăng nhập
- `POST /api/v1/auth/register` - Đăng ký
- `GET /api/v1/recipes` - Lấy danh sách công thức
- `POST /api/v1/chat` - Chat với AI
- `POST /api/v1/chat/voice` - Chat bằng giọng nói

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Chạy tất cả tests
pytest

# Chạy với coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Chạy unit tests
flutter test

# Chạy integration tests
flutter test integration_test/
```

## 🚀 Deployment

### Backend Deployment

```bash
# Build production image
docker build -t cooking-assistant-backend .

# Chạy với docker-compose production
docker-compose -f docker-compose.prod.yml up -d
```

### Frontend Deployment

```bash
# Build APK
flutter build apk --release

# Build iOS
flutter build ios --release

# Build web
flutter build web --release
```
---