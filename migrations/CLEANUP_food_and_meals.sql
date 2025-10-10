-- ============================================================================
-- CLEANUP: Drop All Food and Meal Related Tables
-- ============================================================================
-- Purpose: Start fresh with a clean, well-designed food and meal system
-- Author: System Redesign
-- Date: 2025-01-10
-- 
-- WARNING: This will DELETE ALL food and meal data permanently!
-- Make sure you have a backup if needed.
-- ============================================================================

BEGIN;

-- Drop tables in reverse dependency order to avoid foreign key errors
DROP TABLE IF EXISTS meal_foods CASCADE;
DROP TABLE IF EXISTS meals CASCADE;
DROP TABLE IF EXISTS food_preferences CASCADE;
DROP TABLE IF EXISTS foods CASCADE;

-- Drop any related sequences
DROP SEQUENCE IF EXISTS foods_id_seq CASCADE;
DROP SEQUENCE IF EXISTS meals_id_seq CASCADE;

-- Drop any related functions or triggers
DROP FUNCTION IF EXISTS update_food_last_logged CASCADE;
DROP FUNCTION IF EXISTS calculate_meal_nutrition CASCADE;

COMMIT;

-- Verification: List remaining food/meal related objects (should be empty)
SELECT tablename 
FROM pg_tables 
WHERE tablename LIKE '%food%' OR tablename LIKE '%meal%'
ORDER BY tablename;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Cleanup complete! All food and meal tables have been dropped.';
    RAISE NOTICE '📝 Ready for fresh schema creation.';
END $$;
