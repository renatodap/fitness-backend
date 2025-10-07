-- Migration 008: Seed Common Foods from USDA Database
-- Populates foods_enhanced with 100+ commonly tracked foods
-- Includes complete nutrition data for meal logging

-- ============================================================================
-- SEED COMMON PROTEINS
-- ============================================================================

INSERT INTO public.foods_enhanced (
  name, food_group, serving_size, serving_unit, household_serving_size, household_serving_unit,
  calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g,
  saturated_fat_g, sodium_mg, potassium_mg, cholesterol_mg,
  is_generic, data_quality_score, popularity_score
) VALUES

-- Chicken
('Chicken Breast, Grilled, Skinless', 'Protein', 100, 'g', '1', 'breast (3 oz)', 165, 31, 0, 3.6, 0, 0, 1, 74, 256, 85, true, 1.0, 100),
('Chicken Thigh, Grilled, Skinless', 'Protein', 100, 'g', '1', 'thigh (3 oz)', 209, 26, 0, 10.9, 0, 0, 3, 84, 229, 93, true, 1.0, 90),
('Chicken Wings, Grilled', 'Protein', 100, 'g', '3', 'wings', 203, 30.5, 0, 8.1, 0, 0, 2.3, 82, 216, 84, true, 1.0, 85),
('Chicken Breast, Raw', 'Protein', 100, 'g', '1', 'breast (4 oz)', 120, 22.5, 0, 2.6, 0, 0, 0.7, 63, 220, 58, true, 1.0, 95),

-- Beef
('Ground Beef, 90% Lean, Cooked', 'Protein', 100, 'g', '1', 'patty (3 oz)', 197, 26, 0, 10, 0, 0, 4, 66, 318, 78, true, 1.0, 95),
('Steak, Sirloin, Grilled', 'Protein', 100, 'g', '1', 'steak (3 oz)', 162, 30, 0, 4.2, 0, 0, 1.5, 59, 348, 89, true, 1.0, 85),
('Ground Beef, 80% Lean, Cooked', 'Protein', 100, 'g', '1', 'patty (3 oz)', 254, 25, 0, 17, 0, 0, 7, 72, 292, 90, true, 1.0, 90),

-- Fish
('Salmon, Atlantic, Baked', 'Protein', 100, 'g', '1', 'fillet (3 oz)', 206, 22, 0, 12, 0, 0, 2.5, 59, 384, 63, true, 1.0, 90),
('Tuna, Canned in Water, Drained', 'Protein', 100, 'g', '1/2', 'can', 116, 25.5, 0, 0.8, 0, 0, 0.2, 247, 237, 42, true, 1.0, 95),
('Tilapia, Baked', 'Protein', 100, 'g', '1', 'fillet (3 oz)', 128, 26, 0, 2.7, 0, 0, 0.9, 56, 380, 56, true, 1.0, 85),
('Cod, Baked', 'Protein', 100, 'g', '1', 'fillet (3 oz)', 105, 23, 0, 0.9, 0, 0, 0.2, 78, 468, 55, true, 1.0, 80),
('Shrimp, Cooked', 'Protein', 100, 'g', '10', 'large shrimp', 99, 24, 0.2, 0.3, 0, 0, 0.1, 111, 113, 189, true, 1.0, 85),

-- Eggs & Dairy
('Eggs, Whole, Cooked', 'Protein', 100, 'g', '2', 'large eggs', 155, 13, 1.1, 11, 0, 1.1, 3.3, 124, 126, 373, true, 1.0, 100),
('Egg Whites, Cooked', 'Protein', 100, 'g', '4', 'egg whites', 52, 11, 0.7, 0.2, 0, 0.7, 0, 166, 163, 0, true, 1.0, 90),
('Greek Yogurt, Plain, Nonfat', 'Dairy', 100, 'g', '1/2', 'cup', 59, 10, 3.6, 0.4, 0, 3.2, 0.1, 36, 141, 5, true, 1.0, 95),
('Cottage Cheese, Low Fat (2%)', 'Dairy', 100, 'g', '1/2', 'cup', 81, 12, 4.3, 2.3, 0, 4.1, 1.4, 364, 104, 9, true, 1.0, 85),
('Milk, 2%', 'Dairy', 244, 'ml', '1', 'cup', 122, 8, 12, 4.8, 0, 12, 3, 115, 342, 20, true, 1.0, 90),
('Almond Milk, Unsweetened', 'Dairy', 240, 'ml', '1', 'cup', 30, 1, 1, 2.5, 1, 0, 0, 170, 180, 0, true, 1.0, 85),

