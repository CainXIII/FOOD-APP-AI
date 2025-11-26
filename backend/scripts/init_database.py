"""
Initialize SQLite database with tables
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, Base
from sqlalchemy import text

async def init_database():
    """Create all tables"""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        # Drop all tables first (clean start)
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ Dropped existing tables")
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Created all tables")
    
    print("\n🎉 Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(init_database())
