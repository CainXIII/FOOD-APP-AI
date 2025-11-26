# SQLite Database Setup Script for CookingAssistant
# SQLite is built into Python, no additional setup required

Write-Host "📱 SQLite Database Setup" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Database configuration
$DB_PATH = "$PSScriptRoot\..\cooking_assistant.db"
$SCRIPT_DIR = $PSScriptRoot

Write-Host "`n📋 SQLite Setup (No installation required)" -ForegroundColor Yellow
Write-Host "SQLite comes built-in with Python 3.x" -ForegroundColor Green

# Check Python installation
Write-Host "`n📋 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "`nPlease install Python 3.11+ from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    exit 1
}

# Check if database file exists
Write-Host "`n📋 Checking database file..." -ForegroundColor Yellow
if (Test-Path $DB_PATH) {
    Write-Host "✅ Database file exists: $DB_PATH" -ForegroundColor Green
    $fileInfo = Get-Item $DB_PATH
    Write-Host "   Size: $([math]::Round($fileInfo.Length / 1MB, 2)) MB" -ForegroundColor Gray
    Write-Host "   Modified: $($fileInfo.LastWriteTime)" -ForegroundColor Gray
} else {
    Write-Host "ℹ️  Database file does not exist yet" -ForegroundColor Yellow
    Write-Host "   It will be created automatically when the application runs" -ForegroundColor Cyan
}

# Create .env file if it doesn't exist
Write-Host "`n📋 Checking .env file..." -ForegroundColor Yellow
$envPath = "$PSScriptRoot\..\.env"
if (Test-Path $envPath) {
    Write-Host "✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    try {
        Copy-Item "$PSScriptRoot\..\.env.example" $envPath -ErrorAction Stop
        Write-Host "✅ .env file created successfully" -ForegroundColor Green
        Write-Host "⚠️  Please edit .env file with your actual values:" -ForegroundColor Yellow
        Write-Host "   - OPENAI_API_KEY" -ForegroundColor Cyan
        Write-Host "   - SECRET_KEY" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Failed to create .env file: $_" -ForegroundColor Red
    }
}

# Test database connection
Write-Host "`n📋 Testing database setup..." -ForegroundColor Yellow
try {
    # Run a simple Python script to test database
    $testScript = @"
import sys
sys.path.insert(0, '$SCRIPT_DIR/..')
from app.database import engine
import asyncio

async def test_db():
    try:
        async with engine.begin() as conn:
            result = await conn.execute('SELECT 1')
            print('✅ Database connection successful')
        return True
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

asyncio.run(test_db())
"@

    $testResult = python -c $testScript 2>&1
    if ($testResult -match "✅ Database connection successful") {
        Write-Host "✅ Database setup completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Database setup failed" -ForegroundColor Red
        Write-Host "Error: $testResult" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Database test failed: $_" -ForegroundColor Red
}

Write-Host "`n🎉 SQLite setup completed!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your OpenAI API key" -ForegroundColor White
Write-Host "2. Run: alembic upgrade head  # Create database tables" -ForegroundColor White
Write-Host "3. Run: python scripts/seed_data.py  # Add sample data (optional)" -ForegroundColor White
Write-Host "4. Run: uvicorn app.main:app --reload  # Start the server" -ForegroundColor White

Write-Host "`n📚 Useful commands:" -ForegroundColor Yellow
Write-Host "• View API docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "• View database: Use any SQLite browser or DB Browser for SQLite" -ForegroundColor Gray
Write-Host "• Reset database: Delete cooking_assistant.db and run alembic upgrade head" -ForegroundColor Gray

# Create user
Write-Host "Creating user $DB_USER..." -ForegroundColor Gray
$createUserCmd = "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
echo $createUserCmd | psql -U postgres -h $DB_HOST -p $DB_PORT 2>&1 | Out-Null

# Create database
Write-Host "Creating database $DB_NAME..." -ForegroundColor Gray
$createDbCmd = "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
echo $createDbCmd | psql -U postgres -h $DB_HOST -p $DB_PORT 2>&1 | Out-Null

# Grant privileges
Write-Host "Granting privileges..." -ForegroundColor Gray
$grantCmd = "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
echo $grantCmd | psql -U postgres -h $DB_HOST -p $DB_PORT 2>&1 | Out-Null

Write-Host "✅ Database and user setup completed (may already exist)" -ForegroundColor Green

# Enable pgvector extension
Write-Host "`n📋 Installing pgvector extension..." -ForegroundColor Yellow
$extensions = @(
    "CREATE EXTENSION IF NOT EXISTS vector;",
    "CREATE EXTENSION IF NOT EXISTS `"uuid-ossp`";",
    "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
)

foreach ($ext in $extensions) {
    echo $ext | psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME 2>&1 | Out-Null
}

# Verify extensions
$verifyCmd = "SELECT extname, extversion FROM pg_extension WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm');"
Write-Host "Installed extensions:" -ForegroundColor Gray
echo $verifyCmd | psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Extensions installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install pgvector extension" -ForegroundColor Red
    Write-Host "`nTo install pgvector:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://github.com/pgvector/pgvector/releases" -ForegroundColor Cyan
    Write-Host "2. Or use Docker: docker-compose up -d (recommended)" -ForegroundColor Cyan
    Write-Host "3. The docker-compose.yml uses ankane/pgvector image with pgvector pre-installed" -ForegroundColor Cyan
}

# Create .env file for database connection
Write-Host "`n📋 Creating .env file..." -ForegroundColor Yellow
$envPath = Join-Path $PSScriptRoot ".." ".env"
$envContent = @"
# Database Configuration
DATABASE_URL=postgresql+asyncpg://$DB_USER`:$DB_PASSWORD@$DB_HOST`:$DB_PORT/$DB_NAME
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

# Redis Configuration (for future use)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-this-in-production-$(Get-Random)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Application Settings
ENVIRONMENT=development
DEBUG=true
API_V1_PREFIX=/api/v1
"@

$envContent | Out-File -FilePath $envPath -Encoding utf8 -NoNewline
Write-Host "✅ .env file created at: $envPath" -ForegroundColor Green

# Test connection
Write-Host "`n📋 Testing database connection..." -ForegroundColor Yellow
$testCmd = "SELECT version();"
$result = echo $testCmd | psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database connection successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Database connection failed: $result" -ForegroundColor Red
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "🎉 Database Setup Complete!" -ForegroundColor Green
Write-Host "`nDatabase Details:" -ForegroundColor Cyan
Write-Host "  Name: $DB_NAME" -ForegroundColor White
Write-Host "  User: $DB_USER" -ForegroundColor White
Write-Host "  Host: $DB_HOST" -ForegroundColor White
Write-Host "  Port: $DB_PORT" -ForegroundColor White
Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Update .env file with your actual OpenAI API key" -ForegroundColor White
Write-Host "  2. Run migrations: poetry run alembic upgrade head" -ForegroundColor White
Write-Host "  3. Seed database: poetry run python scripts/seed_data.py" -ForegroundColor White
Write-Host "`nAlternative - Use Docker:" -ForegroundColor Yellow
Write-Host "  docker-compose up -d" -ForegroundColor Cyan
Write-Host "  (Includes PostgreSQL with pgvector + Redis)" -ForegroundColor Gray
