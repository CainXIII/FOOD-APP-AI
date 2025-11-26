# 🚀 Quick Setup Guide

Hướng dẫn setup nhanh để chạy dự án AI Cooking Assistant.

## ⚡ Quick Start (5 phút)

### 1. Clone và setup

```bash
# Clone repository
git clone <repository-url>
cd ai-cooking-assistant

# Setup backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
flutter pub get
```

### 2. Chạy services

```bash
# Terminal 1: Redis (tùy chọn cho caching)
docker run -d -p 6379:6379 --name redis redis:7.2-alpine

# Terminal 2: Backend
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 3: Frontend
cd frontend
flutter run
```

### 3. Truy cập ứng dụng

- **Backend API**: http://localhost:8000/docs
- **Frontend App**: Chạy trên emulator/simulator
- **Database Admin**: http://localhost:5050 (admin@cooking-assistant.com / admin123)

## 🔧 Troubleshooting

### Backend không chạy được
```bash
# Kiểm tra Python version
python --version  # Cần 3.11+

# Kiểm tra dependencies
pip list | grep fastapi

# Kiểm tra database connection
python -c "from app.database import engine; print('DB OK')"
```

### Frontend không build được
```bash
# Clean và rebuild
flutter clean
flutter pub get
flutter run

# Kiểm tra Flutter version
flutter --version
```

### Database connection failed
```bash
# Với SQLite, database sẽ được tạo tự động
# Kiểm tra file database có tồn tại
ls cooking_assistant.db

# Nếu có vấn đề, xóa file và chạy lại
rm cooking_assistant.db
alembic upgrade head
```

## 📞 Support

Nếu gặp vấn đề, hãy:
1. Kiểm tra logs trong terminal
2. Xem documentation trong `docs/`
3. Tạo issue trên GitHub

## 🎯 Next Steps

Sau khi setup xong:
1. Đọc `README.md` để hiểu chi tiết
2. Chạy tests: `pytest` (backend) hoặc `flutter test` (frontend)
3. Tìm hiểu API tại http://localhost:8000/docs
4. Bắt đầu development!