-- ============================================================================
-- COMPREHENSIVE SEED: Fruits, Vegetables, and Fats
-- ============================================================================
-- Purpose: Continue populating foods_enhanced with atomic foods
-- Date: 2025-10-09
-- Foods: ~80 foods (Fruits, Vegetables, Fats/Oils, Nuts/Seeds)
-- Note: Run after 003_COMPREHENSIVE_seed_atomic_foods.sql
-- ============================================================================

-- ============================================================================
-- PART 3: FRUITS (25 foods)
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
-- Common Fruits
('Banana', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 118, 'g', '1', 'medium', 105, 1.3, 27, 0.4, 3.1,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,potassium}', 1.0),

('Apple', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 182, 'g', '1', 'medium', 95, 0.5, 25, 0.3, 4.4,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,fiber}', 1.0),

('Orange', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 131, 'g', '1', 'medium', 62, 1.2, 15, 0.2, 3.1,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-c}', 1.0),

('Strawberries', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup', 32, 0.7, 7.7, 0.3, 2,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-c,low-carb}', 1.0),

('Blueberries', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup', 57, 0.7, 14, 0.3, 2.4,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,antioxidant}', 1.0),

('Raspberries', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup', 52, 1.2, 12, 0.7, 6.5,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,high-fiber}', 1.0),

('Blackberries', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup', 43, 1.4, 10, 0.5, 5.3,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,high-fiber}', 1.0),

('Grapes', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup', 69, 0.7, 18, 0.2, 0.9,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free}', 1.0),

('Watermelon', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup diced', 30, 0.6, 8, 0.2, 0.4,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,hydrating,low-calorie}', 1.0),

('Cantaloupe', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup diced', 34, 0.8, 8, 0.2, 0.9,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-a}', 1.0),

('Honeydew', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup diced', 36, 0.5, 9, 0.1, 0.8,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free}', 1.0),

('Pineapple', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup chunks', 50, 0.5, 13, 0.1, 1.4,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-c}', 1.0),

('Mango', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup chunks', 60, 0.8, 15, 0.4, 1.6,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-a}', 1.0),

('Papaya', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup chunks', 43, 0.5, 11, 0.3, 1.7,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-c}', 1.0),

('Kiwi', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 69, 'g', '1', 'medium', 42, 0.8, 10, 0.4, 2.1,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,vitamin-c}', 1.0),

('Peach', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 150, 'g', '1', 'medium', 58, 1.4, 14, 0.4, 2.3,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free}', 1.0),

('Plum', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 66, 'g', '1', 'medium', 30, 0.5, 8, 0.2, 0.9,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free}', 1.0),

('Nectarine', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 142, 'g', '1', 'medium', 63, 1.5, 15, 0.5, 2.4,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free}', 1.0),

('Pear', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 178, 'g', '1', 'medium', 101, 0.6, 27, 0.2, 5.5,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,fiber}', 1.0),

('Cherries', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '1', 'cup', 63, 1.1, 16, 0.2, 2.1,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,antioxidant}', 1.0),

('Grapefruit', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 123, 'g', '0.5', 'fruit', 52, 0.9, 13, 0.2, 2,
 true, true, true, 'unprocessed', 'raw', '{breakfast}', '{gluten-free,vitamin-c}', 1.0),

('Pomegranate Seeds', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '0.5', 'cup', 83, 1.7, 19, 1.2, 4,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,antioxidant}', 1.0),

('Avocado', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 100, 'g', '0.5', 'medium', 160, 2, 9, 15, 7,
 true, true, true, 'unprocessed', 'raw', '{breakfast,lunch,dinner}', '{gluten-free,healthy-fat,high-fiber}', 1.0),

('Dates (Medjool)', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 24, 'g', '1', 'date', 66, 0.4, 18, 0, 1.6,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,natural-sweetener}', 1.0),

('Figs (Fresh)', 'Fruits', (SELECT id FROM food_categories WHERE name = 'Fruits'),
 50, 'g', '1', 'large', 37, 0.4, 10, 0.2, 1.5,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free}', 1.0);

-- ============================================================================
-- PART 4: VEGETABLES (30 foods)
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
-- Leafy Greens
('Spinach (Raw)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '3', 'cups', 23, 2.9, 3.6, 0.4, 2.2,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb,vitamin-k}', 1.0),

('Kale (Raw)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '2.5', 'cups chopped', 35, 2.9, 4.4, 1.5, 4.1,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb,superfood}', 1.0),

('Arugula', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '3', 'cups', 25, 2.6, 3.7, 0.7, 1.6,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Romaine Lettuce', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '3', 'cups chopped', 17, 1.2, 3.3, 0.3, 2.1,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb,low-calorie}', 1.0),

