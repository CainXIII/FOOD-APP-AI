# 🍳 AI Cooking Assistant - Backend

FastAPI backend cho ứng dụng trợ lý nấu ăn AI với RAG, voice chat và đề xuất cá nhân hóa.

## 🚀 Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLite** - Database file-based nhẹ nhàng
- **Redis 7.2** - Caching và session management (tùy chọn)
- **OpenAI** - GPT-4o, Whisper, TTS, Embeddings
- **LangChain** - RAG pipeline orchestration
- **SQLAlchemy** - ORM database
- **Alembic** - Database migrations

## 📦 Quick Start

### Prerequisites

- Python 3.11+
- Redis 7+ (tùy chọn cho caching)
- Poetry hoặc pip (Python package manager)

### 1. Cài đặt Dependencies

```bash
cd backend

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình Database

**SQLite Setup (Mặc định)**

SQLite sẽ được tạo tự động khi chạy ứng dụng lần đầu. File database `cooking_assistant.db` sẽ được tạo trong thư mục backend.

**Tùy chọn: Redis cho Caching**

```bash
# Sử dụng Docker
docker run -d -p 6379:6379 --name redis redis:7.2-alpine

# Hoặc cài đặt local Redis
# Windows: https://redis.io/download
# macOS: brew install redis
# Ubuntu: sudo apt install redis-server
```

# Script sẽ:
# - Kiểm tra cài đặt PostgreSQL
# - Tạo database và user
# - Bật pgvector extension
# - Tạo file .env
# - Test kết nối
```

### 3. Cấu hình Environment Variables

```bash
# Copy file template
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn:
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./cooking_assistant.db
REDIS_URL=redis://localhost:6379  # Tùy chọn
SECRET_KEY=your-secret-key-here
```

### 4. Khởi tạo Database

```bash
# Chạy migrations
alembic upgrade head

# Seed dữ liệu mẫu (tùy chọn)
python scripts/seed_data.py

# Tạo embeddings cho công thức (tùy chọn)
python scripts/generate_embeddings.py
```

### 5. Chạy Backend

```bash
# Development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Khi server đang chạy, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🏗️ Kiến trúc Backend

```
app/
├── api/              # API routes
│   └── v1/          # API version 1
├── core/            # Core functionality
├── models/          # Database models
├── schemas/         # Pydantic schemas
├── services/        # Business logic
├── dependencies/    # FastAPI dependencies
├── database.py      # Database connection
├── config.py        # Configuration
└── main.py          # Application entry point

scripts/             # Utility scripts
docs/               # Documentation
alembic/            # Database migrations
```

## 🔑 API Endpoints chính

### Authentication
- `POST /api/v1/auth/register` - Đăng ký
- `POST /api/v1/auth/login` - Đăng nhập
- `POST /api/v1/auth/refresh` - Refresh token

### Recipes
- `GET /api/v1/recipes` - Lấy danh sách công thức
- `GET /api/v1/recipes/{id}` - Chi tiết công thức
- `POST /api/v1/recipes` - Tạo công thức mới
- `PUT /api/v1/recipes/{id}` - Cập nhật công thức

### Chat & AI
- `POST /api/v1/chat` - Chat với AI
- `POST /api/v1/chat/voice` - Chat bằng giọng nói
- `GET /api/v1/chat/history` - Lịch sử chat

### User
- `GET /api/v1/users/me` - Thông tin user hiện tại
- `PUT /api/v1/users/me` - Cập nhật profile
- `GET /api/v1/users/favorites` - Công thức yêu thích

## 🧪 Testing

```bash
# Chạy tất cả tests
pytest

# Chạy với coverage
pytest --cov=app --cov-report=html

# Chạy specific test
pytest tests/test_auth.py

# Chạy tests với verbose output
pytest -v
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t cooking-assistant-backend .

# Chạy container
docker run -p 8000:8000 cooking-assistant-backend
```

### Production với Gunicorn

```bash
# Cài đặt gunicorn
pip install gunicorn

# Chạy với gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Development Scripts

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/

# Run pre-commit hooks
pre-commit run --all-files

# Generate API docs
python scripts/generate_api_docs.py
```

## 📊 Monitoring

- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics` (Prometheus format)
- **Logs**: Structured logging với JSON format

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

### Installation Steps

1. Install dependencies:
```powershell
poetry install
```

2. Activate virtual environment:
```powershell
poetry shell
```

3. Setup database (choose Docker or Local option above)

4. Update `.env` file with your configuration:
   - OpenAI API key
   - JWT secret key
   - Other environment-specific settings

