-- ============================================================================
-- SEED DATA: Foods with Intuitive Household Units
-- ============================================================================
-- Purpose: Populate foods table with common foods using intuitive units
-- Design Philosophy: Users think in "slices", "scoops", "medium" not grams
-- Date: 2025-01-10
-- ============================================================================

BEGIN;

-- ============================================================================
-- DISHES (Generic prepared foods)
-- ============================================================================

INSERT INTO foods (name, food_type, brand_name, household_serving_unit, household_serving_grams, serving_size, serving_unit, calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, source, verified) VALUES
('Pepperoni Pizza', 'dish', NULL, 'slice', 107, 100, 'g', 298, 13.0, 34.0, 12.0, 2.0, 'usda', true),
('Cheese Pizza', 'dish', NULL, 'slice', 107, 100, 'g', 266, 11.0, 33.0, 10.0, 2.0, 'usda', true),
('Cheeseburger', 'dish', NULL, 'burger', 150, 100, 'g', 295, 17.0, 28.0, 12.0, 1.5, 'usda', true),
('Taco', 'dish', NULL, 'taco', 80, 100, 'g', 226, 9.0, 20.0, 13.0, 2.0, 'usda', true),

-- ============================================================================
-- INGREDIENTS (Whole foods)
-- ============================================================================

('Whole Wheat Bread', 'ingredient', NULL, 'slice', 28, 100, 'g', 247, 13.0, 41.0, 3.4, 7.0, 'usda', true),
('White Bread', 'ingredient', NULL, 'slice', 28, 100, 'g', 265, 9.0, 49.0, 3.2, 2.4, 'usda', true),
('Bagel', 'ingredient', NULL, 'bagel', 95, 100, 'g', 257, 10.0, 50.0, 1.5, 2.1, 'usda', true),

('Chicken Breast (Raw)', 'ingredient', NULL, 'breast', 174, 100, 'g', 165, 31.0, 0, 3.6, 0, 'usda', true),
('Chicken Breast (Cooked)', 'ingredient', NULL, 'breast', 140, 100, 'g', 165, 31.0, 0, 3.6, 0, 'usda', true),
('Ground Beef (80/20)', 'ingredient', NULL, 'patty', 113, 100, 'g', 254, 17.2, 0, 20.0, 0, 'usda', true),
('Salmon Fillet', 'ingredient', NULL, 'fillet', 178, 100, 'g', 208, 20.0, 0, 13.4, 0, 'usda', true),
('Eggs (Large)', 'ingredient', NULL, 'egg', 50, 100, 'g', 143, 12.6, 0.7, 9.5, 0, 'usda', true),
('Tuna (Canned)', 'ingredient', NULL, 'can', 142, 100, 'g', 116, 26.0, 0, 0.8, 0, 'usda', true),

-- ============================================================================
-- BRANDED FOODS (Packaged products)
-- ============================================================================

('Greek Yogurt (Plain)', 'branded', 'Fage', NULL, 'container', 170, 100, 'g', 97, 10.0, 3.6, 5.0, 0, 'usda', true),
('Whey Protein Powder', 'branded', 'Optimum Nutrition Gold Standard', NULL, 'scoop', 30, 100, 'g', 400, 80.0, 10.0, 3.3, 0, 'custom', true),
('Whey Protein Powder', 'branded', 'MyProtein Impact Whey', NULL, 'scoop', 25, 100, 'g', 412, 82.0, 4.0, 7.5, 0, 'custom', true),
('Casein Protein Powder', 'branded', 'Optimum Nutrition', NULL, 'scoop', 34, 100, 'g', 353, 76.5, 11.8, 2.9, 0, 'custom', true),
('Plant Protein Powder', 'branded', 'Vega Sport', NULL, 'scoop', 44, 100, 'g', 386, 68.2, 13.6, 9.1, 11.4, 'custom', true),
('Protein Bar', 'branded', 'Quest', NULL, 'bar', 60, 100, 'g', 350, 33.3, 38.3, 10.0, 28.3, 'custom', true),
('Protein Bar', 'branded', 'RxBar', NULL, 'bar', 52, 100, 'g', 404, 23.1, 44.2, 14.4, 9.6, 'custom', true),

('Banana', 'ingredient', NULL, NULL, 'medium', 118, 100, 'g', 89, 1.1, 22.8, 0.3, 2.6, 'usda', true),
('Apple', 'ingredient', NULL, NULL, 'medium', 182, 100, 'g', 52, 0.3, 13.8, 0.2, 2.4, 'usda', true),
('Orange', 'ingredient', NULL, NULL, 'medium', 131, 100, 'g', 47, 0.9, 11.8, 0.1, 2.4, 'usda', true),
('Strawberries', 'ingredient', NULL, NULL, 'cup', 152, 100, 'g', 32, 0.7, 7.7, 0.3, 2.0, 'usda', true),
('Blueberries', 'ingredient', NULL, NULL, 'cup', 148, 100, 'g', 57, 0.7, 14.5, 0.3, 2.4, 'usda', true),
('Avocado', 'ingredient', NULL, NULL, 'medium', 150, 100, 'g', 160, 2.0, 8.5, 14.7, 6.7, 'usda', true),

