"""
Migration runner script for Wagner Coach backend.

Runs SQL migration files against Supabase database.
"""
import sys
from pathlib import Path
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.config import get_settings
from app.services.supabase_service import get_service_client

def run_migration(migration_file: str):
    """
    Run a SQL migration file against Supabase.

    Args:
        migration_file: Path to SQL migration file
    """
    settings = get_settings()
    supabase = get_service_client()

    # Read migration file
    migration_path = Path(__file__).parent.parent / "migrations" / migration_file

    if not migration_path.exists():
        print(f"❌ Migration file not found: {migration_path}")
        sys.exit(1)

    print(f"📄 Reading migration: {migration_file}")
    with open(migration_path, 'r') as f:
        sql = f.read()

    print(f"🚀 Executing migration...")

    try:
        # Execute raw SQL via Supabase client
        # Note: Supabase Python client doesn't have direct SQL execution
        # So we'll use the REST API directly
        import httpx

        response = httpx.post(
            f"{settings.SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers={
                "apikey": settings.SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json"
            },
            json={"query": sql},
            timeout=30.0
        )

        if response.status_code == 200:
            print(f"✅ Migration completed successfully!")
        else:
            print(f"❌ Migration failed: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Migration failed with error: {e}")
        print("\n⚠️  Manual migration required:")
        print(f"   1. Go to Supabase Dashboard → SQL Editor")
        print(f"   2. Paste contents of: {migration_path}")
        print(f"   3. Run the SQL")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_migration.py <migration_file>")
        print("Example: python run_migration.py 010_add_ai_food_tracking.sql")
        sys.exit(1)

    migration_file = sys.argv[1]
    run_migration(migration_file)
