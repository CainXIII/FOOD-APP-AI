import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="postgres",
        user="cooking_admin2",
        password="cooking_pass_2024"
    )
    print("✅ Connection successful with cooking_admin2!")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")
