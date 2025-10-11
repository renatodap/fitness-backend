-- ============================================================================
-- MIGRATION 029: ADD LANGUAGE PREFERENCE TO USERS
-- ============================================================================
-- Description: Add language_preference column to user_profiles for i18n support
-- ============================================================================

BEGIN;

-- Add language_preference column to user_profiles table
ALTER TABLE user_profiles
ADD COLUMN IF NOT EXISTS language_preference VARCHAR(5) DEFAULT 'en' CHECK (language_preference IN ('en', 'pt'));

-- Create index for efficient querying
CREATE INDEX IF NOT EXISTS idx_user_profiles_language_preference
ON user_profiles(language_preference);

-- Update existing users to default language (English)
UPDATE user_profiles
SET language_preference = 'en'
WHERE language_preference IS NULL;

COMMIT;

SELECT '✅ LANGUAGE PREFERENCE ADDED!' as status;
