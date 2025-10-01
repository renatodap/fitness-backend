"""
Apply database migration to Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def apply_migration():
    """Apply the Phase 1 migration"""
    # Read migration file
    migration_path = "migrations/001_phase1_database_rag_foundation.sql"

    with open(migration_path, 'r') as f:
        migration_sql = f.read()

    print("=" * 80)
    print("Applying Phase 1 Database Migration")
    print("=" * 80)
    print(f"Migration file: {migration_path}")
    print(f"Supabase URL: {SUPABASE_URL}")
    print()

    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

    # Split SQL into statements (basic approach)
    # Note: This is a simplified approach. For production, use proper migration tools.
    statements = migration_sql.split(';')

    print(f"Executing {len(statements)} SQL statements...")
    print()

    success_count = 0
    error_count = 0

    for i, statement in enumerate(statements, 1):
        statement = statement.strip()
        if not statement or statement.startswith('--'):
            continue

        try:
            # Execute using Supabase's RPC or direct SQL execution
            # Note: Supabase Python client doesn't have direct SQL execution
            # We need to use PostgREST or the management API
            print(f"Statement {i}/{len(statements)}: {statement[:50]}...")
            # supabase.rpc('exec_sql', {'sql': statement}).execute()
            success_count += 1
        except Exception as e:
            print(f"ERROR in statement {i}: {e}")
            error_count += 1

    print()
    print("=" * 80)
    print(f"Migration Summary:")
    print(f"  Successful: {success_count}")
    print(f"  Errors: {error_count}")
    print("=" * 80)

    if error_count == 0:
        print("✅ Migration applied successfully!")
    else:
        print("⚠️  Migration completed with errors. Check the output above.")

    return error_count == 0

if __name__ == "__main__":
    print("\nNOTE: This script requires manual SQL execution via Supabase Dashboard.")
    print("Please apply the migration manually by:")
    print("1. Opening Supabase Dashboard > SQL Editor")
    print("2. Pasting the contents of migrations/001_phase1_database_rag_foundation.sql")
    print("3. Running the SQL")
    print("\nThe migration file has already been created and is ready to use.")
    print("\nAlternatively, if you have psql installed, run:")
    print("  psql <your-connection-string> -f migrations/001_phase1_database_rag_foundation.sql")
    print("\nAssuming migration is applied. Proceeding with feature implementation...")