('Broccoli (Cooked)', 'ingredient', NULL, NULL, 'cup', 156, 100, 'g', 35, 2.4, 7.2, 0.4, 3.3, 'usda', true),
('Spinach (Raw)', 'ingredient', NULL, NULL, 'cup', 30, 100, 'g', 23, 2.9, 3.6, 0.4, 2.2, 'usda', true),
('Sweet Potato (Baked)', 'ingredient', NULL, NULL, 'medium', 114, 100, 'g', 90, 2.0, 20.7, 0.2, 3.3, 'usda', true),
('Carrots (Raw)', 'ingredient', NULL, NULL, 'medium', 61, 100, 'g', 41, 0.9, 9.6, 0.2, 2.8, 'usda', true),
('Bell Pepper (Red)', 'ingredient', NULL, NULL, 'medium', 119, 100, 'g', 31, 1.0, 6.0, 0.3, 2.1, 'usda', true),

('White Rice (Cooked)', 'ingredient', NULL, NULL, 'cup', 158, 100, 'g', 130, 2.7, 28.2, 0.3, 0.4, 'usda', true),
('Brown Rice (Cooked)', 'ingredient', NULL, NULL, 'cup', 195, 100, 'g', 112, 2.3, 23.5, 0.9, 1.8, 'usda', true),
('Pasta (Cooked)', 'ingredient', NULL, NULL, 'cup', 140, 100, 'g', 131, 5.0, 25.1, 1.1, 1.8, 'usda', true),
('Quinoa (Cooked)', 'ingredient', NULL, NULL, 'cup', 185, 100, 'g', 120, 4.4, 21.3, 1.9, 2.8, 'usda', true),
('Oatmeal (Cooked)', 'ingredient', NULL, NULL, 'cup', 234, 100, 'g', 71, 2.5, 12.0, 1.5, 1.7, 'usda', true),
('Oats (Raw)', 'ingredient', NULL, NULL, 'cup', 81, 100, 'g', 379, 13.2, 67.7, 6.5, 10.1, 'usda', true),

('Almonds', 'ingredient', NULL, NULL, 'handful', 28, 100, 'g', 579, 21.2, 21.6, 49.9, 12.5, 'usda', true),
('Peanut Butter', 'ingredient', 'Natural', NULL, 'tbsp', 16, 100, 'g', 588, 25.1, 19.6, 50.0, 6.0, 'usda', true),
('Cashews', 'ingredient', NULL, NULL, 'handful', 28, 100, 'g', 553, 18.2, 30.2, 43.9, 3.3, 'usda', true),
('Walnuts', 'ingredient', NULL, NULL, 'handful', 28, 100, 'g', 654, 15.2, 13.7, 65.2, 6.7, 'usda', true),
('Chia Seeds', 'ingredient', NULL, NULL, 'tbsp', 12, 100, 'g', 486, 16.5, 42.1, 30.7, 34.4, 'usda', true),

('Milk (Whole)', 'ingredient', NULL, NULL, 'cup', 244, 100, 'g', 61, 3.2, 4.8, 3.3, 0, 'usda', true),
('Milk (2%)', 'ingredient', NULL, NULL, 'cup', 244, 100, 'g', 50, 3.3, 4.7, 2.0, 0, 'usda', true),
('Almond Milk (Unsweetened)', 'ingredient', NULL, NULL, 'cup', 240, 100, 'g', 15, 0.6, 0.6, 1.1, 0.2, 'usda', true),
('Cheddar Cheese', 'ingredient', NULL, NULL, 'slice', 28, 100, 'g', 403, 24.9, 1.3, 33.1, 0, 'usda', true),
('Cottage Cheese (Low Fat)', 'ingredient', NULL, NULL, 'cup', 226, 100, 'g', 72, 12.4, 4.3, 1.0, 0, 'usda', true),

('Dark Chocolate', 'ingredient', '70% Cacao', NULL, 'square', 10, 100, 'g', 598, 7.8, 45.8, 42.6, 11.0, 'usda', true),
('Granola', 'ingredient', NULL, NULL, 'cup', 61, 100, 'g', 471, 13.7, 64.4, 19.7, 8.9, 'usda', true);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Count foods by household unit
SELECT household_serving_unit, COUNT(*) as count
FROM foods
GROUP BY household_serving_unit
ORDER BY count DESC;

-- Show sample foods with their intuitive units
SELECT 
    name,
    household_serving_unit,
    household_serving_grams,
    ROUND(calories, 0) as cal_per_100g,
    ROUND(protein_g, 1) as protein_per_100g
FROM foods
ORDER BY name
LIMIT 20;

COMMIT;

-- Success message
DO $$
DECLARE
    food_count INT;
BEGIN
    SELECT COUNT(*) INTO food_count FROM foods;
    RAISE NOTICE '✅ Seed data loaded successfully!';
    RAISE NOTICE '📊 Total foods: %', food_count;
    RAISE NOTICE '🍕 Pizza: slice (107g)';
    RAISE NOTICE '🥄 Whey Protein: scoop (30g)';
    RAISE NOTICE '🍌 Banana: medium (118g)';
    RAISE NOTICE '🥚 Egg: egg (50g)';
    RAISE NOTICE '🍞 Bread: slice (28g)';
    RAISE NOTICE '🚀 Ready for intuitive food logging!';
END $$;
