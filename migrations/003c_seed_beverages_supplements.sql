-- ============================================================================
-- COMPREHENSIVE SEED: Beverages and Supplements
-- ============================================================================
-- Purpose: Complete atomic foods with beverages and supplements
-- Date: 2025-10-09
-- Foods: ~30 foods (Beverages, Supplements, Condiments)
-- Note: Run after 003b_seed_fruits_vegetables_fats.sql
-- ============================================================================

-- ============================================================================
-- PART 7: BEVERAGES (15 foods)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
-- Non-Caloric Beverages
('Water', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 0, 0, 0, 0, 0,
 true, true, true, 'unprocessed', 'ready', '{breakfast,lunch,dinner,snack}', '{gluten-free,zero-calorie,hydration}', 1.0),

('Black Coffee', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 2, 0.3, 0, 0, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast}', '{gluten-free,zero-calorie,caffeine}', 1.0),

('Green Tea', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 2, 0.5, 0, 0, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,zero-calorie,antioxidant}', 1.0),

('Black Tea', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 2, 0, 0.7, 0, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,zero-calorie,caffeine}', 1.0),

('Herbal Tea', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 2, 0, 0.5, 0, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,zero-calorie,caffeine-free}', 1.0),

-- Caloric Beverages
('Whole Milk', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 240, 'ml', '1', 'cup', 149, 7.7, 12, 8, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,dairy,calcium}', 1.0),

('2% Milk', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 240, 'ml', '1', 'cup', 122, 8.1, 12, 4.8, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,dairy,calcium}', 1.0),

('Skim Milk (Nonfat)', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 240, 'ml', '1', 'cup', 83, 8.3, 12, 0.2, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,dairy,low-fat,calcium}', 1.0),

('Almond Milk (Unsweetened)', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 30, 1, 1, 2.5, 0,
 true, true, false, 'processed', 'ready', '{breakfast,snack}', '{gluten-free,vegan,low-calorie,dairy-free}', 0.9),

('Oat Milk', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 120, 3, 16, 5, 2,
 true, true, false, 'processed', 'ready', '{breakfast,snack}', '{gluten-free,vegan,dairy-free}', 0.9),

('Coconut Milk (Unsweetened)', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 45, 0, 1, 4.5, 0,
 true, true, false, 'processed', 'ready', '{breakfast,snack}', '{gluten-free,vegan,dairy-free}', 0.9),

('Orange Juice (Fresh)', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 112, 1.7, 26, 0.5, 0.5,
 true, true, true, 'minimally_processed', 'ready', '{breakfast}', '{gluten-free,vitamin-c}', 0.9),

('Apple Juice', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 114, 0.2, 28, 0.3, 0.2,
 true, true, false, 'processed', 'ready', '{breakfast,snack}', '{gluten-free}', 0.7),

('Coconut Water', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 46, 1.7, 9, 0.5, 2.6,
 true, true, true, 'minimally_processed', 'ready', '{snack}', '{gluten-free,electrolytes,hydration}', 0.9),

('Sports Drink (Gatorade)', 'Beverages', (SELECT id FROM food_categories WHERE name = 'Beverages'),
 240, 'ml', '1', 'cup', 50, 0, 14, 0, 0,
 true, true, false, 'processed', 'ready', '{snack}', '{gluten-free,electrolytes}', 0.6);

-- ============================================================================
-- PART 8: SUPPLEMENTS & PROTEIN POWDERS (8 foods)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Whey Protein Isolate', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 30, 'g', '1', 'scoop', 110, 25, 1, 0.5, 0,
 true, true, false, 'processed', 'powder', '{breakfast,snack}', '{high-protein,dairy,post-workout}', 1.0),

('Whey Protein Concentrate', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 30, 'g', '1', 'scoop', 120, 24, 3, 1.5, 0,
 true, true, false, 'processed', 'powder', '{breakfast,snack}', '{high-protein,dairy,post-workout}', 1.0),

('Casein Protein', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 30, 'g', '1', 'scoop', 120, 24, 3, 1, 0,
 true, true, false, 'processed', 'powder', '{snack}', '{high-protein,dairy,slow-digesting}', 1.0),

('Pea Protein', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 33, 'g', '1', 'scoop', 120, 24, 1, 2, 0,
 true, true, false, 'processed', 'powder', '{breakfast,snack}', '{high-protein,vegan,dairy-free}', 1.0),

('Soy Protein Isolate', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 30, 'g', '1', 'scoop', 110, 25, 1, 0.5, 0,
 true, true, false, 'processed', 'powder', '{breakfast,snack}', '{high-protein,vegan,soy}', 1.0),

