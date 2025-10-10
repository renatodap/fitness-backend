-- ============================================================================
-- COMPREHENSIVE SEED: Meal Templates (Composite Meals)
-- ============================================================================
-- Purpose: Populate meal_templates with restaurant meals and common combinations
-- Date: 2025-10-09
-- Templates: ~50 meal templates (Restaurant + Community + Custom)
-- Note: Run after all 003* atomic food scripts
-- ============================================================================

-- ============================================================================
-- HELPER: Get food IDs by name (for template foods)
-- ============================================================================

-- This script assumes all atomic foods from 003* scripts are loaded
-- Template structure:
-- 1. Insert meal_template metadata
-- 2. Insert meal_template_foods (links to foods_enhanced)
-- 3. Manually set nutrition totals (no auto-calculation triggers)

-- ============================================================================
-- PART 1: COMMUNITY TEMPLATES (Popular Meal Combinations) - 15 templates
-- ============================================================================

-- Template 1: Classic Protein Shake
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000001',
    NULL,
    'Classic Protein Shake',
    'snack',
    'Post-workout protein shake: 1 scoop whey + 1 cup whole milk + 1 banana',
    true, false, 'community', 100,
    '{breakfast,snack}', '{high-protein,post-workout}',
    '{post-workout,quick,high-protein}',
    364, 34, 55, 9, 3.1
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000001',
    id,
    CASE name
        WHEN 'Whey Protein Isolate' THEN 30
        WHEN 'Whole Milk' THEN 240
        WHEN 'Banana' THEN 118
    END,
    CASE name
        WHEN 'Whey Protein Isolate' THEN 'g'
        WHEN 'Whole Milk' THEN 'ml'
        WHEN 'Banana' THEN 'g'
    END,
    CASE name
        WHEN 'Whey Protein Isolate' THEN 1
        WHEN 'Whole Milk' THEN 2
        WHEN 'Banana' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Whey Protein Isolate', 'Whole Milk', 'Banana');

-- Template 2: Chicken & Rice Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000002',
    NULL,
    'Chicken & Rice Bowl',
    'lunch',
    'Simple meal prep staple: 6oz chicken breast + 1 cup brown rice + 1 cup broccoli',
    true, false, 'community', 95,
    '{lunch,dinner}', '{high-protein,balanced}',
    '{meal-prep,balanced,clean-eating}',
    447, 58, 50, 6, 7.4
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000002',
    id,
    CASE name
        WHEN 'Chicken Breast' THEN 170
        WHEN 'Brown Rice (Cooked)' THEN 200
        WHEN 'Broccoli (Cooked)' THEN 100
    END,
    'g',
    CASE name
        WHEN 'Chicken Breast' THEN 1
        WHEN 'Brown Rice (Cooked)' THEN 2
        WHEN 'Broccoli (Cooked)' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Chicken Breast', 'Brown Rice (Cooked)', 'Broccoli (Cooked)');

-- Template 3: Oatmeal Power Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000003',
    NULL,
    'Oatmeal Power Bowl',
    'breakfast',
    'Protein-packed breakfast: 1 cup oatmeal + 1 scoop whey + 1 tbsp peanut butter + blueberries',
    true, false, 'community', 90,
    '{breakfast}', '{high-protein,high-fiber}',
    '{breakfast,filling,balanced}',
    489, 40, 52, 14, 7.3
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000003',
    id,
    CASE name
        WHEN 'Oatmeal (Cooked)' THEN 200
        WHEN 'Whey Protein Isolate' THEN 30
        WHEN 'Peanut Butter (Natural)' THEN 16
        WHEN 'Blueberries' THEN 100
    END,
    CASE name
        WHEN 'Oatmeal (Cooked)' THEN 'g'
        WHEN 'Whey Protein Isolate' THEN 'g'
        WHEN 'Peanut Butter (Natural)' THEN 'g'
        WHEN 'Blueberries' THEN 'g'
    END,
    CASE name
        WHEN 'Oatmeal (Cooked)' THEN 1
        WHEN 'Whey Protein Isolate' THEN 2
        WHEN 'Peanut Butter (Natural)' THEN 3
        WHEN 'Blueberries' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Oatmeal (Cooked)', 'Whey Protein Isolate', 'Peanut Butter (Natural)', 'Blueberries');

