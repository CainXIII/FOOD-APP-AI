# PostgreSQL Database Setup Script
# Simple version without complex SQL

param(
    [string]$DbName = "cooking_assistant",
    [string]$DbUser = "cooking_admin",
    [string]$DbPassword = "cooking_pass_2024",
    [string]$DbHost = "localhost",
    [string]$DbPort = "5432"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Database Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check PostgreSQL
Write-Host "[1/5] Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $version = psql --version 2>&1
    Write-Host "OK - PostgreSQL found: $version" -ForegroundColor Green
} catch {
    Write-Host "ERROR - PostgreSQL not found in PATH" -ForegroundColor Red
    Write-Host "Install from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    Write-Host "Or use Docker: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

# Create user
Write-Host "`n[2/5] Creating database user..." -ForegroundColor Yellow
$createUser = "CREATE USER $DbUser WITH PASSWORD '$DbPassword';"
$userOutput = echo $createUser | psql -U postgres -h $DbHost -p $DbPort 2>&1 | Out-String
if ($userOutput -match "already exists") {
    Write-Host "OK - User already exists" -ForegroundColor Green
} elseif ($LASTEXITCODE -eq 0) {
    Write-Host "OK - User created" -ForegroundColor Green
} else {
    Write-Host "WARNING - $userOutput" -ForegroundColor Yellow
}

# Create database
Write-Host "`n[3/5] Creating database..." -ForegroundColor Yellow
$createDb = "CREATE DATABASE $DbName OWNER $DbUser;"
$dbOutput = echo $createDb | psql -U postgres -h $DbHost -p $DbPort 2>&1 | Out-String
if ($dbOutput -match "already exists") {
    Write-Host "OK - Database already exists" -ForegroundColor Green
} elseif ($LASTEXITCODE -eq 0) {
    Write-Host "OK - Database created" -ForegroundColor Green
} else {
    Write-Host "WARNING - $dbOutput" -ForegroundColor Yellow
}

# Install extensions
Write-Host "`n[4/5] Installing extensions..." -ForegroundColor Yellow
$extensions = @"
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
"@

$extOutput = echo $extensions | psql -U $DbUser -h $DbHost -p $DbPort -d $DbName 2>&1 | Out-String

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK - Extensions installed" -ForegroundColor Green
    
    # Show installed extensions
    $showExt = "SELECT extname, extversion FROM pg_extension WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm');"
    echo $showExt | psql -U $DbUser -h $DbHost -p $DbPort -d $DbName
} else {
    Write-Host "ERROR - Failed to install extensions" -ForegroundColor Red
    Write-Host $extOutput -ForegroundColor Red
    Write-Host "`nTry using Docker instead: docker-compose up -d" -ForegroundColor Yellow
}

# Create .env file
Write-Host "`n[5/5] Creating .env file..." -ForegroundColor Yellow
$envPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
$randomKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})

$envContent = @"
# Database Configuration
DATABASE_URL=postgresql+asyncpg://$DbUser`:$DbPassword@$DbHost`:$DbPort/$DbName
DB_HOST=$DbHost
DB_PORT=$DbPort
DB_NAME=$DbName
DB_USER=$DbUser
DB_PASSWORD=$DbPassword

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT Configuration  
JWT_SECRET_KEY=$randomKey
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

$envContent | Out-File -FilePath $envPath -Encoding UTF8 -NoNewline
Write-Host "OK - .env file created at: $envPath" -ForegroundColor Green

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nDatabase Details:" -ForegroundColor White
Write-Host "  Name:     $DbName"
Write-Host "  User:     $DbUser"
Write-Host "  Host:     $DbHost"
Write-Host "  Port:     $DbPort"
Write-Host "`nConnection String:" -ForegroundColor White
Write-Host "  postgresql+asyncpg://$DbUser`:$DbPassword@$DbHost`:$DbPort/$DbName" -ForegroundColor Cyan
Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env and add your OpenAI API key"
Write-Host "  2. Run: poetry run alembic upgrade head"
Write-Host "  3. Run: poetry run python scripts/seed_data.py"
Write-Host "`n"
