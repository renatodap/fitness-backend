-- ============================================================================
-- MIGRATION 008: SEED RESTAURANT CHAIN FOODS
-- ============================================================================
-- Description: Popular items from major restaurant chains
-- Chains: McDonald's, Chipotle, Subway, Starbucks, Panera, Chick-fil-A,
--         Taco Bell, Five Guys, Sweetgreen, Pizza Hut, Domino's, Papa John's
-- Total items: ~120 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (full item weight in grams)
-- - User typically logs "1 item" as the household serving
-- - For example: Big Mac is 219g total, household_serving = "burger (219g)"
-- - Nutrition calculated: multiplier = gram_quantity / serving_size
-- ============================================================================

BEGIN;

-- ============================================================================
-- RESTAURANT CHAIN FOODS
-- ============================================================================

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, cholesterol_mg,
    sodium_mg, potassium_mg, calcium_mg, iron_mg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES

-- ============================================================================
-- McDONALD'S
-- ============================================================================

('McDonalds Big Mac', 'ingredient', 'Big Mac burger with special sauce',
    219, 'g', 'burger (219g)', 219,
    563, 25.9, 46.1, 32.9,
    3.2, 9.1, 10.4, 85,
    1010, 400, 200, 4.5,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.95, true),

('McDonalds Quarter Pounder with Cheese', 'ingredient', 'Quarter Pounder burger',
    200, 'g', 'burger (200g)', 200,
    520, 30, 41, 26,
    3, 10, 13, 95,
    1110, 410, 250, 4.5,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.95, true),

('McDonalds Chicken McNuggets (6 piece)', 'ingredient', 'Six chicken nuggets',
    96, 'g', 'serving (96g)', 96,
    259, 14.6, 16.7, 15.6,
    1, 0, 2.6, 35,
    463, 208, 10, 0.6,
    ARRAY['gluten'], NULL, 'restaurant', 0.94, true),

('McDonalds Medium Fries', 'ingredient', 'Medium french fries',
    111, 'g', 'serving (111g)', 111,
    333, 3.6, 42.3, 15.8,
    3.6, 0.9, 2.3, 0,
    189, 459, 18, 0.7,
    NULL, ARRAY['vegan', 'vegetarian'], 'restaurant', 0.94, true),

('McDonalds McChicken', 'ingredient', 'McChicken sandwich',
    143, 'g', 'sandwich (143g)', 143,
    400, 14, 39, 21,
    2, 5, 3.5, 40,
    560, 200, 80, 2.2,
    ARRAY['gluten'], NULL, 'restaurant', 0.93, true),

('McDonalds Egg McMuffin', 'ingredient', 'Egg McMuffin breakfast sandwich',
    137, 'g', 'sandwich (137g)', 137,
    310, 17.5, 30.7, 13.1,
    2.2, 2.9, 5.1, 260,
    760, 175, 262, 2.9,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.95, true),

('McDonalds Sausage McMuffin with Egg', 'ingredient', 'Sausage egg McMuffin',
    165, 'g', 'sandwich (165g)', 165,
    480, 21.2, 30.9, 30.3,
    1.8, 2.4, 11.5, 285,
    860, 242, 262, 3,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.94, true),

('McDonalds Hash Browns', 'ingredient', 'Crispy hash browns',
    56, 'g', 'hash brown (56g)', 56,
    143, 1.4, 15, 9.1,
    1.4, 0.4, 1.6, 0,
    310, 218, 7, 0.4,
    NULL, ARRAY['vegan', 'vegetarian'], 'restaurant', 0.93, true),

