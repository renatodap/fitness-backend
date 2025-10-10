-- Migration: 001_meal_logging_improvements
-- Description: Improvements to meal logging system
--   - Add food_servings table for better portion defaults
--   - Remove template_id from meal_foods (always expand templates)
--   - Add performance indexes
--   - Add functions for template expansion
--   - Add triggers for automatic calculations
-- Date: 2025-10-09
-- Author: Claude Code

-- ============================================================================
-- PART 1: SCHEMA CHANGES
-- ============================================================================

-- 1.1 Create food_servings table for better portion defaults
-- This allows foods to have multiple common serving sizes
CREATE TABLE IF NOT EXISTS food_servings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  food_id uuid NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
  serving_name text NOT NULL,  -- "1 cup", "1 scoop", "1 medium apple", "1 slice"
  serving_size_g numeric NOT NULL CHECK (serving_size_g > 0),  -- Grams equivalent
  is_default boolean DEFAULT false,  -- Most common serving for this food
  is_household_standard boolean DEFAULT true,  -- vs metric/imperial (cups vs grams)
  popularity_score integer DEFAULT 0,  -- Track how often this serving is used
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  CONSTRAINT unique_food_serving_name UNIQUE(food_id, serving_name)
);

COMMENT ON TABLE food_servings IS 'Multiple serving size options for each food, e.g., "1 cup (240g)", "1 scoop (30g)"';
COMMENT ON COLUMN food_servings.serving_name IS 'User-friendly serving name like "1 cup", "1 scoop", "1 medium"';
COMMENT ON COLUMN food_servings.serving_size_g IS 'Serving size converted to grams for normalization';
COMMENT ON COLUMN food_servings.is_default IS 'The most common/recommended serving size for this food';
COMMENT ON COLUMN food_servings.popularity_score IS 'Incremented each time this serving is used';

-- 1.2 Remove template_id and item_type from meal_foods (always expand templates)
-- This simplifies the data model - templates are always expanded into foods when logging
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'meal_foods' AND column_name = 'template_id'
  ) THEN
    ALTER TABLE meal_foods DROP COLUMN IF EXISTS template_id;
  END IF;

  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'meal_foods' AND column_name = 'item_type'
  ) THEN
    ALTER TABLE meal_foods DROP COLUMN IF EXISTS item_type;
  END IF;
END $$;

COMMENT ON TABLE meal_foods IS 'Individual foods in a meal log (templates are expanded)';

-- ============================================================================
-- PART 2: INDEXES FOR PERFORMANCE
-- ============================================================================

-- 2.1 Critical indexes for food search (GIN for full-text search)
CREATE INDEX IF NOT EXISTS idx_foods_enhanced_search_vector
  ON foods_enhanced USING gin(search_vector);

COMMENT ON INDEX idx_foods_enhanced_search_vector IS 'Full-text search index for food names';

-- 2.2 Indexes for meal_foods (foreign key lookups)
CREATE INDEX IF NOT EXISTS idx_meal_foods_meal_log_id
  ON meal_foods(meal_log_id);

CREATE INDEX IF NOT EXISTS idx_meal_foods_food_id
  ON meal_foods(food_id);

COMMENT ON INDEX idx_meal_foods_meal_log_id IS 'Fast lookup of foods in a meal';
COMMENT ON INDEX idx_meal_foods_food_id IS 'Fast lookup of meals containing a specific food';

-- 2.3 Indexes for meal_template_foods (template expansion)
CREATE INDEX IF NOT EXISTS idx_meal_template_foods_template_id
  ON meal_template_foods(meal_template_id);

CREATE INDEX IF NOT EXISTS idx_meal_template_foods_food_id
  ON meal_template_foods(food_id);

CREATE INDEX IF NOT EXISTS idx_meal_template_foods_child_template_id
  ON meal_template_foods(child_template_id)
  WHERE child_template_id IS NOT NULL;