('Mixed Greens', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '3', 'cups', 20, 1.5, 3.5, 0.3, 2,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Swiss Chard', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '2', 'cups chopped', 19, 1.8, 3.7, 0.2, 1.6,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

-- Cruciferous Vegetables
('Broccoli (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup', 35, 2.4, 7, 0.4, 3.3,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb,vitamin-c}', 1.0),

('Cauliflower (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup', 23, 1.8, 4.1, 0.5, 2.3,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Brussels Sprouts (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup', 36, 2.6, 7.1, 0.5, 2.6,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Cabbage (Raw)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1.5', 'cups shredded', 25, 1.3, 5.8, 0.1, 2.5,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb,low-calorie}', 1.0),

-- Colorful Vegetables
('Bell Pepper (Red)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'medium', 31, 1, 6, 0.3, 2.1,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner,snack}', '{gluten-free,low-carb,vitamin-c}', 1.0),

('Bell Pepper (Green)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'medium', 20, 0.9, 4.6, 0.2, 1.7,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner,snack}', '{gluten-free,low-carb}', 1.0),

('Tomato', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 123, 'g', '1', 'medium', 22, 1.1, 4.8, 0.2, 1.5,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free,low-carb,lycopene}', 1.0),

('Cherry Tomatoes', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup', 18, 0.9, 3.9, 0.2, 1.2,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner,snack}', '{gluten-free,low-carb}', 1.0),

('Cucumber', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '0.5', 'cucumber', 15, 0.7, 3.6, 0.1, 0.5,
 true, true, true, 'unprocessed', 'raw', '{lunch,snack}', '{gluten-free,low-carb,hydrating}', 1.0),

('Zucchini (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup sliced', 17, 1.2, 3.1, 0.3, 1,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb,low-calorie}', 1.0),

('Eggplant (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup cubed', 35, 0.8, 8.6, 0.2, 2.5,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Carrots (Raw)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'large', 41, 0.9, 10, 0.2, 2.8,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner,snack}', '{gluten-free,vitamin-a}', 1.0),

-- Root Vegetables & Others
('Beets (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '0.5', 'cup', 44, 1.7, 10, 0.2, 2,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0),

('Radish', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '10', 'radishes', 16, 0.7, 3.4, 0.1, 1.6,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,low-carb,low-calorie}', 1.0),

('Celery', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '2', 'stalks', 14, 0.7, 3, 0.2, 1.6,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,low-carb,low-calorie}', 1.0),

('Asparagus (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '7', 'spears', 22, 2.4, 4.1, 0.2, 2.1,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Green Beans (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup', 35, 1.9, 7.9, 0.1, 3.4,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb}', 1.0),

('Mushrooms (White, Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup sliced', 28, 3.9, 4.3, 0.5, 2.2,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb,vitamin-d}', 1.0),

('Onion (Raw)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'medium', 40, 1.1, 9.3, 0.1, 1.7,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free}', 1.0),

('Garlic (Raw)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 3, 'g', '1', 'clove', 4, 0.2, 1, 0, 0.1,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free}', 1.0),

('Snow Peas', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup', 42, 2.8, 7.6, 0.2, 2.6,
 true, true, true, 'unprocessed', 'raw', '{lunch,dinner}', '{gluten-free}', 1.0),

('Bok Choy (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '1', 'cup shredded', 13, 1.6, 2, 0.2, 1,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,low-carb,low-calorie}', 1.0),

('Butternut Squash (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '0.5', 'cup cubed', 40, 0.9, 10, 0.1, 2,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free,vitamin-a}', 1.0),

('Acorn Squash (Cooked)', 'Vegetables', (SELECT id FROM food_categories WHERE name = 'Vegetables'),
 100, 'g', '0.5', 'cup cubed', 56, 1.1, 15, 0.1, 2.3,
 true, true, true, 'unprocessed', 'cooked', '{lunch,dinner}', '{gluten-free}', 1.0);

-- ============================================================================
-- PART 5: FATS & OILS (15 foods)
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
-- Oils
('Olive Oil (Extra Virgin)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 14, 'g', '1', 'tbsp', 119, 0, 0, 14, 0,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free,heart-healthy}', 1.0),

('Coconut Oil', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 14, 'g', '1', 'tbsp', 121, 0, 0, 14, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch,dinner}', '{gluten-free}', 0.9),

('Avocado Oil', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 14, 'g', '1', 'tbsp', 124, 0, 0, 14, 0,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free,heart-healthy}', 1.0),

('Sesame Oil', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 14, 'g', '1', 'tbsp', 120, 0, 0, 14, 0,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free}', 1.0),

('Grapeseed Oil', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 14, 'g', '1', 'tbsp', 120, 0, 0, 14, 0,
 true, true, true, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free}', 0.9),

-- Butter & Spreads
('Butter (Salted)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 14, 'g', '1', 'tbsp', 102, 0.1, 0, 12, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch,dinner}', '{gluten-free,dairy}', 0.9),

('Ghee (Clarified Butter)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 13, 'g', '1', 'tbsp', 112, 0, 0, 13, 0,
 true, true, true, 'minimally_processed', 'ready', '{breakfast,lunch,dinner}', '{gluten-free,lactose-free}', 1.0),

-- Nuts (whole)
('Almonds', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '23', 'almonds', 164, 6, 6, 14, 3.5,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,high-protein,heart-healthy}', 1.0),

('Walnuts', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '14', 'halves', 185, 4.3, 3.9, 18.5, 1.9,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,omega-3}', 1.0),

('Cashews', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '18', 'cashews', 157, 5.2, 8.6, 12.4, 0.9,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free}', 1.0),

('Peanuts', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '28', 'peanuts', 161, 7.3, 4.6, 14, 2.4,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,high-protein}', 1.0),

('Pecans', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '19', 'halves', 196, 2.6, 3.9, 20.4, 2.7,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free}', 1.0),

('Pistachios', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '49', 'pistachios', 159, 5.7, 7.7, 12.9, 3,
 true, true, true, 'unprocessed', 'raw', '{snack}', '{gluten-free,high-protein}', 1.0),

-- Seeds
('Chia Seeds', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 28, 'g', '2', 'tbsp', 138, 4.7, 12, 8.7, 9.8,
 true, true, true, 'unprocessed', 'raw', '{breakfast,snack}', '{gluten-free,omega-3,high-fiber}', 1.0),

('Flaxseed (Ground)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 10, 'g', '1', 'tbsp', 55, 1.9, 3, 4.3, 2.8,
 true, true, true, 'minimally_processed', 'ground', '{breakfast,snack}', '{gluten-free,omega-3,high-fiber}', 1.0);

-- ============================================================================
-- PART 6: NUT BUTTERS & SPREADS (10 foods)
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
('Peanut Butter (Natural)', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 32, 'g', '2', 'tbsp', 190, 8, 7, 16, 2,
 true, true, false, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,high-protein}', 1.0),

('Almond Butter', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 32, 'g', '2', 'tbsp', 196, 6.7, 6, 18, 3.3,
 true, true, false, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,heart-healthy}', 1.0),

('Cashew Butter', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 32, 'g', '2', 'tbsp', 188, 5.6, 9, 16, 1,
 true, true, false, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free}', 1.0),

('Sunflower Seed Butter', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 32, 'g', '2', 'tbsp', 200, 6.5, 7, 17, 3,
 true, true, false, 'minimally_processed', 'ready', '{breakfast,snack}', '{gluten-free,nut-free}', 1.0),

('Tahini', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 30, 'g', '2', 'tbsp', 178, 5.1, 6.4, 16, 2.8,
 true, true, false, 'minimally_processed', 'ready', '{lunch,dinner,snack}', '{gluten-free}', 1.0),

('Hummus', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 100, 'g', '0.33', 'cup', 166, 7.9, 14, 10, 6,
 true, true, false, 'minimally_processed', 'ready', '{lunch,snack}', '{gluten-free,vegan,fiber}', 0.9),

('Guacamole', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 100, 'g', '0.5', 'cup', 150, 2, 9, 14, 6,
 true, true, false, 'minimally_processed', 'ready', '{lunch,snack}', '{gluten-free,healthy-fat}', 0.9),

('Cream Cheese', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 28, 'g', '2', 'tbsp', 99, 1.8, 1.6, 10, 0,
 true, true, false, 'processed', 'ready', '{breakfast}', '{gluten-free,dairy}', 0.8),

('Sour Cream', 'Dairy', (SELECT id FROM food_categories WHERE name = 'Dairy'),
 28, 'g', '2', 'tbsp', 51, 0.6, 1.2, 5, 0,
 true, true, false, 'minimally_processed', 'ready', '{lunch,dinner}', '{gluten-free,dairy}', 0.8),

('Mayonnaise', 'Fats', (SELECT id FROM food_categories WHERE name = 'Fats'),
 15, 'g', '1', 'tbsp', 94, 0.1, 0.1, 10, 0,
 true, true, false, 'processed', 'ready', '{lunch,dinner}', '{gluten-free}', 0.7);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Count foods by food_group
SELECT
    food_group,
    COUNT(*) AS total_count,
    AVG(data_quality_score) AS avg_quality
FROM foods_enhanced
WHERE is_atomic = true
GROUP BY food_group
ORDER BY total_count DESC;

-- Check household serving coverage
SELECT
    food_group,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE household_serving_size IS NOT NULL) AS has_household,
    ROUND(100.0 * COUNT(*) FILTER (WHERE household_serving_size IS NOT NULL) / COUNT(*), 1) AS coverage_pct
FROM foods_enhanced
WHERE is_atomic = true
GROUP BY food_group;

-- ============================================================================
-- END PART 2 (Fruits + Vegetables + Fats = 80 foods)
-- Total so far: 190 atomic foods
-- Next: Beverages, Supplements, Condiments
-- ============================================================================