-- Template 4: Salmon & Quinoa Plate
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000004',
    NULL,
    'Salmon & Quinoa Plate',
    'dinner',
    'Heart-healthy dinner: 6oz wild salmon + 1 cup quinoa + asparagus',
    true, false, 'community', 85,
    '{lunch,dinner}', '{omega-3,balanced,heart-healthy}',
    '{omega-3,clean-eating,balanced}',
    521, 54, 45, 15, 7.4
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000004',
    id,
    CASE name
        WHEN 'Salmon (Wild)' THEN 170
        WHEN 'Quinoa (Cooked)' THEN 200
        WHEN 'Asparagus (Cooked)' THEN 100
    END,
    'g',
    CASE name
        WHEN 'Salmon (Wild)' THEN 1
        WHEN 'Quinoa (Cooked)' THEN 2
        WHEN 'Asparagus (Cooked)' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Salmon (Wild)', 'Quinoa (Cooked)', 'Asparagus (Cooked)');

-- Template 5: Greek Yogurt Parfait
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000005',
    NULL,
    'Greek Yogurt Parfait',
    'breakfast',
    'High-protein breakfast: 1 cup Greek yogurt + granola + strawberries + honey',
    true, false, 'community', 88,
    '{breakfast,snack}', '{high-protein,vegetarian}',
    '{breakfast,quick,high-protein}',
    337, 22, 51, 5, 4.5
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000005',
    id,
    CASE name
        WHEN 'Greek Yogurt (Nonfat)' THEN 200
        WHEN 'Strawberries' THEN 100
        WHEN 'Honey' THEN 21
    END,
    CASE name
        WHEN 'Greek Yogurt (Nonfat)' THEN 'g'
        WHEN 'Strawberries' THEN 'g'
        WHEN 'Honey' THEN 'g'
    END,
    CASE name
        WHEN 'Greek Yogurt (Nonfat)' THEN 1
        WHEN 'Strawberries' THEN 2
        WHEN 'Honey' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Greek Yogurt (Nonfat)', 'Strawberries', 'Honey');

-- Template 6: Steak & Sweet Potato
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000006',
    NULL,
    'Steak & Sweet Potato',
    'dinner',
    'Classic dinner: 8oz sirloin steak + 1 medium sweet potato + green beans',
    true, false, 'community', 82,
    '{dinner}', '{high-protein,balanced}',
    '{dinner,satisfying,balanced}',
    559, 63, 48, 14, 10.1
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000006',
    id,
    CASE name
        WHEN 'Sirloin Steak' THEN 226
        WHEN 'Sweet Potato (Baked)' THEN 200
        WHEN 'Green Beans (Cooked)' THEN 100
    END,
    'g',
    CASE name
        WHEN 'Sirloin Steak' THEN 1
        WHEN 'Sweet Potato (Baked)' THEN 2
        WHEN 'Green Beans (Cooked)' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Sirloin Steak', 'Sweet Potato (Baked)', 'Green Beans (Cooked)');

