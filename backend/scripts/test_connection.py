import psycopg2
from psycopg2 import OperationalError

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="cooking_assistant",
        user="cooking_admin",
        password="cooking_pass_2024"
    )
    print("✅ Connection successful with 127.0.0.1!")
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    cur.execute("SELECT extname FROM pg_extension WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm');")
    extensions = cur.fetchall()
    print("\nInstalled extensions:")
    for ext in extensions:
        print(f"  - {ext[0]}")
    
    cur.close()
    conn.close()
    
except OperationalError as e:
    print(f"❌ Connection failed: {e}")
