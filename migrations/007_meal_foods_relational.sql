-- Migration 007: Create proper relational meal-food tracking
-- Replaces JSONB foods array with proper many-to-many relationship
-- Follows best practices for meal tracking applications

-- ============================================================================
-- CREATE MEAL_FOODS JOIN TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.meal_foods (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign keys
  meal_log_id uuid NOT NULL REFERENCES public.meal_logs(id) ON DELETE CASCADE,
  food_id uuid NOT NULL REFERENCES public.foods_enhanced(id) ON DELETE RESTRICT,

  -- Quantity information
  quantity numeric NOT NULL CHECK (quantity > 0),
  unit text NOT NULL CHECK (unit IN (
    'g', 'kg', 'mg',                          -- Weight
    'ml', 'l',                                 -- Volume
    'oz', 'lb',                                -- Imperial weight
    'cup', 'tbsp', 'tsp',                      -- Cooking measures
    'serving', 'piece', 'slice', 'item',       -- Portions
    'fl oz', 'pt', 'qt', 'gal'                 -- Imperial volume
  )),

  -- Cached nutrition values (calculated at insert time from food_id)
  -- Allows efficient aggregation without joins
  calories numeric DEFAULT 0 CHECK (calories >= 0),
  protein_g numeric DEFAULT 0 CHECK (protein_g >= 0),
  carbs_g numeric DEFAULT 0 CHECK (carbs_g >= 0),
  fat_g numeric DEFAULT 0 CHECK (fat_g >= 0),
  fiber_g numeric DEFAULT 0 CHECK (fiber_g >= 0),
  sugar_g numeric DEFAULT 0 CHECK (sugar_g >= 0),
  sodium_mg numeric DEFAULT 0 CHECK (sodium_mg >= 0),

  -- Optional metadata
  notes text CHECK (char_length(notes) <= 500),

  -- Timestamps
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),

  -- Constraints
  CONSTRAINT meal_foods_unique_meal_food UNIQUE(meal_log_id, food_id)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Index for querying foods in a specific meal
CREATE INDEX idx_meal_foods_meal_log_id ON public.meal_foods(meal_log_id);

-- Index for finding all meals containing a specific food
CREATE INDEX idx_meal_foods_food_id ON public.meal_foods(food_id);

-- Composite index for efficient joins
CREATE INDEX idx_meal_foods_meal_food ON public.meal_foods(meal_log_id, food_id);

-- Index for timestamp-based queries
CREATE INDEX idx_meal_foods_created_at ON public.meal_foods(created_at DESC);

-- ============================================================================
-- ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE public.meal_foods ENABLE ROW LEVEL SECURITY;

-- Users can only see their own meal foods (via meal_logs.user_id)
CREATE POLICY "Users can view own meal foods"
ON public.meal_foods
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM public.meal_logs
    WHERE meal_logs.id = meal_foods.meal_log_id
    AND meal_logs.user_id = auth.uid()
  )
);

-- Users can insert meal foods for their own meals
CREATE POLICY "Users can insert own meal foods"
ON public.meal_foods
FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM public.meal_logs
    WHERE meal_logs.id = meal_foods.meal_log_id
    AND meal_logs.user_id = auth.uid()
  )
);

-- Users can update their own meal foods
CREATE POLICY "Users can update own meal foods"
ON public.meal_foods
FOR UPDATE
USING (
  EXISTS (
    SELECT 1 FROM public.meal_logs
    WHERE meal_logs.id = meal_foods.meal_log_id
    AND meal_logs.user_id = auth.uid()
  )
);

-- Users can delete their own meal foods
CREATE POLICY "Users can delete own meal foods"
ON public.meal_foods
FOR DELETE
USING (
  EXISTS (
    SELECT 1 FROM public.meal_logs
    WHERE meal_logs.id = meal_foods.meal_log_id
    AND meal_logs.user_id = auth.uid()
  )
);

-- ============================================================================
-- TRIGGER: AUTO-UPDATE TIMESTAMPS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_meal_foods_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_meal_foods_updated_at
  BEFORE UPDATE ON public.meal_foods
  FOR EACH ROW
  EXECUTE FUNCTION update_meal_foods_updated_at();