-- Template 7: Egg White Scramble
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000007',
    NULL,
    'Egg White Veggie Scramble',
    'breakfast',
    'Low-cal breakfast: 6 egg whites + spinach + bell peppers + whole wheat toast',
    true, false, 'community', 80,
    '{breakfast}', '{high-protein,low-fat}',
    '{breakfast,lean,high-protein}',
    221, 28, 25, 3, 5.3
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000007',
    id,
    CASE name
        WHEN 'Egg White' THEN 198
        WHEN 'Spinach (Raw)' THEN 50
        WHEN 'Bell Pepper (Red)' THEN 50
        WHEN 'Whole Wheat Bread' THEN 28
    END,
    CASE name
        WHEN 'Whole Wheat Bread' THEN 'g'
        ELSE 'g'
    END,
    CASE name
        WHEN 'Egg White' THEN 1
        WHEN 'Spinach (Raw)' THEN 2
        WHEN 'Bell Pepper (Red)' THEN 3
        WHEN 'Whole Wheat Bread' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Egg White', 'Spinach (Raw)', 'Bell Pepper (Red)', 'Whole Wheat Bread');

-- Template 8: Turkey Wrap
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000008',
    NULL,
    'Turkey & Avocado Wrap',
    'lunch',
    'Quick lunch: 4oz turkey breast + avocado + whole wheat tortilla + veggies',
    true, false, 'community', 78,
    '{lunch}', '{high-protein,balanced}',
    '{lunch,quick,portable}',
    394, 38, 31, 14, 9
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000008',
    id,
    CASE name
        WHEN 'Turkey Breast' THEN 113
        WHEN 'Avocado' THEN 50
        WHEN 'Tortilla (Whole Wheat)' THEN 46
        WHEN 'Romaine Lettuce' THEN 50
    END,
    'g',
    CASE name
        WHEN 'Turkey Breast' THEN 1
        WHEN 'Avocado' THEN 2
        WHEN 'Tortilla (Whole Wheat)' THEN 3
        WHEN 'Romaine Lettuce' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Turkey Breast', 'Avocado', 'Tortilla (Whole Wheat)', 'Romaine Lettuce');

-- Template 9: Tuna Salad
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000009',
    NULL,
    'Classic Tuna Salad',
    'lunch',
    'Simple lunch: 1 can tuna + mixed greens + cucumber + tomato + olive oil',
    true, false, 'community', 75,
    '{lunch}', '{high-protein,omega-3}',
    '{lunch,quick,omega-3}',
    268, 28, 11, 14, 3.6
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000009',
    id,
    CASE name
        WHEN 'Tuna (Canned in Water)' THEN 100
        WHEN 'Mixed Greens' THEN 100
        WHEN 'Cucumber' THEN 50
        WHEN 'Cherry Tomatoes' THEN 50
        WHEN 'Olive Oil (Extra Virgin)' THEN 14
    END,
    CASE name
        WHEN 'Olive Oil (Extra Virgin)' THEN 'g'
        ELSE 'g'
    END,
    CASE name
        WHEN 'Tuna (Canned in Water)' THEN 1
        WHEN 'Mixed Greens' THEN 2
        WHEN 'Cucumber' THEN 3
        WHEN 'Cherry Tomatoes' THEN 4
        WHEN 'Olive Oil (Extra Virgin)' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Tuna (Canned in Water)', 'Mixed Greens', 'Cucumber', 'Cherry Tomatoes', 'Olive Oil (Extra Virgin)');

-- Template 10: Shrimp Stir Fry
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '10000000-0000-0000-0000-000000000010',
    NULL,
    'Shrimp Stir Fry',
    'dinner',
    'Quick dinner: 6oz shrimp + jasmine rice + mixed vegetables + sesame oil',
    true, false, 'community', 72,
    '{lunch,dinner}', '{high-protein,balanced}',
    '{dinner,quick,asian-inspired}',
    453, 44, 52, 9, 4.2
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '10000000-0000-0000-0000-000000000010',
    id,
    CASE name
        WHEN 'Shrimp' THEN 170
        WHEN 'Jasmine Rice (Cooked)' THEN 200
        WHEN 'Broccoli (Cooked)' THEN 100
        WHEN 'Bell Pepper (Red)' THEN 50
        WHEN 'Sesame Oil' THEN 14
    END,
    CASE name
        WHEN 'Sesame Oil' THEN 'g'
        ELSE 'g'
    END,
    CASE name
        WHEN 'Shrimp' THEN 1
        WHEN 'Jasmine Rice (Cooked)' THEN 2
        WHEN 'Broccoli (Cooked)' THEN 3
        WHEN 'Bell Pepper (Red)' THEN 4
        WHEN 'Sesame Oil' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Shrimp', 'Jasmine Rice (Cooked)', 'Broccoli (Cooked)', 'Bell Pepper (Red)', 'Sesame Oil');

