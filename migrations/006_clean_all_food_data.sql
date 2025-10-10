-- Migration: 006_clean_all_food_data
-- Description: Clean all food-related data to start fresh
-- Date: 2025-10-10
-- Purpose: Remove test/garbage data and prepare for clean data import

-- ============================================================================
-- STEP 1: BACKUP VERIFICATION (Run this first to see what will be deleted)
-- ============================================================================

-- Check how many records will be deleted
SELECT 
  'foods_enhanced' as table_name, 
  COUNT(*) as record_count,
  COUNT(DISTINCT created_by) as unique_users
FROM foods_enhanced
UNION ALL
SELECT 
  'meal_logs' as table_name,
  COUNT(*),
  COUNT(DISTINCT user_id)
FROM meal_logs
UNION ALL
SELECT 
  'meal_foods' as table_name,
  COUNT(*),
  NULL
FROM meal_foods
UNION ALL
SELECT 
  'meal_templates' as table_name,
  COUNT(*),
  COUNT(DISTINCT user_id)
FROM meal_templates
UNION ALL
SELECT 
  'meal_template_foods' as table_name,
  COUNT(*),
  NULL
FROM meal_template_foods
UNION ALL
SELECT 
  'food_search_log' as table_name,
  COUNT(*),
  COUNT(DISTINCT user_id)
FROM food_search_log
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'food_search_log');

-- ============================================================================
-- STEP 2: DELETE ALL FOOD-RELATED DATA (Execute after verification)
-- ============================================================================

-- Delete in correct order to respect foreign key constraints

-- 1. Delete meal template foods first (references meal_templates and foods_enhanced)
DELETE FROM meal_template_foods;

-- 2. Delete meal foods (references meal_logs and foods_enhanced)  
DELETE FROM meal_foods;

-- 3. Delete meal templates (references users)
DELETE FROM meal_templates;

-- 4. Delete meal logs (references users)
DELETE FROM meal_logs;

-- 5. Delete food search logs if table exists
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'food_search_log') THEN
    DELETE FROM food_search_log;
  END IF;
END $$;

-- 6. Finally, delete all foods
DELETE FROM foods_enhanced;

-- ============================================================================
-- STEP 3: RESET SEQUENCES AND VERIFY
-- ============================================================================

-- Verify all tables are empty
SELECT 
  'foods_enhanced' as table_name, 
  COUNT(*) as remaining_records
FROM foods_enhanced
UNION ALL
SELECT 'meal_logs', COUNT(*) FROM meal_logs
UNION ALL
SELECT 'meal_foods', COUNT(*) FROM meal_foods
UNION ALL
SELECT 'meal_templates', COUNT(*) FROM meal_templates
UNION ALL
SELECT 'meal_template_foods', COUNT(*) FROM meal_template_foods;

-- Reset popularity scores and search counts (if needed later)
-- This is just for verification that the schema is ready

-- ============================================================================
-- STEP 4: VERIFY SCHEMA IS INTACT
-- ============================================================================

-- Verify foods_enhanced table structure
SELECT 
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'foods_enhanced'
  AND column_name IN (
    'serving_size',
    'serving_unit', 
    'household_serving_size',
    'household_serving_unit'
  )
ORDER BY ordinal_position;

-- ============================================================================
-- NOTES FOR REPOPULATION
-- ============================================================================

/*
After running this migration, repopulate with:

1. Run existing seed migrations in order:
   - 003a_seed_atomic_foods_proteins_carbs.sql
   - 003b_seed_fruits_vegetables_fats.sql
   - 003c_seed_beverages_supplements.sql
   - 003d_seed_real_world_foods_phase1.sql
   - 003e_seed_real_world_foods_phase2.sql
   - 003f_seed_real_world_foods_phase3.sql
   - 003g_seed_real_world_produce_phase4.sql
   - 005_seed_comprehensive_foods_phase5.sql

2. Each food should have:
   - serving_size: Base nutritional reference (usually 100g)
   - serving_unit: Usually 'g' for the database reference
   - household_serving_size: User-friendly amount (e.g., "1", "0.5", "2")
   - household_serving_unit: User-friendly unit (e.g., "slice", "scoop", "medium")

3. Examples of proper food entries:
   
   Pizza:
   - serving_size: 100, serving_unit: 'g'
   - household_serving_size: '1', household_serving_unit: 'slice'
   - (1 slice ≈ 120g, so user can toggle between "1 slice" or "120g")
   
   Banana:
   - serving_size: 100, serving_unit: 'g'
   - household_serving_size: '1', household_serving_unit: 'medium'
   - (1 medium ≈ 118g, so user can toggle between "1 medium" or "118g")
   
   Whey Protein:
   - serving_size: 100, serving_unit: 'g'
   - household_serving_size: '1', household_serving_unit: 'scoop'
   - (1 scoop ≈ 30g, so user can toggle between "1 scoop" or "30g")
   
   Rice (cooked):
   - serving_size: 100, serving_unit: 'g'
   - household_serving_size: '1', household_serving_unit: 'cup'
   - (1 cup ≈ 195g, so user can toggle between "1 cup" or "195g")

4. The UI should calculate conversions dynamically:
   - If user changes servings: grams = servings × (household_serving_grams)
   - If user changes grams: servings = grams / (household_serving_grams)
   - household_serving_grams can be calculated from existing seed data ratios
*/

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
  RAISE NOTICE '✅ Food data cleanup complete!';
  RAISE NOTICE '📝 Next steps:';
  RAISE NOTICE '   1. Review the verification queries above';
  RAISE NOTICE '   2. Run seed migrations 003a through 005 to repopulate';
  RAISE NOTICE '   3. Verify household_serving fields are populated correctly';
  RAISE NOTICE '   4. Test the UI conversion functionality';
END $$;