COMMENT ON INDEX idx_meal_template_foods_template_id IS 'Fast lookup of foods in a template';
COMMENT ON INDEX idx_meal_template_foods_child_template_id IS 'Fast lookup of nested templates';

-- 2.4 Indexes for food_servings
CREATE INDEX IF NOT EXISTS idx_food_servings_food_id
  ON food_servings(food_id);

CREATE INDEX IF NOT EXISTS idx_food_servings_default
  ON food_servings(food_id)
  WHERE is_default = true;

COMMENT ON INDEX idx_food_servings_food_id IS 'Fast lookup of serving sizes for a food';
COMMENT ON INDEX idx_food_servings_default IS 'Fast lookup of default serving for a food';

-- 2.5 Indexes for meal_templates
CREATE INDEX IF NOT EXISTS idx_meal_templates_user_id
  ON meal_templates(user_id);

CREATE INDEX IF NOT EXISTS idx_meal_templates_user_id_favorite
  ON meal_templates(user_id)
  WHERE is_favorite = true;

COMMENT ON INDEX idx_meal_templates_user_id_favorite IS 'Fast lookup of user favorite templates';

-- ============================================================================
-- PART 3: FUNCTIONS FOR TEMPLATE EXPANSION
-- ============================================================================

-- 3.1 Function to expand meal templates recursively
-- This function takes a template_id and returns all foods (with quantities)
-- including foods from nested templates
CREATE OR REPLACE FUNCTION expand_meal_template(template_id_param uuid)
RETURNS TABLE (
  food_id uuid,
  quantity numeric,
  unit text
) AS $$
BEGIN
  RETURN QUERY
  WITH RECURSIVE expanded_foods AS (
    -- Base case: direct foods in template
    SELECT
      mtf.food_id,
      mtf.quantity,
      mtf.unit,
      mtf.child_template_id,
      0 as depth
    FROM meal_template_foods mtf
    WHERE mtf.meal_template_id = template_id_param

    UNION ALL

    -- Recursive case: foods from nested templates
    SELECT
      mtf2.food_id,
      mtf2.quantity * ef.quantity as quantity,  -- Multiply quantities (e.g., 2x template with 3x food = 6x food)
      mtf2.unit,
      mtf2.child_template_id,
      ef.depth + 1
    FROM expanded_foods ef
    INNER JOIN meal_template_foods mtf2
      ON mtf2.meal_template_id = ef.child_template_id
    WHERE ef.child_template_id IS NOT NULL
      AND ef.depth < 10  -- Prevent infinite recursion (max 10 levels deep)
  )
  SELECT
    ef.food_id,
    SUM(ef.quantity) as quantity,  -- Combine quantities if same food appears multiple times
    ef.unit
  FROM expanded_foods ef
  WHERE ef.food_id IS NOT NULL
  GROUP BY ef.food_id, ef.unit;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION expand_meal_template IS 'Recursively expand a meal template into individual foods with quantities';

-- Example usage:
-- SELECT * FROM expand_meal_template('template-uuid-here');
-- Returns: [(food_id_1, 100, 'g'), (food_id_2, 2, 'serving'), ...]