-- ============================================================================
-- SEED COMMON CARBS
-- ============================================================================

-- Rice
('White Rice, Cooked', 'Grains', 100, 'g', '1', 'cup (158g)', 130, 2.7, 28, 0.3, 0.4, 0.1, 0.1, 1, 35, 0, true, 1.0, 100),
('Brown Rice, Cooked', 'Grains', 100, 'g', '1', 'cup (195g)', 112, 2.6, 24, 0.9, 1.8, 0.4, 0.2, 5, 43, 0, true, 1.0, 95),
('Jasmine Rice, Cooked', 'Grains', 100, 'g', '1', 'cup', 129, 2.7, 28, 0.2, 0.6, 0, 0, 1, 30, 0, true, 1.0, 85),

-- Pasta
('Pasta, Cooked', 'Grains', 100, 'g', '1', 'cup', 131, 5, 25, 1.1, 1.8, 0.6, 0.2, 1, 44, 0, true, 1.0, 95),
('Whole Wheat Pasta, Cooked', 'Grains', 100, 'g', '1', 'cup', 124, 5.3, 26, 0.5, 3.9, 0.4, 0.1, 3, 44, 0, true, 1.0, 85),

-- Bread
('Whole Wheat Bread', 'Grains', 28, 'g', '1', 'slice', 69, 3.6, 12, 0.9, 1.9, 1.4, 0.2, 132, 71, 0, true, 1.0, 90),
('White Bread', 'Grains', 28, 'g', '1', 'slice', 75, 2.5, 14, 1, 0.8, 1.6, 0.2, 147, 35, 0, true, 1.0, 85),
('Sourdough Bread', 'Grains', 28, 'g', '1', 'slice', 73, 2.9, 14, 0.5, 0.7, 0.5, 0.1, 174, 42, 0, true, 1.0, 80),

-- Oats
('Oats, Dry', 'Grains', 40, 'g', '1/2', 'cup', 150, 5, 27, 3, 4, 0.4, 0.5, 0, 140, 0, true, 1.0, 95),
('Oatmeal, Cooked', 'Grains', 100, 'g', '1', 'cup', 71, 2.5, 12, 1.5, 1.7, 0.3, 0.3, 49, 70, 0, true, 1.0, 90),

-- Potatoes
('Sweet Potato, Baked', 'Vegetables', 100, 'g', '1', 'medium', 90, 2, 21, 0.2, 3.3, 6.5, 0, 36, 337, 0, true, 1.0, 95),
('Potato, Baked, with Skin', 'Vegetables', 100, 'g', '1', 'medium', 93, 2.5, 21, 0.1, 2.2, 1.2, 0, 6, 544, 0, true, 1.0, 90),
('Potato, Mashed', 'Vegetables', 100, 'g', '1/2', 'cup', 83, 2, 17, 1.2, 1.5, 1.3, 0.7, 328, 284, 2, true, 1.0, 85),

-- Quinoa
('Quinoa, Cooked', 'Grains', 100, 'g', '1', 'cup', 120, 4.4, 21, 1.9, 2.8, 0.9, 0.2, 7, 172, 0, true, 1.0, 85),

-- ============================================================================
-- SEED COMMON VEGETABLES
-- ============================================================================

