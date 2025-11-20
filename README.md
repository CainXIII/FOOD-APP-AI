# Food App Backend

Backend API và Web App cho ứng dụng nấu ăn thông minh với AI.

## Cấu trúc thư mục

```
food-app/
├── app/                    # Backend source code
│   ├── api/               # API endpoints
│   ├── core/              # Core config & database
│   ├── models/            # Database models
│   ├── orchestration/     # Chat orchestration & tools
│   └── services/          # AI services (OpenAI, Whisper, TTS, RAG, etc.)
├── alembic/               # Database migrations
├── web-app-test/          # Streamlit test interface
├── run.py                 # Backend server entry point
├── setup.py               # Package setup
├── requirements.txt       # Backend dependencies
├── alembic.ini           # Alembic configuration
├── docker-compose.yml    # Docker services (PostgreSQL, Qdrant)
└── .env.example          # Environment variables template
```

## Cài đặt

### 1. Tạo file .env

```bash
cp .env.example .env
```

Cập nhật các thông tin cần thiết trong `.env`:
- Database credentials
- OpenAI API keys
- Secret key

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Khởi động databases (Docker)

```bash
docker-compose up -d
```

### 4. Tạo database và chạy migrations

```bash
# Tạo database
docker exec -it food-app-postgres psql -U postgres -c "CREATE DATABASE food_app"

# Chạy migrations
alembic upgrade head
```

## Chạy ứng dụng

### Backend API

```bash
python run.py
```

API sẽ chạy tại: http://localhost:8000

### Web Test Interface

```bash
cd web-app-test
streamlit run app.py
```

Web app sẽ chạy tại: http://localhost:8501

## API Endpoints

- `GET /` - Health check
- `POST /api/chat/chat` - Chat with RAG
- `POST /api/chat/chat-simple` - Simple chat
- `POST /api/voice/transcribe` - Voice transcription
- `POST /api/voice/synthesize` - Text-to-speech
- `POST /api/menu/generate` - Generate menu
- `POST /api/recipes/generate` - Generate recipe
- `POST /api/sessions/` - Create cooking session
- `GET /api/sessions/{session_id}` - Get session details

## Tài liệu tham khảo

- FastAPI: https://fastapi.tiangolo.com
- Streamlit: https://streamlit.io
- Alembic: https://alembic.sqlalchemy.org
- Qdrant: https://qdrant.tech

## Troubleshooting

### Database connection error
Kiểm tra PostgreSQL đang chạy: `docker ps`

### Qdrant connection error
Kiểm tra Qdrant đang chạy: `docker ps`

### API key error
Kiểm tra file `.env` có đúng API keys chưa
