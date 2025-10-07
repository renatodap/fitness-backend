-- Migration: Fix meal nutrition calculations
-- Description: Add triggers to auto-calculate meal_foods nutrition and update meal_logs totals
-- Author: Claude Code
-- Date: 2025-10-07

-- ============================================================================
-- PART 1: Unit Conversion Function
-- ============================================================================

CREATE OR REPLACE FUNCTION convert_to_base_unit(
    quantity NUMERIC,
    from_unit TEXT,
    to_unit TEXT
) RETURNS NUMERIC AS $$
DECLARE
    converted_quantity NUMERIC;
BEGIN
    -- If units are the same, no conversion needed
    IF from_unit = to_unit THEN
        RETURN quantity;
    END IF;

    -- Convert from_unit to grams (base weight unit)
    CASE from_unit
        WHEN 'g' THEN converted_quantity := quantity;
        WHEN 'kg' THEN converted_quantity := quantity * 1000;
        WHEN 'mg' THEN converted_quantity := quantity / 1000;
        WHEN 'oz' THEN converted_quantity := quantity * 28.3495;
        WHEN 'lb' THEN converted_quantity := quantity * 453.592;
        -- Volume conversions (approximate - assume 1ml = 1g for liquids)
        WHEN 'ml' THEN converted_quantity := quantity;
        WHEN 'l' THEN converted_quantity := quantity * 1000;
        WHEN 'fl oz' THEN converted_quantity := quantity * 29.5735;
        WHEN 'cup' THEN converted_quantity := quantity * 240;
        WHEN 'tbsp' THEN converted_quantity := quantity * 15;
        WHEN 'tsp' THEN converted_quantity := quantity * 5;
        -- For serving/piece, use quantity as-is (no conversion)
        WHEN 'serving', 'piece', 'slice', 'item' THEN converted_quantity := quantity;
        ELSE converted_quantity := quantity; -- Default: no conversion
    END CASE;

    -- Convert from grams to target unit
    CASE to_unit
        WHEN 'g' THEN RETURN converted_quantity;
        WHEN 'kg' THEN RETURN converted_quantity / 1000;
        WHEN 'mg' THEN RETURN converted_quantity * 1000;
        WHEN 'oz' THEN RETURN converted_quantity / 28.3495;
        WHEN 'lb' THEN RETURN converted_quantity / 453.592;
        WHEN 'ml' THEN RETURN converted_quantity;
        WHEN 'l' THEN RETURN converted_quantity / 1000;
        WHEN 'fl oz' THEN RETURN converted_quantity / 29.5735;
        WHEN 'cup' THEN RETURN converted_quantity / 240;
        WHEN 'tbsp' THEN RETURN converted_quantity / 15;
        WHEN 'tsp' THEN RETURN converted_quantity / 5;
        WHEN 'serving', 'piece', 'slice', 'item' THEN RETURN converted_quantity;
        ELSE RETURN converted_quantity;
    END CASE;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ============================================================================
-- PART 2: Auto-calculate meal_foods nutrition trigger
-- ============================================================================

CREATE OR REPLACE FUNCTION calculate_meal_food_nutrition()
RETURNS TRIGGER AS $$
DECLARE
    food_record RECORD;
    quantity_multiplier NUMERIC;
    converted_quantity NUMERIC;
BEGIN
    -- Fetch the food details
    SELECT * INTO food_record
    FROM foods_enhanced
    WHERE id = NEW.food_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Food with id % not found', NEW.food_id;
    END IF;

    -- Convert user quantity to food's serving unit
    converted_quantity := convert_to_base_unit(
        NEW.quantity,
        NEW.unit,
        food_record.serving_unit
    );

    -- Calculate multiplier: (user_quantity / serving_size)
    -- Example: User wants 50g, food serving is 100g -> multiplier = 0.5
    IF food_record.serving_size > 0 THEN
        quantity_multiplier := converted_quantity / food_record.serving_size;
    ELSE
        quantity_multiplier := 1; -- Fallback
    END IF;

    -- Calculate nutrition values based on multiplier
    NEW.calories := COALESCE(food_record.calories * quantity_multiplier, 0);
    NEW.protein_g := COALESCE(food_record.protein_g * quantity_multiplier, 0);
    NEW.carbs_g := COALESCE(food_record.total_carbs_g * quantity_multiplier, 0);
    NEW.fat_g := COALESCE(food_record.total_fat_g * quantity_multiplier, 0);
    NEW.fiber_g := COALESCE(food_record.dietary_fiber_g * quantity_multiplier, 0);
    NEW.sugar_g := COALESCE(food_record.total_sugars_g * quantity_multiplier, 0);
    NEW.sodium_mg := COALESCE(food_record.sodium_mg * quantity_multiplier, 0);

    -- Set timestamps
    IF TG_OP = 'INSERT' THEN
        NEW.created_at := NOW();
    END IF;
    NEW.updated_at := NOW();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if exists