('McDonalds McFlurry Oreo (Regular)', 'ingredient', 'Oreo McFlurry dessert',
    340, 'g', 'cup (340g)', 340,
    510, 11.8, 80.9, 15.9,
    0.9, 61.8, 8.8, 45,
    280, 412, 353, 0.7,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

('McDonalds Apple Pie', 'ingredient', 'Baked apple pie',
    81, 'g', 'pie (81g)', 81,
    232, 2.5, 34.6, 9.9,
    3.7, 13.6, 4.9, 0,
    105, 37, 6, 0.5,
    ARRAY['gluten'], ARRAY['vegetarian'], 'restaurant', 0.93, true),

-- ============================================================================
-- CHIPOTLE
-- ============================================================================

('Chipotle Chicken Bowl (No Rice)', 'ingredient', 'Chicken bowl with fajita veggies, beans, salsa',
    370, 'g', 'bowl (370g)', 370,
    405, 35.1, 34.3, 15.7,
    11.4, 4.6, 4.3, 95,
    1162, 919, 108, 4.3,
    NULL, ARRAY['gluten-free'], 'restaurant', 0.93, true),

('Chipotle Steak Bowl (With Brown Rice)', 'ingredient', 'Steak bowl with brown rice',
    510, 'g', 'bowl (510g)', 510,
    650, 38, 67, 24,
    11, 8, 8, 110,
    1450, 1050, 150, 6,
    ARRAY['dairy'], ARRAY['gluten-free'], 'restaurant', 0.92, true),

('Chipotle Burrito (Chicken)', 'ingredient', 'Chicken burrito with rice and beans',
    510, 'g', 'burrito (510g)', 510,
    965, 47.1, 123, 35.3,
    15.7, 6.9, 12.2, 130,
    2220, 1254, 314, 7.8,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.93, true),

('Chipotle Carnitas Bowl', 'ingredient', 'Carnitas pork bowl',
    400, 'g', 'bowl (400g)', 400,
    550, 32, 40, 30,
    10, 5, 10, 100,
    1300, 850, 120, 5,
    NULL, ARRAY['gluten-free'], 'restaurant', 0.91, false),

('Chipotle Guacamole Side', 'ingredient', 'Side of guacamole',
    113, 'g', 'serving (113g)', 113,
    230, 2.3, 8, 22,
    6.8, 1.1, 3.4, 0,
    370, 460, 11, 0.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'restaurant', 0.94, true),

('Chipotle Chips', 'ingredient', 'Tortilla chips',
    120, 'g', 'bag (120g)', 120,
    540, 7.5, 73.3, 25,
    7.5, 1.7, 3.3, 0,
    420, 233, 167, 1.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'restaurant', 0.93, true),

('Chipotle Sofritas (Tofu)', 'ingredient', 'Braised tofu sofritas',
    113, 'g', 'serving (113g)', 113,
    150, 8, 9, 10,
    6, 2, 1.5, 0,
    560, 200, 80, 2,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'restaurant', 0.92, true),

-- ============================================================================
-- SUBWAY
-- ============================================================================

('Subway 6" Turkey Breast Sub', 'ingredient', 'Turkey breast 6-inch sub on wheat',
    238, 'g', 'sub (238g)', 238,
    280, 19.3, 40.3, 4.6,
    4.2, 5.9, 0.8, 25,
    730, 270, 80, 3.2,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.94, true),

('Subway 6" Italian BMT', 'ingredient', 'Italian BMT 6-inch sub',
    243, 'g', 'sub (243g)', 243,
    390, 18.9, 41.2, 16.5,
    2.9, 7, 6.2, 55,
    1260, 320, 200, 3.3,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'restaurant', 0.93, true),

('Subway 6" Veggie Delite', 'ingredient', 'Veggie Delite 6-inch sub',
    166, 'g', 'sub (166g)', 166,
    200, 8.4, 39.8, 2.4,
    4.8, 6, 0.6, 0,
    310, 300, 60, 2.8,
    ARRAY['gluten'], ARRAY['vegetarian'], 'restaurant', 0.93, true),

('Subway Footlong Meatball Marinara', 'ingredient', 'Meatball marinara 12-inch sub',
    538, 'g', 'sub (538g)', 538,
    940, 38.6, 125.6, 32.7,
    11.2, 18.7, 13.1, 90,
    2340, 850, 400, 7.5,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'restaurant', 0.92, true),

('Subway Chicken Teriyaki 6"', 'ingredient', 'Chicken teriyaki 6-inch sub',
    281, 'g', 'sub (281g)', 281,
    360, 24.9, 53.4, 5.7,
    4.3, 16.3, 1.1, 50,
    1030, 350, 80, 3.6,
    ARRAY['gluten', 'soy'], NULL, 'restaurant', 0.92, true),

-- ============================================================================
-- STARBUCKS
-- ============================================================================

('Starbucks Bacon Gouda Egg Sandwich', 'ingredient', 'Bacon gouda breakfast sandwich',
    136, 'g', 'sandwich (136g)', 136,
    350, 16.2, 30.9, 18.4,
    1.5, 2.9, 7.4, 140,
    720, 176, 221, 2.3,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.94, true),

('Starbucks Spinach Feta Wrap', 'ingredient', 'Spinach feta egg white wrap',
    106, 'g', 'wrap (106g)', 106,
    290, 19.8, 33, 8.5,
    6.6, 3.8, 3.8, 10,
    830, 264, 189, 3.4,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.93, true),

('Starbucks Grilled Cheese', 'ingredient', 'Grilled cheese sandwich',
    127, 'g', 'sandwich (127g)', 127,
    520, 19.7, 42.5, 28.3,
    1.6, 3.9, 15.7, 75,
    940, 157, 520, 2.4,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

('Starbucks Turkey Bacon Wrap', 'ingredient', 'Turkey bacon breakfast wrap',
    123, 'g', 'wrap (123g)', 123,
    320, 19.5, 28.5, 15.4,
    4.1, 2.4, 5.7, 105,
    800, 228, 162, 2.6,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.92, true),

('Starbucks Blueberry Muffin', 'ingredient', 'Blueberry muffin',
    129, 'g', 'muffin (129g)', 129,
    390, 5.4, 61.2, 13.2,
    1.6, 31, 3.1, 55,
    330, 116, 62, 1.9,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.93, true),

-- ============================================================================
-- PANERA BREAD
-- ============================================================================

('Panera Green Goddess Salad (with Chicken)', 'ingredient', 'Green goddess cobb salad',
    397, 'g', 'salad (397g)', 397,
    530, 35.5, 26.9, 33.2,
    7.6, 8.6, 7.6, 145,
    1010, 756, 277, 3.3,
    ARRAY['dairy', 'eggs'], ARRAY['gluten-free'], 'restaurant', 0.93, true),

('Panera Mac & Cheese (Regular)', 'ingredient', 'Classic mac and cheese',
    227, 'g', 'bowl (227g)', 227,
    490, 18.5, 44.1, 26.9,
    1.8, 4.8, 15.4, 80,
    990, 220, 485, 1.3,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.94, true),

('Panera Broccoli Cheddar Soup (Bowl)', 'ingredient', 'Broccoli cheddar soup',
    340, 'g', 'bowl (340g)', 340,
    360, 12.9, 25.9, 23.5,
    4.7, 8.2, 14.1, 65,
    1180, 400, 341, 1.2,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.94, true),

('Panera Mediterranean Bowl', 'ingredient', 'Mediterranean grain bowl',
    392, 'g', 'bowl (392g)', 392,
    500, 17.9, 58.7, 23.5,
    11.2, 8.9, 7.4, 30,
    1010, 714, 255, 4.6,
    ARRAY['dairy'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

('Panera Turkey Avocado BLT', 'ingredient', 'Turkey avocado BLT sandwich',
    368, 'g', 'sandwich (368g)', 368,
    590, 38.6, 47.8, 27.2,
    5.2, 6.5, 6.8, 70,
    1360, 679, 163, 4.1,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.93, true),

-- ============================================================================
-- CHICK-FIL-A
-- ============================================================================

('Chick-fil-A Original Chicken Sandwich', 'ingredient', 'Fried chicken sandwich',
    183, 'g', 'sandwich (183g)', 183,
    440, 28.1, 41, 18.6,
    1.6, 6.0, 3.9, 65,
    1460, 280, 60, 2.5,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.95, true),

('Chick-fil-A Grilled Chicken Sandwich', 'ingredient', 'Grilled chicken sandwich',
    195, 'g', 'sandwich (195g)', 195,
    320, 28.7, 41.5, 5.6,
    3.6, 10.8, 1.5, 65,
    720, 360, 80, 2.6,
    ARRAY['gluten'], NULL, 'restaurant', 0.94, true),

('Chick-fil-A Nuggets (8-count)', 'ingredient', 'Eight chicken nuggets',
    113, 'g', 'serving (113g)', 113,
    250, 27.4, 10.6, 11.5,
    0.9, 1.8, 2.7, 85,
    1210, 354, 18, 0.9,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.94, true),

('Chick-fil-A Waffle Fries (Medium)', 'ingredient', 'Medium waffle fries',
    128, 'g', 'serving (128g)', 128,
    420, 4.7, 45.3, 24.2,
    5.5, 0.8, 4.7, 0,
    280, 766, 23, 0.9,
    NULL, ARRAY['vegan', 'vegetarian'], 'restaurant', 0.93, true),

('Chick-fil-A Cobb Salad', 'ingredient', 'Cobb salad with grilled chicken',
    376, 'g', 'salad (376g)', 376,
    430, 39.9, 12.5, 25.5,
    4.5, 6.4, 8.8, 270,
    1360, 757, 159, 2.3,
    ARRAY['dairy', 'eggs'], ARRAY['gluten-free'], 'restaurant', 0.93, true),

('Chick-fil-A Chicken Biscuit', 'ingredient', 'Chicken biscuit breakfast sandwich',
    150, 'g', 'biscuit (150g)', 150,
    460, 17.3, 45.3, 23.3,
    2, 6, 10.7, 40,
    1500, 200, 80, 2.4,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'restaurant', 0.93, true),

-- ============================================================================
-- TACO BELL
-- ============================================================================

('Taco Bell Crunchy Taco', 'ingredient', 'Crunchy taco with beef',
    78, 'g', 'taco (78g)', 78,
    170, 8, 13, 9,
    3, 1, 3.5, 25,
    310, 130, 60, 1.1,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.94, true),

('Taco Bell Chicken Quesadilla', 'ingredient', 'Chicken quesadilla',
    184, 'g', 'quesadilla (184g)', 184,
    510, 27.2, 37.5, 26.1,
    3.3, 3.8, 12.5, 75,
    1250, 337, 457, 2.7,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.93, true),

('Taco Bell Burrito Supreme (Beef)', 'ingredient', 'Beef burrito supreme',
    248, 'g', 'burrito (248g)', 248,
    390, 16.5, 48, 14.5,
    6.5, 4.8, 7.3, 40,
    1140, 450, 200, 3.6,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.93, true),

('Taco Bell Chalupa Supreme (Chicken)', 'ingredient', 'Chicken chalupa supreme',
    153, 'g', 'chalupa (153g)', 153,
    350, 17, 30, 18,
    3, 3, 5, 40,
    630, 260, 120, 2,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.92, true),

('Taco Bell Mexican Pizza', 'ingredient', 'Mexican pizza',
    216, 'g', 'pizza (216g)', 216,
    540, 20.4, 46.3, 30.6,
    7.4, 4.6, 10.2, 45,
    1000, 444, 296, 3.2,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.92, true),

('Taco Bell Crunchwrap Supreme', 'ingredient', 'Crunchwrap supreme',
    254, 'g', 'crunchwrap (254g)', 254,
    530, 16.5, 71.7, 20.5,
    5.9, 5.9, 7.9, 35,
    1210, 433, 197, 4.3,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.92, true),

-- ============================================================================
-- FIVE GUYS
-- ============================================================================

('Five Guys Hamburger (1 Patty)', 'ingredient', 'Hamburger with one patty',
    303, 'g', 'burger (303g)', 303,
    700, 39.3, 39.6, 43,
    2, 8.3, 18.2, 130,
    430, 567, 100, 5.6,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.93, true),

('Five Guys Cheeseburger (1 Patty)', 'ingredient', 'Cheeseburger with one patty',
    332, 'g', 'burger (332g)', 332,
    840, 47.3, 40.2, 55.1,
    2, 9, 26.1, 165,
    1050, 630, 300, 5.9,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.93, true),

('Five Guys Little Fries', 'ingredient', 'Small fries',
    227, 'g', 'serving (227g)', 227,
    526, 7, 72.2, 23.3,
    8.8, 1.3, 4.4, 0,
    531, 1323, 44, 2.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'restaurant', 0.93, true),

('Five Guys Regular Fries', 'ingredient', 'Regular fries',
    454, 'g', 'serving (454g)', 454,
    953, 12.8, 131.2, 41.4,
    15.9, 2.2, 7.9, 0,
    962, 2405, 79, 4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'restaurant', 0.93, true),

('Five Guys Hot Dog', 'ingredient', 'All-beef hot dog',
    181, 'g', 'hot dog (181g)', 181,
    520, 26, 40.3, 28.5,
    1.7, 8.3, 11, 60,
    1130, 386, 100, 3.5,
    ARRAY['gluten'], NULL, 'restaurant', 0.92, true),

-- ============================================================================
-- SWEETGREEN
-- ============================================================================

('Sweetgreen Harvest Bowl', 'ingredient', 'Harvest bowl with chicken',
    420, 'g', 'bowl (420g)', 420,
    550, 27.1, 58.1, 25.2,
    8.3, 16.7, 4.8, 60,
    570, 905, 119, 3.8,
    ARRAY['nuts'], ARRAY['gluten-free'], 'restaurant', 0.92, true),

('Sweetgreen Kale Caesar', 'ingredient', 'Kale caesar salad with chicken',
    368, 'g', 'salad (368g)', 368,
    560, 30.7, 27.2, 37,
    5.4, 4.3, 8.2, 80,
    650, 652, 272, 2.4,
    ARRAY['dairy', 'eggs', 'fish'], ARRAY['gluten-free'], 'restaurant', 0.92, true),

('Sweetgreen Fish Taco Bowl', 'ingredient', 'Fish taco bowl',
    397, 'g', 'bowl (397g)', 397,
    520, 30.4, 52.4, 21.6,
    11.1, 10.4, 4.8, 55,
    540, 857, 189, 3.3,
    ARRAY['fish', 'dairy'], ARRAY['gluten-free'], 'restaurant', 0.91, false),

('Sweetgreen Shroomami Bowl', 'ingredient', 'Plant-based shroomami bowl',
    397, 'g', 'bowl (397g)', 397,
    490, 13.4, 61.6, 22.9,
    10.9, 14.3, 3.3, 0,
    670, 778, 127, 4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'restaurant', 0.91, false),

-- ============================================================================
-- PIZZA HUT
-- ============================================================================

('Pizza Hut Hand-Tossed Pepperoni (1 Slice)', 'ingredient', 'Hand-tossed pepperoni pizza slice',
    101, 'g', 'slice (101g)', 101,
    260, 11.9, 29.7, 10.9,
    2, 3, 5, 25,
    640, 178, 168, 1.8,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.94, true),

('Pizza Hut Pan Cheese (1 Slice)', 'ingredient', 'Pan cheese pizza slice',
    102, 'g', 'slice (102g)', 102,
    280, 10.8, 29.4, 12.7,
    1, 2, 5.9, 25,
    540, 137, 157, 1.6,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.93, true),

('Pizza Hut Thin Crust Supreme (1 Slice)', 'ingredient', 'Thin crust supreme pizza slice',
    98, 'g', 'slice (98g)', 98,
    230, 10.2, 21.4, 11.2,
    2, 3.1, 5.1, 25,
    570, 224, 143, 1.5,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.93, true),

('Pizza Hut Breadsticks (1 Stick)', 'ingredient', 'Breadstick with marinara',
    36, 'g', 'breadstick (36g)', 36,
    110, 3.3, 15, 4.2,
    0.6, 0.8, 1.4, 0,
    210, 28, 28, 0.8,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

-- ============================================================================
-- DOMINO'S
-- ============================================================================

('Dominos Hand-Tossed Cheese (1 Slice)', 'ingredient', 'Hand-tossed cheese pizza slice',
    98, 'g', 'slice (98g)', 98,
    220, 9.2, 28.6, 7.1,
    1, 2, 3.1, 15,
    460, 122, 143, 1.6,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.94, true),

('Dominos Thin Crust Pepperoni (1 Slice)', 'ingredient', 'Thin crust pepperoni pizza slice',
    69, 'g', 'slice (69g)', 69,
    210, 8.7, 14.5, 13,
    1.4, 1.4, 5.8, 25,
    490, 130, 130, 1.2,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.93, true),

('Dominos Pan Pizza Cheese (1 Slice)', 'ingredient', 'Pan pizza cheese slice',
    125, 'g', 'slice (125g)', 125,
    290, 10.4, 33.6, 12,
    1.6, 3.2, 4.8, 20,
    600, 152, 168, 2,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.93, true),

('Dominos Buffalo Wings (1 Wing)', 'ingredient', 'Hot buffalo chicken wing',
    25, 'g', 'wing (25g)', 25,
    60, 5.6, 0.8, 4,
    0, 0, 1.2, 20,
    360, 32, 8, 0.2,
    NULL, ARRAY['gluten-free'], 'restaurant', 0.92, true),

-- ============================================================================
-- PAPA JOHN'S
-- ============================================================================

('Papa Johns Original Crust Cheese (1 Slice)', 'ingredient', 'Original crust cheese pizza slice',
    105, 'g', 'slice (105g)', 105,
    240, 10.5, 31.4, 8.6,
    1.9, 3.8, 3.8, 20,
    520, 143, 162, 1.7,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.94, true),

('Papa Johns Thin Crust Pepperoni (1 Slice)', 'ingredient', 'Thin crust pepperoni pizza slice',
    71, 'g', 'slice (71g)', 71,
    210, 9.9, 18.3, 11.3,
    1.4, 2.8, 4.2, 25,
    550, 141, 141, 1.3,
    ARRAY['dairy', 'gluten'], NULL, 'restaurant', 0.93, true),

('Papa Johns Garlic Knots (1 Knot)', 'ingredient', 'Garlic parmesan breadstick knot',
    32, 'g', 'knot (32g)', 32,
    90, 2.8, 11.9, 3.4,
    0.6, 0.9, 1.6, 5,
    200, 25, 28, 0.7,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

('Papa Johns Chicken Poppers (5 Pieces)', 'ingredient', 'Five chicken poppers',
    81, 'g', 'serving (81g)', 81,
    170, 11.1, 12.3, 9.9,
    0.6, 0.6, 1.9, 35,
    530, 148, 25, 0.7,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.92, true),

-- ============================================================================
-- MISC POPULAR CHAINS
-- ============================================================================

('Panda Express Orange Chicken', 'ingredient', 'Orange chicken entree',
    196, 'g', 'serving (196g)', 196,
    420, 13.3, 42.9, 21.4,
    1, 18.4, 3.6, 80,
    620, 255, 31, 1.5,
    ARRAY['gluten', 'soy'], NULL, 'restaurant', 0.93, true),

('Panda Express Chow Mein', 'ingredient', 'Stir-fried chow mein noodles',
    227, 'g', 'serving (227g)', 227,
    490, 12.8, 80.2, 13.2,
    6.2, 8.4, 2.2, 0,
    860, 308, 44, 2.6,
    ARRAY['gluten', 'soy'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

('Panda Express Fried Rice', 'ingredient', 'Vegetable fried rice',
    258, 'g', 'serving (258g)', 258,
    520, 11.2, 85.3, 16.3,
    2.7, 5.8, 3.1, 95,
    850, 258, 39, 1.9,
    ARRAY['eggs', 'soy'], ARRAY['vegetarian'], 'restaurant', 0.92, true),

('Wingstop Boneless Wings (6 Pieces)', 'ingredient', 'Six boneless wings',
    170, 'g', 'serving (170g)', 170,
    477, 30.6, 33.5, 23.5,
    1.8, 0, 4.7, 90,
    1270, 353, 41, 2.1,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.92, true),

('Popeyes Chicken Sandwich', 'ingredient', 'Classic fried chicken sandwich',
    207, 'g', 'sandwich (207g)', 207,
    700, 28, 50, 42,
    2, 7, 14, 65,
    1443, 338, 96, 3.4,
    ARRAY['gluten', 'eggs'], NULL, 'restaurant', 0.93, true),

('Popeyes Red Beans and Rice (Regular)', 'ingredient', 'Red beans and rice side',
    174, 'g', 'serving (174g)', 174,
    270, 8, 41.4, 8,
    7.5, 1.1, 2.9, 5,
    680, 368, 57, 2.5,
    NULL, NULL, 'restaurant', 0.92, true),

('Shake Shack ShackBurger', 'ingredient', 'ShackBurger with cheese',
    197, 'g', 'burger (197g)', 197,
    550, 28.9, 33, 32.5,
    1.5, 7.1, 14.7, 95,
    1180, 386, 197, 3.9,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.93, true),

('Shake Shack Cheese Fries', 'ingredient', 'Fries with cheese sauce',
    232, 'g', 'serving (232g)', 232,
    490, 10.3, 45.7, 30.2,
    3.4, 2.6, 8.6, 30,
    1030, 603, 232, 1.7,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'restaurant', 0.92, true),

('In-N-Out Burger Double-Double', 'ingredient', 'Double-Double burger',
    328, 'g', 'burger (328g)', 328,
    670, 37.2, 39, 41.5,
    3, 10.4, 18.3, 120,
    1440, 689, 328, 5.6,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'restaurant', 0.94, true),

('In-N-Out Burger Fries', 'ingredient', 'French fries',
    125, 'g', 'serving (125g)', 125,
    395, 7.2, 54.4, 17.6,
    2.4, 0.8, 5.6, 0,
    245, 680, 24, 1.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'restaurant', 0.93, true);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ RESTAURANT CHAINS SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name LIKE 'McDonalds%'
   OR name LIKE 'Chipotle%'
   OR name LIKE 'Subway%'
   OR name LIKE 'Starbucks%'
   OR name LIKE 'Panera%'
   OR name LIKE 'Chick-fil-A%'
   OR name LIKE 'Taco Bell%'
   OR name LIKE 'Five Guys%'
   OR name LIKE 'Sweetgreen%'
   OR name LIKE 'Pizza Hut%'
   OR name LIKE 'Dominos%'
   OR name LIKE 'Papa Johns%'
   OR name LIKE 'Panda Express%'
   OR name LIKE 'Wingstop%'
   OR name LIKE 'Popeyes%'
   OR name LIKE 'Shake Shack%'
   OR name LIKE 'In-N-Out%';