-- ============================================================================
-- PART 2: RESTAURANT TEMPLATES (Chipotle, Subway, etc.) - 20 templates
-- ============================================================================

-- Chipotle Template 1: Chicken Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000001',
    NULL,
    'Chipotle Chicken Bowl',
    'lunch',
    'Chipotle bowl: Chicken + white rice + black beans + salsa + cheese + lettuce',
    true, true, 'Chipotle', 'restaurant', 100,
    '{lunch,dinner}', '{high-protein}',
    '{chipotle,fast-casual,customizable}',
    665, 50, 78, 17, 14
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000001',
    id,
    CASE name
        WHEN 'Chicken Breast' THEN 113
        WHEN 'White Rice (Cooked)' THEN 150
        WHEN 'Black Beans (Cooked)' THEN 100
        WHEN 'Romaine Lettuce' THEN 50
    END,
    'g',
    CASE name
        WHEN 'Chicken Breast' THEN 1
        WHEN 'White Rice (Cooked)' THEN 2
        WHEN 'Black Beans (Cooked)' THEN 3
        WHEN 'Romaine Lettuce' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Chicken Breast', 'White Rice (Cooked)', 'Black Beans (Cooked)', 'Romaine Lettuce');

-- Chipotle Template 2: Steak Bowl (No Rice)
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000002',
    NULL,
    'Chipotle Steak Bowl (No Rice)',
    'lunch',
    'Low-carb Chipotle: Steak + lettuce + black beans + guacamole + salsa',
    true, true, 'Chipotle', 'restaurant', 95,
    '{lunch,dinner}', '{high-protein,low-carb}',
    '{chipotle,low-carb,keto-friendly}',
    485, 35, 28, 27, 14
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000002',
    id,
    CASE name
        WHEN 'Flank Steak' THEN 113
        WHEN 'Black Beans (Cooked)' THEN 100
        WHEN 'Romaine Lettuce' THEN 100
        WHEN 'Avocado' THEN 60
    END,
    'g',
    CASE name
        WHEN 'Flank Steak' THEN 1
        WHEN 'Black Beans (Cooked)' THEN 2
        WHEN 'Romaine Lettuce' THEN 3
        WHEN 'Avocado' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Flank Steak', 'Black Beans (Cooked)', 'Romaine Lettuce', 'Avocado');

-- Chipotle Template 3: Carnitas Burrito Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000003',
    NULL,
    'Chipotle Carnitas Bowl',
    'lunch',
    'Chipotle: Carnitas + brown rice + pinto beans + salsa + sour cream',
    true, true, 'Chipotle', 'restaurant', 88,
    '{lunch,dinner}', '{high-protein}',
    '{chipotle,hearty}',
    710, 41, 72, 28, 12
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000003',
    id,
    CASE name
        WHEN 'Pork Shoulder' THEN 113
        WHEN 'Brown Rice (Cooked)' THEN 150
        WHEN 'Black Beans (Cooked)' THEN 100
        WHEN 'Sour Cream' THEN 28
    END,
    'g',
    CASE name
        WHEN 'Pork Shoulder' THEN 1
        WHEN 'Brown Rice (Cooked)' THEN 2
        WHEN 'Black Beans (Cooked)' THEN 3
        WHEN 'Sour Cream' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Pork Shoulder', 'Brown Rice (Cooked)', 'Black Beans (Cooked)', 'Sour Cream');

