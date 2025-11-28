"""Check PostgreSQL tables and verify no pgvector columns"""
import asyncio
from sqlalchemy import inspect, text
from app.database import engine

async def check_database():
    async with engine.begin() as conn:
        # Get table names
        def get_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()
        
        tables = await conn.run_sync(get_tables)
        
        print("=" * 60)
        print("DATABASE TABLES")
        print("=" * 60)
        for table in sorted(tables):
            print(f"✓ {table}")
        print(f"\nTotal: {len(tables)} tables")
        
        # Check embedding tables structure
        print("\n" + "=" * 60)
        print("EMBEDDING TABLES STRUCTURE")
        print("=" * 60)
        
        for table_name in ['recipe_embeddings', 'ingredient_embeddings']:
            if table_name in tables:
                print(f"\n{table_name}:")
                
                def get_columns(sync_conn):
                    inspector = inspect(sync_conn)
                    return inspector.get_columns(table_name)
                
                columns = await conn.run_sync(get_columns)
                
                for col in columns:
                    col_type = str(col['type'])
                    print(f"  - {col['name']}: {col_type}")
                    
                    # Check if any vector type
                    if 'vector' in col_type.lower() and 'qdrant' not in col['name']:
                        print(f"    ⚠️  WARNING: Found vector type column!")
        
        # Check for pgvector extension
        print("\n" + "=" * 60)
        print("POSTGRESQL EXTENSIONS")
        print("=" * 60)
        
        result = await conn.execute(text("SELECT extname FROM pg_extension;"))
        extensions = [row[0] for row in result]
        
        for ext in sorted(extensions):
            if ext == 'vector':
                print(f"⚠️  {ext} (pgvector - should be removed)")
            else:
                print(f"✓ {ext}")
        
        if 'vector' not in extensions:
            print("✅ No pgvector extension found!")
        
        print("\n" + "=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(check_database())
