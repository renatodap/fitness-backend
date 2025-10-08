-- Migration 012: Add Auto-Log Preference
-- Purpose: Add user preference for automatic logging vs manual review
-- Date: 2025-10-08
--
-- This migration adds the auto_log_enabled column to profiles table.
-- When FALSE (default): User reviews logs before saving
-- When TRUE: Logs are saved immediately, user can edit later

-- UP MIGRATION --

-- Add auto_log_enabled column to profiles
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS auto_log_enabled BOOLEAN DEFAULT FALSE;

-- Add comment explaining the column
COMMENT ON COLUMN profiles.auto_log_enabled IS 'When true, meals/workouts/measurements are logged automatically without user review. When false (default), user must confirm logs before saving.';

-- Create index for faster lookups (coach queries this frequently)
CREATE INDEX IF NOT EXISTS idx_profiles_auto_log_enabled
ON profiles(auto_log_enabled)
WHERE auto_log_enabled = TRUE;

-- DOWN MIGRATION (in comments for reference) --

-- To rollback:
-- DROP INDEX IF EXISTS idx_profiles_auto_log_enabled;
-- ALTER TABLE profiles DROP COLUMN IF EXISTS auto_log_enabled;
