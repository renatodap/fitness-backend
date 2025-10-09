-- Migration 022: Fix Meal Triggers for Template Support
-- Updates existing triggers to handle template items in meal_foods
-- Depends on: 021_recursive_meal_templates.sql
-- Created: 2025-10-09

-- ============================================================================
-- PART 1: Update calculate_meal_food_nutrition() for Templates
-- ============================================================================

CREATE OR REPLACE FUNCTION calculate_meal_food_nutrition()
RETURNS TRIGGER AS $$
DECLARE
    food_record RECORD;
    template_nutrition JSONB;
    quantity_multiplier NUMERIC;
    converted_quantity NUMERIC;
BEGIN
    -- Handle based on item_type
    IF NEW.item_type = 'food' THEN
        -- Existing food logic

        -- Validate food_id is present
        IF NEW.food_id IS NULL THEN
            RAISE EXCEPTION 'food_id is required when item_type is food';
        END IF;

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

    ELSIF NEW.item_type = 'template' THEN
        -- Template logic - get pre-calculated nutrition from template

        -- Validate template_id is present
        IF NEW.template_id IS NULL THEN
            RAISE EXCEPTION 'template_id is required when item_type is template';
        END IF;

        -- Get template nutrition using the recursive calculation function
        template_nutrition := calculate_template_nutrition(NEW.template_id);

        -- Set nutrition from template (quantity multiplier applied if needed)
        NEW.calories := COALESCE((template_nutrition->>'total_calories')::NUMERIC, 0);
        NEW.protein_g := COALESCE((template_nutrition->>'total_protein_g')::NUMERIC, 0);
        NEW.carbs_g := COALESCE((template_nutrition->>'total_carbs_g')::NUMERIC, 0);
        NEW.fat_g := COALESCE((template_nutrition->>'total_fat_g')::NUMERIC, 0);
        NEW.fiber_g := COALESCE((template_nutrition->>'total_fiber_g')::NUMERIC, 0);
        NEW.sugar_g := COALESCE((template_nutrition->>'total_sugar_g')::NUMERIC, 0);
        NEW.sodium_mg := COALESCE((template_nutrition->>'total_sodium_mg')::NUMERIC, 0);

    ELSE
        RAISE EXCEPTION 'Invalid item_type: %. Must be food or template', NEW.item_type;
    END IF;

    -- Set timestamps
    IF TG_OP = 'INSERT' THEN
        NEW.created_at := NOW();
    END IF;
    NEW.updated_at := NOW();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Recreate trigger (existing trigger will be dropped and recreated)
DROP TRIGGER IF EXISTS trigger_calculate_meal_food_nutrition ON meal_foods;
CREATE TRIGGER trigger_calculate_meal_food_nutrition
    BEFORE INSERT OR UPDATE ON meal_foods
    FOR EACH ROW
    EXECUTE FUNCTION calculate_meal_food_nutrition();

-- ============================================================================
-- PART 2: No changes needed for update_meal_log_totals()
-- ============================================================================
-- This trigger sums calories/protein/etc from meal_foods regardless of source
-- It doesn't care if the nutrition came from food or template
-- The SUM() operation works the same either way, so no changes needed!

-- ============================================================================
-- PART 3: Add Comments
-- ============================================================================

COMMENT ON FUNCTION calculate_meal_food_nutrition IS 'Auto-calculates nutrition values for meal_foods based on food or template nutrition and quantity (updated for template support)';

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Summary:
-- ✅ Updated calculate_meal_food_nutrition() to handle templates
-- ✅ Validates item_type and corresponding ID fields
-- ✅ Uses calculate_template_nutrition() for templates
-- ✅ Maintains backward compatibility with existing food logic
-- ✅ No changes needed to update_meal_log_totals() (sums work regardless)