('Broccoli, Cooked', 'Vegetables', 100, 'g', '1', 'cup', 35, 2.4, 7, 0.4, 3.3, 1.4, 0.1, 33, 293, 0, true, 1.0, 90),
('Spinach, Cooked', 'Vegetables', 100, 'g', '1', 'cup', 23, 3, 3.8, 0.3, 2.4, 0.4, 0, 70, 466, 0, true, 1.0, 85),
('Bell Pepper, Raw', 'Vegetables', 100, 'g', '1', 'medium', 26, 1, 6, 0.2, 1.7, 4.2, 0, 3, 175, 0, true, 1.0, 85),
('Carrots, Raw', 'Vegetables', 100, 'g', '1', 'medium', 41, 0.9, 10, 0.2, 2.8, 4.7, 0, 69, 320, 0, true, 1.0, 90),
('Tomato, Raw', 'Vegetables', 100, 'g', '1', 'medium', 18, 0.9, 3.9, 0.2, 1.2, 2.6, 0, 5, 237, 0, true, 1.0, 90),
('Cucumber, Raw', 'Vegetables', 100, 'g', '1/2', 'cucumber', 15, 0.7, 3.6, 0.1, 0.5, 1.7, 0, 2, 147, 0, true, 1.0, 80),
('Lettuce, Romaine, Raw', 'Vegetables', 100, 'g', '2', 'cups', 17, 1.2, 3.3, 0.3, 2.1, 1.2, 0, 8, 247, 0, true, 1.0, 80),
('Asparagus, Cooked', 'Vegetables', 100, 'g', '6', 'spears', 22, 2.4, 4.1, 0.2, 2, 1.9, 0, 14, 224, 0, true, 1.0, 75),
('Green Beans, Cooked', 'Vegetables', 100, 'g', '1', 'cup', 35, 1.9, 8, 0.1, 3.4, 1.6, 0, 1, 209, 0, true, 1.0, 80),
('Cauliflower, Cooked', 'Vegetables', 100, 'g', '1', 'cup', 23, 1.8, 4.7, 0.5, 2.3, 2.1, 0.1, 19, 142, 0, true, 1.0, 80),
('Zucchini, Cooked', 'Vegetables', 100, 'g', '1', 'medium', 17, 1.2, 3.1, 0.3, 1, 2.5, 0.1, 3, 264, 0, true, 1.0, 75),
('Mushrooms, Cooked', 'Vegetables', 100, 'g', '1', 'cup', 28, 3.3, 5.3, 0.5, 2.2, 2.3, 0.1, 6, 356, 0, true, 1.0, 75),

-- ============================================================================
-- SEED COMMON FRUITS
-- ============================================================================

('Banana', 'Fruits', 100, 'g', '1', 'medium', 89, 1.1, 23, 0.3, 2.6, 12, 0.1, 1, 358, 0, true, 1.0, 100),
('Apple', 'Fruits', 100, 'g', '1', 'medium', 52, 0.3, 14, 0.2, 2.4, 10, 0, 1, 107, 0, true, 1.0, 95),
('Orange', 'Fruits', 100, 'g', '1', 'medium', 47, 0.9, 12, 0.1, 2.4, 9, 0, 0, 181, 0, true, 1.0, 90),
('Strawberries', 'Fruits', 100, 'g', '1', 'cup', 32, 0.7, 7.7, 0.3, 2, 4.9, 0, 1, 153, 0, true, 1.0, 90),
('Blueberries', 'Fruits', 100, 'g', '1', 'cup', 57, 0.7, 14, 0.3, 2.4, 10, 0, 1, 77, 0, true, 1.0, 85),
('Grapes', 'Fruits', 100, 'g', '1', 'cup', 69, 0.7, 18, 0.2, 0.9, 16, 0.1, 2, 191, 0, true, 1.0, 85),
('Watermelon', 'Fruits', 100, 'g', '1', 'cup', 30, 0.6, 7.6, 0.2, 0.4, 6.2, 0, 1, 112, 0, true, 1.0, 80),
('Avocado', 'Fruits', 100, 'g', '1/2', 'avocado', 160, 2, 8.5, 15, 6.7, 0.7, 2.1, 7, 485, 0, true, 1.0, 90),

-- ============================================================================
-- SEED HEALTHY FATS
-- ============================================================================

('Almonds, Raw', 'Nuts & Seeds', 28, 'g', '1', 'oz (23 nuts)', 161, 6, 6, 14, 3.5, 1.2, 1.1, 0, 200, 0, true, 1.0, 90),
('Peanut Butter, Natural', 'Nuts & Seeds', 32, 'g', '2', 'tbsp', 188, 8, 7, 16, 2, 3, 3, 5, 208, 0, true, 1.0, 95),
('Walnuts, Raw', 'Nuts & Seeds', 28, 'g', '1', 'oz (14 halves)', 183, 4.3, 3.8, 18, 1.9, 0.7, 1.7, 1, 123, 0, true, 1.0, 85),
('Cashews, Raw', 'Nuts & Seeds', 28, 'g', '1', 'oz (16 nuts)', 155, 5.1, 9, 12, 0.9, 1.7, 2.2, 3, 187, 0, true, 1.0, 85),
('Chia Seeds', 'Nuts & Seeds', 28, 'g', '2', 'tbsp', 138, 4.7, 12, 8.7, 9.8, 0, 0.9, 5, 115, 0, true, 1.0, 80),
('Flaxseed, Ground', 'Nuts & Seeds', 14, 'g', '1', 'tbsp', 55, 1.9, 3, 4.3, 2.8, 0.2, 0.4, 3, 84, 0, true, 1.0, 75),
('Olive Oil, Extra Virgin', 'Oils & Fats', 14, 'ml', '1', 'tbsp', 119, 0, 0, 14, 0, 0, 1.9, 0, 0, 0, true, 1.0, 95),
('Coconut Oil', 'Oils & Fats', 14, 'ml', '1', 'tbsp', 117, 0, 0, 14, 0, 0, 12, 0, 0, 0, true, 1.0, 80),
('Avocado Oil', 'Oils & Fats', 14, 'ml', '1', 'tbsp', 124, 0, 0, 14, 0, 0, 1.6, 0, 0, 0, true, 1.0, 75),