('Collagen Powder', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 20, 'g', '2', 'scoops', 70, 18, 0, 0, 0,
 true, true, false, 'processed', 'powder', '{breakfast,snack}', '{high-protein,joint-health}', 0.9),

('Creatine Monohydrate', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 5, 'g', '1', 'tsp', 0, 0, 0, 0, 0,
 true, true, false, 'processed', 'powder', '{snack}', '{performance,pre-workout}', 1.0),

('BCAAs (Powder)', 'Supplements', (SELECT id FROM food_categories WHERE name = 'Supplements'),
 10, 'g', '1', 'scoop', 40, 10, 0, 0, 0,
 true, true, false, 'processed', 'powder', '{snack}', '{amino-acids,workout-recovery}', 0.9);

-- ============================================================================
-- PART 9: COMMON CONDIMENTS & FLAVOR ENHANCERS (12 foods)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Soy Sauce', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 15, 'ml', '1', 'tbsp', 8, 1.3, 0.8, 0, 0,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free,low-calorie,high-sodium}', 0.8),

('Hot Sauce', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 5, 'ml', '1', 'tsp', 1, 0.1, 0.1, 0, 0,
 true, true, false, 'processed', 'ready', '{breakfast,lunch,dinner}', '{gluten-free,zero-calorie}', 0.8),

('Sriracha', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 15, 'ml', '1', 'tbsp', 15, 0.3, 3, 0.3, 0,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free,spicy}', 0.7),

('Ketchup', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 17, 'g', '1', 'tbsp', 17, 0.2, 4.5, 0, 0,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free,high-sugar}', 0.6),

('Mustard (Yellow)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 5, 'g', '1', 'tsp', 3, 0.2, 0.3, 0.2, 0.2,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free,low-calorie}', 0.8),

('Dijon Mustard', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 5, 'g', '1', 'tsp', 5, 0.3, 0.5, 0.3, 0.3,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free,low-calorie}', 0.8),

('Balsamic Vinegar', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 15, 'ml', '1', 'tbsp', 14, 0, 3, 0, 0,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free,low-calorie}', 0.8),

('Apple Cider Vinegar', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 15, 'ml', '1', 'tbsp', 3, 0, 0.1, 0, 0,
 true, true, false, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free,zero-calorie}', 0.9),

('Honey', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Grains'),
 21, 'g', '1', 'tbsp', 64, 0.1, 17, 0, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,natural-sweetener}', 0.9),

('Maple Syrup (Pure)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Grains'),
 20, 'g', '1', 'tbsp', 52, 0, 13, 0, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast}', '{gluten-free,natural-sweetener}', 0.9),

('Salsa (Fresh)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '0.5', 'cup', 36, 1.5, 8, 0.2, 2,
 true, true, false, 'minimally_processed', 'ready', '{lunch,dinner,snack}', '{gluten-free,low-calorie,vegan}', 0.9),

('Pesto (Basil)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 30, 'g', '2', 'tbsp', 80, 2, 2, 8, 0.5,
 true, true, false, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free,vegetarian}', 0.8);

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Final count by food_group
SELECT
    food_group,
    COUNT(*) AS total_foods,
    COUNT(*) FILTER (WHERE is_atomic = true) AS atomic_foods,
    AVG(data_quality_score) AS avg_quality
FROM foods_enhanced
GROUP BY food_group
ORDER BY total_foods DESC;

-- Total atomic foods count
SELECT
    COUNT(*) AS total_atomic_foods,
    COUNT(*) FILTER (WHERE household_serving_size IS NOT NULL) AS has_household_serving,
    ROUND(100.0 * COUNT(*) FILTER (WHERE household_serving_size IS NOT NULL) / COUNT(*), 1) AS coverage_pct
FROM foods_enhanced
WHERE is_atomic = true;

-- Foods by processing level
SELECT
    processing_level,
    COUNT(*) AS count
FROM foods_enhanced
WHERE is_atomic = true
GROUP BY processing_level
ORDER BY count DESC;

-- Foods by dietary flags
SELECT
    UNNEST(dietary_flags) AS flag,
    COUNT(*) AS count
FROM foods_enhanced
WHERE is_atomic = true AND dietary_flags != '{}'
GROUP BY flag
ORDER BY count DESC
LIMIT 20;

-- ============================================================================
-- END COMPREHENSIVE ATOMIC FOODS SEED
-- Total: ~225 atomic foods across all categories
-- Next: 004_COMPREHENSIVE_seed_meal_templates.sql
-- ============================================================================