-- 3.2 Function to get default serving for a food
CREATE OR REPLACE FUNCTION get_default_serving(food_id_param uuid)
RETURNS TABLE (
  serving_name text,
  serving_size_g numeric,
  quantity numeric,
  unit text
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    fs.serving_name,
    fs.serving_size_g,
    -- Return quantity = 1 and unit from serving_name (e.g., "1 cup" -> unit="cup", qty=1)
    1.0::numeric as quantity,
    CASE
      WHEN fs.serving_name ~ '^\d+(\.\d+)?\s+(\w+)' THEN
        -- Extract unit from "1 cup" -> "cup", "2.5 oz" -> "oz"
        regexp_replace(fs.serving_name, '^\d+(\.\d+)?\s+', '')
      ELSE
        'serving'
    END as unit
  FROM food_servings fs
  WHERE fs.food_id = food_id_param
    AND fs.is_default = true
  LIMIT 1;

  -- If no default serving found, fall back to food's base serving_size
  IF NOT FOUND THEN
    RETURN QUERY
    SELECT
      f.household_serving_size || ' ' || COALESCE(f.household_serving_unit, f.serving_unit) as serving_name,
      f.serving_size as serving_size_g,
      f.serving_size as quantity,
      COALESCE(f.household_serving_unit, f.serving_unit) as unit
    FROM foods_enhanced f
    WHERE f.id = food_id_param
    LIMIT 1;
  END IF;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_default_serving IS 'Get the default serving size for a food (used for initial portion when adding food)';

-- Example usage:
-- SELECT * FROM get_default_serving('food-uuid-here');
-- Returns: ('1 cup', 240, 1, 'cup') or ('100g', 100, 100, 'g')

-- ============================================================================
-- PART 4: TRIGGERS FOR AUTOMATIC CALCULATIONS
-- ============================================================================

-- 4.1 Trigger to auto-populate food_servings from household_serving_size
CREATE OR REPLACE FUNCTION populate_food_servings()
RETURNS TRIGGER AS $$
BEGIN
  -- If household_serving_size exists, create a food_serving entry
  IF NEW.household_serving_size IS NOT NULL AND NEW.household_serving_size != '' THEN
    INSERT INTO food_servings (
      food_id,
      serving_name,
      serving_size_g,
      is_default,
      is_household_standard
    )
    VALUES (
      NEW.id,
      NEW.household_serving_size || ' ' || COALESCE(NEW.household_serving_unit, ''),
      NEW.serving_size,  -- Assume household_serving_size is already in base units
      true,  -- Make it the default
      true   -- It's a household standard (vs metric)
    )
    ON CONFLICT (food_id, serving_name)
    DO UPDATE SET
      serving_size_g = EXCLUDED.serving_size_g,
      is_default = EXCLUDED.is_default,
      updated_at = now();
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER auto_populate_food_servings
AFTER INSERT OR UPDATE OF household_serving_size, household_serving_unit
ON foods_enhanced
FOR EACH ROW
EXECUTE FUNCTION populate_food_servings();

COMMENT ON FUNCTION populate_food_servings IS 'Automatically create food_serving entry when food has household_serving_size';

-- 4.2 Trigger to recalculate parent template totals when child templates change
CREATE OR REPLACE FUNCTION recalculate_parent_template_totals()
RETURNS TRIGGER AS $$
BEGIN
  -- Recalculate totals for all parent templates that contain this template
  UPDATE meal_templates
  SET
    total_calories = COALESCE((
      SELECT SUM(
        CASE
          WHEN mtf.item_type = 'food' THEN
            -- Food: calories from foods_enhanced
            (f.calories * mtf.quantity)
          WHEN mtf.item_type = 'template' THEN
            -- Template: use pre-calculated total_calories
            child.total_calories
        END
      )
      FROM meal_template_foods mtf
      LEFT JOIN foods_enhanced f ON f.id = mtf.food_id
      LEFT JOIN meal_templates child ON child.id = mtf.child_template_id
      WHERE mtf.meal_template_id = meal_templates.id
    ), 0),

    total_protein_g = COALESCE((
      SELECT SUM(
        CASE
          WHEN mtf.item_type = 'food' THEN (f.protein_g * mtf.quantity)
          WHEN mtf.item_type = 'template' THEN child.total_protein_g
        END
      )
      FROM meal_template_foods mtf
      LEFT JOIN foods_enhanced f ON f.id = mtf.food_id
      LEFT JOIN meal_templates child ON child.id = mtf.child_template_id
      WHERE mtf.meal_template_id = meal_templates.id
    ), 0),

    total_carbs_g = COALESCE((
      SELECT SUM(
        CASE
          WHEN mtf.item_type = 'food' THEN (f.total_carbs_g * mtf.quantity)
          WHEN mtf.item_type = 'template' THEN child.total_carbs_g
        END
      )
      FROM meal_template_foods mtf
      LEFT JOIN foods_enhanced f ON f.id = mtf.food_id
      LEFT JOIN meal_templates child ON child.id = mtf.child_template_id
      WHERE mtf.meal_template_id = meal_templates.id
    ), 0),

    total_fat_g = COALESCE((
      SELECT SUM(
        CASE
          WHEN mtf.item_type = 'food' THEN (f.total_fat_g * mtf.quantity)
          WHEN mtf.item_type = 'template' THEN child.total_fat_g
        END
      )
      FROM meal_template_foods mtf
      LEFT JOIN foods_enhanced f ON f.id = mtf.food_id
      LEFT JOIN meal_templates child ON child.id = mtf.child_template_id
      WHERE mtf.meal_template_id = meal_templates.id
    ), 0),

    total_fiber_g = COALESCE((
      SELECT SUM(
        CASE
          WHEN mtf.item_type = 'food' THEN (f.dietary_fiber_g * mtf.quantity)
          WHEN mtf.item_type = 'template' THEN child.total_fiber_g
        END
      )
      FROM meal_template_foods mtf
      LEFT JOIN foods_enhanced f ON f.id = mtf.food_id
      LEFT JOIN meal_templates child ON child.id = mtf.child_template_id
      WHERE mtf.meal_template_id = meal_templates.id
    ), 0),

    updated_at = now()
  WHERE id IN (
    SELECT meal_template_id
    FROM meal_template_foods
    WHERE child_template_id = NEW.id
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_parent_template_totals
AFTER UPDATE OF total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
ON meal_templates
FOR EACH ROW
WHEN (
  OLD.total_calories IS DISTINCT FROM NEW.total_calories OR
  OLD.total_protein_g IS DISTINCT FROM NEW.total_protein_g OR
  OLD.total_carbs_g IS DISTINCT FROM NEW.total_carbs_g OR
  OLD.total_fat_g IS DISTINCT FROM NEW.total_fat_g OR
  OLD.total_fiber_g IS DISTINCT FROM NEW.total_fiber_g
)
EXECUTE FUNCTION recalculate_parent_template_totals();

COMMENT ON FUNCTION recalculate_parent_template_totals IS 'Automatically recalculate parent template totals when child templates change';

-- 4.3 Trigger to increment popularity_score when serving is used
CREATE OR REPLACE FUNCTION increment_serving_popularity()
RETURNS TRIGGER AS $$
BEGIN
  -- Find matching food_serving and increment its popularity
  UPDATE food_servings
  SET
    popularity_score = popularity_score + 1,
    updated_at = now()
  WHERE food_id = NEW.food_id
    AND serving_name = NEW.quantity::text || ' ' || NEW.unit;

  -- If no exact match, create a new serving entry
  IF NOT FOUND THEN
    INSERT INTO food_servings (
      food_id,
      serving_name,
      serving_size_g,
      is_default,
      is_household_standard,
      popularity_score
    )
    SELECT
      NEW.food_id,
      NEW.quantity::text || ' ' || NEW.unit,
      NEW.quantity,  -- Simplified: assume unit matches food's base unit
      false,  -- Not default (user-created)
      false,  -- Not household standard
      1  -- First use
    WHERE NOT EXISTS (
      SELECT 1 FROM food_servings
      WHERE food_id = NEW.food_id
        AND serving_name = NEW.quantity::text || ' ' || NEW.unit
    );
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER track_serving_popularity
AFTER INSERT ON meal_foods
FOR EACH ROW
EXECUTE FUNCTION increment_serving_popularity();

COMMENT ON FUNCTION increment_serving_popularity IS 'Track how often each serving size is used to improve defaults';

-- ============================================================================
-- PART 5: ROW-LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- 5.1 Enable RLS on food_servings
ALTER TABLE food_servings ENABLE ROW LEVEL SECURITY;

-- 5.2 RLS Policies for food_servings (publicly readable for all foods)
CREATE POLICY "Anyone can view food servings"
ON food_servings FOR SELECT
USING (true);  -- All users can see all serving sizes

CREATE POLICY "Users can insert food servings for their own foods"
ON food_servings FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM foods_enhanced
    WHERE id = food_id
      AND (created_by = auth.uid() OR is_public = true)
  )
);

