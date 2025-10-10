-- ============================================================================
-- COMPREHENSIVE FOOD & MEAL SYSTEM V2
-- ============================================================================
-- Purpose: MyFitnessPal-level organization with better UX
-- Features: Barcodes, favorites, recipes, full micronutrients, smart search
-- Date: 2025-01-10
-- ============================================================================

BEGIN;

-- ============================================================================
-- FOODS TABLE (Enhanced with everything MFP has + better)
-- ============================================================================

CREATE TABLE foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic Info
    name VARCHAR(255) NOT NULL,
    food_type VARCHAR(50) NOT NULL DEFAULT 'ingredient',
    brand_name VARCHAR(255),
    restaurant_name VARCHAR(255),
    description TEXT,
    
    -- Barcode Support
    barcode_upc VARCHAR(50),
    barcode_ean VARCHAR(50),
    barcode_type VARCHAR(20),  -- 'upc-a', 'upc-e', 'ean-13', 'ean-8'
    
    -- Editing Control
    allow_gram_editing BOOLEAN NOT NULL DEFAULT true,
    
    -- Serving Information
    serving_size DECIMAL(10,2) NOT NULL DEFAULT 100,
    serving_unit VARCHAR(50) NOT NULL DEFAULT 'g',
    household_serving_unit VARCHAR(50),
    household_serving_grams DECIMAL(10,2),
    servings_per_container DECIMAL(10,2),  -- For packaged foods
    
    -- Macronutrients (per serving_size)
    calories DECIMAL(10,2) NOT NULL DEFAULT 0,
    protein_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_carbs_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_fat_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    
    -- Carbs Breakdown
    dietary_fiber_g DECIMAL(10,2) DEFAULT 0,
    total_sugars_g DECIMAL(10,2) DEFAULT 0,
    added_sugars_g DECIMAL(10,2) DEFAULT 0,  -- Important for health tracking
    sugar_alcohols_g DECIMAL(10,2) DEFAULT 0,
    
    -- Fats Breakdown
    saturated_fat_g DECIMAL(10,2) DEFAULT 0,
    trans_fat_g DECIMAL(10,2) DEFAULT 0,
    monounsaturated_fat_g DECIMAL(10,2) DEFAULT 0,
    polyunsaturated_fat_g DECIMAL(10,2) DEFAULT 0,
    omega3_mg DECIMAL(10,2) DEFAULT 0,
    omega6_mg DECIMAL(10,2) DEFAULT 0,
    cholesterol_mg DECIMAL(10,2) DEFAULT 0,
    
    -- Essential Minerals
    sodium_mg DECIMAL(10,2) DEFAULT 0,
    potassium_mg DECIMAL(10,2) DEFAULT 0,
    calcium_mg DECIMAL(10,2) DEFAULT 0,
    iron_mg DECIMAL(10,2) DEFAULT 0,
    magnesium_mg DECIMAL(10,2) DEFAULT 0,
    zinc_mg DECIMAL(10,2) DEFAULT 0,
    
    -- Essential Vitamins
    vitamin_a_mcg DECIMAL(10,2) DEFAULT 0,
    vitamin_c_mg DECIMAL(10,2) DEFAULT 0,
    vitamin_d_mcg DECIMAL(10,2) DEFAULT 0,
    vitamin_e_mg DECIMAL(10,2) DEFAULT 0,
    vitamin_k_mcg DECIMAL(10,2) DEFAULT 0,
    vitamin_b6_mg DECIMAL(10,2) DEFAULT 0,
    vitamin_b12_mcg DECIMAL(10,2) DEFAULT 0,
    folate_mcg DECIMAL(10,2) DEFAULT 0,
    
    -- Other Nutrients
    caffeine_mg DECIMAL(10,2) DEFAULT 0,
    alcohol_g DECIMAL(10,2) DEFAULT 0,
    water_g DECIMAL(10,2) DEFAULT 0,
    
    -- Tags & Categories
    allergens TEXT[],  -- ['dairy', 'gluten', 'nuts', 'soy', 'eggs', 'fish', 'shellfish']
    dietary_flags TEXT[],  -- ['vegan', 'vegetarian', 'gluten-free', 'keto', 'paleo', 'halal', 'kosher']
    ingredients TEXT[],  -- For packaged foods
    
    -- Data Quality & Source
    source VARCHAR(100),  -- 'usda', 'fdc', 'user', 'openfoodfacts', 'nutritionix'
    external_id VARCHAR(255),
    data_quality_score DECIMAL(3,2),  -- 0.00 to 1.00
    verified BOOLEAN DEFAULT false,
    verified_by UUID REFERENCES profiles(id),
    verified_at TIMESTAMPTZ,
    
    -- Ownership & Privacy
    is_public BOOLEAN DEFAULT true,
    created_by UUID REFERENCES profiles(id),
    is_recipe BOOLEAN DEFAULT false,  -- User-created recipe
    
    -- Usage Stats (for smart suggestions)
    popularity_score INT DEFAULT 0,
    global_use_count INT DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT foods_serving_size_positive CHECK (serving_size > 0),
    CONSTRAINT foods_household_grams_positive CHECK (household_serving_grams IS NULL OR household_serving_grams > 0),
    CONSTRAINT foods_food_type_valid CHECK (food_type IN ('ingredient', 'dish', 'branded', 'restaurant')),
    CONSTRAINT foods_data_quality_range CHECK (data_quality_score IS NULL OR (data_quality_score >= 0 AND data_quality_score <= 1))
);

