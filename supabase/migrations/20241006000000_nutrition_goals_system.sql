-- ============================================================================
-- NUTRITION GOALS SYSTEM MIGRATION
-- ============================================================================
-- Purpose: Create comprehensive nutrition goals tracking system
-- - Separates nutrition goals from users table
-- - Supports macro and micronutrient goals
-- - Allows goal history and versioning
-- - Enables multiple goal sets (cutting, bulking, maintenance)
-- ============================================================================

-- Create nutrition_goals table
CREATE TABLE IF NOT EXISTS public.nutrition_goals (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,

  -- Goal metadata
  goal_name text NOT NULL DEFAULT 'My Nutrition Goals',
  goal_type text NOT NULL DEFAULT 'maintenance' CHECK (goal_type = ANY (ARRAY[
    'cutting'::text,
    'bulking'::text,
    'maintenance'::text,
    'performance'::text,
    'custom'::text
  ])),
  is_active boolean NOT NULL DEFAULT true,

  -- Macro goals (grams and calories)
  daily_calories integer NOT NULL DEFAULT 2000 CHECK (daily_calories >= 1000 AND daily_calories <= 10000),
  daily_protein_g integer NOT NULL DEFAULT 150 CHECK (daily_protein_g >= 50 AND daily_protein_g <= 500),
  daily_carbs_g integer NOT NULL DEFAULT 200 CHECK (daily_carbs_g >= 50 AND daily_carbs_g <= 800),
  daily_fat_g integer NOT NULL DEFAULT 65 CHECK (daily_fat_g >= 20 AND daily_fat_g <= 300),
  daily_fiber_g integer DEFAULT 30 CHECK (daily_fiber_g >= 10 AND daily_fiber_g <= 100),

  -- Sugar and sodium limits
  daily_sugar_limit_g integer DEFAULT 50 CHECK (daily_sugar_limit_g >= 0 AND daily_sugar_limit_g <= 200),
  daily_sodium_limit_mg integer DEFAULT 2300 CHECK (daily_sodium_limit_mg >= 500 AND daily_sodium_limit_mg <= 5000),

  -- Hydration
  daily_water_ml integer DEFAULT 2500 CHECK (daily_water_ml >= 1000 AND daily_water_ml <= 10000),

  -- Key micronutrients (optional, can be null if user doesn't track)
  daily_vitamin_a_mcg numeric CHECK (daily_vitamin_a_mcg IS NULL OR (daily_vitamin_a_mcg >= 0 AND daily_vitamin_a_mcg <= 10000)),
  daily_vitamin_c_mg numeric CHECK (daily_vitamin_c_mg IS NULL OR (daily_vitamin_c_mg >= 0 AND daily_vitamin_c_mg <= 2000)),
  daily_vitamin_d_mcg numeric CHECK (daily_vitamin_d_mcg IS NULL OR (daily_vitamin_d_mcg >= 0 AND daily_vitamin_d_mcg <= 200)),
  daily_vitamin_e_mg numeric CHECK (daily_vitamin_e_mg IS NULL OR (daily_vitamin_e_mg >= 0 AND daily_vitamin_e_mg <= 1000)),
  daily_vitamin_k_mcg numeric CHECK (daily_vitamin_k_mcg IS NULL OR (daily_vitamin_k_mcg >= 0 AND daily_vitamin_k_mcg <= 1000)),
  daily_vitamin_b12_mcg numeric CHECK (daily_vitamin_b12_mcg IS NULL OR (daily_vitamin_b12_mcg >= 0 AND daily_vitamin_b12_mcg <= 100)),
  daily_folate_mcg numeric CHECK (daily_folate_mcg IS NULL OR (daily_folate_mcg >= 0 AND daily_folate_mcg <= 1000)),

  daily_calcium_mg numeric CHECK (daily_calcium_mg IS NULL OR (daily_calcium_mg >= 0 AND daily_calcium_mg <= 3000)),
  daily_iron_mg numeric CHECK (daily_iron_mg IS NULL OR (daily_iron_mg >= 0 AND daily_iron_mg <= 50)),
  daily_magnesium_mg numeric CHECK (daily_magnesium_mg IS NULL OR (daily_magnesium_mg >= 0 AND daily_magnesium_mg <= 1000)),
  daily_potassium_mg numeric CHECK (daily_potassium_mg IS NULL OR (daily_potassium_mg >= 0 AND daily_potassium_mg <= 10000)),
  daily_zinc_mg numeric CHECK (daily_zinc_mg IS NULL OR (daily_zinc_mg >= 0 AND daily_zinc_mg <= 100)),

  -- Additional settings
  track_micronutrients boolean DEFAULT false,
  auto_adjust_goals boolean DEFAULT false,
  goal_notes text,

  -- Timestamps
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  activated_at timestamptz,

  CONSTRAINT nutrition_goals_pkey PRIMARY KEY (id),
  CONSTRAINT nutrition_goals_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

-- Create index on user_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_nutrition_goals_user_id ON public.nutrition_goals(user_id);

-- Create index on active goals for fast queries
CREATE INDEX IF NOT EXISTS idx_nutrition_goals_active ON public.nutrition_goals(user_id, is_active) WHERE is_active = true;

-- Create unique constraint: only one active goal per user
CREATE UNIQUE INDEX IF NOT EXISTS idx_nutrition_goals_one_active_per_user
  ON public.nutrition_goals(user_id)
  WHERE is_active = true;

-- Create trigger to update updated_at
CREATE OR REPLACE FUNCTION update_nutrition_goals_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_nutrition_goals_updated_at
  BEFORE UPDATE ON public.nutrition_goals
  FOR EACH ROW
  EXECUTE FUNCTION update_nutrition_goals_updated_at();

-- Create trigger to set activated_at when is_active becomes true
CREATE OR REPLACE FUNCTION set_nutrition_goal_activated_at()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.is_active = true AND (OLD IS NULL OR OLD.is_active = false) THEN
    NEW.activated_at = now();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_nutrition_goal_activated_at
  BEFORE INSERT OR UPDATE ON public.nutrition_goals
  FOR EACH ROW
  EXECUTE FUNCTION set_nutrition_goal_activated_at();

-- Create trigger to deactivate other goals when one is activated
CREATE OR REPLACE FUNCTION deactivate_other_nutrition_goals()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.is_active = true THEN
    UPDATE public.nutrition_goals
    SET is_active = false
    WHERE user_id = NEW.user_id
      AND id != NEW.id
      AND is_active = true;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_deactivate_other_nutrition_goals
  AFTER INSERT OR UPDATE ON public.nutrition_goals
  FOR EACH ROW
  WHEN (NEW.is_active = true)
  EXECUTE FUNCTION deactivate_other_nutrition_goals();

-- ============================================================================
-- MIGRATE EXISTING DATA FROM USERS TABLE
-- ============================================================================

-- Insert nutrition goals for users who have targets set
INSERT INTO public.nutrition_goals (
  user_id,
  goal_name,
  goal_type,
  is_active,
  daily_calories,
  daily_protein_g,
  daily_carbs_g,
  daily_fat_g,
  daily_fiber_g,
  created_at,
  activated_at
)
SELECT
  id as user_id,
  'Imported Goals' as goal_name,
  CASE
    WHEN primary_goal = 'lose_fat' THEN 'cutting'
    WHEN primary_goal = 'build_muscle' THEN 'bulking'
    ELSE 'maintenance'
  END as goal_type,
  true as is_active,
  COALESCE(daily_calorie_target, 2000) as daily_calories,
  COALESCE(daily_protein_target_g, 150) as daily_protein_g,
  COALESCE(daily_carbs_target_g, 200) as daily_carbs_g,
  COALESCE(daily_fat_target_g, 65) as daily_fat_g,
  30 as daily_fiber_g, -- default
  created_at,
  created_at as activated_at
FROM public.users
WHERE id NOT IN (SELECT user_id FROM public.nutrition_goals WHERE is_active = true)
  AND (daily_calorie_target IS NOT NULL OR daily_protein_target_g IS NOT NULL);

-- ============================================================================
-- RLS POLICIES
-- ============================================================================

-- Enable RLS
ALTER TABLE public.nutrition_goals ENABLE ROW LEVEL SECURITY;

-- Users can view their own goals
CREATE POLICY "Users can view own nutrition goals"
  ON public.nutrition_goals
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own goals
CREATE POLICY "Users can insert own nutrition goals"
  ON public.nutrition_goals
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own goals
CREATE POLICY "Users can update own nutrition goals"
  ON public.nutrition_goals
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Users can delete their own goals
CREATE POLICY "Users can delete own nutrition goals"
  ON public.nutrition_goals
  FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Function to get active nutrition goals for a user
CREATE OR REPLACE FUNCTION get_active_nutrition_goals(p_user_id uuid)
RETURNS TABLE (
  id uuid,
  goal_name text,
  goal_type text,
  daily_calories integer,
  daily_protein_g integer,
  daily_carbs_g integer,
  daily_fat_g integer,
  daily_fiber_g integer,
  daily_sugar_limit_g integer,
  daily_sodium_limit_mg integer,
  daily_water_ml integer,
  track_micronutrients boolean
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    ng.id,
    ng.goal_name,
    ng.goal_type,
    ng.daily_calories,
    ng.daily_protein_g,
    ng.daily_carbs_g,
    ng.daily_fat_g,
    ng.daily_fiber_g,
    ng.daily_sugar_limit_g,
    ng.daily_sodium_limit_mg,
    ng.daily_water_ml,
    ng.track_micronutrients
  FROM public.nutrition_goals ng
  WHERE ng.user_id = p_user_id
    AND ng.is_active = true
  LIMIT 1;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION get_active_nutrition_goals(uuid) TO authenticated;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE public.nutrition_goals IS 'User nutrition goals with macro and micronutrient targets';
COMMENT ON COLUMN public.nutrition_goals.goal_type IS 'Type of goal: cutting (deficit), bulking (surplus), maintenance, performance, custom';
COMMENT ON COLUMN public.nutrition_goals.is_active IS 'Only one goal can be active per user at a time';
COMMENT ON COLUMN public.nutrition_goals.track_micronutrients IS 'Whether user wants to track micronutrients (vitamins/minerals)';
COMMENT ON COLUMN public.nutrition_goals.auto_adjust_goals IS 'Whether to auto-adjust goals based on progress (future feature)';

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
-- This migration:
-- ✅ Creates nutrition_goals table with comprehensive macro/micro targets
-- ✅ Migrates existing data from users table
-- ✅ Sets up RLS policies
-- ✅ Creates helper functions
-- ✅ Adds proper indexes and constraints
-- ✅ Ensures only one active goal per user
-- ============================================================================
