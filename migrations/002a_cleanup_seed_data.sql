-- ============================================================================
-- CLEANUP: Remove old seed data before comprehensive seed
-- ============================================================================
-- Purpose: Clean up any existing seed data from previous scripts
-- Date: 2025-10-09
-- Run this BEFORE running the comprehensive seed scripts
-- ============================================================================

-- ============================================================================
-- PART 1: Remove old meal templates
-- ============================================================================

-- Delete all public meal templates (community + restaurant)
DELETE FROM meal_template_foods
WHERE meal_template_id IN (
    SELECT id FROM meal_templates WHERE is_public = true
);

DELETE FROM meal_templates
WHERE is_public = true;

-- Verify deletion
SELECT COUNT(*) AS remaining_public_templates
FROM meal_templates
WHERE is_public = true;
-- Should return 0

-- ============================================================================
-- PART 2: Remove all atomic foods (will be re-seeded)
-- ============================================================================

-- Delete meal_foods entries that reference foods_enhanced
DELETE FROM meal_foods
WHERE food_id IN (SELECT id FROM foods_enhanced);

-- Delete all foods (keeps categories)
DELETE FROM foods_enhanced;

-- Verify deletion
SELECT COUNT(*) AS remaining_foods FROM foods_enhanced;
-- Should return 0

-- ============================================================================
-- PART 3: Keep food categories (needed for seed)
-- ============================================================================

-- Verify categories still exist
SELECT
    fc.name AS category,
    fc.level,
    fc.parent_id IS NOT NULL AS has_parent
FROM food_categories fc
ORDER BY fc.level, fc.sort_order;

-- Should show:
-- Level 0: Protein, Carbohydrates, Fats, Vegetables, Fruits, Dairy, Beverages, Supplements
-- Level 1: Subcategories (Poultry, Beef, Rice, Pasta, etc.)

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Check what's left in database
SELECT 'foods_enhanced' AS table_name, COUNT(*) AS count FROM foods_enhanced
UNION ALL
SELECT 'meal_templates', COUNT(*) FROM meal_templates
UNION ALL
SELECT 'meal_template_foods', COUNT(*) FROM meal_template_foods
UNION ALL
SELECT 'food_categories', COUNT(*) FROM food_categories
UNION ALL
SELECT 'user_favorite_foods', COUNT(*) FROM user_favorite_foods
UNION ALL
SELECT 'food_pairings', COUNT(*) FROM food_pairings;

-- Expected results:
-- foods_enhanced: 0
-- meal_templates: 0 (or only user-created ones if is_public = false)
-- meal_template_foods: 0 (or only user entries)
-- food_categories: ~20 (kept for seed)
-- user_favorite_foods: 0 (no users yet)
-- food_pairings: 0

-- ============================================================================
-- READY FOR COMPREHENSIVE SEED
-- ============================================================================

-- Now you can run in order:
-- 1. 003_COMPREHENSIVE_seed_atomic_foods.sql
-- 2. 003b_seed_fruits_vegetables_fats.sql
-- 3. 003c_seed_beverages_supplements.sql
-- 4. 004_COMPREHENSIVE_seed_meal_templates.sql
-- 5. 004b_seed_more_restaurant_templates.sql

-- ============================================================================
-- END CLEANUP
-- ============================================================================
