-- Migration: Fix Missing Nutrition Data in foods_enhanced
-- Description: Mark foods with missing/zero carbs and fats as low quality
--              This allows the AI to recreate them with better data
-- Author: Claude Code
-- Date: 2025-10-08

-- ============================================================================
-- PART 1: Identify the problem
-- ============================================================================

-- Check how many foods have missing/zero nutrition
-- Uncomment to run diagnostics:
/*
SELECT
    COUNT(*) as total_foods,
    COUNT(*) FILTER (WHERE total_carbs_g IS NULL OR total_carbs_g = 0) as missing_carbs,
    COUNT(*) FILTER (WHERE total_fat_g IS NULL OR total_fat_g = 0) as missing_fats,
    COUNT(*) FILTER (WHERE
        (total_carbs_g IS NULL OR total_carbs_g = 0) AND
        (total_fat_g IS NULL OR total_fat_g = 0) AND
        calories > 0
    ) as incomplete_nutrition
FROM foods_enhanced;
*/

-- ============================================================================
-- PART 2: Mark incomplete foods as low quality
-- ============================================================================

-- Strategy: Instead of deleting, mark as low quality so AI will prefer to
-- create new entries rather than match to these incomplete ones

UPDATE foods_enhanced
SET
    data_quality_score = 0.2,  -- Very low quality
    updated_at = NOW()
WHERE
    -- Has calories but missing carbs OR fat
    calories IS NOT NULL
    AND calories > 0
    AND (
        total_carbs_g IS NULL
        OR total_carbs_g = 0
        OR total_fat_g IS NULL
        OR total_fat_g = 0
    )
    -- Don't downgrade already low-quality foods
    AND (data_quality_score IS NULL OR data_quality_score > 0.3);

-- ============================================================================
-- PART 3: Add validation constraint for future inserts
-- ============================================================================

-- Add check constraint to prevent inserting foods with incomplete nutrition
-- (Optional - may be too strict for some use cases)

-- DO $$
-- BEGIN
--     IF NOT EXISTS (
--         SELECT 1 FROM pg_constraint WHERE conname = 'check_nutrition_complete'
--     ) THEN
--         ALTER TABLE foods_enhanced
--         ADD CONSTRAINT check_nutrition_complete
--         CHECK (
--             -- If calories > 50, must have carbs AND fat
--             (calories IS NULL OR calories <= 50) OR
--             (total_carbs_g IS NOT NULL AND total_fat_g IS NOT NULL)
--         );
--     END IF;
-- END $$;

-- ============================================================================
-- PART 4: Create helper function to validate nutrition data
-- ============================================================================

CREATE OR REPLACE FUNCTION validate_nutrition_macros(
    p_calories FLOAT,
    p_protein_g FLOAT,
    p_carbs_g FLOAT,
    p_fat_g FLOAT
) RETURNS BOOLEAN AS $$
DECLARE
    protein_cal FLOAT;
    carb_cal FLOAT;
    fat_cal FLOAT;
    total_cal FLOAT;
    variance FLOAT;
BEGIN
    -- Calculate calories from macros
    protein_cal := COALESCE(p_protein_g, 0) * 4;
    carb_cal := COALESCE(p_carbs_g, 0) * 4;
    fat_cal := COALESCE(p_fat_g, 0) * 9;
    total_cal := protein_cal + carb_cal + fat_cal;

    -- Allow 25% variance (fiber, alcohol, rounding, water content)
    variance := ABS(total_cal - COALESCE(p_calories, 0));

    -- Return true if variance is within acceptable range
    RETURN variance <= (COALESCE(p_calories, 0) * 0.25);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION validate_nutrition_macros IS
'Validates that macro nutrients (protein, carbs, fat) reasonably add up to total calories. Allows 25% variance for fiber, alcohol, and rounding.';

-- ============================================================================
-- PART 5: Identify foods that need manual review
-- ============================================================================

-- Create view for admin to review low-quality foods
CREATE OR REPLACE VIEW foods_needing_review AS
SELECT
    id,
    name,
    brand_name,
    calories,
    protein_g,
    total_carbs_g,
    total_fat_g,
    dietary_fiber_g,
    data_quality_score,
    source,
    created_at,
    -- Calculate what's wrong
    CASE
        WHEN total_carbs_g IS NULL THEN 'Missing carbs'
        WHEN total_carbs_g = 0 AND calories > 50 THEN 'Zero carbs (suspicious)'
        ELSE NULL
    END as carbs_issue,
    CASE
        WHEN total_fat_g IS NULL THEN 'Missing fat'
        WHEN total_fat_g = 0 AND calories > 50 THEN 'Zero fat (suspicious)'
        ELSE NULL
    END as fat_issue,
    -- Macro math validation
    NOT validate_nutrition_macros(calories, protein_g, total_carbs_g, total_fat_g) as macros_dont_add_up
FROM foods_enhanced
WHERE
    data_quality_score IS NOT NULL
    AND data_quality_score < 0.5
ORDER BY data_quality_score ASC, created_at DESC;

COMMENT ON VIEW foods_needing_review IS
'Foods with low data quality that need manual review or AI recreation';

-- ============================================================================
-- PART 6: Verification queries
-- ============================================================================

-- After running migration, verify:

-- 1. How many foods were marked as low quality?
-- SELECT COUNT(*) FROM foods_enhanced WHERE data_quality_score = 0.2;

-- 2. Sample of low-quality foods
-- SELECT * FROM foods_needing_review LIMIT 10;

-- 3. Test validation function
-- SELECT
--     validate_nutrition_macros(200, 20, 10, 5) as valid_example,      -- Should be TRUE
--     validate_nutrition_macros(200, 0, 0, 0) as invalid_example;      -- Should be FALSE

-- ============================================================================
-- ROLLBACK (if needed)
-- ============================================================================

-- To restore data_quality_score for affected foods:
-- UPDATE foods_enhanced
-- SET data_quality_score = 0.8
-- WHERE data_quality_score = 0.2;

-- To drop validation function:
-- DROP FUNCTION IF EXISTS validate_nutrition_macros;
-- DROP VIEW IF EXISTS foods_needing_review;
