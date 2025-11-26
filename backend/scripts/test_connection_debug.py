import psycopg2

# Test 1: With password
print("Test 1: Connection with password...")
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="cooking_assistant",
        user="cooking_admin",
        password="cooking_pass_2024"
    )
    print("✅ SUCCESS with password!")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 2: No password
print("\nTest 2: Connection without password...")
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="cooking_assistant",
        user="cooking_admin"
    )
    print("✅ SUCCESS without password!")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 3: Check via docker exec
print("\nTest 3: Via docker exec...")
import subprocess
result = subprocess.run([
    "docker", "exec", "cooking_assistant_db",
    "psql", "-U", "cooking_admin", "-d", "cooking_assistant",
    "-c", "SELECT current_user, current_database();"
], capture_output=True, text=True)
print(result.stdout)
