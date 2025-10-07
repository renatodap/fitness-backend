-- Migration 009: Clean up obsolete meal logging schema elements
-- Deprecates JSONB foods column in favor of relational meal_foods table
-- Removes unnecessary denormalization

-- ============================================================================
-- DEPRECATE (BUT DON'T DELETE) meal_logs.foods JSONB COLUMN
-- ============================================================================

-- Add comment marking column as deprecated
COMMENT ON COLUMN public.meal_logs.foods IS '
DEPRECATED: This JSONB column is replaced by the meal_foods table for proper relational structure.
Data has been migrated to meal_foods table in migration 007.
This column is kept for backward compatibility and will be removed in a future migration.
DO NOT USE THIS COLUMN in new code - use meal_foods table instead.
';

-- ============================================================================
-- ADD MISSING INDEXES FOR PERFORMANCE
-- ============================================================================

-- Index for querying meals by user and date range (most common query)
CREATE INDEX IF NOT EXISTS idx_meal_logs_user_logged_at
ON public.meal_logs(user_id, logged_at DESC);

-- Index for meal category filtering
CREATE INDEX IF NOT EXISTS idx_meal_logs_user_category
ON public.meal_logs(user_id, category);

-- Index for quick entry linkage
CREATE INDEX IF NOT EXISTS idx_meal_logs_quick_entry_log_id
ON public.meal_logs(quick_entry_log_id)
WHERE quick_entry_log_id IS NOT NULL;

-- Index for AI-extracted meals
CREATE INDEX IF NOT EXISTS idx_meal_logs_ai_extracted
ON public.meal_logs(user_id, ai_extracted)
WHERE ai_extracted = true;

-- Index for source filtering
CREATE INDEX IF NOT EXISTS idx_meal_logs_source
ON public.meal_logs(source);

-- ============================================================================
-- UPDATE meal_logs TABLE COMMENTS
-- ============================================================================

COMMENT ON TABLE public.meal_logs IS '
Main meal logging table. Stores meal metadata and totals.
Individual foods are stored in the meal_foods table (many-to-many relationship).
Total nutrition values are automatically calculated via triggers when meal_foods are added/updated/deleted.
';

COMMENT ON COLUMN public.meal_logs.total_calories IS 'Auto-calculated sum from meal_foods table via trigger';
COMMENT ON COLUMN public.meal_logs.total_protein_g IS 'Auto-calculated sum from meal_foods table via trigger';
COMMENT ON COLUMN public.meal_logs.total_carbs_g IS 'Auto-calculated sum from meal_foods table via trigger';
COMMENT ON COLUMN public.meal_logs.total_fat_g IS 'Auto-calculated sum from meal_foods table via trigger';
COMMENT ON COLUMN public.meal_logs.total_fiber_g IS 'Auto-calculated sum from meal_foods table via trigger';
COMMENT ON COLUMN public.meal_logs.total_sugar_g IS 'Auto-calculated sum from meal_foods table via trigger';
COMMENT ON COLUMN public.meal_logs.total_sodium_mg IS 'Auto-calculated sum from meal_foods table via trigger';

-- ============================================================================
-- CREATE HELPER FUNCTIONS
-- ============================================================================

-- Function to get meal with all foods (returns JSONB for API responses)
CREATE OR REPLACE FUNCTION get_meal_with_foods(meal_id uuid)
RETURNS JSONB AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT jsonb_build_object(
    'id', ml.id,
    'user_id', ml.user_id,
    'name', ml.name,
    'category', ml.category,
    'logged_at', ml.logged_at,
    'notes', ml.notes,
    'source', ml.source,
    'total_calories', ml.total_calories,
    'total_protein_g', ml.total_protein_g,
    'total_carbs_g', ml.total_carbs_g,
    'total_fat_g', ml.total_fat_g,
    'total_fiber_g', ml.total_fiber_g,
    'total_sugar_g', ml.total_sugar_g,
    'total_sodium_mg', ml.total_sodium_mg,
    'foods', (
      SELECT jsonb_agg(
        jsonb_build_object(
          'id', mf.id,
          'food_id', f.id,
          'name', f.name,
          'brand_name', f.brand_name,
          'quantity', mf.quantity,
          'unit', mf.unit,
          'serving_size', f.serving_size,
          'serving_unit', f.serving_unit,
          'calories', mf.calories,
          'protein_g', mf.protein_g,
          'carbs_g', mf.carbs_g,
          'fat_g', mf.fat_g,
          'fiber_g', mf.fiber_g,
          'sugar_g', mf.sugar_g,
          'sodium_mg', mf.sodium_mg
        )
      )
      FROM public.meal_foods mf
      JOIN public.foods_enhanced f ON mf.food_id = f.id
      WHERE mf.meal_log_id = ml.id
      ORDER BY mf.created_at
    ),
    'created_at', ml.created_at,
    'updated_at', ml.updated_at
  ) INTO result
  FROM public.meal_logs ml
  WHERE ml.id = meal_id;

  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_meal_with_foods IS 'Returns complete meal data with all foods as JSONB for API responses';

-- Function to calculate nutrition for a food quantity
CREATE OR REPLACE FUNCTION calculate_food_nutrition(
  p_food_id uuid,
  p_quantity numeric,
  p_unit text
)
RETURNS JSONB AS $$
DECLARE
  food_data RECORD;
  scale_factor numeric;
  result JSONB;
BEGIN
  -- Get food base nutrition
  SELECT
    calories, protein_g, total_carbs_g as carbs_g, total_fat_g as fat_g,
    dietary_fiber_g as fiber_g, total_sugars_g as sugar_g, sodium_mg,
    serving_size, serving_unit
  INTO food_data
  FROM public.foods_enhanced
  WHERE id = p_food_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Food not found: %', p_food_id;
  END IF;

  -- Calculate scale factor based on quantity and unit
  -- This is a simplified calculation - real implementation would handle unit conversions
  IF p_unit = 'serving' THEN
    scale_factor := p_quantity;
  ELSE
    -- For now, assume quantity is in same unit as serving_size
    scale_factor := p_quantity / food_data.serving_size;
  END IF;

  -- Build result
  result := jsonb_build_object(
    'calories', ROUND(food_data.calories * scale_factor, 1),
    'protein_g', ROUND(food_data.protein_g * scale_factor, 1),
    'carbs_g', ROUND(food_data.carbs_g * scale_factor, 1),
    'fat_g', ROUND(food_data.fat_g * scale_factor, 1),
    'fiber_g', ROUND(food_data.fiber_g * scale_factor, 1),
    'sugar_g', ROUND(food_data.sugar_g * scale_factor, 1),
    'sodium_mg', ROUND(food_data.sodium_mg * scale_factor, 1),
    'scale_factor', scale_factor
  );

  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION calculate_food_nutrition IS 'Calculates nutrition values for a specific food quantity and unit';

-- ============================================================================
-- UPDATE DAILY NUTRITION SUMMARIES CALCULATION
-- ============================================================================

-- Function to recalculate daily nutrition summaries from meal_logs
CREATE OR REPLACE FUNCTION update_daily_nutrition_summary(p_user_id uuid, p_date date)
RETURNS void AS $$
DECLARE
  summary RECORD;
BEGIN
  -- Calculate totals from meal_logs for the day
  SELECT
    COUNT(*) as meals_logged,
    SUM(CASE WHEN category = 'breakfast' THEN total_calories ELSE 0 END) as breakfast_calories,
    SUM(CASE WHEN category = 'lunch' THEN total_calories ELSE 0 END) as lunch_calories,
    SUM(CASE WHEN category = 'dinner' THEN total_calories ELSE 0 END) as dinner_calories,
    SUM(CASE WHEN category NOT IN ('breakfast', 'lunch', 'dinner') THEN total_calories ELSE 0 END) as snacks_calories,
    SUM(total_calories) as total_calories,
    SUM(total_protein_g) as total_protein_g,
    SUM(total_carbs_g) as total_carbs_g,
    SUM(total_fat_g) as total_fat_g,
    SUM(total_fiber_g) as total_fiber_g,
    SUM(total_sugar_g) as total_sugar_g,
    SUM(total_sodium_mg) as total_sodium_mg
  INTO summary
  FROM public.meal_logs
  WHERE user_id = p_user_id
  AND DATE(logged_at) = p_date;

  -- Upsert into daily_nutrition_summaries
  INSERT INTO public.daily_nutrition_summaries (
    user_id, date, meals_logged,
    breakfast_calories, lunch_calories, dinner_calories, snacks_calories,
    total_calories, total_protein_g, total_carbs_g, total_fat_g,
    total_fiber_g, total_sugar_g, total_sodium_mg
  ) VALUES (
    p_user_id, p_date, summary.meals_logged,
    summary.breakfast_calories, summary.lunch_calories, summary.dinner_calories, summary.snacks_calories,
    summary.total_calories, summary.total_protein_g, summary.total_carbs_g, summary.total_fat_g,
    summary.total_fiber_g, summary.total_sugar_g, summary.total_sodium_mg
  )
  ON CONFLICT (user_id, date) DO UPDATE SET
    meals_logged = EXCLUDED.meals_logged,
    breakfast_calories = EXCLUDED.breakfast_calories,
    lunch_calories = EXCLUDED.lunch_calories,
    dinner_calories = EXCLUDED.dinner_calories,
    snacks_calories = EXCLUDED.snacks_calories,
    total_calories = EXCLUDED.total_calories,
    total_protein_g = EXCLUDED.total_protein_g,
    total_carbs_g = EXCLUDED.total_carbs_g,
    total_fat_g = EXCLUDED.total_fat_g,
    total_fiber_g = EXCLUDED.total_fiber_g,
    total_sugar_g = EXCLUDED.total_sugar_g,
    total_sodium_mg = EXCLUDED.total_sodium_mg,
    updated_at = now();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION update_daily_nutrition_summary IS 'Recalculates and updates daily nutrition summary for a user and date';

-- Trigger to auto-update daily summaries when meals are logged/updated/deleted
CREATE OR REPLACE FUNCTION trigger_update_daily_summary()
RETURNS TRIGGER AS $$
BEGIN
  -- Update summary for affected date(s)
  IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
    PERFORM update_daily_nutrition_summary(NEW.user_id, DATE(NEW.logged_at));
  END IF;

  IF TG_OP = 'DELETE' THEN
    PERFORM update_daily_nutrition_summary(OLD.user_id, DATE(OLD.logged_at));
  END IF;

  -- If logged_at changed, update both old and new dates
  IF TG_OP = 'UPDATE' AND DATE(OLD.logged_at) != DATE(NEW.logged_at) THEN
    PERFORM update_daily_nutrition_summary(OLD.user_id, DATE(OLD.logged_at));
  END IF;

  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_meal_logs_update_daily_summary ON public.meal_logs;
CREATE TRIGGER trigger_meal_logs_update_daily_summary
  AFTER INSERT OR UPDATE OR DELETE ON public.meal_logs
  FOR EACH ROW
  EXECUTE FUNCTION trigger_update_daily_summary();

-- ============================================================================
-- ADD UNIQUE CONSTRAINTS/INDEXES WHERE MISSING
-- ============================================================================

-- Ensure user can't have duplicate active nutrition goals
-- Use partial unique index (not constraint) for conditional uniqueness
CREATE UNIQUE INDEX IF NOT EXISTS idx_nutrition_goals_user_active_unique
ON public.nutrition_goals (user_id)
WHERE (is_active = true);

COMMENT ON INDEX idx_nutrition_goals_user_active_unique IS
'Ensures each user can only have one active nutrition goal at a time';

-- Ensure daily_nutrition_summaries has unique constraint on user_id + date
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'daily_nutrition_summaries_user_date_unique'
  ) THEN
    ALTER TABLE public.daily_nutrition_summaries
    ADD CONSTRAINT daily_nutrition_summaries_user_date_unique
    UNIQUE (user_id, date);
  END IF;
END $$;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

DO $$
DECLARE
  meal_logs_count int;
  meal_foods_count int;
  foods_count int;
BEGIN
  SELECT COUNT(*) INTO meal_logs_count FROM public.meal_logs;
  SELECT COUNT(*) INTO meal_foods_count FROM public.meal_foods;
  SELECT COUNT(*) INTO foods_count FROM public.foods_enhanced;

  RAISE NOTICE 'Migration 009 complete!';
  RAISE NOTICE 'Total meal_logs: %', meal_logs_count;
  RAISE NOTICE 'Total meal_foods entries: %', meal_foods_count;
  RAISE NOTICE 'Total foods available: %', foods_count;
  RAISE NOTICE 'Schema cleanup and helper functions added';
END $$;
