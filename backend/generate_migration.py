"""Generate initial Alembic migration"""
import subprocess
import sys

if __name__ == "__main__":
    try:
        # Run alembic command
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", "initial_schema_without_pgvector"],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
