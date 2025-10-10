-- ============================================================================
-- CLEAN FOOD & MEAL SYSTEM - Database Schema
-- ============================================================================
-- Purpose: Create intuitive, user-friendly food tracking system from scratch
-- Design: Dual quantity tracking (servings + grams) built-in from day one
-- Date: 2025-01-10
-- ============================================================================

BEGIN;

-- ============================================================================
-- FOODS TABLE
-- ============================================================================
-- Stores all food items with their nutrition and serving information
-- Key Features:
-- - All nutrition values are per serving_size (typically 100g)
-- - household_serving_unit: intuitive units like "slice", "scoop", "medium"
-- - household_serving_grams: how many grams per household unit
-- Example: Pizza -> serving_size=100g, household_serving_unit="slice", household_serving_grams=107
-- ============================================================================

CREATE TABLE foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic Info
    name VARCHAR(255) NOT NULL,
    food_type VARCHAR(50) NOT NULL DEFAULT 'ingredient',  -- 'ingredient', 'dish', 'branded', 'restaurant'
    brand_name VARCHAR(255),                               -- For branded/restaurant items
    restaurant_name VARCHAR(255),                          -- For restaurant items
    description TEXT,
    
    -- Editing behavior control
    allow_gram_editing BOOLEAN NOT NULL DEFAULT true,     -- Can users edit grams? (false for branded/restaurant)
    
    -- Serving Information (BASE UNIT for nutrition calculation)
    serving_size DECIMAL(10,2) NOT NULL DEFAULT 100,  -- Always in grams (typically 100g)
    serving_unit VARCHAR(50) NOT NULL DEFAULT 'g',     -- Always 'g' for consistency
    
    -- Household Serving (INTUITIVE UNIT for users)
    household_serving_unit VARCHAR(50),                -- e.g., "slice", "scoop", "medium", "tbsp"
    household_serving_grams DECIMAL(10,2),             -- e.g., 107 (grams per slice)
    
    -- Nutrition (per serving_size, typically per 100g)
    calories DECIMAL(10,2) NOT NULL DEFAULT 0,
    protein_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_carbs_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_fat_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    dietary_fiber_g DECIMAL(10,2) DEFAULT 0,
    total_sugars_g DECIMAL(10,2) DEFAULT 0,
    sodium_mg DECIMAL(10,2) DEFAULT 0,
    
    -- Metadata
    source VARCHAR(100),                               -- 'usda', 'user', 'custom'
    external_id VARCHAR(255),                          -- ID from external API
    verified BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT true,
    created_by UUID REFERENCES profiles(id),
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT foods_serving_size_positive CHECK (serving_size > 0),
    CONSTRAINT foods_household_grams_positive CHECK (household_serving_grams IS NULL OR household_serving_grams > 0),
    CONSTRAINT foods_food_type_valid CHECK (food_type IN ('ingredient', 'dish', 'branded', 'restaurant'))
);

-- Indexes for fast lookups
CREATE INDEX idx_foods_name ON foods(name);
CREATE INDEX idx_foods_food_type ON foods(food_type);
CREATE INDEX idx_foods_brand ON foods(brand_name);
CREATE INDEX idx_foods_restaurant ON foods(restaurant_name);
CREATE INDEX idx_foods_name_trgm ON foods USING gin(name gin_trgm_ops);
CREATE INDEX idx_foods_created_by ON foods(created_by);
CREATE INDEX idx_foods_is_public ON foods(is_public);

-- ============================================================================
-- MEALS TABLE
-- ============================================================================
-- Stores meal entries (breakfast, lunch, dinner, snacks)
-- ============================================================================

CREATE TABLE meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Meal Info
    category VARCHAR(50) NOT NULL,                     -- 'breakfast', 'lunch', 'dinner', 'snack', 'other'
    logged_at TIMESTAMPTZ NOT NULL,
    notes TEXT,
    
    -- Total Nutrition (calculated from meal_foods)
    total_calories DECIMAL(10,2) DEFAULT 0,
    total_protein_g DECIMAL(10,2) DEFAULT 0,
    total_carbs_g DECIMAL(10,2) DEFAULT 0,
    total_fat_g DECIMAL(10,2) DEFAULT 0,
    total_fiber_g DECIMAL(10,2) DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT meals_category_valid CHECK (category IN ('breakfast', 'lunch', 'dinner', 'snack', 'other'))
);

