-- ============================================================================
-- MIGRATION 002: Clean Food Architecture (CONSOLIDATED)
-- ============================================================================
-- Purpose: Separate atomic foods from composite meals, add organization
-- Date: 2025-10-09
-- Consolidates: 002, 002b, 002c, 002d
-- Breaking Change: YES - removes restaurant fields from foods_enhanced
-- ============================================================================

-- ============================================================================
-- PART 1: Drop Old Problematic Triggers
-- ============================================================================

-- Force drop ALL old trigger functions that reference wrong column names
DROP FUNCTION IF EXISTS calculate_template_nutrition(uuid) CASCADE;
DROP FUNCTION IF EXISTS update_template_nutrition() CASCADE;
DROP FUNCTION IF EXISTS recalculate_parent_template_totals() CASCADE;
DROP FUNCTION IF EXISTS populate_food_servings() CASCADE;
DROP FUNCTION IF EXISTS increment_serving_popularity() CASCADE;

-- ============================================================================
-- PART 2: Clean up foods_enhanced (ATOMIC FOODS ONLY)
-- ============================================================================

-- Remove restaurant-specific fields (meals should be templates, not foods)
ALTER TABLE foods_enhanced
DROP COLUMN IF EXISTS is_restaurant CASCADE,
DROP COLUMN IF EXISTS restaurant_name CASCADE,
DROP COLUMN IF EXISTS menu_item_id CASCADE;

-- Add constraint: foods must be atomic
ALTER TABLE foods_enhanced
ADD COLUMN IF NOT EXISTS is_atomic boolean DEFAULT true;

COMMENT ON COLUMN foods_enhanced.is_atomic IS 'True = single ingredient (chicken, rice). False = should be a meal_template instead.';

