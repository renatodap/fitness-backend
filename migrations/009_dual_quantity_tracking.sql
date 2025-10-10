-- ============================================================
-- Migration 009: Dual Quantity Tracking for Meal Foods
-- ============================================================
-- Purpose: Add separate columns for serving and gram quantities
--          to enable accurate bidirectional quantity tracking
-- 
-- Problem Solved:
--   Current system stores only ONE quantity (either servings OR grams)
--   This causes data loss and broken math when users switch between units
--
-- Solution:
--   Store BOTH serving and gram quantities simultaneously
--   Always maintain perfect synchronization between the two
--   Use gram_quantity as source of truth for nutrition calculations
-- ============================================================

BEGIN;

-- Step 1: Add new columns
ALTER TABLE meal_foods 
ADD COLUMN IF NOT EXISTS serving_quantity NUMERIC(10,3),
ADD COLUMN IF NOT EXISTS serving_unit VARCHAR(50),
ADD COLUMN IF NOT EXISTS gram_quantity NUMERIC(10,3),
ADD COLUMN IF NOT EXISTS last_edited_field VARCHAR(20) DEFAULT 'grams'
    CHECK (last_edited_field IN ('serving', 'grams'));

-- Step 2: Create temporary function for data migration
CREATE OR REPLACE FUNCTION migrate_meal_food_quantities()
RETURNS void AS $$
DECLARE
    food_record RECORD;
    food_info RECORD;
    calculated_grams NUMERIC;
    calculated_servings NUMERIC;
    rows_processed INTEGER := 0;
    rows_failed INTEGER := 0;
BEGIN
    RAISE NOTICE 'Starting migration of meal_foods quantities...';
    
    FOR food_record IN 
        SELECT mf.id, mf.food_id, mf.quantity, mf.unit
        FROM meal_foods mf
        WHERE mf.gram_quantity IS NULL
    LOOP
        BEGIN
            rows_processed := rows_processed + 1;
            
            -- Get food serving info
            SELECT 
                serving_size, 
                household_serving_size, 
                household_serving_unit
            INTO food_info
            FROM foods_enhanced
            WHERE id = food_record.food_id;
            
            -- Skip if food not found
            IF NOT FOUND THEN
                RAISE WARNING 'Food not found for meal_food id %, food_id %', 
                    food_record.id, food_record.food_id;
                rows_failed := rows_failed + 1;
                CONTINUE;
            END IF;
            
            -- Calculate gram quantity based on current unit
            IF food_record.unit = 'g' THEN
                -- Already in grams
                calculated_grams := food_record.quantity;
                
                -- Calculate serving quantity from grams
                IF food_info.household_serving_size IS NOT NULL 
                   AND food_info.household_serving_size::numeric > 0 THEN
                    calculated_servings := calculated_grams / food_info.household_serving_size::numeric;
                ELSIF food_info.serving_size > 0 THEN
                    calculated_servings := calculated_grams / food_info.serving_size;
                ELSE
                    calculated_servings := calculated_grams / 100.0;
                END IF;
                
                UPDATE meal_foods
                SET gram_quantity = calculated_grams,
                    serving_quantity = calculated_servings,
                    serving_unit = food_info.household_serving_unit,
                    last_edited_field = 'grams'
                WHERE id = food_record.id;
                
            ELSIF food_record.unit = food_info.household_serving_unit THEN
                -- User logged in household servings (e.g., "2 slices")
                calculated_servings := food_record.quantity;
                
                IF food_info.household_serving_size IS NOT NULL 
                   AND food_info.household_serving_size::numeric > 0 THEN
                    calculated_grams := calculated_servings * food_info.household_serving_size::numeric;
                ELSE
                    calculated_grams := calculated_servings * COALESCE(food_info.serving_size, 100);
                END IF;
                
                UPDATE meal_foods
                SET gram_quantity = calculated_grams,
                    serving_quantity = calculated_servings,
                    serving_unit = food_info.household_serving_unit,
                    last_edited_field = 'serving'
                WHERE id = food_record.id;
                
            ELSE
                -- Generic "serving" or other unit
                calculated_servings := food_record.quantity;
                calculated_grams := calculated_servings * COALESCE(food_info.serving_size, 100);
                
                UPDATE meal_foods
                SET gram_quantity = calculated_grams,
                    serving_quantity = calculated_servings,
                    serving_unit = COALESCE(food_info.household_serving_unit, 'serving'),
                    last_edited_field = 'serving'
                WHERE id = food_record.id;
            END IF;
            
            -- Log progress every 100 rows
            IF rows_processed % 100 = 0 THEN
                RAISE NOTICE 'Processed % rows...', rows_processed;
            END IF;
            
        EXCEPTION WHEN OTHERS THEN
            RAISE WARNING 'Failed to migrate meal_food id %: %', food_record.id, SQLERRM;
            rows_failed := rows_failed + 1;
        END;
    END LOOP;
    
    RAISE NOTICE 'Migration complete: % rows processed, % failed', rows_processed, rows_failed;