CREATE POLICY "Users can update food servings for their own foods"
ON food_servings FOR UPDATE
USING (
  EXISTS (
    SELECT 1 FROM foods_enhanced
    WHERE id = food_id
      AND created_by = auth.uid()
  )
);

CREATE POLICY "Users can delete food servings for their own foods"
ON food_servings FOR DELETE
USING (
  EXISTS (
    SELECT 1 FROM foods_enhanced
    WHERE id = food_id
      AND created_by = auth.uid()
  )
);

COMMENT ON POLICY "Anyone can view food servings" ON food_servings IS 'All users can see serving sizes for all foods';
COMMENT ON POLICY "Users can insert food servings for their own foods" ON food_servings IS 'Users can add servings to their own foods or public foods';

-- ============================================================================
-- PART 6: DATA MIGRATION (POPULATE EXISTING DATA)
-- ============================================================================

-- 6.1 Populate food_servings from existing household_serving_size data
INSERT INTO food_servings (food_id, serving_name, serving_size_g, is_default, is_household_standard)
SELECT
  id,
  household_serving_size || ' ' || COALESCE(household_serving_unit, serving_unit),
  serving_size,
  true,  -- Make it default
  true   -- Household standard
FROM foods_enhanced
WHERE household_serving_size IS NOT NULL
  AND household_serving_size != ''
