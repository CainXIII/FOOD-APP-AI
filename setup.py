"""
Food App Backend - Quick Setup Script
Automates the setup process for development environment
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description, shell=True):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print("\n" + "="*60)
    print("📋 Checking Prerequisites")
    print("="*60)
    
    prerequisites = {
        "Python": ["python", "--version"],
        "Docker": ["docker", "--version"],
        "Docker Compose": ["docker-compose", "--version"],
    }
    
    all_present = True
    for name, command in prerequisites.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            print(f"✅ {name}: {version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name}: NOT FOUND")
            all_present = False
    
    return all_present

def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("\n📦 Creating virtual environment...")
        run_command("python -m venv venv", "Create venv")
    else:
        print("\n✅ Virtual environment already exists")
    
    # Note: Activation is handled by user
    print("\n⚠️  Please activate the virtual environment:")
    print("   Windows PowerShell: .\\venv\\Scripts\\Activate.ps1")
    print("   Windows CMD: .\\venv\\Scripts\\activate.bat")
    print("   Linux/Mac: source venv/bin/activate")

def install_dependencies():
    """Install Python dependencies"""
    pip_path = Path("venv/Scripts/pip") if os.name == 'nt' else Path("venv/bin/pip")
    
    if pip_path.exists():
        command = f"{pip_path} install -r requirements.txt"
    else:
        print("⚠️  Using system pip (virtual environment not activated)")
        command = "pip install -r requirements.txt"
    
    return run_command(command, "Install dependencies")

def setup_environment_file():
    """Create .env file from .env.example"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("\n✅ .env file already exists")
        return True
    
    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("\n✅ Created .env from .env.example")
        print("\n⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY")
        print("   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx")
        return True
    else:
        print("\n❌ .env.example not found")
        return False

def start_docker_services():
    """Start Docker Compose services"""
    return run_command(
        "docker-compose up -d",
        "Start Docker services (PostgreSQL, Qdrant, Redis)"
    )

def check_docker_services():
    """Check if Docker services are running"""
    return run_command(
        "docker-compose ps",
        "Check Docker services status"
    )

def run_migrations():
    """Run database migrations"""
    alembic_path = Path("venv/Scripts/alembic") if os.name == 'nt' else Path("venv/bin/alembic")
    
    if alembic_path.exists():
        alembic_cmd = str(alembic_path)
    else:
        alembic_cmd = "alembic"
    
    # Generate migration
    success = run_command(
        f'{alembic_cmd} revision --autogenerate -m "Initial schema"',
        "Generate database migration"
    )
    
    if not success:
        print("⚠️  Migration generation failed - this is normal if tables already exist")
    
    # Run migration
    return run_command(
        f"{alembic_cmd} upgrade head",
        "Apply database migrations"
    )

def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      Food App Backend - Quick Setup Script              ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Please install missing prerequisites and try again")
        sys.exit(1)
    
    # Step 2: Setup virtual environment
    setup_virtual_environment()
    
    # Ask user to confirm venv activation
    response = input("\n❓ Have you activated the virtual environment? (y/n): ")
    if response.lower() != 'y':
        print("\n⚠️  Please activate the virtual environment and run this script again")
        sys.exit(0)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Step 4: Setup .env file
    if not setup_environment_file():
        print("\n❌ Failed to setup .env file")
        sys.exit(1)
    
    # Ask user to confirm .env configuration
    response = input("\n❓ Have you added your OPENAI_API_KEY to .env? (y/n): ")
    if response.lower() != 'y':
        print("\n⚠️  Please add your OPENAI_API_KEY to .env and run migrations manually:")
        print("   alembic revision --autogenerate -m 'Initial schema'")
        print("   alembic upgrade head")
        sys.exit(0)
    
    # Step 5: Start Docker services
    if not start_docker_services():
        print("\n❌ Failed to start Docker services")
        sys.exit(1)
    
    # Wait for services to start
    print("\n⏳ Waiting for services to start (5 seconds)...")
    import time
    time.sleep(5)
    
    # Step 6: Check Docker services
    check_docker_services()
    
    # Step 7: Run migrations
    if not run_migrations():
        print("\n⚠️  Migrations failed - you may need to run them manually")
    
    # Success message
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      ✅ Setup Complete!                                  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    Next steps:
    
    1. Start the backend server:
       uvicorn app.main:app --reload
    
    2. Open API documentation:
       http://localhost:8000/docs
    
    3. Test the API:
       python test_api.py
    
    4. Read the testing guide:
       docs/10-BACKEND-TESTING-GUIDE.md
    
    Happy coding! 🚀
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
