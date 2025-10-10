-- ============================================================================
-- COMPREHENSIVE CLEANUP: Remove EVERYTHING Food & Meal Related
-- ============================================================================
-- Purpose: Complete nuclear reset of all food and meal tracking components
-- Date: 2025-01-10
-- Compatible with: Supabase SQL Editor
-- 
-- ⚠️  WARNING: THIS WILL PERMANENTLY DELETE:
--   - All food data (foods_enhanced table and old foods tables)
--   - All meal logs (meal_logs, meal_foods)
--   - All meal templates (meal_templates, meal_template_foods)
--   - All AI-created food logs
--   - All food preferences
--   - All daily nutrition summaries
--   - All related indexes, functions, triggers, and constraints
-- 
-- Make sure you have a backup if needed!
-- ============================================================================

BEGIN;

-- ============================================================================
-- Step 1: Drop junction and dependent tables first
-- ============================================================================

DROP TABLE IF EXISTS meal_foods CASCADE;
DROP TABLE IF EXISTS meal_template_foods CASCADE;
DROP TABLE IF EXISTS food_preferences CASCADE;
DROP TABLE IF EXISTS ai_created_foods_log CASCADE;

-- ============================================================================
-- Step 2: Drop main tables
-- ============================================================================

DROP TABLE IF EXISTS meal_logs CASCADE;
DROP TABLE IF EXISTS meal_templates CASCADE;
DROP TABLE IF EXISTS meals CASCADE;
DROP TABLE IF EXISTS foods_enhanced CASCADE;
DROP TABLE IF EXISTS foods CASCADE;

-- ============================================================================
-- Step 3: Drop daily summaries that reference meals
-- ============================================================================

DROP TABLE IF EXISTS daily_nutrition_summaries CASCADE;

-- ============================================================================
-- Step 4: Drop any custom types related to meals
-- ============================================================================

DROP TYPE IF EXISTS meal_category CASCADE;

-- ============================================================================
-- Step 5: Drop sequences
-- ============================================================================

DROP SEQUENCE IF EXISTS foods_id_seq CASCADE;
DROP SEQUENCE IF EXISTS foods_enhanced_id_seq CASCADE;
DROP SEQUENCE IF EXISTS meals_id_seq CASCADE;
DROP SEQUENCE IF EXISTS meal_logs_id_seq CASCADE;
DROP SEQUENCE IF EXISTS meal_templates_id_seq CASCADE;

-- ============================================================================
-- Step 6: Drop functions and triggers
-- ============================================================================

DROP FUNCTION IF EXISTS update_food_last_logged CASCADE;
DROP FUNCTION IF EXISTS calculate_meal_nutrition CASCADE;
DROP FUNCTION IF EXISTS update_meal_totals CASCADE;
DROP FUNCTION IF EXISTS update_daily_nutrition_summary CASCADE;
DROP FUNCTION IF EXISTS search_foods CASCADE;
DROP FUNCTION IF EXISTS search_foods_enhanced CASCADE;

-- ============================================================================
-- Step 7: Drop any views and related tables
-- ============================================================================

DROP VIEW IF EXISTS meal_logs_with_details CASCADE;
DROP VIEW IF EXISTS meal_foods_with_nutrition CASCADE;
DROP VIEW IF EXISTS recent_foods CASCADE;
DROP TABLE IF EXISTS user_favorite_foods CASCADE;

-- ============================================================================
-- Step 8: Remove any food/meal related multimodal embeddings
-- ============================================================================

DELETE FROM multimodal_embeddings 
WHERE source_type IN ('meal', 'meal_log', 'meal_photo', 'food_label', 'nutrition_label');

-- ============================================================================
-- Step 9: Remove any food/meal related program items
-- ============================================================================

UPDATE ai_program_items 
SET meal_foods = NULL, meal_recipe = NULL 
WHERE item_type = 'meal';

-- ============================================================================
-- Step 10: Remove food/meal related recommendations
-- ============================================================================

DELETE FROM daily_recommendations 
WHERE recommendation_type = 'meal';

COMMIT;

-- ============================================================================
-- VERIFICATION QUERIES (Run these separately to check results)
-- ============================================================================

-- Check for remaining tables (should return nothing)
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND (tablename LIKE '%food%' OR tablename LIKE '%meal%');

-- Check for remaining functions (should return nothing)
-- SELECT proname FROM pg_proc WHERE proname LIKE '%food%' OR proname LIKE '%meal%';

-- Success message
SELECT '✅ COMPREHENSIVE CLEANUP COMPLETE!' as status,
       'All food and meal tables, functions, and data have been removed.' as message,
       'Next step: Run CREATE_clean_food_system.sql' as next_step;
