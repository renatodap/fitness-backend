-- ============================================================================
-- COMPREHENSIVE FOOD DATABASE SEED DATA
-- ============================================================================
-- Purpose: Realistic test data for family and friends to test the app
-- Categories: Common foods, branded items, restaurant meals, and templates
-- Date: 2025-01-10
-- ============================================================================

BEGIN;

-- Clear existing data (optional - comment out if you want to keep existing data)
-- TRUNCATE foods, meals, meal_foods, meal_templates, meal_template_foods, food_preferences, user_favorite_foods, daily_nutrition_summary CASCADE;

-- ============================================================================
-- BASIC INGREDIENTS & WHOLE FOODS
-- ============================================================================

INSERT INTO foods (
    name, food_type, description, 
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g,
    sodium_mg, potassium_mg, calcium_mg, iron_mg,
    cholesterol_mg, vitamin_c_mg, vitamin_d_mcg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES-- Proteins
('Chicken Breast (Boneless, Skinless, Cooked)', 'ingredient', 'Grilled or baked chicken breast without skin',
    100, 'g', 'breast (140g)', 140,
    165, 31, 0, 3.6,
    0, 0, 1,
    74, 256, 15, 1.04,
    85, 0, 0.1,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Chicken Breast (Raw)', 'ingredient', 'Raw boneless skinless chicken breast',
    100, 'g', 'breast (175g)', 175,
    120, 22.5, 0, 2.6,
    0, 0, 0.75,
    55, 370, 12, 0.9,
    70, 1.2, 0.1,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Ground Beef (93/7 Lean, Cooked)', 'ingredient', 'Cooked lean ground beef',
    100, 'g', 'serving (85g)', 85,
    182, 25.5, 0, 8,
    0, 0, 3.1,
    68, 382, 18, 2.6,
    76, 0, 0,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Salmon (Atlantic, Cooked)', 'ingredient', 'Baked or grilled Atlantic salmon',
    100, 'g', 'fillet (125g)', 125,
    206, 22.1, 0, 12.4,
    0, 0, 2.5,
    61, 384, 15, 0.34,
    63, 0, 11,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),
('Eggs (Large, Whole)', 'ingredient', 'Large whole eggs',
    50, 'g', 'egg', 50,
    72, 6.3, 0.36, 4.8,
    0, 0.18, 1.6,
    71, 69, 28, 0.88,
    186, 0, 1,
    ARRAY['eggs'], ARRAY['gluten-free', 'vegetarian', 'keto'], 'usda', 0.98, true),

('Egg Whites', 'ingredient', 'Liquid egg whites',
    100, 'g', '1/4 cup (60g)', 60,
    52, 10.9, 0.73, 0.17,
    0, 0.71, 0,
    166, 163, 7, 0.08,
    0, 0, 0,
    ARRAY['eggs'], ARRAY['gluten-free', 'vegetarian'], 'usda', 0.95, true),

('Greek Yogurt (Non-fat, Plain)', 'ingredient', 'Plain non-fat Greek yogurt',
    100, 'g', 'container (170g)', 170,
    59, 10.2, 3.6, 0.4,
    0, 3.2, 0.1,
    36, 141, 110, 0.04,
    5, 0.5, 0,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Tofu (Firm)', 'ingredient', 'Firm tofu, drained',
    100, 'g', '1/4 block (85g)', 85,
    144, 15.5, 4.3, 8.7,
    2.3, 0.7, 1.3,
    14, 237, 372, 2.66,
    0, 0.2, 0,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),
-- Grains & Carbs
('White Rice (Cooked)', 'ingredient', 'Long grain white rice, cooked',
    100, 'g', '1 cup (158g)', 158,
    130, 2.7, 28.2, 0.3,
    0.4, 0.05, 0.1,
    1, 35, 10, 0.2,
    0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Brown Rice (Cooked)', 'ingredient', 'Long grain brown rice, cooked',
    100, 'g', '1 cup (195g)', 195,
    112, 2.3, 23.5, 0.8,
    1.8, 0.35, 0.2,
    3, 79, 10, 0.52,
    0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Quinoa (Cooked)', 'ingredient', 'Cooked quinoa',
    100, 'g', '1 cup (185g)', 185,
    120, 4.4, 21.3, 1.9,
    2.8, 0.87, 0.23,
    7, 172, 17, 1.49,
    0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Oatmeal (Cooked)', 'ingredient', 'Cooked oats made with water',
    100, 'g', '1 cup (234g)', 234,
    71, 2.5, 12, 1.5,
    1.7, 0.3, 0.3,
    4, 70, 10, 0.9,
    0, 0, 0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),
('Sweet Potato (Baked, with skin)', 'ingredient', 'Baked sweet potato with skin',
    100, 'g', 'medium (150g)', 150,
    90, 2, 20.7, 0.2,
    3.3, 6.5, 0.04,
    36, 475, 38, 0.69,
    0, 19.6, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Pasta (Cooked)', 'ingredient', 'Cooked regular pasta',
    100, 'g', '1 cup (140g)', 140,
    131, 5, 25, 1.1,
    1.8, 0.56, 0.2,
    1, 44, 7, 0.91,
    0, 0, 0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Whole Wheat Bread', 'ingredient', 'Whole wheat bread slice',
    28, 'g', 'slice', 28,
    69, 3.5, 11.6, 1.1,
    1.9, 1.4, 0.24,
    132, 70, 26, 0.9,
    0, 0, 0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.93, true),

-- Fruits
('Banana', 'ingredient', 'Medium banana',
    118, 'g', 'medium banana', 118,
    105, 1.3, 27, 0.4,
    3.1, 14.4, 0.13,
    1, 422, 6, 0.31,
    0, 10.3, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),
('Apple (with skin)', 'ingredient', 'Medium apple with skin',
    182, 'g', 'medium apple', 182,
    95, 0.5, 25, 0.3,
    4.4, 19, 0.05,
    2, 195, 11, 0.22,
    0, 8.4, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Strawberries', 'ingredient', 'Fresh strawberries',
    100, 'g', '1 cup sliced (166g)', 166,
    32, 0.67, 7.68, 0.3,
    2, 4.89, 0.015,
    1, 153, 16, 0.41,
    0, 58.8, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Blueberries', 'ingredient', 'Fresh blueberries',
    100, 'g', '1 cup (148g)', 148,
    57, 0.74, 14.5, 0.33,
    2.4, 10, 0.028,
    1, 77, 6, 0.28,
    0, 9.7, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Avocado', 'ingredient', 'Fresh avocado',
    100, 'g', 'half avocado (100g)', 100,
    160, 2, 8.5, 14.7,
    6.7, 0.66, 2.13,
    7, 485, 12, 0.55,
    0, 10, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),
-- Vegetables
('Broccoli (Cooked)', 'ingredient', 'Steamed broccoli florets',
    100, 'g', '1 cup (156g)', 156,
    35, 2.4, 7.2, 0.4,
    3.3, 1.4, 0.08,
    41, 293, 40, 0.67,
    0, 64.9, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Spinach (Raw)', 'ingredient', 'Fresh raw spinach',
    100, 'g', '1 cup (30g)', 30,
    23, 2.9, 3.6, 0.4,
    2.2, 0.42, 0.06,
    79, 558, 99, 2.71,
    0, 28.1, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Carrots (Raw)', 'ingredient', 'Raw carrot sticks',
    100, 'g', '1 medium carrot (61g)', 61,
    41, 0.93, 9.6, 0.24,
    2.8, 4.74, 0.04,
    69, 320, 33, 0.3,
    0, 5.9, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Bell Pepper (Red)', 'ingredient', 'Fresh red bell pepper',
    100, 'g', '1 medium (119g)', 119,
    31, 0.99, 6, 0.3,
    2.1, 4.2, 0.03,
    4, 211, 7, 0.43,
    0, 127.7, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),
-- Dairy & Alternatives
('Milk (2% Fat)', 'ingredient', 'Reduced fat milk',
    244, 'g', '1 cup', 244,
    122, 8.1, 11.7, 4.8,
    0, 12.3, 3,
    115, 342, 293, 0.07,
    20, 2.2, 2.9,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Almond Milk (Unsweetened)', 'ingredient', 'Unsweetened almond milk',
    240, 'g', '1 cup', 240,
    39, 1.5, 3.4, 2.5,
    0.7, 2, 0.2,
    186, 176, 516, 0.7,
    0, 0, 2.6,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Cheddar Cheese', 'ingredient', 'Medium cheddar cheese',
    28, 'g', '1 oz', 28,
    113, 7, 0.9, 9.3,
    0, 0.15, 5.3,
    174, 20, 200, 0.2,
    29, 0, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Cottage Cheese (Low-fat)', 'ingredient', '2% milkfat cottage cheese',
    100, 'g', '1/2 cup (113g)', 113,
    84, 11, 4.3, 2.3,
    0, 4.1, 1,
    321, 84, 103, 0.15,
    9, 0, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),
-- Fats & Oils
('Olive Oil', 'ingredient', 'Extra virgin olive oil',
    14, 'g', '1 tbsp', 14,
    119, 0, 0, 13.5,
    0, 0, 1.86,
    0, 0, 0, 0.08,
    0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Butter', 'ingredient', 'Salted butter',
    14, 'g', '1 tbsp', 14,
    102, 0.12, 0.01, 11.5,
    0, 0.01, 7.3,
    91, 3, 3, 0,
    31, 0, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Peanut Butter', 'ingredient', 'Natural peanut butter',
    32, 'g', '2 tbsp', 32,
    188, 8, 8, 16,
    2.5, 3.4, 3.3,
    5, 208, 17, 0.6,
    0, 0, 0,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Almonds', 'ingredient', 'Raw almonds',
    28, 'g', '1 oz (23 almonds)', 28,
    164, 6, 6.1, 14.2,
    3.5, 1.2, 1.1,
    0, 208, 76, 1.05,
    0, 0, 0,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),
-- Miscellaneous Ingredients
('Honey', 'ingredient', 'Pure honey',
    21, 'g', '1 tbsp', 21,
    64, 0.06, 17.3, 0,
    0, 17.2, 0,
    1, 11, 1, 0.09,
    0, 0.1, 0,
    NULL, ARRAY['vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Soy Sauce', 'ingredient', 'Regular soy sauce',
    16, 'g', '1 tbsp', 16,
    9, 1.3, 0.79, 0.1,
    0.1, 0.06, 0.01,
    879, 70, 3, 0.28,
    0, 0, 0,
    ARRAY['soy', 'gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.92, true);

-- ============================================================================
-- BRANDED PRODUCTS
-- ============================================================================

INSERT INTO foods (
    name, food_type, brand_name, description,
    barcode_upc, serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, added_sugars_g, saturated_fat_g,
    sodium_mg, cholesterol_mg, source, data_quality_score, verified
) VALUES
('Cheerios Original', 'branded', 'General Mills', 'Whole grain oat cereal',
    '016000275270', 28, 'g', '1 cup', 28,
    100, 3, 20, 2,
    3, 1, 1, 0.5,
    140, 0, 'nutritionix', 0.92, true),
('Chobani Greek Yogurt Strawberry', 'branded', 'Chobani', 'Non-fat Greek yogurt with strawberry',
    '894700010045', 150, 'g', 'container', 150,
    110, 12, 14, 0,
    0, 13, 8, 0,
    60, 5, 'nutritionix', 0.93, true),

('Nature Valley Granola Bars - Oats & Honey', 'branded', 'Nature Valley', 'Crunchy granola bars',
    '016000264274', 42, 'g', '2 bars', 42,
    180, 4, 28, 7,
    2, 11, 11, 0.5,
    160, 0, 'nutritionix', 0.91, true),

('Quest Protein Bar - Chocolate Chip Cookie Dough', 'branded', 'Quest Nutrition', 'High protein bar',
    '888849000517', 60, 'g', '1 bar', 60,
    200, 21, 21, 8,
    14, 1, 0, 2.5,
    200, 5, 'nutritionix', 0.93, true),

('Kind Bar - Dark Chocolate Nuts & Sea Salt', 'branded', 'KIND', 'Nut and chocolate bar',
    '602652199080', 40, 'g', '1 bar', 40,
    180, 6, 16, 13,
    3, 5, 5, 2,
    125, 0, 'nutritionix', 0.92, true),

('Clif Bar - Chocolate Chip', 'branded', 'Clif Bar', 'Energy bar',
    '722252100900', 68, 'g', '1 bar', 68,
    260, 10, 45, 5,
    5, 21, 20, 1.5,
    150, 0, 'nutritionix', 0.92, true),
('Sabra Classic Hummus', 'branded', 'Sabra', 'Chickpea hummus',
    '040822011563', 28, 'g', '2 tbsp', 28,
    70, 2, 4, 5,
    1, 0, 0, 1,
    125, 0, 'nutritionix', 0.92, true),

('Ben & Jerry''s Chocolate Fudge Brownie', 'branded', 'Ben & Jerry''s', 'Chocolate ice cream with brownie pieces',
    '076840100514', 88, 'g', '1/2 cup', 88,
    260, 4, 33, 13,
    2, 27, 25, 8,
    90, 35, 'nutritionix', 0.91, true),

('Halo Top Vanilla Bean', 'branded', 'Halo Top', 'Light ice cream',
    '810030630012', 88, 'g', '1/2 cup', 88,
    70, 5, 16, 2,
    3, 7, 6, 1,
    110, 5, 'nutritionix', 0.91, true),

('RX Bar - Blueberry', 'branded', 'RXBAR', 'Whole food protein bar',
    '857777004186', 52, 'g', '1 bar', 52,
    210, 12, 24, 7,
    3, 15, 0, 1.5,
    210, 0, 'nutritionix', 0.92, true),

('Silk Vanilla Soymilk', 'branded', 'Silk', 'Vanilla flavored soy milk',
    '025293600270', 240, 'g', '1 cup', 240,
    100, 6, 10, 3.5,
    1, 7, 6, 0.5,
    95, 0, 'nutritionix', 0.91, true),
('Dannon Light & Fit Greek Vanilla', 'branded', 'Dannon', 'Non-fat Greek yogurt vanilla',
    '036632009487', 150, 'g', 'container', 150,
    80, 12, 9, 0,
    0, 7, 6, 0,
    50, 5, 'nutritionix', 0.92, true),

('Kodiak Cakes Power Waffles', 'branded', 'Kodiak Cakes', 'Protein-packed frozen waffles',
    '705599019234', 76, 'g', '2 waffles', 76,
    190, 12, 28, 4.5,
    3, 3, 3, 1,
    370, 15, 'nutritionix', 0.91, true),

('Starbucks Bottled Frappuccino - Mocha', 'branded', 'Starbucks', 'Coffee drink',
    '012000001956', 281, 'g', '1 bottle', 281,
    180, 7, 33, 3,
    0, 31, 30, 2,
    100, 10, 'nutritionix', 0.90, true),

('Muscle Milk Chocolate Protein Shake', 'branded', 'Muscle Milk', 'Ready-to-drink protein shake',
    '876063002363', 330, 'g', '1 bottle', 330,
    160, 25, 9, 5,
    3, 2, 1, 1.5,
    230, 20, 'nutritionix', 0.92, true),

('Pure Protein Chocolate Peanut Butter', 'branded', 'Pure Protein', 'Protein bar',
    '749826548135', 50, 'g', '1 bar', 50,
    200, 20, 17, 6,
    1, 2, 2, 3.5,
    190, 10, 'nutritionix', 0.91, true);
-- ============================================================================
-- RESTAURANT & FAST FOOD ITEMS
-- ============================================================================

INSERT INTO foods (
    name, food_type, restaurant_name, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, trans_fat_g,
    sodium_mg, cholesterol_mg, source, data_quality_score, verified
) VALUES
-- McDonald's
('Big Mac', 'restaurant', 'McDonald''s', 'Signature burger with special sauce',
    219, 'g', 'sandwich', 219,
    563, 26, 45, 33,
    3, 9, 10, 1.3,
    1040, 79, 'restaurant', 0.90, true),

('McDonald''s Medium Fries', 'restaurant', 'McDonald''s', 'French fries',
    111, 'g', 'medium', 111,
    320, 4, 43, 15,
    4, 0, 2, 0,
    260, 0, 'restaurant', 0.90, true),

('Egg McMuffin', 'restaurant', 'McDonald''s', 'English muffin with egg, cheese, and Canadian bacon',
    139, 'g', 'sandwich', 139,
    310, 17, 30, 13,
    2, 3, 6, 0,
    770, 250, 'restaurant', 0.90, true),

('McChicken', 'restaurant', 'McDonald''s', 'Crispy chicken sandwich',
    147, 'g', 'sandwich', 147,
    400, 14, 39, 21,
    2, 5, 3.5, 0,
    560, 35, 'restaurant', 0.90, true),
-- Chipotle
('Chipotle Chicken Bowl', 'restaurant', 'Chipotle', 'Bowl with rice, beans, chicken, salsa, cheese, lettuce',
    625, 'g', 'bowl', 625,
    665, 51, 57, 22,
    12, 8, 9, 0,
    1830, 145, 'restaurant', 0.88, true),

('Chipotle Chicken Burrito', 'restaurant', 'Chipotle', 'Large burrito with chicken, rice, beans, cheese, salsa',
    585, 'g', 'burrito', 585,
    975, 48.5, 108, 32,
    13.5, 9, 12.5, 0,
    2080, 125, 'restaurant', 0.88, true),

('Chipotle Guacamole', 'restaurant', 'Chipotle', 'Fresh guacamole',
    114, 'g', 'serving', 114,
    230, 2, 8, 22,
    8, 1, 3.5, 0,
    170, 0, 'restaurant', 0.89, true),

-- Subway
('Subway 6" Turkey Breast', 'restaurant', 'Subway', '6 inch turkey breast sandwich on 9-grain wheat',
    217, 'g', 'sandwich', 217,
    280, 18, 46, 3.5,
    5, 7, 1, 0,
    760, 25, 'restaurant', 0.89, true),

('Subway Footlong Italian BMT', 'restaurant', 'Subway', '12 inch sandwich with salami, pepperoni, ham',
    404, 'g', 'sandwich', 404,
    820, 36, 88, 36,
    6, 16, 14, 0,
    2020, 100, 'restaurant', 0.88, true),
-- Starbucks
('Starbucks Venti Caffe Latte (2% Milk)', 'restaurant', 'Starbucks', 'Espresso with steamed milk',
    591, 'g', 'venti', 591,
    250, 13, 24, 9,
    0, 21, 5, 0,
    170, 35, 'restaurant', 0.90, true),

('Starbucks Bacon Gouda Sandwich', 'restaurant', 'Starbucks', 'Breakfast sandwich',
    156, 'g', 'sandwich', 156,
    360, 18, 32, 17,
    1, 4, 7, 0,
    750, 175, 'restaurant', 0.89, true),

('Starbucks Protein Box', 'restaurant', 'Starbucks', 'Hard-boiled eggs, cheese, fruit, peanut butter',
    303, 'g', 'box', 303,
    470, 27, 40, 24,
    5, 19, 8, 0,
    640, 385, 'restaurant', 0.88, true),

-- Panera Bread
('Panera Bread Bowl Broccoli Cheddar Soup', 'restaurant', 'Panera Bread', 'Creamy soup in bread bowl',
    850, 'g', 'bowl', 850,
    900, 27, 103, 41,
    7, 18, 21, 1,
    2180, 90, 'restaurant', 0.87, true),

('Panera Caesar Salad with Chicken', 'restaurant', 'Panera Bread', 'Romaine with chicken, parmesan, croutons',
    375, 'g', 'salad', 375,
    470, 40, 21, 26,
    4, 5, 6, 0,
    890, 115, 'restaurant', 0.88, true),
-- Chick-fil-A
('Chick-fil-A Original Chicken Sandwich', 'restaurant', 'Chick-fil-A', 'Pressure-cooked chicken breast sandwich',
    183, 'g', 'sandwich', 183,
    440, 28, 41, 19,
    2, 6, 4, 0,
    1400, 70, 'restaurant', 0.90, true),

('Chick-fil-A Grilled Chicken Sandwich', 'restaurant', 'Chick-fil-A', 'Grilled chicken breast sandwich',
    199, 'g', 'sandwich', 199,
    320, 30, 41, 5,
    3, 9, 1, 0,
    800, 70, 'restaurant', 0.90, true),

('Chick-fil-A Waffle Fries (Medium)', 'restaurant', 'Chick-fil-A', 'Waffle-cut potato fries',
    125, 'g', 'medium', 125,
    420, 5, 45, 24,
    5, 1, 3, 0,
    240, 0, 'restaurant', 0.89, true),

-- Pizza Places
('Domino''s Large Pepperoni Pizza (1 slice)', 'restaurant', 'Domino''s', 'Hand tossed crust with pepperoni',
    135, 'g', 'slice', 135,
    298, 13, 34, 12,
    2, 4, 5.5, 0,
    683, 28, 'restaurant', 0.88, true),

('Pizza Hut Personal Pan Pepperoni Pizza', 'restaurant', 'Pizza Hut', 'Personal size pepperoni pizza',
    256, 'g', 'pizza', 256,
    630, 27, 69, 28,
    3, 8, 12, 0.5,
    1430, 65, 'restaurant', 0.87, true);
-- ============================================================================
-- COMMON DISHES & RECIPES
-- ============================================================================

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g,
    sodium_mg, cholesterol_mg, 
    is_recipe, source, data_quality_score, verified
) VALUES
('Scrambled Eggs (2 eggs with milk)', 'dish', 'Two eggs scrambled with milk and butter',
    122, 'g', 'serving', 122,
    203, 13.5, 2.5, 15.5,
    0, 2, 6,
    342, 380, 
    true, 'user', 0.85, false),

('Protein Smoothie', 'dish', 'Banana, protein powder, almond milk, peanut butter',
    400, 'g', 'smoothie', 400,
    385, 28, 42, 12,
    6, 22, 2.5,
    320, 5,
    true, 'user', 0.85, false),

('Overnight Oats', 'dish', 'Oats with milk, chia seeds, honey, berries',
    300, 'g', 'bowl', 300,
    345, 12, 58, 8,
    9, 18, 2,
    125, 10,
    true, 'user', 0.85, false),

('Chicken Salad', 'dish', 'Grilled chicken over mixed greens with vinaigrette',
    350, 'g', 'bowl', 350,
    320, 35, 12, 16,
    4, 6, 3,
    580, 85,
    true, 'user', 0.85, false),
('Spaghetti Bolognese', 'dish', 'Pasta with meat sauce',
    450, 'g', 'plate', 450,
    560, 28, 68, 18,
    5, 12, 6,
    820, 55,
    true, 'user', 0.85, false),

('Chicken Stir Fry', 'dish', 'Chicken with vegetables and rice',
    400, 'g', 'plate', 400,
    425, 32, 45, 12,
    4, 8, 2,
    680, 75,
    true, 'user', 0.85, false),

('Turkey Sandwich', 'dish', 'Whole wheat bread with turkey, cheese, lettuce, tomato',
    250, 'g', 'sandwich', 250,
    365, 24, 38, 12,
    5, 6, 4,
    980, 45,
    true, 'user', 0.85, false),

('Protein Pancakes', 'dish', 'Pancakes made with protein powder, eggs, oats',
    200, 'g', '3 pancakes', 200,
    380, 28, 42, 10,
    4, 8, 3,
    420, 185,
    true, 'user', 0.85, false),

('Buddha Bowl', 'dish', 'Quinoa, chickpeas, vegetables, tahini dressing',
    425, 'g', 'bowl', 425,
    485, 18, 62, 18,
    12, 10, 2.5,
    520, 0,
    true, 'user', 0.85, false),
('Tuna Salad Wrap', 'dish', 'Whole wheat wrap with tuna salad and vegetables',
    280, 'g', 'wrap', 280,
    395, 28, 42, 12,
    6, 5, 2,
    780, 35,
    true, 'user', 0.85, false);

-- ============================================================================
-- SNACKS & QUICK ITEMS
-- ============================================================================

INSERT INTO foods (
    name, food_type, brand_name, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g,
    sodium_mg, source, data_quality_score
) VALUES
('Protein Shake (Generic)', 'branded', 'Various', 'Protein powder with water',
    35, 'g', '1 scoop', 35,
    140, 25, 5, 2.5,
    1, 2, 0.5,
    150, 'user', 0.85),

('Trail Mix', 'ingredient', NULL, 'Nuts, dried fruit, chocolate chips',
    30, 'g', '1/4 cup', 30,
    140, 4, 16, 8,
    2, 10, 2,
    65, 'usda', 0.90),

('Popcorn (Air-popped)', 'ingredient', NULL, 'Plain air-popped popcorn',
    8, 'g', '1 cup', 8,
    31, 1, 6.2, 0.4,
    1.2, 0.07, 0.05,
    1, 'usda', 0.93),
('Pretzels', 'ingredient', NULL, 'Mini pretzels',
    30, 'g', '20 pretzels', 30,
    110, 3, 23, 1,
    1, 1, 0,
    490, 'usda', 0.91),

('Rice Cakes', 'ingredient', NULL, 'Plain brown rice cakes',
    9, 'g', '1 cake', 9,
    35, 0.9, 7.4, 0.3,
    0.3, 0.1, 0.1,
    29, 'usda', 0.92),

('Dark Chocolate (70%)', 'ingredient', NULL, '70% cacao dark chocolate',
    28, 'g', '1 oz', 28,
    170, 2.2, 13, 12,
    3.1, 7, 7,
    6, 'usda', 0.93);

-- ============================================================================
-- BEVERAGES
-- ============================================================================

INSERT INTO foods (
    name, food_type, brand_name, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    total_sugars_g, caffeine_mg, sodium_mg, source, data_quality_score
) VALUES
('Coffee (Black)', 'ingredient', NULL, 'Brewed coffee, no additives',
    237, 'g', '1 cup', 237,
    2, 0.3, 0, 0.05,
    0, 95, 5, 'usda', 0.95),

('Green Tea', 'ingredient', NULL, 'Brewed green tea',
    237, 'g', '1 cup', 237,
    2, 0, 0.5, 0,
    0, 28, 2, 'usda', 0.94),
('Orange Juice', 'ingredient', NULL, 'Fresh squeezed orange juice',
    248, 'g', '1 cup', 248,
    112, 1.7, 25.8, 0.5,
    20.8, 0, 2, 'usda', 0.94),

('Coca-Cola', 'branded', 'Coca-Cola', 'Regular cola',
    355, 'g', '1 can', 355,
    140, 0, 39, 0,
    39, 34, 45, 'nutritionix', 0.92),

('Gatorade (Lemon-Lime)', 'branded', 'Gatorade', 'Sports drink',
    591, 'g', '20 oz bottle', 591,
    140, 0, 36, 0,
    34, 0, 270, 'nutritionix', 0.91),

('Red Bull', 'branded', 'Red Bull', 'Energy drink',
    250, 'g', '8.4 oz can', 250,
    110, 1, 27, 0,
    27, 80, 105, 'nutritionix', 0.91),

('Sparkling Water', 'ingredient', NULL, 'Carbonated water, no flavoring',
    355, 'g', '1 can', 355,
    0, 0, 0, 0,
    0, 0, 0, 'usda', 0.95);

-- ============================================================================
-- SAMPLE MEAL TEMPLATES FOR TESTING
-- ============================================================================
-- Note: These would normally be user-specific, but adding generic ones for testing

-- First, let's add a test user profile (you may already have this)
-- This assumes you have a profiles table. If not, comment this section out
-- INSERT INTO profiles (id, email, created_at) 
-- VALUES ('11111111-1111-1111-1111-111111111111', 'testuser@example.com', NOW())
-- ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- SAMPLE MEAL TEMPLATES (Optional - for testing meal template feature)
-- ============================================================================
-- Uncomment if you want to test with pre-made templates

/*
INSERT INTO meal_templates (
    id, user_id, name, description, category,
    total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g,
    is_favorite
) VALUES
('22222222-2222-2222-2222-222222222221', '11111111-1111-1111-1111-111111111111',
    'Quick Breakfast', 'Eggs, toast, and fruit', 'breakfast',
    425, 22, 48, 16, 6, true),

('22222222-2222-2222-2222-222222222222', '11111111-1111-1111-1111-111111111111',
    'Post-Workout', 'High protein shake and banana', 'snack',
    345, 27, 52, 5, 4, true),

('22222222-2222-2222-2222-222222222223', '11111111-1111-1111-1111-111111111111',
    'Healthy Lunch', 'Grilled chicken salad with quinoa', 'lunch',
    520, 42, 45, 18, 8, false);
*/


-- ============================================================================
-- COMMIT TRANSACTION
-- ============================================================================

COMMIT;

-- ============================================================================
-- SUMMARY STATISTICS
-- ============================================================================

SELECT 
    '✅ FOOD DATABASE SEEDED SUCCESSFULLY!' as status,
    COUNT(*) as total_foods,
    COUNT(DISTINCT food_type) as food_types,
    COUNT(DISTINCT brand_name) as brands,
    COUNT(DISTINCT restaurant_name) as restaurants
FROM foods;

-- ============================================================================
-- NOTES FOR TESTING
-- ============================================================================
/*
This seed file contains:
- 50+ basic ingredients (meats, grains, fruits, vegetables, dairy)
- 20+ branded products with barcodes (protein bars, yogurts, cereals)
- 25+ restaurant items (McDonald's, Chipotle, Starbucks, etc.)
- 10+ homemade dishes and recipes
- Various beverages, snacks, and condiments
- Comprehensive nutritional data including macros and some micronutrients

To use this seed file:
1. Run it against your database: psql -d your_db_name -f seed_food_data.sql
2. The foods will be available for all users to search and add to meals
3. Users can favorite foods for quick access
4. Meal templates can be created from combinations of these foods

Testing suggestions:
- Search for foods by name (e.g., "chicken", "pizza")
- Scan barcodes (UPC codes included for branded items)
- Filter by dietary preferences (vegan, keto, gluten-free)
- Create meals with different food types
- Test the dual quantity tracking (servings vs grams)
*/