-- Comprehensive Indexes
CREATE INDEX idx_foods_name ON foods(name);
CREATE INDEX idx_foods_name_trgm ON foods USING gin(name gin_trgm_ops);
CREATE INDEX idx_foods_food_type ON foods(food_type);
CREATE INDEX idx_foods_brand ON foods(brand_name) WHERE brand_name IS NOT NULL;
CREATE INDEX idx_foods_restaurant ON foods(restaurant_name) WHERE restaurant_name IS NOT NULL;
CREATE INDEX idx_foods_barcode_upc ON foods(barcode_upc) WHERE barcode_upc IS NOT NULL;
CREATE INDEX idx_foods_barcode_ean ON foods(barcode_ean) WHERE barcode_ean IS NOT NULL;
CREATE INDEX idx_foods_created_by ON foods(created_by);
CREATE INDEX idx_foods_is_public ON foods(is_public);
CREATE INDEX idx_foods_is_recipe ON foods(is_recipe);
CREATE INDEX idx_foods_verified ON foods(verified);
CREATE INDEX idx_foods_popularity ON foods(popularity_score DESC);

-- ============================================================================
-- USER_FAVORITE_FOODS TABLE
-- ============================================================================
-- Track user's starred/favorite foods for quick access
-- ============================================================================

CREATE TABLE user_favorite_foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    food_id UUID NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    favorited_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT user_favorite_foods_unique UNIQUE (user_id, food_id)
);

CREATE INDEX idx_user_favorite_foods_user ON user_favorite_foods(user_id, favorited_at DESC);

-- ============================================================================
-- FOOD_PREFERENCES TABLE (Enhanced with smart suggestions)
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
    
    -- Usage patterns
    use_count INT DEFAULT 1,
    last_meal_category VARCHAR(50),  -- breakfast, lunch, dinner, snack
    typical_meal_categories TEXT[],  -- Most common meal times
    
    -- Smart suggestions
    is_frequent BOOLEAN DEFAULT false,  -- Used > 10 times
    is_recent BOOLEAN DEFAULT true,  -- Used in last 30 days
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT food_preferences_unique UNIQUE (user_id, food_id)
);

CREATE INDEX idx_food_preferences_user ON food_preferences(user_id);
CREATE INDEX idx_food_preferences_user_recent ON food_preferences(user_id, last_used_at DESC);
CREATE INDEX idx_food_preferences_user_frequent ON food_preferences(user_id, use_count DESC) WHERE is_frequent = true;

-- ============================================================================
-- MEAL_TEMPLATES TABLE (Saved meal combinations)
-- ============================================================================
-- "My usual breakfast", "Post-workout meal", etc.
-- ============================================================================

CREATE TABLE meal_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Template Info
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),  -- breakfast, lunch, dinner, snack, other
    tags TEXT[],  -- ['quick', 'meal-prep', 'post-workout']
    
    -- Nutrition (calculated from foods)
    total_calories DECIMAL(10,2) DEFAULT 0,
    total_protein_g DECIMAL(10,2) DEFAULT 0,
    total_carbs_g DECIMAL(10,2) DEFAULT 0,
    total_fat_g DECIMAL(10,2) DEFAULT 0,
    total_fiber_g DECIMAL(10,2) DEFAULT 0,
    
    -- Usage Stats
    use_count INT DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    is_favorite BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_meal_templates_user ON meal_templates(user_id);
CREATE INDEX idx_meal_templates_user_category ON meal_templates(user_id, category);
CREATE INDEX idx_meal_templates_user_favorite ON meal_templates(user_id, is_favorite DESC, last_used_at DESC);

-- ============================================================================
-- MEAL_TEMPLATE_FOODS TABLE
-- ============================================================================

CREATE TABLE meal_template_foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID NOT NULL REFERENCES meal_templates(id) ON DELETE CASCADE,
    food_id UUID NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    
    -- Dual quantity tracking
    serving_quantity DECIMAL(10,3) NOT NULL,
    serving_unit VARCHAR(50),
    gram_quantity DECIMAL(10,2) NOT NULL,
    
    -- Order in template
    display_order INT DEFAULT 0,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_meal_template_foods_template ON meal_template_foods(template_id, display_order);

-- ============================================================================
-- MEALS TABLE (Enhanced)
-- ============================================================================

