# PostgreSQL Setup Guide

This document provides multiple options to set up PostgreSQL with pgvector extension for the Cooking Assistant backend.

## ⚡ Quick Start (Recommended)

### Option 1: Docker Compose (Easiest)

**Prerequisites:**
- Docker Desktop installed and running

**Steps:**

1. Start Docker Desktop (make sure it's running)

2. Navigate to backend directory and run:
```powershell
cd d:\Projects\Hackathon\backend
docker-compose up -d
```

3. Verify services are running:
```powershell
docker-compose ps
```

4. The .env file will be auto-created. Update it with your OpenAI API key:
```powershell
notepad .env
# Add your OPENAI_API_KEY=sk-...
```

5. Run database migrations:
```powershell
poetry run alembic upgrade head
```

**Services included:**
- PostgreSQL 15+ with pgvector extension (port 5432)
- Redis 7 for caching (port 6379)
- pgAdmin UI (optional, port 5050)

**To stop services:**
```powershell
docker-compose down
```

**To view logs:**
```powershell
docker-compose logs -f
```

---

### Option 2: Local PostgreSQL Installation

**Prerequisites:**
- PostgreSQL 15+ installed
- pgvector extension installed

**Install PostgreSQL:**

```powershell
# Using Chocolatey (recommended)
choco install postgresql15 -y

# Or download from:
# https://www.postgresql.org/download/windows/
```

**Install pgvector:**

Unfortunately, pgvector doesn't have a simple Windows installer. Options:
1. Compile from source (complex)
2. Use pre-built binaries (if available)
3. **Use Docker instead (much easier)**

**Run setup script:**
```powershell
.\scripts\setup_db_simple.ps1
```

---

### Option 3: Cloud Database (Production)

For production or if local setup is too complex:

**Supabase (Recommended - Free tier with pgvector):**
1. Go to https://supabase.com
2. Create a new project
3. Enable pgvector extension in SQL Editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
4. Copy connection string from Settings > Database
5. Update .env file with the connection string

**Other options:**
- Neon (PostgreSQL with pgvector support)
- AWS RDS PostgreSQL + pgvector
- Google Cloud SQL
- Azure Database for PostgreSQL

---

## 📋 Database Configuration

Once PostgreSQL is running, update your `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://cooking_admin:cooking_pass_2024@localhost:5432/cooking_assistant
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cooking_assistant
DB_USER=cooking_admin
DB_PASSWORD=cooking_pass_2024

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT Configuration
JWT_SECRET_KEY=<generated-random-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-key-here

# Application Settings
ENVIRONMENT=development
DEBUG=true
API_V1_PREFIX=/api/v1
```

---

## 🗄️ Database Schema

The application uses 23 tables:

### Authentication
- `users` - User accounts with roles
- `oauth_accounts` - OAuth provider linking
- `refresh_tokens` - JWT refresh tokens

### Content
- `categories` - Recipe categories
- `ingredients` - Ingredients with nutrition data

### Recipes
- `recipes` - Main recipe data
- `recipe_ingredients` - Recipe-ingredient junction
- `recipe_steps` - Step-by-step instructions
- `nutrition_facts` - Nutritional information

### Social Features
- `favorites` - User favorites
- `ratings` - Recipe ratings
- `comments` - Recipe comments
- `recipe_lists` - User collections
- `recipe_list_items` - Collection items

### Cooking
- `cooking_sessions` - Active cooking sessions
- `cooking_timers` - Session timers

### AI Chat
- `chats` - Conversation threads
- `chat_messages` - Messages with RAG metadata

### Analytics
- `search_queries` - Search logging
- `trending_keywords` - Trending searches
- `user_activities` - Behavior tracking

### Embeddings (RAG)
- `recipe_embeddings` - Recipe vector embeddings (1536D)
- `ingredient_embeddings` - Ingredient vectors

---

## 🔄 Running Migrations

After database is set up:

```powershell
# Navigate to backend
cd d:\Projects\Hackathon\backend

# Generate initial migration (already done, but for reference)
poetry run alembic revision --autogenerate -m "Initial migration"

# Apply migrations to create tables
poetry run alembic upgrade head

# Check current version
poetry run alembic current

# View migration history
poetry run alembic history
```

---

## 🌱 Seeding Data

After migrations, seed the database with sample data:

```powershell
# Run seeding script (to be created)
poetry run python scripts/seed_data.py
```

This will:
- Create sample categories
- Add ingredients with nutrition data
- Insert recipe data
- Generate embeddings for RAG
- Create test users

---

## 🔍 Verifying Setup

### Check Database Connection

```powershell
# Via Docker
docker exec -it cooking_assistant_db psql -U cooking_admin -d cooking_assistant

# Via local psql
psql -U cooking_admin -d cooking_assistant
```

### Check Extensions

```sql
SELECT extname, extversion 
FROM pg_extension 
WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm');
```

Should show:
```
  extname   | extversion
------------+------------
 vector     | 0.5.1
 uuid-ossp  | 1.1
 pg_trgm    | 1.6
```

### Check Tables

```sql
\dt
```

Should list all 23 tables after migrations.

### Test Vector Similarity

```sql
SELECT '[1,2,3]'::vector <-> '[3,2,1]'::vector AS distance;
```

---

## 🛠️ Troubleshooting

### Docker Desktop not running
```
Error: "cannot connect to docker daemon"
Solution: Start Docker Desktop application
```

### Port already in use
```
Error: "port 5432 is already allocated"
Solution: 
1. Stop existing PostgreSQL: Stop-Service postgresql*
2. Or change port in docker-compose.yml
```

### pgvector not available
```
Error: "extension vector does not exist"
Solution: Use Docker setup (pgvector pre-installed)
```

### Connection refused
```
Error: "connection refused"
Solution:
1. Check Docker: docker-compose ps
2. Check PostgreSQL service: Get-Service postgresql*
3. Verify credentials in .env
```

---

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)

---

## 🎯 Current Status

✅ **Completed:**
- Project structure created
- Database models implemented (23 tables)
- Docker Compose configuration
- Alembic setup
- Setup scripts created

⏳ **Next Steps:**
1. **Start Docker Desktop** ← YOU ARE HERE
2. Run `docker-compose up -d`
3. Run migrations: `poetry run alembic upgrade head`
4. Create seeding script
5. Seed database with sample data
