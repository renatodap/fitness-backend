-- ============================================================================
-- COMPREHENSIVE SEED: More Restaurant Templates
-- ============================================================================
-- Purpose: Add more popular restaurant meal templates
-- Date: 2025-10-09
-- Templates: ~15 additional restaurant templates (Starbucks, McDonald's, etc.)
-- Note: Run after 004_COMPREHENSIVE_seed_meal_templates.sql
-- ============================================================================

-- ============================================================================
-- STARBUCKS TEMPLATES (5 templates)
-- ============================================================================

-- Starbucks 1: Egg White Bites
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000006',
    NULL,
    'Starbucks Egg White Bites (2 pack)',
    'breakfast',
    'Starbucks: Egg white & roasted red pepper bites',
    true, true, 'Starbucks', 'restaurant', 90,
    '{breakfast,snack}', '{high-protein,vegetarian}',
    '{starbucks,breakfast,grab-and-go}',
    170, 13, 13, 7, 0
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000006',
    id,
    CASE name
        WHEN 'Egg White' THEN 132
        WHEN 'Bell Pepper (Red)' THEN 30
        WHEN 'Cottage Cheese (1%)' THEN 50
    END,
    'g',
    CASE name
        WHEN 'Egg White' THEN 1
        WHEN 'Bell Pepper (Red)' THEN 2
        WHEN 'Cottage Cheese (1%)' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Egg White', 'Bell Pepper (Red)', 'Cottage Cheese (1%)');

-- Starbucks 2: Protein Box
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000007',
    NULL,
    'Starbucks Chicken & Quinoa Protein Bowl',
    'lunch',
    'Starbucks: Chicken, quinoa, vegetables, and vinaigrette',
    true, true, 'Starbucks', 'restaurant', 85,
    '{lunch,snack}', '{high-protein,balanced}',
    '{starbucks,balanced,grab-and-go}',
    420, 32, 43, 14, 7
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000007',
    id,
    CASE name
        WHEN 'Chicken Breast' THEN 100
        WHEN 'Quinoa (Cooked)' THEN 100
        WHEN 'Kale (Raw)' THEN 50
        WHEN 'Olive Oil (Extra Virgin)' THEN 14
    END,
    'g',
    CASE name
        WHEN 'Chicken Breast' THEN 1
        WHEN 'Quinoa (Cooked)' THEN 2
        WHEN 'Kale (Raw)' THEN 3
        WHEN 'Olive Oil (Extra Virgin)' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Chicken Breast', 'Quinoa (Cooked)', 'Kale (Raw)', 'Olive Oil (Extra Virgin)');

-- Starbucks 3: Oatmeal
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000008',
    NULL,
    'Starbucks Classic Oatmeal',
    'breakfast',
    'Starbucks: Steel cut oats with brown sugar and dried fruit',
    true, true, 'Starbucks', 'restaurant', 82,
    '{breakfast}', '{vegetarian}',
    '{starbucks,breakfast,warm}',
    160, 5, 28, 2.5, 4
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000008',
    id,
    CASE name
        WHEN 'Steel Cut Oats (Cooked)' THEN 200
    END,
    'g',
    1
FROM foods_enhanced
WHERE name IN ('Steel Cut Oats (Cooked)');

-- Starbucks 4: Reduced-Fat Turkey Bacon Sandwich
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000009',
    NULL,
    'Starbucks Turkey Bacon Breakfast Sandwich',
    'breakfast',
    'Starbucks: Turkey bacon, egg whites, and reduced-fat cheese on English muffin',
    true, true, 'Starbucks', 'restaurant', 78,
    '{breakfast}', '{high-protein}',
    '{starbucks,breakfast,sandwich}',
    230, 17, 28, 5, 3
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000009',
    id,
    CASE name
        WHEN 'Egg White' THEN 66
        WHEN 'Canadian Bacon' THEN 30
        WHEN 'English Muffin' THEN 57
    END,
    'g',
    CASE name
        WHEN 'Egg White' THEN 1
        WHEN 'Canadian Bacon' THEN 2
        WHEN 'English Muffin' THEN 3
    END
FROM foods_enhanced
WHERE name IN ('Egg White', 'Canadian Bacon', 'English Muffin');

-- Starbucks 5: Grilled Chicken Wrap
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000010',
    NULL,
    'Starbucks Grilled Chicken Wrap',
    'lunch',
    'Starbucks: Grilled chicken, hummus, and vegetables in a tortilla',
    true, true, 'Starbucks', 'restaurant', 75,
    '{lunch}', '{high-protein}',
    '{starbucks,wrap,lunch}',
    330, 21, 41, 9, 6
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000010',
    id,
    CASE name
        WHEN 'Chicken Breast' THEN 85
        WHEN 'Tortilla (Whole Wheat)' THEN 46
        WHEN 'Hummus' THEN 50
        WHEN 'Romaine Lettuce' THEN 30
    END,
    'g',
    CASE name
        WHEN 'Chicken Breast' THEN 1
        WHEN 'Tortilla (Whole Wheat)' THEN 2
        WHEN 'Hummus' THEN 3
        WHEN 'Romaine Lettuce' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Chicken Breast', 'Tortilla (Whole Wheat)', 'Hummus', 'Romaine Lettuce');

-- ============================================================================
-- PANERA BREAD TEMPLATES (5 templates)
-- ============================================================================

-- Panera 1: Mediterranean Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000011',
    NULL,
    'Panera Mediterranean Bowl',
    'lunch',
    'Panera: Quinoa, greens, hummus, cucumber, tomato, feta',
    true, true, 'Panera Bread', 'restaurant', 88,
    '{lunch,dinner}', '{vegetarian,balanced}',
    '{panera,mediterranean,vegetarian}',
    510, 17, 52, 27, 11
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000011',
    id,
    CASE name
        WHEN 'Quinoa (Cooked)' THEN 150
        WHEN 'Mixed Greens' THEN 100
        WHEN 'Hummus' THEN 80
        WHEN 'Cucumber' THEN 50
        WHEN 'Cherry Tomatoes' THEN 50
        WHEN 'Olive Oil (Extra Virgin)' THEN 14
    END,
    'g',
    CASE name
        WHEN 'Quinoa (Cooked)' THEN 1
        WHEN 'Mixed Greens' THEN 2
        WHEN 'Hummus' THEN 3
        WHEN 'Cucumber' THEN 4
        WHEN 'Cherry Tomatoes' THEN 5
        WHEN 'Olive Oil (Extra Virgin)' THEN 6
    END
FROM foods_enhanced
WHERE name IN ('Quinoa (Cooked)', 'Mixed Greens', 'Hummus', 'Cucumber', 'Cherry Tomatoes', 'Olive Oil (Extra Virgin)');

-- Panera 2: Greek Salad
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000012',
    NULL,
    'Panera Greek Salad',
    'lunch',
    'Panera: Romaine, tomato, cucumber, olives, feta, Greek dressing',
    true, true, 'Panera Bread', 'restaurant', 83,
    '{lunch,dinner}', '{vegetarian,low-carb}',
    '{panera,salad,mediterranean}',
    380, 9, 16, 31, 5
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000012',
    id,
    CASE name
        WHEN 'Romaine Lettuce' THEN 150
        WHEN 'Tomato' THEN 80
        WHEN 'Cucumber' THEN 70
        WHEN 'Olive Oil (Extra Virgin)' THEN 28
    END,
    'g',
    CASE name
        WHEN 'Romaine Lettuce' THEN 1
        WHEN 'Tomato' THEN 2
        WHEN 'Cucumber' THEN 3
        WHEN 'Olive Oil (Extra Virgin)' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Romaine Lettuce', 'Tomato', 'Cucumber', 'Olive Oil (Extra Virgin)');

-- Panera 3: Turkey Avocado BLT
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000013',
    NULL,
    'Panera Turkey Avocado BLT',
    'lunch',
    'Panera: Turkey, bacon, avocado, lettuce, tomato on sourdough',
    true, true, 'Panera Bread', 'restaurant', 80,
    '{lunch}', '{high-protein}',
    '{panera,sandwich}',
    590, 32, 48, 31, 10
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000013',
    id,
    CASE name
        WHEN 'Turkey Breast' THEN 100
        WHEN 'Bacon' THEN 30
        WHEN 'Avocado' THEN 60
        WHEN 'Sourdough Bread' THEN 60
        WHEN 'Romaine Lettuce' THEN 30
        WHEN 'Tomato' THEN 50
    END,
    'g',
    CASE name
        WHEN 'Turkey Breast' THEN 1
        WHEN 'Bacon' THEN 2
        WHEN 'Avocado' THEN 3
        WHEN 'Sourdough Bread' THEN 4
        WHEN 'Romaine Lettuce' THEN 5
        WHEN 'Tomato' THEN 6
    END
FROM foods_enhanced
WHERE name IN ('Turkey Breast', 'Bacon', 'Avocado', 'Sourdough Bread', 'Romaine Lettuce', 'Tomato');

-- Panera 4: Chicken Noodle Soup (Cup)
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000014',
    NULL,
    'Panera Chicken Noodle Soup',
    'lunch',
    'Panera: Classic chicken noodle soup with vegetables',
    true, true, 'Panera Bread', 'restaurant', 77,
    '{lunch,snack}', '{comfort-food}',
    '{panera,soup,warm}',
    110, 8, 16, 2, 1
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000014',
    id,
    CASE name
        WHEN 'Chicken Breast' THEN 50
        WHEN 'Egg Noodles (Cooked)' THEN 60
        WHEN 'Carrots (Raw)' THEN 30
        WHEN 'Celery' THEN 20
    END,
    'g',
    CASE name
        WHEN 'Chicken Breast' THEN 1
        WHEN 'Egg Noodles (Cooked)' THEN 2
        WHEN 'Carrots (Raw)' THEN 3
        WHEN 'Celery' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Chicken Breast', 'Egg Noodles (Cooked)', 'Carrots (Raw)', 'Celery');

-- Panera 5: Power Breakfast Egg Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000015',
    NULL,
    'Panera Power Breakfast Egg Bowl',
    'breakfast',
    'Panera: Scrambled eggs, quinoa, avocado, tomato, basil',
    true, true, 'Panera Bread', 'restaurant', 75,
    '{breakfast}', '{high-protein,vegetarian}',
    '{panera,breakfast,bowl}',
    350, 19, 22, 21, 8
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000015',
    id,
    CASE name
        WHEN 'Whole Egg' THEN 100
        WHEN 'Quinoa (Cooked)' THEN 80
        WHEN 'Avocado' THEN 50
        WHEN 'Cherry Tomatoes' THEN 40
    END,
    'g',
    CASE name
        WHEN 'Whole Egg' THEN 1
        WHEN 'Quinoa (Cooked)' THEN 2
        WHEN 'Avocado' THEN 3
        WHEN 'Cherry Tomatoes' THEN 4
    END
FROM foods_enhanced
WHERE name IN ('Whole Egg', 'Quinoa (Cooked)', 'Avocado', 'Cherry Tomatoes');

-- ============================================================================
-- SWEETGREEN TEMPLATES (5 templates)
-- ============================================================================

-- Sweetgreen 1: Harvest Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000016',
    NULL,
    'Sweetgreen Harvest Bowl',
    'lunch',
    'Sweetgreen: Kale, wild rice, chicken, sweet potato, almonds, balsamic',
    true, true, 'Sweetgreen', 'restaurant', 90,
    '{lunch,dinner}', '{high-protein,balanced}',
    '{sweetgreen,salad,seasonal}',
    580, 35, 62, 21, 11
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000016',
    id,
    CASE name
        WHEN 'Kale (Raw)' THEN 100
        WHEN 'Wild Rice (Cooked)' THEN 100
        WHEN 'Chicken Breast' THEN 100
        WHEN 'Sweet Potato (Baked)' THEN 100
        WHEN 'Almonds' THEN 28
        WHEN 'Balsamic Vinegar' THEN 15
    END,
    CASE name
        WHEN 'Balsamic Vinegar' THEN 'ml'
        ELSE 'g'
    END,
    CASE name
        WHEN 'Kale (Raw)' THEN 1
        WHEN 'Wild Rice (Cooked)' THEN 2
        WHEN 'Chicken Breast' THEN 3
        WHEN 'Sweet Potato (Baked)' THEN 4
        WHEN 'Almonds' THEN 5
        WHEN 'Balsamic Vinegar' THEN 6
    END
FROM foods_enhanced
WHERE name IN ('Kale (Raw)', 'Wild Rice (Cooked)', 'Chicken Breast', 'Sweet Potato (Baked)', 'Almonds', 'Balsamic Vinegar');

-- Sweetgreen 2: Kale Caesar
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000017',
    NULL,
    'Sweetgreen Kale Caesar',
    'lunch',
    'Sweetgreen: Kale, chicken, tomatoes, parmesan, sourdough croutons',
    true, true, 'Sweetgreen', 'restaurant', 87,
    '{lunch,dinner}', '{high-protein}',
    '{sweetgreen,salad,caesar}',
    490, 30, 35, 27, 7
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000017',
    id,
    CASE name
        WHEN 'Kale (Raw)' THEN 150
        WHEN 'Chicken Breast' THEN 100
        WHEN 'Cherry Tomatoes' THEN 50
        WHEN 'Sourdough Bread' THEN 30
        WHEN 'Olive Oil (Extra Virgin)' THEN 21
    END,
    'g',
    CASE name
        WHEN 'Kale (Raw)' THEN 1
        WHEN 'Chicken Breast' THEN 2
        WHEN 'Cherry Tomatoes' THEN 3
        WHEN 'Sourdough Bread' THEN 4
        WHEN 'Olive Oil (Extra Virgin)' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Kale (Raw)', 'Chicken Breast', 'Cherry Tomatoes', 'Sourdough Bread', 'Olive Oil (Extra Virgin)');

-- Sweetgreen 3: Fish Taco Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000018',
    NULL,
    'Sweetgreen Fish Taco Bowl',
    'lunch',
    'Sweetgreen: Blackened fish, cabbage, avocado, lime cilantro jalapeño dressing',
    true, true, 'Sweetgreen', 'restaurant', 84,
    '{lunch,dinner}', '{high-protein,omega-3}',
    '{sweetgreen,bowl,mexican-inspired}',
    570, 32, 45, 30, 12
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000018',
    id,
    CASE name
        WHEN 'Tilapia' THEN 120
        WHEN 'Cabbage (Raw)' THEN 100
        WHEN 'Avocado' THEN 60
        WHEN 'Corn (Cooked)' THEN 80
        WHEN 'Olive Oil (Extra Virgin)' THEN 14
    END,
    'g',
    CASE name
        WHEN 'Tilapia' THEN 1
        WHEN 'Cabbage (Raw)' THEN 2
        WHEN 'Avocado' THEN 3
        WHEN 'Corn (Cooked)' THEN 4
        WHEN 'Olive Oil (Extra Virgin)' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Tilapia', 'Cabbage (Raw)', 'Avocado', 'Corn (Cooked)', 'Olive Oil (Extra Virgin)');

-- Sweetgreen 4: Shroomami Bowl
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000019',
    NULL,
    'Sweetgreen Shroomami Bowl',
    'lunch',
    'Sweetgreen: Warm wild rice, portobello, roasted chicken, cabbage, miso dressing',
    true, true, 'Sweetgreen', 'restaurant', 81,
    '{lunch,dinner}', '{high-protein,umami}',
    '{sweetgreen,warm-bowl,asian-inspired}',
    510, 33, 52, 19, 8
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000019',
    id,
    CASE name
        WHEN 'Wild Rice (Cooked)' THEN 150
        WHEN 'Mushrooms (White, Cooked)' THEN 80
        WHEN 'Chicken Breast' THEN 100
        WHEN 'Cabbage (Raw)' THEN 80
        WHEN 'Sesame Oil' THEN 14
    END,
    'g',
    CASE name
        WHEN 'Wild Rice (Cooked)' THEN 1
        WHEN 'Mushrooms (White, Cooked)' THEN 2
        WHEN 'Chicken Breast' THEN 3
        WHEN 'Cabbage (Raw)' THEN 4
        WHEN 'Sesame Oil' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Wild Rice (Cooked)', 'Mushrooms (White, Cooked)', 'Chicken Breast', 'Cabbage (Raw)', 'Sesame Oil');

-- Sweetgreen 5: Guacamole Greens
INSERT INTO meal_templates (
    id, user_id, name, category, description,
    is_public, is_restaurant, restaurant_name, source, popularity_score,
    meal_suitability, dietary_flags, tags,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g
) VALUES (
    '20000000-0000-0000-0000-000000000020',
    NULL,
    'Sweetgreen Guacamole Greens',
    'lunch',
    'Sweetgreen: Mixed greens, chicken, corn, tomato, tortilla chips, guacamole',
    true, true, 'Sweetgreen', 'restaurant', 78,
    '{lunch,dinner}', '{high-protein}',
    '{sweetgreen,salad,mexican-inspired}',
    620, 34, 48, 35, 14
);

INSERT INTO meal_template_foods (meal_template_id, food_id, quantity, unit, order_index)
SELECT
    '20000000-0000-0000-0000-000000000020',
    id,
    CASE name
        WHEN 'Mixed Greens' THEN 100
        WHEN 'Chicken Breast' THEN 100
        WHEN 'Corn (Cooked)' THEN 80
        WHEN 'Cherry Tomatoes' THEN 60
        WHEN 'Guacamole' THEN 80
    END,
    'g',
    CASE name
        WHEN 'Mixed Greens' THEN 1
        WHEN 'Chicken Breast' THEN 2
        WHEN 'Corn (Cooked)' THEN 3
        WHEN 'Cherry Tomatoes' THEN 4
        WHEN 'Guacamole' THEN 5
    END
FROM foods_enhanced
WHERE name IN ('Mixed Greens', 'Chicken Breast', 'Corn (Cooked)', 'Cherry Tomatoes', 'Guacamole');

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Count by restaurant
SELECT
    restaurant_name,
    COUNT(*) AS template_count,
    ROUND(AVG(total_calories), 0) AS avg_calories,
    ROUND(AVG(total_protein_g), 1) AS avg_protein
FROM meal_templates
WHERE is_restaurant = true
GROUP BY restaurant_name
ORDER BY template_count DESC;

-- Total public templates
SELECT
    COUNT(*) AS total_public_templates,
    COUNT(*) FILTER (WHERE is_restaurant = true) AS restaurant_templates,
    COUNT(*) FILTER (WHERE is_restaurant = false) AS community_templates
FROM meal_templates
WHERE is_public = true;

-- ============================================================================
-- END ADDITIONAL RESTAURANT TEMPLATES
-- Total restaurant chains: Chipotle (3), Subway (2), Starbucks (5), Panera (5), Sweetgreen (5)
-- Total templates: ~30 public meal templates
-- ============================================================================