CREATE TABLE meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Meal Info
    name VARCHAR(255),  -- Optional meal name
    category VARCHAR(50) NOT NULL,
    logged_at TIMESTAMPTZ NOT NULL,
    notes TEXT,
    
    -- Source tracking
    created_from_template_id UUID REFERENCES meal_templates(id),
    copied_from_date DATE,  -- "Copy from yesterday"
    
    -- Total Nutrition (calculated)
    total_calories DECIMAL(10,2) DEFAULT 0,
    total_protein_g DECIMAL(10,2) DEFAULT 0,
    total_carbs_g DECIMAL(10,2) DEFAULT 0,
    total_fat_g DECIMAL(10,2) DEFAULT 0,
    total_fiber_g DECIMAL(10,2) DEFAULT 0,
    total_sugar_g DECIMAL(10,2) DEFAULT 0,
    total_sodium_mg DECIMAL(10,2) DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT meals_category_valid CHECK (category IN ('breakfast', 'lunch', 'dinner', 'snack', 'other'))
);

CREATE INDEX idx_meals_user_id ON meals(user_id);
CREATE INDEX idx_meals_logged_at ON meals(logged_at DESC);
CREATE INDEX idx_meals_user_logged ON meals(user_id, logged_at DESC);
CREATE INDEX idx_meals_user_category ON meals(user_id, category, logged_at DESC);

-- ============================================================================
-- MEAL_FOODS TABLE (Dual quantity tracking)
-- ============================================================================

CREATE TABLE meal_foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_id UUID NOT NULL REFERENCES meals(id) ON DELETE CASCADE,
    food_id UUID NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    
    -- DUAL QUANTITY TRACKING
    serving_quantity DECIMAL(10,3) NOT NULL,
    serving_unit VARCHAR(50),
    gram_quantity DECIMAL(10,2) NOT NULL,
    last_edited_field VARCHAR(20) NOT NULL,
    
    -- Calculated Nutrition
    calories DECIMAL(10,2) NOT NULL DEFAULT 0,
    protein_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    carbs_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    fat_g DECIMAL(10,2) NOT NULL DEFAULT 0,
    fiber_g DECIMAL(10,2) DEFAULT 0,
    sugar_g DECIMAL(10,2) DEFAULT 0,
    sodium_mg DECIMAL(10,2) DEFAULT 0,
    
    -- Order in meal
    display_order INT DEFAULT 0,
    
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT meal_foods_serving_quantity_positive CHECK (serving_quantity > 0),
    CONSTRAINT meal_foods_gram_quantity_positive CHECK (gram_quantity > 0),
    CONSTRAINT meal_foods_last_edited_valid CHECK (last_edited_field IN ('serving', 'grams'))
);

CREATE INDEX idx_meal_foods_meal ON meal_foods(meal_id, display_order);
CREATE INDEX idx_meal_foods_food ON meal_foods(food_id);

-- ============================================================================
-- DAILY_NUTRITION_SUMMARY TABLE
-- ============================================================================
-- Pre-calculated daily totals for performance
-- ============================================================================

CREATE TABLE daily_nutrition_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    
    -- Totals by meal category
    breakfast_calories DECIMAL(10,2) DEFAULT 0,
    lunch_calories DECIMAL(10,2) DEFAULT 0,
    dinner_calories DECIMAL(10,2) DEFAULT 0,
    snacks_calories DECIMAL(10,2) DEFAULT 0,
    
    -- Daily totals
    total_calories DECIMAL(10,2) DEFAULT 0,
    total_protein_g DECIMAL(10,2) DEFAULT 0,
    total_carbs_g DECIMAL(10,2) DEFAULT 0,
    total_fat_g DECIMAL(10,2) DEFAULT 0,
    total_fiber_g DECIMAL(10,2) DEFAULT 0,
    total_sugar_g DECIMAL(10,2) DEFAULT 0,
    total_sodium_mg DECIMAL(10,2) DEFAULT 0,
    
    -- Meal counts
    meals_logged INT DEFAULT 0,
    foods_logged INT DEFAULT 0,
    
    -- Water tracking
    water_ml INT DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT daily_nutrition_summary_unique UNIQUE (user_id, date)
);

CREATE INDEX idx_daily_nutrition_user_date ON daily_nutrition_summary(user_id, date DESC);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_foods_updated_at BEFORE UPDATE ON foods
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_food_preferences_updated_at BEFORE UPDATE ON food_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_meal_templates_updated_at BEFORE UPDATE ON meal_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_meals_updated_at BEFORE UPDATE ON meals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_daily_nutrition_summary_updated_at BEFORE UPDATE ON daily_nutrition_summary
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;

-- ============================================================================
-- SUMMARY
-- ============================================================================

SELECT 
    '✅ COMPREHENSIVE FOOD SYSTEM V2 CREATED!' as status,
    'Ready for MyFitnessPal-level organization with better UX' as description;

SELECT 
    'Tables Created:' as category,
    string_agg(tablename, ', ' ORDER BY tablename) as tables
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN ('foods', 'meals', 'meal_foods', 'meal_templates', 'meal_template_foods', 
                    'food_preferences', 'user_favorite_foods', 'daily_nutrition_summary')
GROUP BY category;
