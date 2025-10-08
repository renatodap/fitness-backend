"""
Apply migration 012: Add auto_log_enabled column to profiles table.

This script manually applies the migration using direct PostgreSQL connection.
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv("wagner-coach-backend/.env")

print("="*60)
print("MIGRATION 012: Add auto_log_enabled preference")
print("="*60)

print("\nTo apply this migration, you need to run the following SQL in Supabase SQL Editor:")
print("\n" + "-"*60)

migration_sql = """
-- Add auto_log_enabled column to profiles
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS auto_log_enabled BOOLEAN DEFAULT FALSE;

-- Add comment explaining the column
COMMENT ON COLUMN profiles.auto_log_enabled IS 'When true, meals/workouts/measurements are logged automatically without user review. When false (default), user must confirm logs before saving.';

-- Create index for faster lookups (coach queries this frequently)
CREATE INDEX IF NOT EXISTS idx_profiles_auto_log_enabled
ON profiles(auto_log_enabled)
WHERE auto_log_enabled = TRUE;
"""

print(migration_sql)
print("-"*60)

print("\nSteps to apply:")
print("1. Go to Supabase Dashboard > SQL Editor")
print("2. Copy the SQL above")
print("3. Paste and run it")
print("4. Verify with: SELECT column_name FROM information_schema.columns WHERE table_name='profiles' AND column_name='auto_log_enabled';")

print("\nOR use Supabase CLI:")
print("  supabase db push --include-all")
