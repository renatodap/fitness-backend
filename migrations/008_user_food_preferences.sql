-- Migration: User Food Preferences
-- Description: Track user's preferred serving sizes for personalized defaults
-- Example: User always logs 2 scoops of protein → auto-default to 2 scoops next time
-- Date: 2025-01-10

-- =============================================================================
-- Create user_food_preferences table
-- =============================================================================

CREATE TABLE IF NOT EXISTS user_food_preferences (
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  food_id UUID NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
  
  -- User's typical serving size for this food
  typical_serving_grams NUMERIC NOT NULL CHECK (typical_serving_grams > 0),
  
  -- User's typical serving name (e.g., "2 scoops", "1 medium")
  typical_serving_name TEXT,
  
  -- How many times has the user logged this food?
  use_count INTEGER DEFAULT 1 CHECK (use_count > 0),
  
  -- When was this food last used?
  last_used_at TIMESTAMPTZ DEFAULT now(),
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  
  -- Primary key: one preference per user per food
  PRIMARY KEY (user_id, food_id)
);

-- =============================================================================
-- Indexes for performance
-- =============================================================================

-- Fast lookup of user's food preferences
CREATE INDEX idx_user_food_preferences_user_id 
  ON user_food_preferences(user_id);

-- Lookup user's most frequently used foods
CREATE INDEX idx_user_food_preferences_user_frequency 
  ON user_food_preferences(user_id, use_count DESC);

-- Lookup user's recently used foods
CREATE INDEX idx_user_food_preferences_user_recent 
  ON user_food_preferences(user_id, last_used_at DESC);

-- =============================================================================
-- Trigger: Update updated_at timestamp
-- =============================================================================

CREATE OR REPLACE FUNCTION update_user_food_preferences_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_food_preferences_updated_at
  BEFORE UPDATE ON user_food_preferences
  FOR EACH ROW
  EXECUTE FUNCTION update_user_food_preferences_updated_at();

-- =============================================================================
-- Function: Record user's food usage
-- =============================================================================

CREATE OR REPLACE FUNCTION record_user_food_usage(
  p_user_id UUID,
  p_food_id UUID,
  p_grams NUMERIC,
  p_serving_name TEXT DEFAULT NULL
)
RETURNS void AS $$
BEGIN
  -- Insert or update user's preference for this food
  INSERT INTO user_food_preferences (
    user_id,
    food_id,
    typical_serving_grams,
    typical_serving_name,
    use_count,
    last_used_at
  )
  VALUES (
    p_user_id,
    p_food_id,
    p_grams,
    p_serving_name,
    1,
    now()
  )
  ON CONFLICT (user_id, food_id)
  DO UPDATE SET
    -- Calculate running average of typical serving size
    typical_serving_grams = (
      user_food_preferences.typical_serving_grams * user_food_preferences.use_count + p_grams
    ) / (user_food_preferences.use_count + 1),
    
    -- Update serving name if provided
    typical_serving_name = COALESCE(p_serving_name, user_food_preferences.typical_serving_name),
    
    -- Increment use count
    use_count = user_food_preferences.use_count + 1,
    
    -- Update last used timestamp
    last_used_at = now();
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Function: Get user's preferred serving for a food
-- =============================================================================

CREATE OR REPLACE FUNCTION get_user_preferred_serving(
  p_user_id UUID,
  p_food_id UUID
)
RETURNS TABLE (
  typical_serving_grams NUMERIC,
  typical_serving_name TEXT,
  use_count INTEGER,
  last_used_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    ufp.typical_serving_grams,
    ufp.typical_serving_name,
    ufp.use_count,
    ufp.last_used_at
  FROM user_food_preferences ufp
  WHERE ufp.user_id = p_user_id
    AND ufp.food_id = p_food_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Function: Get user's frequently used foods
-- =============================================================================

CREATE OR REPLACE FUNCTION get_user_frequent_foods(
  p_user_id UUID,
  p_limit INTEGER DEFAULT 20
)
RETURNS TABLE (
  food_id UUID,
  food_name TEXT,
  typical_serving_grams NUMERIC,
  typical_serving_name TEXT,
  use_count INTEGER,
  last_used_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    f.id,
    f.name,
    ufp.typical_serving_grams,
    ufp.typical_serving_name,
    ufp.use_count,
    ufp.last_used_at
  FROM user_food_preferences ufp
  JOIN foods_enhanced f ON f.id = ufp.food_id
  WHERE ufp.user_id = p_user_id
  ORDER BY ufp.use_count DESC, ufp.last_used_at DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Function: Get user's recently used foods
-- =============================================================================

CREATE OR REPLACE FUNCTION get_user_recent_foods(
  p_user_id UUID,
  p_limit INTEGER DEFAULT 20
)
RETURNS TABLE (
  food_id UUID,
  food_name TEXT,
  typical_serving_grams NUMERIC,
  typical_serving_name TEXT,
  use_count INTEGER,
  last_used_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    f.id,
    f.name,
    ufp.typical_serving_grams,
    ufp.typical_serving_name,
    ufp.use_count,
    ufp.last_used_at
  FROM user_food_preferences ufp
  JOIN foods_enhanced f ON f.id = ufp.food_id
  WHERE ufp.user_id = p_user_id
  ORDER BY ufp.last_used_at DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Trigger: Auto-record preferences when meals are logged
-- =============================================================================

CREATE OR REPLACE FUNCTION auto_record_food_preferences()
RETURNS TRIGGER AS $$
DECLARE
  v_user_id UUID;
  v_meal_food RECORD;
BEGIN
  -- Get user_id from meal_log
  SELECT user_id INTO v_user_id
  FROM meal_logs
  WHERE id = NEW.meal_log_id;
  
  -- Only proceed if we have a user_id
  IF v_user_id IS NOT NULL THEN
    -- Get food details from meal_foods
    FOR v_meal_food IN
      SELECT 
        food_id,
        quantity,
        unit
      FROM meal_foods
      WHERE meal_log_id = NEW.meal_log_id
    LOOP
      -- Record usage (quantity is already in grams)
      PERFORM record_user_food_usage(
        v_user_id,
        v_meal_food.food_id,
        v_meal_food.quantity,
        v_meal_food.unit
      );
    END LOOP;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Note: Trigger creation commented out - enable if you want auto-tracking
-- CREATE TRIGGER trigger_auto_record_food_preferences
--   AFTER INSERT ON meal_foods
--   FOR EACH ROW
--   EXECUTE FUNCTION auto_record_food_preferences();

-- =============================================================================
-- Verification queries
-- =============================================================================

-- Verify table created
SELECT 'user_food_preferences table created successfully' AS status
WHERE EXISTS (
  SELECT 1 FROM information_schema.tables 
  WHERE table_name = 'user_food_preferences'
);

-- Check indexes
SELECT 
  indexname, 
  indexdef
FROM pg_indexes
WHERE tablename = 'user_food_preferences'
ORDER BY indexname;

-- Check functions
SELECT 
  routine_name,
  routine_type
FROM information_schema.routines
WHERE routine_name LIKE '%user_food%' OR routine_name LIKE '%food_preferences%'
ORDER BY routine_name;