5. Run database migrations:
```powershell
poetry run alembic upgrade head
```

6. Seed sample data (to be implemented):
```powershell
poetry run python scripts/seed_data.py
```

7. Start development server:
```powershell
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── database.py                # Database connection setup
│   │
│   ├── models/                    # SQLAlchemy ORM models (✅ COMPLETED)
│   │   ├── __init__.py           # Export all models
│   │   ├── user.py               # User, OAuthAccount, RefreshToken
│   │   ├── category.py           # Category, Ingredient
│   │   ├── recipe.py             # Recipe, RecipeIngredient, RecipeStep, NutritionFacts
│   │   ├── social.py             # Favorite, Rating, Comment, RecipeList, RecipeListItem
│   │   ├── cooking.py            # CookingSession, CookingTimer
│   │   ├── chat.py               # Chat, ChatMessage
│   │   ├── analytics.py          # SearchQuery, TrendingKeyword, UserActivity
│   │   └── embedding.py          # RecipeEmbedding, IngredientEmbedding
│   │
│   ├── api/                       # API endpoints (to be created)
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── auth.py        # Authentication endpoints
│   │           ├── users.py       # User management
│   │           ├── recipes.py     # Recipe CRUD
│   │           ├── chat.py        # AI chat endpoints
│   │           └── ...
│   │
│   ├── schemas/                   # Pydantic schemas (to be created)
│   │   ├── user.py
│   │   ├── recipe.py
│   │   ├── auth.py
│   │   └── ...
│   │
│   ├── services/                  # Business logic (to be created)
│   │   ├── auth.py
│   │   ├── recipe.py
│   │   ├── rag/                   # RAG pipeline
│   │   │   ├── embeddings.py
│   │   │   ├── retrieval.py
│   │   │   ├── generation.py
│   │   │   └── pipeline.py
│   │   └── cache.py
│   │
│   ├── middleware/                # Custom middleware (✅ COMPLETED)
│   │   ├── __init__.py
│   │   ├── security.py            # Security headers
│   │   └── logging.py             # Request logging
│   │
│   └── utils/                     # Utilities (to be created)
│       ├── validators.py
│       └── helpers.py
│
├── alembic/                       # Database migrations (✅ SETUP COMPLETE)
│   ├── versions/                  # Migration files (to be generated)
│   ├── env.py                     # Alembic environment config
│   └── script.py.mako
│
├── scripts/                       # Setup and utility scripts
│   ├── setup_database.ps1         # Automated PostgreSQL setup (✅ CREATED)
│   ├── init_db.sql                # Database initialization (✅ CREATED)
│   ├── seed_data.py               # Database seeding (to be created)
│   └── generate_embeddings.py     # Generate recipe embeddings (to be created)
│
├── data/                          # Sample data (✅ CREATED in Phase 3)
│   ├── categories.json
│   ├── ingredients.json
│   ├── recipes.json
│   └── users.json
│
├── tests/                         # Test files (to be created)
│   ├── api/
│   ├── services/
│   └── conftest.py
│
├── docker-compose.yml             # Docker services config (✅ CREATED)
├── .env                           # Environment variables (generated by setup script)
├── .gitignore
├── alembic.ini
├── poetry.lock
├── pyproject.toml                 # Dependencies (✅ COMPLETED)
└── README.md
```

## 🗃️ Database Models

The application uses **23 database tables** organized into 8 model files:

### Authentication (user.py)
- `User` - User accounts with role-based access
- `OAuthAccount` - OAuth provider linking
- `RefreshToken` - Multi-device token management

### Content (category.py)
- `Category` - Recipe categories
- `Ingredient` - Ingredients with nutritional info

### Recipes (recipe.py)
- `Recipe` - Main recipe data with bilingual content
- `RecipeIngredient` - Recipe-ingredient junction with quantities
- `RecipeStep` - Step-by-step instructions with media
- `NutritionFacts` - Detailed nutritional information

### Social (social.py)
- `Favorite` - User favorites
- `Rating` - Recipe ratings
- `Comment` - Recipe comments with threading
- `RecipeList` - User recipe collections
- `RecipeListItem` - Items in collections

### Cooking (cooking.py)
- `CookingSession` - Active cooking session tracking
- `CookingTimer` - Multiple timers per session

### Chat (chat.py)
- `Chat` - AI conversation threads
- `ChatMessage` - Messages with RAG metadata

### Analytics (analytics.py)
- `SearchQuery` - Search query logging
- `TrendingKeyword` - Trending search terms
- `UserActivity` - User behavior tracking

