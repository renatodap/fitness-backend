-- Migration: Food Serving Conversions (Phase 1 Enhancement)
-- Description: Add support for multiple serving options per food
-- Example: Banana can have small (90g), medium (118g), large (136g) options
-- Date: 2025-01-10

-- =============================================================================
-- Create food_serving_conversions table
-- =============================================================================

CREATE TABLE IF NOT EXISTS food_serving_conversions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  food_id UUID NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
  
  -- Serving description (e.g., "1 slice", "1 medium", "1 scoop", "2 scoops")
  serving_name TEXT NOT NULL,
  
  -- Actual weight in grams for this serving
  serving_grams NUMERIC NOT NULL CHECK (serving_grams > 0),
  
  -- Is this the default/recommended serving for this food?
  is_default BOOLEAN DEFAULT false,
  
  -- Track popularity (which servings users choose most often)
  popularity_score INTEGER DEFAULT 0,
  
  -- Source of this conversion data
  -- Values: 'manual', 'usda', 'user_average', 'manufacturer'
  source TEXT DEFAULT 'manual',
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  
  -- Constraints
  UNIQUE(food_id, serving_name),
  CHECK (source IN ('manual', 'usda', 'user_average', 'manufacturer'))
);

-- =============================================================================
-- Indexes for performance
-- =============================================================================

-- Fast lookup of servings for a specific food
CREATE INDEX idx_food_serving_conversions_food_id 
  ON food_serving_conversions(food_id);

-- Fast lookup of default serving for a food
CREATE INDEX idx_food_serving_conversions_default 
  ON food_serving_conversions(food_id) 
  WHERE is_default = true;

-- Lookup by popularity (for suggesting common servings)
CREATE INDEX idx_food_serving_conversions_popularity 
  ON food_serving_conversions(food_id, popularity_score DESC);

-- =============================================================================
-- Trigger: Update updated_at timestamp
-- =============================================================================

CREATE OR REPLACE FUNCTION update_food_serving_conversions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_food_serving_conversions_updated_at
  BEFORE UPDATE ON food_serving_conversions
  FOR EACH ROW
  EXECUTE FUNCTION update_food_serving_conversions_updated_at();

-- =============================================================================
-- Example seed data (optional - comment out if not needed)
-- =============================================================================

-- Pizza serving options
/*
INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 slice',
  120,
  true,
  'manual'
FROM foods_enhanced 
WHERE name ILIKE '%pizza%' 
  AND NOT EXISTS (
    SELECT 1 FROM food_serving_conversions 
    WHERE food_id = foods_enhanced.id AND serving_name = '1 slice'
  )
LIMIT 1;

INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 small slice',
  90,
  false,
  'manual'
FROM foods_enhanced 
WHERE name ILIKE '%pizza%'
LIMIT 1;

INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 large slice',
  150,
  false,
  'manual'
FROM foods_enhanced 
WHERE name ILIKE '%pizza%'
LIMIT 1;

-- Banana serving options
INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 small',
  90,
  false,
  'usda'
FROM foods_enhanced 
WHERE name ILIKE '%banana%' AND name NOT ILIKE '%bread%'
LIMIT 1;

INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 medium',
  118,
  true,
  'usda'
FROM foods_enhanced 
WHERE name ILIKE '%banana%' AND name NOT ILIKE '%bread%'
LIMIT 1;

INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 large',
  136,
  true,
  'usda'
FROM foods_enhanced 
WHERE name ILIKE '%banana%' AND name NOT ILIKE '%bread%'
LIMIT 1;

-- Protein powder serving options
INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '1 scoop',
  30,
  true,
  'manufacturer'
FROM foods_enhanced 
WHERE name ILIKE '%whey%protein%'
LIMIT 1;

INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default, source) 
SELECT 
  id,
  '2 scoops',
  60,
  false,
  'manufacturer'
FROM foods_enhanced 
WHERE name ILIKE '%whey%protein%'
LIMIT 1;
*/

-- =============================================================================
-- Helper function: Get default serving for a food
-- =============================================================================

-- Drop existing functions first to avoid conflicts
DROP FUNCTION IF EXISTS get_default_serving(UUID);
DROP FUNCTION IF EXISTS get_food_servings(UUID);

CREATE OR REPLACE FUNCTION get_default_serving(p_food_id UUID)
RETURNS TABLE (
  serving_name TEXT,
  serving_grams NUMERIC
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    fsc.serving_name,
    fsc.serving_grams
  FROM food_serving_conversions fsc
  WHERE fsc.food_id = p_food_id
    AND fsc.is_default = true
  LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Helper function: Get all servings for a food (ordered by popularity)
-- =============================================================================

CREATE OR REPLACE FUNCTION get_food_servings(p_food_id UUID)
RETURNS TABLE (
  serving_name TEXT,
  serving_grams NUMERIC,
  is_default BOOLEAN,
  popularity_score INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    fsc.serving_name,
    fsc.serving_grams,
    fsc.is_default,
    fsc.popularity_score
  FROM food_serving_conversions fsc
  WHERE fsc.food_id = p_food_id
  ORDER BY fsc.is_default DESC, fsc.popularity_score DESC, fsc.serving_grams ASC;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Verification queries
-- =============================================================================

-- Verify table created
SELECT 'food_serving_conversions table created successfully' AS status
WHERE EXISTS (
  SELECT 1 FROM information_schema.tables 
  WHERE table_name = 'food_serving_conversions'
);

-- Check indexes
SELECT 
  indexname, 
  indexdef
FROM pg_indexes
WHERE tablename = 'food_serving_conversions'
ORDER BY indexname;

-- Sample data (if inserted)
SELECT 
  f.name,
  fsc.serving_name,
  fsc.serving_grams,
  fsc.is_default,
  fsc.source
FROM food_serving_conversions fsc
JOIN foods_enhanced f ON f.id = fsc.food_id
ORDER BY f.name, fsc.is_default DESC, fsc.serving_grams ASC
LIMIT 20;