-- Indexes for fast lookups
CREATE INDEX idx_meals_user_id ON meals(user_id);
CREATE INDEX idx_meals_logged_at ON meals(logged_at DESC);
CREATE INDEX idx_meals_user_logged ON meals(user_id, logged_at DESC);

-- ============================================================================
-- MEAL_FOODS TABLE (Junction table with dual quantity tracking)
-- ============================================================================
-- Links foods to meals with BOTH serving and gram quantities
-- This is the CORE of the dual quantity system
-- ============================================================================

CREATE TABLE meal_foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_id UUID NOT NULL REFERENCES meals(id) ON DELETE CASCADE,
    food_id UUID NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    
    -- DUAL QUANTITY TRACKING (the key innovation!)
    -- Both quantities are ALWAYS stored and kept in sync
    serving_quantity DECIMAL(10,3) NOT NULL,           -- e.g., 1.5 (slices)
    serving_unit VARCHAR(50),                          -- e.g., "slice" (null if no household unit)
    gram_quantity DECIMAL(10,2) NOT NULL,              -- e.g., 160.5 (grams) - SOURCE OF TRUTH for nutrition
    last_edited_field VARCHAR(20) NOT NULL,            -- 'serving' or 'grams' - which field user edited last
    
    -- Calculated Nutrition (from gram_quantity)
    -- These are denormalized for performance but calculated from grams
    calories DECIMAL(10,2) NOT NULL DEFAULT 0,
    protein_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    carbs_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    fat_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    fiber_g DECIMAL(10,2) DEFAULT 0,
    
    -- Metadata
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT meal_foods_serving_quantity_positive CHECK (serving_quantity > 0),
    CONSTRAINT meal_foods_gram_quantity_positive CHECK (gram_quantity > 0),
    CONSTRAINT meal_foods_last_edited_valid CHECK (last_edited_field IN ('serving', 'grams'))
);

-- Indexes
CREATE INDEX idx_meal_foods_meal_id ON meal_foods(meal_id);
CREATE INDEX idx_meal_foods_food_id ON meal_foods(food_id);

-- ============================================================================
-- FOOD_PREFERENCES TABLE (Track user's last used quantities)
-- ============================================================================
-- Remembers how much of each food a user typically logs
-- ============================================================================

CREATE TABLE food_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    food_id UUID NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    
    -- Last used quantities
    last_serving_quantity DECIMAL(10,3),
    last_serving_unit VARCHAR(50),
    last_gram_quantity DECIMAL(10,2),
    last_used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    use_count INT DEFAULT 1,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Unique constraint: one preference per user per food
    CONSTRAINT food_preferences_unique UNIQUE (user_id, food_id)
);

-- Indexes
CREATE INDEX idx_food_preferences_user_id ON food_preferences(user_id);
CREATE INDEX idx_food_preferences_food_id ON food_preferences(food_id);
CREATE INDEX idx_food_preferences_last_used ON food_preferences(user_id, last_used_at DESC);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_foods_updated_at BEFORE UPDATE ON foods
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_meals_updated_at BEFORE UPDATE ON meals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_food_preferences_updated_at BEFORE UPDATE ON food_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- List all tables
SELECT tablename, schemaname
FROM pg_tables 
WHERE tablename IN ('foods', 'meals', 'meal_foods', 'food_preferences')
ORDER BY tablename;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Clean food system created successfully!';
    RAISE NOTICE '📊 Tables created: foods, meals, meal_foods, food_preferences';
    RAISE NOTICE '🎯 Dual quantity tracking is built-in from the start';
    RAISE NOTICE '🚀 Ready for seed data!';
END $$;