### Embeddings (embedding.py)
- `RecipeEmbedding` - Vector embeddings for recipes (1536 dimensions, stored as JSON)
- `IngredientEmbedding` - Vector embeddings for ingredients

All models use:
- UUID primary keys
- Async SQLAlchemy 2.0 syntax
- JSON storage for embeddings (SQLite compatible)
- Cosine similarity calculation in Python with NumPy
- Proper relationships with cascade delete

## 🗄️ Database Setup Options

### Option 1: Docker (Recommended)

The easiest way to get started:

```powershell
# Start PostgreSQL + Redis
docker-compose up -d

# Check status
docker-compose ps

# Access database
docker exec -it cooking_assistant_db psql -U cooking_admin -d cooking_assistant

# Optional: Access pgAdmin at http://localhost:5050
docker-compose --profile tools up -d
```

### Option 2: SQLite Setup (Recommended)

SQLite is the default database and requires no additional setup. The database file `cooking_assistant.db` will be created automatically when you run the application.

**Vector Search with SQLite:**
- Embeddings are stored as JSON arrays in SQLite
- Cosine similarity is calculated in Python using NumPy
- No additional extensions required
- Suitable for development and small-scale production

### Option 3: PostgreSQL Setup (For Production Vector Search)

If you need advanced vector search capabilities for large-scale production, you can migrate to PostgreSQL with pgvector:

```powershell
# Run the setup script
.\scripts\setup_database.ps1

# Or manual setup:
psql -U postgres -c "CREATE USER cooking_admin WITH PASSWORD 'cooking_pass_2024';"
psql -U postgres -c "CREATE DATABASE cooking_assistant OWNER cooking_admin;"

# Enable extensions
psql -U cooking_admin -d cooking_assistant -c "CREATE EXTENSION IF NOT EXISTS vector;"
psql -U cooking_admin -d cooking_assistant -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql -U cooking_admin -d cooking_assistant -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

# Update .env file:
DATABASE_URL=postgresql://cooking_admin:cooking_pass_2024@localhost:5432/cooking_assistant
```
```

## 🔄 Database Migrations

Using Alembic for database schema management:

```powershell
# Generate initial migration from models
poetry run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
poetry run alembic upgrade head

# Check current version
poetry run alembic current

# View migration history
poetry run alembic history

# Rollback one migration
poetry run alembic downgrade -1

# Rollback to specific version
poetry run alembic downgrade <revision_id>
```

## 🌐 API Access

Once running, the API is available at:

- **API Base**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Environment Variables

Key environment variables (auto-generated by setup script in `.env`):

```env
# Database
DATABASE_URL=postgresql+asyncpg://cooking_admin:cooking_pass_2024@localhost:5432/cooking_assistant
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cooking_assistant
DB_USER=cooking_admin
DB_PASSWORD=cooking_pass_2024

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here

# Application
ENVIRONMENT=development
DEBUG=true
API_V1_PREFIX=/api/v1
```

**⚠️ Important**: Update `JWT_SECRET_KEY` and `OPENAI_API_KEY` before running!

## 🧪 Testing

```powershell
# Run all tests (to be implemented)
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_auth.py
```

## 🛠️ Development Tools

### Alembic Commands Summary

```powershell
# Create new migration
alembic revision -m "Add new column"

# Auto-generate from model changes
alembic revision --autogenerate -m "Add new table"

# Apply all pending migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current state
alembic current

# Show history
alembic history --verbose
```

### Database Access

```powershell
# Via psql
psql -U cooking_admin -d cooking_assistant

# Via Docker
docker exec -it cooking_assistant_db psql -U cooking_admin -d cooking_assistant

# Via pgAdmin (if started with tools profile)
# http://localhost:5050
# Email: admin@cookingassistant.local
# Password: admin
```

## 📚 Next Steps

1. ✅ Backend project setup - **COMPLETED**
2. ✅ Database models - **COMPLETED**
3. ⏳ **Generate database migrations** - Next step
4. ⏳ Seed sample data
5. ⏳ Implement authentication
6. ⏳ Implement recipe APIs
7. ⏳ Implement RAG pipeline
8. ⏳ Implement caching layer

## 📄 License

Proprietary - All rights reserved

Key environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `OPENAI_API_KEY` - OpenAI API key
- `GOOGLE_CLIENT_ID/SECRET` - Google OAuth
- `FACEBOOK_APP_ID/SECRET` - Facebook OAuth
- `APPLE_CLIENT_ID/SECRET` - Apple Sign In

## 🧪 Testing

Run tests:
```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=app --cov-report=html
```

## 📝 API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 Deployment

See `docs/deployment.md` for production deployment instructions.

## 📄 License

MIT License