ON CONFLICT (food_id, serving_name) DO NOTHING;

-- 6.2 Add common serving sizes for foods without household_serving_size
-- This adds metric/imperial conversions for common units
INSERT INTO food_servings (food_id, serving_name, serving_size_g, is_default, is_household_standard)
SELECT
  id,
  serving_size::text || ' ' || serving_unit,
  serving_size,
  true,  -- Make it default if no household serving exists
  CASE WHEN serving_unit IN ('cup', 'tbsp', 'tsp', 'oz', 'lb') THEN true ELSE false END
FROM foods_enhanced
WHERE (household_serving_size IS NULL OR household_serving_size = '')
  AND NOT EXISTS (
    SELECT 1 FROM food_servings WHERE food_id = foods_enhanced.id
  )
ON CONFLICT (food_id, serving_name) DO NOTHING;

-- ============================================================================
-- PART 7: VERIFICATION QUERIES (FOR TESTING)
-- ============================================================================

-- Test template expansion:
-- SELECT * FROM expand_meal_template('your-template-uuid');

-- Test default serving lookup:
-- SELECT * FROM get_default_serving('your-food-uuid');

-- Check food_servings population:
-- SELECT f.name, fs.serving_name, fs.serving_size_g, fs.is_default
-- FROM food_servings fs
-- JOIN foods_enhanced f ON f.id = fs.food_id
-- ORDER BY f.name, fs.is_default DESC;

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Summary of changes:
-- ✅ Created food_servings table for better portion defaults
-- ✅ Removed template_id from meal_foods (templates always expanded)
-- ✅ Added critical performance indexes (GIN, foreign keys)
-- ✅ Created expand_meal_template() function for recursive expansion
-- ✅ Created get_default_serving() function for portion defaults
-- ✅ Added triggers for auto-population and recalculation
-- ✅ Added RLS policies for food_servings
-- ✅ Migrated existing data to food_servings

-- Next steps:
-- 1. Update frontend to use get_default_serving() when adding foods
-- 2. Update backend API to expand templates before saving meal_logs
-- 3. Update FoodSearchV2 to search meal_templates too
-- 4. Add timezone handling in frontend meal logging
