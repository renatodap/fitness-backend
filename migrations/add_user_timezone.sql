-- Add timezone support to profiles
-- Migration: add_user_timezone.sql
-- Description: Add timezone field to profiles table for proper date/time handling

-- UP Migration
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS timezone TEXT DEFAULT 'UTC';

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_profiles_timezone ON profiles(timezone);

-- Update existing users to UTC (they can change it later in settings)
UPDATE profiles
SET timezone = 'UTC'
WHERE timezone IS NULL;

-- Add comment
COMMENT ON COLUMN profiles.timezone IS 'User timezone (IANA timezone identifier, e.g., "America/New_York", "Europe/London")';

-- DOWN Migration (commented)
-- ALTER TABLE profiles DROP COLUMN IF EXISTS timezone;
-- DROP INDEX IF EXISTS idx_profiles_timezone;