DROP TRIGGER IF EXISTS trigger_calculate_meal_food_nutrition ON meal_foods;

-- Create trigger to run BEFORE INSERT or UPDATE
CREATE TRIGGER trigger_calculate_meal_food_nutrition
    BEFORE INSERT OR UPDATE ON meal_foods
    FOR EACH ROW
    EXECUTE FUNCTION calculate_meal_food_nutrition();

-- ============================================================================
-- PART 3: Auto-update meal_logs totals trigger
-- ============================================================================

CREATE OR REPLACE FUNCTION update_meal_log_totals()
RETURNS TRIGGER AS $$
DECLARE
    meal_log_id_to_update UUID;
BEGIN
    -- Determine which meal_log to update
    IF TG_OP = 'DELETE' THEN
        meal_log_id_to_update := OLD.meal_log_id;
    ELSE
        meal_log_id_to_update := NEW.meal_log_id;
    END IF;

    -- Recalculate totals for the meal_log
    UPDATE meal_logs
    SET
        total_calories = COALESCE((
            SELECT SUM(calories)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        total_protein_g = COALESCE((
            SELECT SUM(protein_g)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        total_carbs_g = COALESCE((
            SELECT SUM(carbs_g)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        total_fat_g = COALESCE((
            SELECT SUM(fat_g)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        total_fiber_g = COALESCE((
            SELECT SUM(fiber_g)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        total_sugar_g = COALESCE((
            SELECT SUM(sugar_g)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        total_sodium_mg = COALESCE((
            SELECT SUM(sodium_mg)
            FROM meal_foods
            WHERE meal_log_id = meal_log_id_to_update
        ), 0),
        updated_at = NOW()
    WHERE id = meal_log_id_to_update;

    RETURN NULL; -- For AFTER trigger
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if exists
DROP TRIGGER IF EXISTS trigger_update_meal_log_totals ON meal_foods;

-- Create trigger to run AFTER INSERT, UPDATE, or DELETE
CREATE TRIGGER trigger_update_meal_log_totals
    AFTER INSERT OR UPDATE OR DELETE ON meal_foods
    FOR EACH ROW
    EXECUTE FUNCTION update_meal_log_totals();

-- ============================================================================
-- PART 4: Recalculate existing meal_foods (data migration)
-- ============================================================================

-- Recalculate all existing meal_foods nutrition values
-- This will trigger the calculate_meal_food_nutrition function
UPDATE meal_foods
SET updated_at = NOW()
WHERE id IN (
    SELECT id FROM meal_foods LIMIT 10000 -- Process in batches if needed
);

-- ============================================================================
-- PART 5: Add helpful comments
-- ============================================================================

COMMENT ON FUNCTION convert_to_base_unit IS 'Converts quantities between different units (g, kg, oz, lb, ml, cup, etc.)';
COMMENT ON FUNCTION calculate_meal_food_nutrition IS 'Auto-calculates nutrition values for meal_foods based on food nutrition and quantity';
COMMENT ON FUNCTION update_meal_log_totals IS 'Auto-updates meal_logs total nutrition when meal_foods change';
COMMENT ON TRIGGER trigger_calculate_meal_food_nutrition ON meal_foods IS 'Triggers before insert/update to calculate nutrition';
COMMENT ON TRIGGER trigger_update_meal_log_totals ON meal_foods IS 'Triggers after insert/update/delete to update meal totals';

-- ============================================================================
-- ROLLBACK (commented out - uncomment to rollback)
-- ============================================================================

-- DROP TRIGGER IF EXISTS trigger_update_meal_log_totals ON meal_foods;
-- DROP TRIGGER IF EXISTS trigger_calculate_meal_food_nutrition ON meal_foods;
-- DROP FUNCTION IF EXISTS update_meal_log_totals();
-- DROP FUNCTION IF EXISTS calculate_meal_food_nutrition();
-- DROP FUNCTION IF EXISTS convert_to_base_unit(NUMERIC, TEXT, TEXT);
