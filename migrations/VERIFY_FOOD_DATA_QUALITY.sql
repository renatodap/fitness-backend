-- =============================================================================
-- Food Data Quality Verification Script
-- =============================================================================
-- Run this script after repopulating food data to verify everything is correct
-- Date: 2025-01-10
-- =============================================================================

\echo '==================================================================='
\echo 'FOOD DATA QUALITY VERIFICATION'
\echo '==================================================================='
\echo ''

-- =============================================================================
-- 1. Overall Statistics
-- =============================================================================

\echo '1. OVERALL STATISTICS'
\echo '-------------------------------------------------------------------'

SELECT 
  COUNT(*) as total_foods,
  COUNT(DISTINCT category) as unique_categories,
  COUNT(CASE WHEN household_serving_unit IS NOT NULL THEN 1 END) as with_household_serving,
  ROUND(
    COUNT(CASE WHEN household_serving_unit IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100, 
    1
  ) as household_serving_percentage,
  COUNT(CASE WHEN brand_name IS NOT NULL THEN 1 END) as with_brand,
  COUNT(CASE WHEN is_verified = true THEN 1 END) as verified_foods
FROM foods_enhanced;

\echo ''

-- =============================================================================
-- 2. Category Breakdown
-- =============================================================================

\echo '2. FOOD COUNT BY CATEGORY'
\echo '-------------------------------------------------------------------'

SELECT 
  category,
  COUNT(*) as food_count,
  COUNT(CASE WHEN household_serving_unit IS NOT NULL THEN 1 END) as with_household_serving,
  ROUND(
    COUNT(CASE WHEN household_serving_unit IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100, 
    1
  ) as percentage_with_serving
FROM foods_enhanced
WHERE category IS NOT NULL
GROUP BY category
ORDER BY food_count DESC;

\echo ''

-- =============================================================================
-- 3. Household Serving Units Distribution
-- =============================================================================

\echo '3. HOUSEHOLD SERVING UNITS DISTRIBUTION'
\echo '-------------------------------------------------------------------'

SELECT 
  household_serving_unit,
  COUNT(*) as food_count,
  ROUND(COUNT(*)::numeric / (SELECT COUNT(*) FROM foods_enhanced WHERE household_serving_unit IS NOT NULL) * 100, 1) as percentage
FROM foods_enhanced
WHERE household_serving_unit IS NOT NULL
GROUP BY household_serving_unit
ORDER BY food_count DESC
LIMIT 20;

\echo ''

-- =============================================================================
-- 4. Nutrition Data Completeness
-- =============================================================================

\echo '4. NUTRITION DATA COMPLETENESS'
\echo '-------------------------------------------------------------------'

SELECT 
  'Calories' as nutrient,
  COUNT(*) as total_foods,
  COUNT(CASE WHEN calories > 0 THEN 1 END) as with_data,
  ROUND(COUNT(CASE WHEN calories > 0 THEN 1 END)::numeric / COUNT(*) * 100, 1) as percentage
FROM foods_enhanced

UNION ALL

SELECT 
  'Protein',
  COUNT(*),
  COUNT(CASE WHEN protein_g > 0 THEN 1 END),
  ROUND(COUNT(CASE WHEN protein_g > 0 THEN 1 END)::numeric / COUNT(*) * 100, 1)
FROM foods_enhanced

UNION ALL

SELECT 
  'Carbs',
  COUNT(*),
  COUNT(CASE WHEN total_carbs_g > 0 THEN 1 END),
  ROUND(COUNT(CASE WHEN total_carbs_g > 0 THEN 1 END)::numeric / COUNT(*) * 100, 1)
FROM foods_enhanced

UNION ALL

SELECT 
  'Fat',
  COUNT(*),
  COUNT(CASE WHEN total_fat_g > 0 THEN 1 END),
  ROUND(COUNT(CASE WHEN total_fat_g > 0 THEN 1 END)::numeric / COUNT(*) * 100, 1)
FROM foods_enhanced

UNION ALL

SELECT 
  'Fiber',
  COUNT(*),
  COUNT(CASE WHEN dietary_fiber_g > 0 THEN 1 END),
  ROUND(COUNT(CASE WHEN dietary_fiber_g > 0 THEN 1 END)::numeric / COUNT(*) * 100, 1)
FROM foods_enhanced;

\echo ''

-- =============================================================================
-- 5. Sample Foods with Household Servings
-- =============================================================================

\echo '5. SAMPLE FOODS WITH HOUSEHOLD SERVINGS (First 30)'
\echo '-------------------------------------------------------------------'

SELECT 
  name,
  category,
  serving_size,
  serving_unit,
  household_serving_size,
  household_serving_unit,
  calories,
  protein_g,
  total_carbs_g,
  total_fat_g
FROM foods_enhanced
WHERE household_serving_unit IS NOT NULL
ORDER BY category, name
LIMIT 30;

\echo ''

-- =============================================================================
-- 6. Foods Without Household Servings (needs attention)
-- =============================================================================

\echo '6. COMMON FOODS WITHOUT HOUSEHOLD SERVINGS (First 20)'
\echo '-------------------------------------------------------------------'

SELECT 
  name,
  category,
  serving_size,
  serving_unit,
  calories,
  protein_g
FROM foods_enhanced
WHERE household_serving_unit IS NULL
  AND category IN ('protein', 'carbs', 'fruits', 'vegetables', 'dairy')
ORDER BY category, name
LIMIT 20;

\echo ''

-- =============================================================================
-- 7. Verify No Duplicate Foods
-- =============================================================================

\echo '7. CHECK FOR DUPLICATE FOODS'
\echo '-------------------------------------------------------------------'

SELECT 
  name,
  category,
  COUNT(*) as duplicate_count
FROM foods_enhanced
GROUP BY name, category
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, name;

-- If no results, show success message
SELECT 'No duplicate foods found! ✓' as status
WHERE NOT EXISTS (
  SELECT 1
  FROM foods_enhanced
  GROUP BY name, category
  HAVING COUNT(*) > 1
);

\echo ''

-- =============================================================================
-- 8. Verify Data Integrity
-- =============================================================================

\echo '8. DATA INTEGRITY CHECKS'
\echo '-------------------------------------------------------------------'

-- Check for invalid serving sizes
SELECT 'Foods with invalid serving size (≤0):' as check_name, COUNT(*) as count
FROM foods_enhanced
WHERE serving_size <= 0

UNION ALL

-- Check for foods with no calories and no macros (likely incomplete)
SELECT 'Foods with no nutrition data:', COUNT(*)
FROM foods_enhanced
WHERE calories = 0 
  AND protein_g = 0 
  AND total_carbs_g = 0 
  AND total_fat_g = 0

UNION ALL

-- Check for foods with extreme calorie values (possible errors)
SELECT 'Foods with suspicious calories (>1000 per 100g):', COUNT(*)
FROM foods_enhanced
WHERE calories > 1000

UNION ALL

-- Check for foods with invalid macro ratios (protein+carbs+fat*9 should ≈ calories)
SELECT 'Foods with mismatched macros vs calories:', COUNT(*)
FROM foods_enhanced
WHERE ABS(
  (protein_g * 4 + total_carbs_g * 4 + total_fat_g * 9) - calories
) > (calories * 0.2)  -- Allow 20% variance
  AND calories > 0;

\echo ''

-- =============================================================================
-- 9. Sample High-Quality Foods
-- =============================================================================

\echo '9. SAMPLE HIGH-QUALITY FOODS (Complete Data)'
\echo '-------------------------------------------------------------------'

SELECT 
  name,
  category,
  household_serving_unit,
  calories,
  protein_g,
  total_carbs_g,
  total_fat_g,
  dietary_fiber_g,
  is_verified
FROM foods_enhanced
WHERE household_serving_unit IS NOT NULL
  AND calories > 0
  AND (protein_g > 0 OR total_carbs_g > 0 OR total_fat_g > 0)
ORDER BY RANDOM()
LIMIT 20;

\echo ''

-- =============================================================================
-- 10. Summary Report
-- =============================================================================

\echo '10. SUMMARY REPORT'
\echo '-------------------------------------------------------------------'

WITH stats AS (
  SELECT 
    COUNT(*) as total_foods,
    COUNT(CASE WHEN household_serving_unit IS NOT NULL THEN 1 END) as with_household,
    COUNT(CASE WHEN calories > 0 THEN 1 END) as with_calories,
    COUNT(CASE WHEN is_verified = true THEN 1 END) as verified,
    COUNT(CASE WHEN 
      household_serving_unit IS NOT NULL 
      AND calories > 0 
      AND (protein_g > 0 OR total_carbs_g > 0 OR total_fat_g > 0)
    THEN 1 END) as high_quality
  FROM foods_enhanced
)
SELECT 
  total_foods || ' total foods' as metric,
  'Database populated' as status
FROM stats

UNION ALL

SELECT 
  with_household || ' with household servings (' || 
  ROUND(with_household::numeric / total_foods * 100, 1) || '%)',
  CASE 
    WHEN with_household::numeric / total_foods > 0.7 THEN '✓ Good'
    WHEN with_household::numeric / total_foods > 0.5 THEN '⚠ Acceptable'
    ELSE '✗ Needs improvement'
  END
FROM stats

UNION ALL

SELECT 
  with_calories || ' with calorie data (' || 
  ROUND(with_calories::numeric / total_foods * 100, 1) || '%)',
  CASE 
    WHEN with_calories::numeric / total_foods > 0.95 THEN '✓ Excellent'
    WHEN with_calories::numeric / total_foods > 0.8 THEN '✓ Good'
    ELSE '⚠ Needs attention'
  END
FROM stats

UNION ALL

SELECT 
  high_quality || ' high-quality foods (' || 
  ROUND(high_quality::numeric / total_foods * 100, 1) || '%)',
  CASE 
    WHEN high_quality::numeric / total_foods > 0.7 THEN '✓ Excellent'
    WHEN high_quality::numeric / total_foods > 0.5 THEN '✓ Good'
    ELSE '⚠ Could be better'
  END
FROM stats;

\echo ''
\echo '==================================================================='
\echo 'VERIFICATION COMPLETE'
\echo '==================================================================='