-- Add better categorization
ALTER TABLE foods_enhanced
ADD COLUMN IF NOT EXISTS cuisine_type text,
ADD COLUMN IF NOT EXISTS meal_suitability text[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS preparation_state text DEFAULT 'raw',
ADD COLUMN IF NOT EXISTS is_whole_food boolean DEFAULT true,
ADD COLUMN IF NOT EXISTS processing_level text DEFAULT 'unprocessed';

COMMENT ON COLUMN foods_enhanced.cuisine_type IS 'e.g., Italian, Mexican, Asian, American';
COMMENT ON COLUMN foods_enhanced.meal_suitability IS 'e.g., {breakfast, lunch, dinner, snack}';
COMMENT ON COLUMN foods_enhanced.preparation_state IS 'raw, cooked, grilled, baked, fried, steamed';
COMMENT ON COLUMN foods_enhanced.is_whole_food IS 'True for whole foods (chicken, rice), false for processed (protein bar)';
COMMENT ON COLUMN foods_enhanced.processing_level IS 'unprocessed, minimally_processed, processed, ultra_processed';

-- ============================================================================
-- PART 3: Enhance meal_templates (COMPOSITE MEALS)
-- ============================================================================

-- Make user_id nullable for public templates
ALTER TABLE meal_templates
ALTER COLUMN user_id DROP NOT NULL;

-- Add restaurant and public template support
ALTER TABLE meal_templates
ADD COLUMN IF NOT EXISTS is_public boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS is_restaurant boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS restaurant_name text,
ADD COLUMN IF NOT EXISTS restaurant_chain_id text,
ADD COLUMN IF NOT EXISTS menu_item_id text,
ADD COLUMN IF NOT EXISTS source text DEFAULT 'user_created' CHECK (source IN ('user_created', 'restaurant', 'imported', 'ai_generated', 'community')),
ADD COLUMN IF NOT EXISTS popularity_score integer DEFAULT 0,
ADD COLUMN IF NOT EXISTS image_url text,
ADD COLUMN IF NOT EXISTS cuisine_type text,
ADD COLUMN IF NOT EXISTS meal_suitability text[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS prep_time_minutes integer,
ADD COLUMN IF NOT EXISTS dietary_flags text[] DEFAULT '{}';

COMMENT ON COLUMN meal_templates.is_public IS 'True = available to all users (restaurant meals, community templates)';
COMMENT ON COLUMN meal_templates.is_restaurant IS 'True = from restaurant (Chipotle, McDonald''s, etc.)';
COMMENT ON COLUMN meal_templates.source IS 'Origin: user_created, restaurant, imported, ai_generated, community';
COMMENT ON COLUMN meal_templates.popularity_score IS 'How often this template is used (for ranking public templates)';

-- Add constraint: public templates MUST have user_id = NULL
ALTER TABLE meal_templates
DROP CONSTRAINT IF EXISTS check_public_template_user;

ALTER TABLE meal_templates
ADD CONSTRAINT check_public_template_user
CHECK (
    (is_public = true AND user_id IS NULL) OR
    (is_public = false AND user_id IS NOT NULL) OR
    (is_public IS NULL AND user_id IS NOT NULL)
);

-- Create index for public template discovery
CREATE INDEX IF NOT EXISTS idx_meal_templates_public
ON meal_templates(is_public, popularity_score DESC)
WHERE is_public = true;

CREATE INDEX IF NOT EXISTS idx_meal_templates_restaurant
ON meal_templates(restaurant_name, is_restaurant)
WHERE is_restaurant = true;

CREATE INDEX IF NOT EXISTS idx_meal_templates_public_popularity
ON meal_templates(is_public, popularity_score DESC)
WHERE is_public = true;

-- ============================================================================
-- PART 4: User Favorites
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_favorite_foods (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    food_id uuid NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
    created_at timestamptz DEFAULT now(),
    CONSTRAINT unique_user_favorite_food UNIQUE(user_id, food_id)
);

CREATE INDEX IF NOT EXISTS idx_user_favorite_foods_user_id ON user_favorite_foods(user_id);

-- RLS Policies
ALTER TABLE user_favorite_foods ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own favorite foods" ON user_favorite_foods;
CREATE POLICY "Users can view own favorite foods"
ON user_favorite_foods FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can add own favorite foods" ON user_favorite_foods;
CREATE POLICY "Users can add own favorite foods"
ON user_favorite_foods FOR INSERT
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can remove own favorite foods" ON user_favorite_foods;
CREATE POLICY "Users can remove own favorite foods"
ON user_favorite_foods FOR DELETE
USING (auth.uid() = user_id);

COMMENT ON TABLE user_favorite_foods IS 'User favorites for quick access (star icon in UI)';

-- ============================================================================
-- PART 5: Food Categories (Hierarchical Organization)
-- ============================================================================

CREATE TABLE IF NOT EXISTS food_categories (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    parent_id uuid REFERENCES food_categories(id) ON DELETE CASCADE,
    level integer NOT NULL DEFAULT 0 CHECK (level >= 0 AND level <= 3),
    icon text,
    color text,
    sort_order integer DEFAULT 0,
    created_at timestamptz DEFAULT now(),
    CONSTRAINT unique_category_name_per_parent UNIQUE(name, parent_id)
);

CREATE INDEX IF NOT EXISTS idx_food_categories_parent_id ON food_categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_food_categories_level ON food_categories(level);

COMMENT ON TABLE food_categories IS 'Hierarchical food categorization (e.g., Protein > Poultry > Chicken > Breast)';
COMMENT ON COLUMN food_categories.level IS '0=top (Protein), 1=sub (Poultry), 2=specific (Chicken), 3=detail (Breast)';

-- Link foods to categories
ALTER TABLE foods_enhanced
ADD COLUMN IF NOT EXISTS category_id uuid REFERENCES food_categories(id);

CREATE INDEX IF NOT EXISTS idx_foods_enhanced_category_id ON foods_enhanced(category_id);

-- ============================================================================
-- PART 6: Food Pairings (AI Suggestions)
-- ============================================================================

CREATE TABLE IF NOT EXISTS food_pairings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    food_a_id uuid NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
    food_b_id uuid NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
    co_occurrence_count integer DEFAULT 1,
    confidence_score numeric CHECK (confidence_score >= 0 AND confidence_score <= 1),
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    CONSTRAINT unique_food_pair UNIQUE(food_a_id, food_b_id),
    CONSTRAINT no_self_pairing CHECK (food_a_id != food_b_id)
);

CREATE INDEX IF NOT EXISTS idx_food_pairings_food_a ON food_pairings(food_a_id, co_occurrence_count DESC);
CREATE INDEX IF NOT EXISTS idx_food_pairings_food_b ON food_pairings(food_b_id, co_occurrence_count DESC);

COMMENT ON TABLE food_pairings IS 'Tracks which foods are commonly logged together (for AI suggestions)';

-- ============================================================================
-- PART 7: Seed Default Food Categories
-- ============================================================================

INSERT INTO food_categories (id, name, level, icon, color, sort_order) VALUES
-- Level 0: Top Categories
('00000000-0000-0000-0000-000000000001', 'Protein', 0, '🥩', '#E53E3E', 1),
('00000000-0000-0000-0000-000000000002', 'Carbohydrates', 0, '🍞', '#D69E2E', 2),
('00000000-0000-0000-0000-000000000003', 'Fats', 0, '🥑', '#38A169', 3),
('00000000-0000-0000-0000-000000000004', 'Vegetables', 0, '🥦', '#48BB78', 4),
('00000000-0000-0000-0000-000000000005', 'Fruits', 0, '🍎', '#ED8936', 5),
('00000000-0000-0000-0000-000000000006', 'Dairy', 0, '🥛', '#4299E1', 6),
('00000000-0000-0000-0000-000000000007', 'Beverages', 0, '☕', '#805AD5', 7),
('00000000-0000-0000-0000-000000000008', 'Supplements', 0, '💊', '#9F7AEA', 8)
ON CONFLICT (id) DO NOTHING;

-- Level 1: Protein Subcategories
INSERT INTO food_categories (name, parent_id, level, sort_order) VALUES
('Poultry', '00000000-0000-0000-0000-000000000001', 1, 1),
('Beef', '00000000-0000-0000-0000-000000000001', 1, 2),
('Pork', '00000000-0000-0000-0000-000000000001', 1, 3),
('Fish', '00000000-0000-0000-0000-000000000001', 1, 4),
('Seafood', '00000000-0000-0000-0000-000000000001', 1, 5),
('Eggs', '00000000-0000-0000-0000-000000000001', 1, 6),
('Plant Protein', '00000000-0000-0000-0000-000000000001', 1, 7)
ON CONFLICT (name, parent_id) DO NOTHING;

-- Level 1: Carbohydrates Subcategories
INSERT INTO food_categories (name, parent_id, level, sort_order) VALUES
('Rice', '00000000-0000-0000-0000-000000000002', 1, 1),
('Pasta', '00000000-0000-0000-0000-000000000002', 1, 2),
('Bread', '00000000-0000-0000-0000-000000000002', 1, 3),
('Grains', '00000000-0000-0000-0000-000000000002', 1, 4),
('Potatoes', '00000000-0000-0000-0000-000000000002', 1, 5)
ON CONFLICT (name, parent_id) DO NOTHING;

-- ============================================================================
-- PART 8: Update Existing Data
-- ============================================================================

-- Link existing foods to categories (map old food_group to new category_id)
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000001' WHERE food_group = 'Protein';
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000002' WHERE food_group = 'Grains';
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000004' WHERE food_group = 'Vegetables';
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000005' WHERE food_group = 'Fruits';
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000006' WHERE food_group = 'Dairy';
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000007' WHERE food_group = 'Beverages';
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000003' WHERE food_group IN ('Fats', 'Nuts', 'Seeds');
UPDATE foods_enhanced SET category_id = '00000000-0000-0000-0000-000000000008' WHERE food_group = 'Supplements';

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check new columns exist
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'foods_enhanced'
AND column_name IN ('is_atomic', 'cuisine_type', 'meal_suitability', 'preparation_state', 'category_id');

-- Check meal_templates enhancements
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'meal_templates'
AND column_name IN ('is_public', 'is_restaurant', 'restaurant_name', 'source');

-- Check new tables created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('user_favorite_foods', 'food_categories', 'food_pairings');

-- Check food categories seeded
SELECT name, level, icon FROM food_categories ORDER BY level, sort_order;

-- Check no problematic triggers exist
SELECT trigger_name, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
AND trigger_name IN (
    'update_parent_template_totals',
    'auto_populate_food_servings',
    'track_serving_popularity'
);
-- Should return 0 rows

-- ============================================================================
-- END MIGRATION 002
-- ============================================================================