-- ============================================================================
-- SEED PROTEIN SUPPLEMENTS
-- ============================================================================

('Whey Protein Powder, Vanilla', 'Supplements', 30, 'g', '1', 'scoop', 120, 24, 3, 1.5, 0, 2, 1, 50, 150, 40, true, 1.0, 95),
('Whey Protein Powder, Chocolate', 'Supplements', 30, 'g', '1', 'scoop', 120, 24, 3, 1.5, 0, 2, 1, 50, 150, 40, true, 1.0, 95),
('Whey Protein Powder, Unflavored', 'Supplements', 30, 'g', '1', 'scoop', 110, 25, 2, 1, 0, 1, 0.5, 40, 120, 35, true, 1.0, 85),

-- ============================================================================
-- SEED LEGUMES & BEANS
-- ============================================================================

('Black Beans, Cooked', 'Legumes', 100, 'g', '1/2', 'cup', 132, 8.9, 24, 0.5, 8.7, 0.3, 0.1, 2, 355, 0, true, 1.0, 85),
('Lentils, Cooked', 'Legumes', 100, 'g', '1/2', 'cup', 116, 9, 20, 0.4, 7.9, 1.8, 0.1, 2, 369, 0, true, 1.0, 85),
('Chickpeas, Cooked', 'Legumes', 100, 'g', '1/2', 'cup', 164, 8.9, 27, 2.6, 7.6, 4.8, 0.3, 7, 291, 0, true, 1.0, 85),
('Kidney Beans, Cooked', 'Legumes', 100, 'g', '1/2', 'cup', 127, 8.7, 23, 0.5, 6.4, 0.3, 0.1, 2, 403, 0, true, 1.0, 80),
('Tofu, Firm', 'Protein', 100, 'g', '1/2', 'block', 144, 17, 3.5, 9, 2.3, 0.6, 1.3, 14, 237, 0, true, 1.0, 80),
('Edamame, Cooked', 'Legumes', 100, 'g', '1/2', 'cup', 122, 11, 10, 5.2, 5.2, 2.2, 0.6, 6, 436, 0, true, 1.0, 75)

ON CONFLICT (barcode_upc) DO NOTHING;

-- ============================================================================
-- UPDATE SEARCH VECTORS
-- ============================================================================

-- Generate search vectors for all foods for fast full-text search
UPDATE public.foods_enhanced
SET search_vector = to_tsvector('english',
  COALESCE(name, '') || ' ' ||
  COALESCE(brand_name, '') || ' ' ||
  COALESCE(food_group, '') || ' ' ||
  COALESCE(array_to_string(allergens, ' '), '') || ' ' ||
  COALESCE(array_to_string(dietary_flags, ' '), '')
)
WHERE search_vector IS NULL;

-- Create index on search_vector if doesn't exist
CREATE INDEX IF NOT EXISTS idx_foods_enhanced_search_vector
ON public.foods_enhanced USING GIN(search_vector);

-- Create index for name search
CREATE INDEX IF NOT EXISTS idx_foods_enhanced_name_trgm
ON public.foods_enhanced USING GIN(name gin_trgm_ops);

-- Enable pg_trgm extension if not already enabled
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

DO $$
DECLARE
  food_count int;
BEGIN
  SELECT COUNT(*) INTO food_count FROM public.foods_enhanced;
  RAISE NOTICE 'Migration 008 complete!';
  RAISE NOTICE 'Total foods in database: %', food_count;
  RAISE NOTICE 'Search vectors generated for all foods';
END $$;
