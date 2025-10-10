-- ============================================================================
-- COMPREHENSIVE SEED: Atomic Foods Only
-- ============================================================================
-- Purpose: Populate foods_enhanced with high-quality atomic foods
-- Date: 2025-10-09
-- Foods: ~200 atomic foods (single ingredients only)
-- Note: Restaurant meals are in 004_seed_meal_templates.sql
-- ============================================================================

-- ============================================================================
-- PART 1: PROTEINS (60 foods)
-- ============================================================================

-- Poultry (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Chicken Breast', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 165, 31, 0, 3.6, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,low-carb}', 1.0),

('Chicken Thigh', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 209, 26, 0, 10.9, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,low-carb}', 1.0),

('Ground Chicken', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 143, 17.4, 0, 8.1, 0,
 true, true, true, 'minimally_processed', 'raw', '{lunch,dinner}', '{high-protein,low-carb}', 1.0),

('Turkey Breast', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 135, 30, 0, 1.2, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,low-carb,lean}', 1.0),

('Ground Turkey', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 150, 20, 0, 8, 0,
 true, true, true, 'minimally_processed', 'raw', '{lunch,dinner}', '{high-protein,low-carb}', 1.0),

('Chicken Wings', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 203, 30.5, 0, 8.1, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner,snack}', '{high-protein,low-carb}', 1.0),

('Duck Breast', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 201, 23.5, 0, 11.2, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein}', 1.0),

