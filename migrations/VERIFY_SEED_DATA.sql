-- ============================================================================
-- DATABASE VERIFICATION SCRIPT
-- ============================================================================
-- Purpose: Verify that seed data was successfully loaded
-- Run this to check database state before testing food search
-- ============================================================================

-- 1. Check if food categories exist (from migration 002)
SELECT
    'Food Categories' AS check_name,
    COUNT(*) AS count,
    CASE
        WHEN COUNT(*) >= 8 THEN '✅ PASS'
        ELSE '❌ FAIL - Expected at least 8 categories'
    END AS status
FROM food_categories;

-- Expected: 8 top-level categories (Protein, Carbs, Fats, Vegetables, Fruits, Dairy, Beverages, Supplements)

-- 2. Check total atomic foods count (from migrations 003a, 003b, 003c)
SELECT
    'Total Atomic Foods' AS check_name,
    COUNT(*) AS count,
    CASE
        WHEN COUNT(*) >= 220 THEN '✅ PASS'
        WHEN COUNT(*) >= 100 THEN '⚠️ PARTIAL - Some migrations may not have run'
        ELSE '❌ FAIL - Expected ~225 foods'
    END AS status
FROM foods_enhanced
WHERE is_atomic = true;

-- Expected: ~225 atomic foods

-- 3. Check if Banana exists (from migration 003b)
SELECT
    'Banana Food' AS check_name,
    COUNT(*) AS count,
    CASE
        WHEN COUNT(*) > 0 THEN '✅ PASS'
        ELSE '❌ FAIL - Banana not found. Run 003b migration.'
    END AS status
FROM foods_enhanced
WHERE name ILIKE '%banana%';

-- 4. Show Banana details if it exists
SELECT
    id,
    name,
    serving_size,
    serving_unit,
    household_serving_size,
    household_serving_unit,
    calories,
    protein_g,
    total_carbs_g
FROM foods_enhanced
WHERE name ILIKE '%banana%';

-- 5. Check foods by food_group
SELECT
    food_group,
    COUNT(*) AS total_count,
    COUNT(*) FILTER (WHERE household_serving_size IS NOT NULL) AS with_household_serving,
    ROUND(AVG(data_quality_score), 2) AS avg_quality
FROM foods_enhanced
WHERE is_atomic = true
GROUP BY food_group
ORDER BY total_count DESC;

-- Expected distribution:
-- Protein: ~60
-- Carbohydrates: ~50
-- Vegetables: ~30
-- Fruits: ~25
-- Fats: ~25
-- Beverages: ~15
-- Supplements: ~8
-- Dairy: ~10

-- 6. Check meal templates (from migrations 004a, 004b)
SELECT
    'Meal Templates' AS check_name,
    COUNT(*) AS count,
    CASE
        WHEN COUNT(*) >= 25 THEN '✅ PASS'
        WHEN COUNT(*) >= 10 THEN '⚠️ PARTIAL - Some templates may be missing'
        ELSE '❌ FAIL - Expected ~30 templates'
    END AS status
FROM meal_templates
WHERE is_public = true;

-- Expected: ~30 public meal templates

-- 7. Sample search test (what the API would do)
SELECT
    'Search Test: "banana"' AS test_name,
    id,
    name,
    food_group,
    serving_size || ' ' || serving_unit AS serving,
    household_serving_size || ' ' || household_serving_unit AS household_serving,
    calories
FROM foods_enhanced
WHERE name ILIKE '%banana%'
  AND data_quality_score >= 0.5
  AND is_atomic = true
ORDER BY data_quality_score DESC
LIMIT 5;

-- 8. Sample search test: "chicken"
SELECT
    'Search Test: "chicken"' AS test_name,
    id,
    name,
    food_group,
    serving_size || ' ' || serving_unit AS serving,
    household_serving_size || ' ' || household_serving_unit AS household_serving,
    calories
FROM foods_enhanced
WHERE name ILIKE '%chicken%'
  AND data_quality_score >= 0.5
  AND is_atomic = true
ORDER BY data_quality_score DESC
LIMIT 5;

-- ============================================================================
-- TROUBLESHOOTING
-- ============================================================================
-- If any checks FAIL:
--
-- 1. Food Categories missing:
--    Run: migrations/002_food_architecture_cleanup.sql
--
-- 2. Atomic foods count low:
--    Run in order:
--    - migrations/003a_seed_atomic_foods_proteins_carbs.sql
--    - migrations/003b_seed_fruits_vegetables_fats.sql
--    - migrations/003c_seed_beverages_supplements.sql
--
-- 3. Meal templates missing:
--    Run in order:
--    - migrations/004a_seed_meal_templates_community.sql
--    - migrations/004b_seed_meal_templates_restaurants.sql
--
-- 4. If you want to start fresh:
--    Run: migrations/002a_cleanup_seed_data.sql (WARNING: Deletes all foods!)
--    Then: Re-run all seed migrations (003a, 003b, 003c, 004a, 004b)
-- ============================================================================