END;
$$ LANGUAGE plpgsql;

-- Step 3: Run migration
SELECT migrate_meal_food_quantities();

-- Step 4: Verify migration
DO $$
DECLARE
    null_count INTEGER;
    total_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_count FROM meal_foods;
    
    SELECT COUNT(*) INTO null_count
    FROM meal_foods
    WHERE gram_quantity IS NULL;
    
    IF null_count > 0 THEN
        RAISE EXCEPTION 'Migration incomplete: % of % rows have NULL gram_quantity', 
            null_count, total_count;
    END IF;
    
    RAISE NOTICE 'Migration verified: All % meal_foods have quantity data', total_count;
END $$;

-- Step 5: Add NOT NULL constraints (after data is migrated)
ALTER TABLE meal_foods 
ALTER COLUMN gram_quantity SET NOT NULL,
ALTER COLUMN last_edited_field SET NOT NULL;

-- Step 6: Add indices for performance
CREATE INDEX IF NOT EXISTS idx_meal_foods_gram_quantity 
    ON meal_foods(gram_quantity);

CREATE INDEX IF NOT EXISTS idx_meal_foods_last_edited_field
    ON meal_foods(last_edited_field);

-- Step 7: Drop temporary function
DROP FUNCTION migrate_meal_food_quantities();

-- Step 8: Add helpful comments
COMMENT ON COLUMN meal_foods.serving_quantity IS 
    'Quantity in household serving units (e.g., 2.5 slices). Can be NULL for foods without household servings.';

COMMENT ON COLUMN meal_foods.serving_unit IS 
    'Household serving unit name (e.g., slice, medium, scoop) or NULL for generic servings';

COMMENT ON COLUMN meal_foods.gram_quantity IS 
    'Quantity in grams (always stored, used for all nutrition calculations). This is the source of truth.';

COMMENT ON COLUMN meal_foods.last_edited_field IS 
    'Tracks which field user last edited: "serving" or "grams". Used for UI hints.';

-- Step 9: Create a view for easy debugging
CREATE OR REPLACE VIEW meal_foods_quantity_debug AS
SELECT 
    mf.id,
    mf.meal_log_id,
    f.name AS food_name,
    f.household_serving_unit,
    f.household_serving_size,
    f.serving_size AS food_serving_size_g,
    mf.quantity AS old_quantity,
    mf.unit AS old_unit,
    mf.serving_quantity AS new_serving_quantity,
    mf.serving_unit AS new_serving_unit,
    mf.gram_quantity AS new_gram_quantity,
    mf.last_edited_field,
    mf.calories,
    mf.created_at
FROM meal_foods mf
JOIN foods_enhanced f ON f.id = mf.food_id
ORDER BY mf.created_at DESC;

COMMENT ON VIEW meal_foods_quantity_debug IS 
    'Debug view to compare old and new quantity columns. Use for verification after migration.';

COMMIT;

-- ============================================================
-- Post-Migration Verification Queries
-- ============================================================
-- Run these queries after migration to verify success:
--
-- 1. Check for NULL values:
--    SELECT COUNT(*) FROM meal_foods WHERE gram_quantity IS NULL;
--    Expected: 0
--
-- 2. Sample converted data:
--    SELECT * FROM meal_foods_quantity_debug LIMIT 20;
--
-- 3. Check conversion accuracy for specific foods:
--    SELECT * FROM meal_foods_quantity_debug 
--    WHERE food_name ILIKE '%bread%'
--    LIMIT 10;
--
-- 4. Verify totals match:
--    SELECT 
--      SUM(calories) as total_cal_old,
--      SUM(calories) as total_cal_new
--    FROM meal_foods;
--
-- ============================================================