-- ============================================================================
-- TRIGGER: AUTO-UPDATE MEAL_LOGS TOTALS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_meal_log_totals()
RETURNS TRIGGER AS $$
BEGIN
  -- Recalculate totals for the affected meal_log
  UPDATE public.meal_logs
  SET
    total_calories = COALESCE((
      SELECT SUM(calories) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    total_protein_g = COALESCE((
      SELECT SUM(protein_g) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    total_carbs_g = COALESCE((
      SELECT SUM(carbs_g) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    total_fat_g = COALESCE((
      SELECT SUM(fat_g) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    total_fiber_g = COALESCE((
      SELECT SUM(fiber_g) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    total_sugar_g = COALESCE((
      SELECT SUM(sugar_g) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    total_sodium_mg = COALESCE((
      SELECT SUM(sodium_mg) FROM public.meal_foods
      WHERE meal_log_id = COALESCE(NEW.meal_log_id, OLD.meal_log_id)
    ), 0),
    updated_at = now()
  WHERE id = COALESCE(NEW.meal_log_id, OLD.meal_log_id);

  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_meal_foods_insert_update_totals
  AFTER INSERT ON public.meal_foods
  FOR EACH ROW
  EXECUTE FUNCTION update_meal_log_totals();

CREATE TRIGGER trigger_meal_foods_update_totals
  AFTER UPDATE ON public.meal_foods
  FOR EACH ROW
  EXECUTE FUNCTION update_meal_log_totals();

CREATE TRIGGER trigger_meal_foods_delete_update_totals
  AFTER DELETE ON public.meal_foods
  FOR EACH ROW
  EXECUTE FUNCTION update_meal_log_totals();

-- ============================================================================
-- MIGRATE EXISTING DATA FROM JSONB TO RELATIONAL
-- ============================================================================

-- This migration moves data from meal_logs.foods (JSONB array) to meal_foods table
-- Handles both old format (simple strings) and new format (objects with nutrition)

DO $$
DECLARE
  meal_record RECORD;
  food_item JSONB;
  food_obj RECORD;
  calculated_calories numeric;
  calculated_protein numeric;
  calculated_carbs numeric;
  calculated_fat numeric;
  calculated_fiber numeric;
BEGIN
  -- Iterate through all meal_logs with foods data
  FOR meal_record IN
    SELECT id, user_id, foods
    FROM public.meal_logs
    WHERE foods IS NOT NULL
    AND jsonb_array_length(foods) > 0
  LOOP
    -- Iterate through each food in the JSONB array
    FOR food_item IN
      SELECT * FROM jsonb_array_elements(meal_record.foods)
    LOOP
      BEGIN
        -- Check if food_item has nutrition data (new format)
        IF food_item ? 'food_id' AND food_item ? 'calories' THEN
          -- New format with full nutrition data
          INSERT INTO public.meal_foods (
            meal_log_id,
            food_id,
            quantity,
            unit,
            calories,
            protein_g,
            carbs_g,
            fat_g,
            fiber_g,
            sugar_g,
            sodium_mg
          ) VALUES (
            meal_record.id,
            (food_item->>'food_id')::uuid,
            COALESCE((food_item->>'quantity')::numeric, 1),
            COALESCE(food_item->>'unit', 'serving'),
            COALESCE((food_item->>'calories')::numeric, 0),
            COALESCE((food_item->>'protein_g')::numeric, 0),
            COALESCE((food_item->>'carbs_g')::numeric, 0),
            COALESCE((food_item->>'fat_g')::numeric, 0),
            COALESCE((food_item->>'fiber_g')::numeric, 0),
            COALESCE((food_item->>'sugar_g')::numeric, 0),
            COALESCE((food_item->>'sodium_mg')::numeric, 0)
          )
          ON CONFLICT (meal_log_id, food_id) DO NOTHING;

        ELSIF food_item ? 'name' THEN
          -- Old format or partial format - try to match by name
          SELECT id, calories, protein_g, carbs_g, fat_g, fiber_g, total_sugars_g, sodium_mg
          INTO food_obj
          FROM public.foods_enhanced
          WHERE LOWER(name) = LOWER(food_item->>'name')
          LIMIT 1;

          IF FOUND THEN
            -- Calculate nutrition based on quantity
            calculated_calories := food_obj.calories * COALESCE((food_item->>'quantity')::numeric, 1);
            calculated_protein := food_obj.protein_g * COALESCE((food_item->>'quantity')::numeric, 1);
            calculated_carbs := food_obj.carbs_g * COALESCE((food_item->>'quantity')::numeric, 1);
            calculated_fat := food_obj.fat_g * COALESCE((food_item->>'quantity')::numeric, 1);
            calculated_fiber := food_obj.fiber_g * COALESCE((food_item->>'quantity')::numeric, 1);

            INSERT INTO public.meal_foods (
              meal_log_id,
              food_id,
              quantity,
              unit,
              calories,
              protein_g,
              carbs_g,
              fat_g,
              fiber_g,
              sugar_g,
              sodium_mg,
              notes
            ) VALUES (
              meal_record.id,
              food_obj.id,
              COALESCE((food_item->>'quantity')::numeric, 1),
              COALESCE(food_item->>'unit', 'serving'),
              calculated_calories,
              calculated_protein,
              calculated_carbs,
              calculated_fat,
              calculated_fiber,
              COALESCE(food_obj.total_sugars_g * COALESCE((food_item->>'quantity')::numeric, 1), 0),
              COALESCE(food_obj.sodium_mg * COALESCE((food_item->>'quantity')::numeric, 1), 0),
              'Migrated from JSONB'
            )
            ON CONFLICT (meal_log_id, food_id) DO NOTHING;
          END IF;
        END IF;
      EXCEPTION WHEN OTHERS THEN
        -- Log error but continue with next food
        RAISE NOTICE 'Error migrating food for meal %: %', meal_record.id, SQLERRM;
      END;
    END LOOP;
  END LOOP;

  RAISE NOTICE 'Migration completed. Check meal_foods table for results.';
END $$;

-- ============================================================================
-- HELPER VIEWS
-- ============================================================================

-- View to get meal details with all foods
CREATE OR REPLACE VIEW meal_details AS
SELECT
  ml.id as meal_id,
  ml.user_id,
  ml.name as meal_name,
  ml.category,
  ml.logged_at,
  ml.notes as meal_notes,
  ml.total_calories,
  ml.total_protein_g,
  ml.total_carbs_g,
  ml.total_fat_g,
  ml.total_fiber_g,
  mf.id as meal_food_id,
  mf.quantity,
  mf.unit,
  f.id as food_id,
  f.name as food_name,
  f.brand_name,
  mf.calories,
  mf.protein_g,
  mf.carbs_g,
  mf.fat_g,
  mf.fiber_g,
  mf.sugar_g,
  mf.sodium_mg
FROM public.meal_logs ml
LEFT JOIN public.meal_foods mf ON ml.id = mf.meal_log_id
LEFT JOIN public.foods_enhanced f ON mf.food_id = f.id
ORDER BY ml.logged_at DESC, mf.created_at ASC;

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE public.meal_foods IS 'Many-to-many join table linking meals to foods with quantities. Replaces JSONB foods array in meal_logs for proper relational structure.';
COMMENT ON COLUMN public.meal_foods.meal_log_id IS 'Foreign key to meal_logs table';
COMMENT ON COLUMN public.meal_foods.food_id IS 'Foreign key to foods_enhanced table';
COMMENT ON COLUMN public.meal_foods.quantity IS 'Amount of food consumed (e.g., 2 for "2 cups")';
COMMENT ON COLUMN public.meal_foods.unit IS 'Unit of measurement (g, oz, cup, serving, etc.)';
COMMENT ON COLUMN public.meal_foods.calories IS 'Cached calories for this specific meal_food entry (calculated from food + quantity)';
COMMENT ON COLUMN public.meal_foods.protein_g IS 'Cached protein for this specific meal_food entry';
COMMENT ON COLUMN public.meal_foods.carbs_g IS 'Cached carbs for this specific meal_food entry';
COMMENT ON COLUMN public.meal_foods.fat_g IS 'Cached fat for this specific meal_food entry';

-- ============================================================================
-- COMPLETE
-- ============================================================================

-- Verify migration
DO $$
DECLARE
  meal_foods_count int;
  meal_logs_count int;
BEGIN
  SELECT COUNT(*) INTO meal_foods_count FROM public.meal_foods;
  SELECT COUNT(*) INTO meal_logs_count FROM public.meal_logs WHERE foods IS NOT NULL;

  RAISE NOTICE 'Migration 007 complete!';
  RAISE NOTICE 'Total meal_foods entries: %', meal_foods_count;
  RAISE NOTICE 'Total meal_logs with foods: %', meal_logs_count;
END $$;