-- Subway Template 1: Turkey Footlong
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000004',
    NULL,
    'Subway Turkey Footlong',
    'lunch',
    'Subway: Turkey breast on 9-grain wheat + veggies + mustard',
    true, true, 'Subway', 'restaurant', 85,
    '{lunch}', '{high-protein,lean}',
    '{subway,sandwich}',
    560, 50, 80, 8, 10
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000004',
    id,
    CASE name
        WHEN 'Turkey Breast' THEN 170
        WHEN 'Whole Wheat Bread' THEN 168
        WHEN 'Romaine Lettuce' THEN 30
        WHEN 'Tomato' THEN 50
        WHEN 'Mustard (Yellow)' THEN 5
    END,
    'g',
    CASE name
        WHEN 'Turkey Breast' THEN 1
        WHEN 'Whole Wheat Bread' THEN 2
        WHEN 'Romaine Lettuce' THEN 3
        WHEN 'Tomato' THEN 4
        WHEN 'Mustard (Yellow)' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Turkey Breast', 'Whole Wheat Bread', 'Romaine Lettuce', 'Tomato', 'Mustard (Yellow)');

-- Subway Template 2: Chicken Teriyaki Sub
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000005',
    NULL,
    'Subway Chicken Teriyaki (6 inch)',
    'lunch',
    'Subway: Grilled chicken on wheat + veggies + teriyaki sauce',
    true, true, 'Subway', 'restaurant', 80,
    '{lunch}', '{high-protein}',
    '{subway,sandwich,asian-inspired}',
    380, 28, 58, 5, 5
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000005',
    id,
    CASE name
        WHEN 'Chicken Breast' THEN 85
        WHEN 'Whole Wheat Bread' THEN 84
        WHEN 'Romaine Lettuce' THEN 20
        WHEN 'Tomato' THEN 30
        WHEN 'Soy Sauce' THEN 15
    END,
    CASE name
        WHEN 'Soy Sauce' THEN 'ml'
        ELSE 'g'
    END,
    CASE name
        WHEN 'Chicken Breast' THEN 1
        WHEN 'Whole Wheat Bread' THEN 2
        WHEN 'Romaine Lettuce' THEN 3
        WHEN 'Tomato' THEN 4
        WHEN 'Soy Sauce' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Chicken Breast', 'Whole Wheat Bread', 'Romaine Lettuce', 'Tomato', 'Soy Sauce');

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Count templates by source
SELECT
    source,
    COUNT(*) AS template_count,
    AVG(total_calories) AS avg_calories,
    AVG(total_protein_g) AS avg_protein
FROM meal_templates
WHERE is_public = true
GROUP BY source
ORDER BY template_count DESC;

-- Count templates by restaurant
SELECT
    restaurant_name,
    COUNT(*) AS template_count
FROM meal_templates
WHERE is_restaurant = true
GROUP BY restaurant_name
ORDER BY template_count DESC;

-- Templates with foods count
SELECT
    mt.name,
    mt.source,
    COUNT(mtf.id) AS food_count,
    mt.total_calories
FROM meal_templates mt
LEFT JOIN meal_template_foods mtf ON mtf.meal_template_id = mt.id
WHERE mt.is_public = true
GROUP BY mt.id, mt.name, mt.source, mt.total_calories
ORDER BY food_count DESC;

-- Check for templates with missing foods
SELECT
    mt.name,
    COUNT(mtf.id) AS food_count
FROM meal_templates mt
LEFT JOIN meal_template_foods mtf ON mtf.meal_template_id = mt.id
WHERE mt.is_public = true
GROUP BY mt.id, mt.name
HAVING COUNT(mtf.id) = 0;

-- ============================================================================
-- END COMPREHENSIVE MEAL TEMPLATES SEED
-- Total: ~15 public meal templates (10 community + 5 restaurant)
-- Note: Add more restaurant templates (McDonald's, Starbucks, etc.) as needed
-- ============================================================================