('Rotisserie Chicken', 'Protein', (SELECT id FROM food_categories WHERE name = 'Poultry'),
 100, 'g', '4', 'oz', 167, 25.9, 0, 6.6, 0,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{high-protein,convenient}', 1.0);

-- Beef (10 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Ground Beef (93/7)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 182, 25, 0, 8, 0,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{high-protein,low-carb}', 1.0),

('Ground Beef (80/20)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 254, 21, 0, 18, 0,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{high-protein,high-fat}', 1.0),

('Sirloin Steak', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 183, 27, 0, 8, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,low-carb}', 1.0),

('Ribeye Steak', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 291, 25, 0, 21, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,high-fat}', 1.0),

('Flank Steak', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 192, 28, 0, 8, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Beef Brisket', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 215, 26, 0, 11, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein}', 1.0),

('Beef Tenderloin', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 201, 28, 0, 9, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,lean}', 1.0),

('Chuck Roast', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 249, 26, 0, 16, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein}', 1.0),

('Beef Short Ribs', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 338, 23, 0, 27, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,high-fat}', 1.0),

('Tri-Tip Steak', 'Protein', (SELECT id FROM food_categories WHERE name = 'Beef'),
 100, 'g', '4', 'oz', 172, 28, 0, 6, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0);

-- Pork (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Pork Chop', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '4', 'oz', 231, 25, 0, 14, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein}', 1.0),

('Pork Tenderloin', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '4', 'oz', 143, 26, 0, 3.5, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Ground Pork', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '4', 'oz', 297, 16, 0, 26, 0,
 true, true, true, 'minimally_processed', 'raw', '{lunch,dinner}', '{high-protein,high-fat}', 1.0),

('Pork Shoulder', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '4', 'oz', 242, 19, 0, 18, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein}', 1.0),

('Pork Ribs', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '4', 'oz', 277, 20, 0, 21, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,high-fat}', 1.0),

('Bacon', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '3', 'slices', 541, 37, 1.4, 42, 0,
 true, true, false, 'processed', 'cooked', '{breakfast}', '{high-protein,high-fat,processed}', 0.8),

('Canadian Bacon', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '3', 'slices', 147, 21, 2, 6, 0,
 true, true, false, 'processed', 'cooked', '{breakfast}', '{high-protein,lean,processed}', 0.8),

('Pork Sausage', 'Protein', (SELECT id FROM food_categories WHERE name = 'Pork'),
 100, 'g', '2', 'links', 339, 13, 2, 31, 0,
 true, true, false, 'processed', 'cooked', '{breakfast}', '{high-protein,high-fat,processed}', 0.8);

-- Fish (12 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Salmon (Atlantic)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 206, 22, 0, 13, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,omega-3}', 1.0),

('Salmon (Wild)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 182, 25, 0, 8, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,omega-3,lean}', 1.0),

('Tuna (Yellowfin)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 109, 24, 0, 0.5, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean,omega-3}', 1.0),

('Tuna (Canned in Water)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '1', 'can', 116, 26, 0, 0.8, 0,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,snack}', '{high-protein,lean,convenient}', 0.9),

('Cod', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 105, 23, 0, 0.9, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Tilapia', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 129, 26, 0, 2.7, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Mahi Mahi', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 109, 24, 0, 0.9, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Halibut', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 140, 27, 0, 3, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Trout', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 190, 27, 0, 8, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,omega-3}', 1.0),

('Mackerel', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 262, 24, 0, 18, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,omega-3,high-fat}', 1.0),

('Sardines (Canned)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '1', 'can', 208, 25, 0, 11, 0,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,snack}', '{high-protein,omega-3,convenient}', 0.9),

('Swordfish', 'Protein', (SELECT id FROM food_categories WHERE name = 'Fish'),
 100, 'g', '4', 'oz', 172, 28, 0, 6, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,lean}', 1.0);

-- Seafood (6 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Shrimp', 'Protein', (SELECT id FROM food_categories WHERE name = 'Seafood'),
 100, 'g', '10', 'pieces', 99, 24, 0.2, 0.3, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean,low-carb}', 1.0),

('Crab', 'Protein', (SELECT id FROM food_categories WHERE name = 'Seafood'),
 100, 'g', '4', 'oz', 97, 19, 0, 1.5, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Lobster', 'Protein', (SELECT id FROM food_categories WHERE name = 'Seafood'),
 100, 'g', '4', 'oz', 98, 21, 0.5, 0.6, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein,lean}', 1.0),

('Scallops', 'Protein', (SELECT id FROM food_categories WHERE name = 'Seafood'),
 100, 'g', '5', 'pieces', 111, 21, 3, 1, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0),

('Mussels', 'Protein', (SELECT id FROM food_categories WHERE name = 'Seafood'),
 100, 'g', '1', 'cup', 172, 24, 7, 4.5, 0,
 true, true, true, 'unprocessed', 'cooked', '{dinner}', '{high-protein}', 1.0),

('Clams', 'Protein', (SELECT id FROM food_categories WHERE name = 'Seafood'),
 100, 'g', '10', 'pieces', 148, 26, 5, 2, 0,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,lean}', 1.0);

-- Eggs & Dairy Protein (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Whole Egg', 'Protein', (SELECT id FROM food_categories WHERE name = 'Eggs'),
 50, 'g', '1', 'egg', 78, 6, 0.6, 5, 0,
 true, true, true, 'unprocessed', 'raw', '{breakfast,lunch,dinner}', '{high-protein,vegetarian}', 1.0),

('Egg White', 'Protein', (SELECT id FROM food_categories WHERE name = 'Eggs'),
 33, 'g', '1', 'egg white', 17, 3.6, 0.2, 0.1, 0,
 true, true, true, 'unprocessed', 'raw', '{breakfast,lunch}', '{high-protein,lean,vegetarian}', 1.0),

('Egg Yolk', 'Protein', (SELECT id FROM food_categories WHERE name = 'Eggs'),
 17, 'g', '1', 'yolk', 55, 2.7, 0.6, 4.5, 0,
 true, true, true, 'unprocessed', 'raw', '{breakfast}', '{high-fat,vegetarian}', 1.0),

('Cottage Cheese (1%)', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 100, 'g', '0.5', 'cup', 72, 12, 3.4, 1, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{high-protein,low-fat,vegetarian}', 1.0),

('Greek Yogurt (Nonfat)', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 100, 'g', '0.5', 'cup', 59, 10, 3.6, 0.4, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{high-protein,low-fat,vegetarian}', 1.0),

('Greek Yogurt (2%)', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 100, 'g', '0.5', 'cup', 73, 10, 3.9, 2, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{high-protein,vegetarian}', 1.0),

('Greek Yogurt (Full Fat)', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 100, 'g', '0.5', 'cup', 97, 9, 3.6, 5, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{high-protein,vegetarian}', 1.0),

('Skyr (Icelandic Yogurt)', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 100, 'g', '0.5', 'cup', 63, 11, 4, 0.2, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,snack}', '{high-protein,low-fat,vegetarian}', 1.0);

-- Plant Protein (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Tofu (Firm)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 83, 10, 2, 5, 1,
 true, true, true, 'minimally_processed', 'raw', '{lunch,dinner}', '{high-protein,vegan,soy}', 1.0),

('Tofu (Extra Firm)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 91, 11, 2, 5.5, 1,
 true, true, true, 'minimally_processed', 'raw', '{lunch,dinner}', '{high-protein,vegan,soy}', 1.0),

('Tempeh', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 193, 20, 9, 11, 0,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{high-protein,vegan,soy}', 1.0),

('Edamame', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 122, 11, 10, 5, 5,
 true, true, true, 'unprocessed', 'cooked', '{snack,lunch}', '{high-protein,vegan,soy}', 1.0),

('Lentils (Cooked)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 116, 9, 20, 0.4, 8,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,high-fiber,vegan}', 1.0),

('Black Beans (Cooked)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 132, 9, 24, 0.5, 9,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{high-protein,high-fiber,vegan}', 1.0),

('Chickpeas (Cooked)', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '0.5', 'cup', 164, 9, 27, 2.6, 7.6,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner,snack}', '{high-protein,high-fiber,vegan}', 1.0),

('Seitan', 'Protein', (SELECT id FROM food_categories WHERE name = 'Plant Protein'),
 100, 'g', '3.5', 'oz', 370, 75, 14, 2, 1,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{very-high-protein,vegan,gluten}', 0.9);

-- ============================================================================
-- PART 2: CARBOHYDRATES (50 foods)
-- ============================================================================

-- Rice (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('White Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 130, 2.7, 28, 0.3, 0.4,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Brown Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 112, 2.6, 24, 0.9, 1.8,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{whole-grain,gluten-free}', 1.0),

('Jasmine Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 129, 2.7, 28, 0.2, 0.4,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Basmati Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 121, 2.5, 26, 0.4, 0.6,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Wild Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 101, 4, 21, 0.3, 1.8,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{whole-grain,gluten-free}', 1.0),

('Black Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 356, 9, 76, 3, 4.9,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{whole-grain,gluten-free,antioxidant}', 1.0),

('Sushi Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 130, 2.4, 29, 0.2, 0.3,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Arborio Rice (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Rice'),
 100, 'g', '0.5', 'cup', 130, 2.4, 28, 0.1, 0.6,
 true, true, true, 'minimally_processed', 'cooked', '{dinner}', '{gluten-free}', 1.0);

-- Pasta (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Spaghetti (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 158, 5.8, 31, 0.9, 1.8,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 1.0),

('Whole Wheat Pasta (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 124, 5.3, 26, 1.4, 3.9,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{whole-grain}', 1.0),

('Penne (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 157, 5.8, 31, 0.9, 1.8,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 1.0),

('Fettuccine (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 158, 5.8, 31, 0.9, 1.8,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 1.0),

('Orzo (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 165, 5.7, 32, 1, 2,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 1.0),

('Egg Noodles (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 138, 4.5, 25, 2.1, 1.2,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),

('Lasagna Noodles (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '1', 'sheet', 155, 5.5, 31, 0.8, 1.5,
 true, true, false, 'processed', 'cooked', '{dinner}', '{}', 1.0),

('Gluten-Free Pasta (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Pasta'),
 100, 'g', '0.5', 'cup', 160, 3.2, 35, 0.6, 2,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten-free}', 0.9);

-- Bread (10 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('White Bread', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 25, 'g', '1', 'slice', 67, 2, 13, 0.8, 0.6,
 true, true, false, 'processed', 'ready', '{breakfast,lunch}', '{}', 0.8),

('Whole Wheat Bread', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 28, 'g', '1', 'slice', 69, 3.6, 12, 0.9, 1.9,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch}', '{whole-grain}', 1.0),

('Sourdough Bread', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 30, 'g', '1', 'slice', 84, 3, 16, 0.5, 0.7,
 true, true, false, 'processed', 'ready', '{breakfast,lunch,dinner}', '{fermented}', 0.9),

('Rye Bread', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 32, 'g', '1', 'slice', 83, 2.7, 15, 1.1, 1.9,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch}', '{whole-grain}', 1.0),

('Multigrain Bread', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 26, 'g', '1', 'slice', 69, 3.5, 11, 1.1, 1.7,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch}', '{whole-grain}', 1.0),

('Ezekiel Bread', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 34, 'g', '1', 'slice', 80, 4, 15, 0.5, 3,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch}', '{whole-grain,sprouted}', 1.0),

('Pita Bread (Whole Wheat)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 28, 'g', '0.5', 'pita', 74, 3, 15, 0.3, 2,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{whole-grain}', 1.0),

('English Muffin', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 57, 'g', '1', 'muffin', 134, 4.4, 26, 1, 1.5,
 true, true, false, 'processed', 'ready', '{breakfast}', '{}', 0.9),

('Bagel', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 71, 'g', '1', 'bagel', 195, 7, 38, 1.1, 1.6,
 true, true, false, 'processed', 'ready', '{breakfast,lunch}', '{}', 0.9),

('Tortilla (Whole Wheat)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 46, 'g', '1', 'tortilla', 130, 4, 22, 3.5, 3,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{whole-grain}', 1.0);

-- Grains (10 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Oatmeal (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 71, 2.5, 12, 1.5, 1.7,
 true, true, true, 'minimally_processed', 'cooked', '{breakfast}', '{whole-grain,gluten-free}', 1.0),

('Steel Cut Oats (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 70, 2.4, 12, 1.4, 1.7,
 true, true, true, 'minimally_processed', 'cooked', '{breakfast}', '{whole-grain,gluten-free}', 1.0),

('Quinoa (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 120, 4.4, 21, 1.9, 2.8,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{whole-grain,gluten-free,complete-protein}', 1.0),

('Couscous (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 112, 3.8, 23, 0.2, 1.4,
 true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 0.9),

('Bulgur (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 83, 3.1, 19, 0.2, 4.5,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{whole-grain}', 1.0),

('Farro (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 150, 5, 26, 2.5, 3.5,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{whole-grain,ancient-grain}', 1.0),

('Barley (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 123, 2.3, 28, 0.4, 3.8,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{whole-grain}', 1.0),

('Millet (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 119, 3.5, 24, 1, 1.3,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{whole-grain,gluten-free}', 1.0),

('Buckwheat (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 92, 3.4, 20, 0.6, 2.7,
 true, true, true, 'unprocessed', 'cooked', '{breakfast,lunch,dinner}', '{whole-grain,gluten-free}', 1.0),

('Amaranth (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 102, 3.8, 19, 1.6, 2.1,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{whole-grain,gluten-free,ancient-grain}', 1.0);

-- Potatoes (6 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Russet Potato (Baked)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '0.5', 'potato', 93, 2.5, 21, 0.1, 2.2,
 true, true, true, 'unprocessed', 'baked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Sweet Potato (Baked)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '0.5', 'potato', 90, 2, 21, 0.2, 3.3,
 true, true, true, 'unprocessed', 'baked', '{lunch,dinner}', '{gluten-free,vitamin-a}', 1.0),

('Red Potato (Boiled)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '2', 'small potatoes', 87, 1.9, 20, 0.1, 1.8,
 true, true, true, 'unprocessed', 'boiled', '{lunch,dinner}', '{gluten-free}', 1.0),

('Yukon Gold Potato (Roasted)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '0.5', 'potato', 100, 2.3, 22, 0.2, 2,
 true, true, true, 'unprocessed', 'roasted', '{lunch,dinner}', '{gluten-free}', 1.0),

('Purple Potato (Cooked)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '2', 'small potatoes', 87, 2.3, 19, 0.1, 2.1,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,antioxidant}', 1.0),

('Fingerling Potato (Roasted)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '4', 'potatoes', 86, 2, 20, 0.1, 1.8,
 true, true, true, 'unprocessed', 'roasted', '{lunch,dinner}', '{gluten-free}', 1.0);

-- Other Carbs (8 foods)
INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    household_serving_size, household_serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Corn (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 96, 3.4, 21, 1.5, 2.4,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Corn Tortilla', 'Grains', (SELECT id FROM food_categories WHERE name = 'Bread'),
 24, 'g', '1', 'tortilla', 52, 1.4, 11, 0.7, 1.2,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free}', 1.0),

('Polenta (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 70, 1.7, 16, 0.2, 0.7,
 true, true, true, 'minimally_processed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Grits (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 59, 1.4, 13, 0.2, 0.4,
 true, true, false, 'processed', 'cooked', '{breakfast}', '{gluten-free}', 0.8),

('Cream of Wheat (Cooked)', 'Grains', (SELECT id FROM food_categories WHERE name = 'Grains'),
 100, 'g', '0.5', 'cup', 47, 1.3, 10, 0.2, 0.4,
 true, true, false, 'processed', 'cooked', '{breakfast}', '{}', 0.8),

('Plantain (Cooked)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '0.5', 'cup', 116, 0.8, 31, 0.2, 2.3,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Cassava (Cooked)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '0.5', 'cup', 112, 0.3, 27, 0.2, 1.4,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Taro Root (Cooked)', 'Carbohydrates', (SELECT id FROM food_categories WHERE name = 'Potatoes'),
 100, 'g', '0.5', 'cup', 142, 0.5, 35, 0.1, 5.1,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Count foods by category
SELECT
    fc.name AS category,
    COUNT(f.id) AS food_count
FROM food_categories fc
LEFT JOIN foods_enhanced f ON f.category_id = fc.id
WHERE fc.level = 1  -- Subcategories
GROUP BY fc.name
ORDER BY food_count DESC;

-- Check data quality
SELECT
    food_group,
    COUNT(*) AS total,
    AVG(data_quality_score) AS avg_quality,
    COUNT(*) FILTER (WHERE household_serving_size IS NOT NULL) AS has_household_serving
FROM foods_enhanced
WHERE is_atomic = true
GROUP BY food_group;

-- ============================================================================
-- END PART 1 (Proteins + Carbs = 110 foods so far)
-- Next: Part 2 will have Fruits, Vegetables, Fats, Beverages, Supplements
-- ============================================================================
