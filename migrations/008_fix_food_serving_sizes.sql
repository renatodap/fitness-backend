-- Migration: Fix food serving sizes in foods_enhanced table
-- Description: Most foods are stored with serving_size=1 but nutrition per 100g
--              This causes incorrect calculations (100g banana = 8900 cal instead of 89)
-- Author: Claude Code
-- Date: 2025-10-07

-- ============================================================================
-- PART 1: Investigate the issue
-- ============================================================================

-- Check current banana data (run this first to verify the issue)
-- SELECT id, name, serving_size, serving_unit, calories, protein_g, total_carbs_g
-- FROM foods_enhanced
-- WHERE LOWER(name) LIKE '%banana%'
-- LIMIT 5;

-- Check how many foods have serving_size = 1
-- SELECT
--     serving_size,
--     serving_unit,
--     COUNT(*) as food_count
-- FROM foods_enhanced
-- GROUP BY serving_size, serving_unit
-- ORDER BY food_count DESC
-- LIMIT 10;

-- ============================================================================
-- PART 2: Fix - Update all foods with serving_size=1 to serving_size=100
-- ============================================================================

-- Most USDA data is per 100g, but was imported with serving_size=1
-- This fix assumes:
-- - If serving_size = 1 and serving_unit = 'g', it should be 100g
-- - Nutrition values are already per 100g (don't need to multiply)

UPDATE foods_enhanced
SET
    serving_size = 100,
    updated_at = NOW()
WHERE
    serving_size = 1
    AND serving_unit = 'g'
    AND calories IS NOT NULL;

-- ============================================================================
-- PART 3: Recalculate all existing meal_foods with new serving sizes
-- ============================================================================

-- Force recalculation of all meal_foods entries
-- This will trigger the calculate_meal_food_nutrition() function
UPDATE meal_foods
SET updated_at = NOW()
WHERE id IN (
    SELECT id FROM meal_foods LIMIT 10000
);

-- ============================================================================
-- PART 4: Verify the fix
-- ============================================================================

-- Check banana again (should now show serving_size = 100)
-- SELECT id, name, serving_size, serving_unit, calories, protein_g, total_carbs_g
-- FROM foods_enhanced
-- WHERE LOWER(name) LIKE '%banana%'
-- LIMIT 5;

-- Check a sample meal calculation
-- SELECT
--     mf.id,
--     f.name,
--     mf.quantity,
--     mf.unit,
--     f.serving_size,
--     f.serving_unit,
--     f.calories as food_calories,
--     mf.calories as calculated_calories,
--     (mf.quantity / f.serving_size) as multiplier
-- FROM meal_foods mf
-- JOIN foods_enhanced f ON f.id = mf.food_id
-- LIMIT 5;

-- ============================================================================
-- PART 5: Add comment
-- ============================================================================

COMMENT ON TABLE foods_enhanced IS 'Enhanced food database with nutrition data. Most entries use serving_size=100 and serving_unit=g (per 100g standard).';

-- ============================================================================
-- ROLLBACK (if needed)
-- ============================================================================

-- To rollback (this will restore serving_size = 1, but calculations will be wrong again):
-- UPDATE foods_enhanced SET serving_size = 1 WHERE serving_size = 100 AND serving_unit = 'g';
