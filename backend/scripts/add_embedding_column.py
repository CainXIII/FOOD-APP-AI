"""
Add embedding column to recipes table for semantic search
"""
import asyncio
import sys
sys.path.insert(0, "d:/Projects/Hackathon/backend")

from sqlalchemy import text
from app.database import async_session_maker


async def add_embedding_column():
    """Add embedding column to recipes table"""
    async with async_session_maker() as session:
        try:
            # Check if column exists
            result = await session.execute(
                text("PRAGMA table_info(recipes)")
            )
            columns = result.fetchall()
            column_names = [col[1] for col in columns]
            
            if 'embedding' in column_names:
                print("✓ Embedding column already exists")
                return
            
            # Add embedding column
            await session.execute(
                text("ALTER TABLE recipes ADD COLUMN embedding TEXT")
            )
            await session.commit()
            print("✓ Added embedding column to recipes table")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(add_embedding_column())
