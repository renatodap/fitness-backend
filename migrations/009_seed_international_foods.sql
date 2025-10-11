-- ============================================================================
-- MIGRATION 009: SEED INTERNATIONAL FOODS
-- ============================================================================
-- Description: Popular dishes from international cuisines
-- Cuisines: Mexican, Italian, Asian (Chinese, Japanese, Thai, Indian),
--           Middle Eastern, Mediterranean, Latin American
-- Total items: ~80 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (typically 100g or full portion)
-- - User inputs in servings (e.g., "1 serving") OR grams
-- - For prepared dishes, serving_size = typical portion weight
-- - Nutrition calculated: multiplier = gram_quantity / serving_size
-- ============================================================================

BEGIN;

-- ============================================================================
-- INTERNATIONAL FOODS
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
-- MEXICAN & LATIN AMERICAN
-- ============================================================================

('Chicken Tacos (2 Tacos)', 'ingredient', 'Two soft chicken tacos with toppings',
    220, 'g', 'serving (220g)', 220,
    380, 24.5, 37.3, 14.5,
    5.5, 3.6, 4.1, 65,
    680, 418, 145, 2.5,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Beef Tacos (3 Tacos)', 'ingredient', 'Three hard shell beef tacos',
    234, 'g', 'serving (234g)', 234,
    510, 26.5, 39, 26.9,
    9, 3, 10.7, 75,
    930, 390, 180, 3.3,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Chicken Enchiladas (2 Enchiladas)', 'ingredient', 'Two chicken enchiladas with cheese and sauce',
    320, 'g', 'serving (320g)', 320,
    480, 28.1, 42.2, 20.6,
    6.2, 6.9, 10, 80,
    1120, 515, 375, 3.2,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Chicken Burrito', 'ingredient', 'Large chicken burrito with rice and beans',
    450, 'g', 'burrito (450g)', 450,
    850, 42.2, 108.9, 28.9,
    13.3, 6.7, 11.1, 90,
    1800, 1022, 278, 6.7,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Beef Burrito', 'ingredient', 'Large beef burrito with rice and beans',
    480, 'g', 'burrito (480g)', 480,
    950, 42.7, 113.3, 35,
    14.6, 7.3, 15, 95,
    1950, 1063, 292, 7.3,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Chicken Quesadilla', 'ingredient', 'Grilled chicken quesadilla',
    200, 'g', 'quesadilla (200g)', 200,
    520, 28, 38, 27,
    3, 4, 13, 80,
    1200, 350, 450, 2.8,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Chicken Fajitas', 'ingredient', 'Chicken fajitas with peppers and onions',
    280, 'g', 'serving (280g)', 280,
    350, 32.1, 25.4, 14.3,
    5, 8.9, 3.9, 85,
    920, 643, 71, 2.5,
    NULL, ARRAY['gluten-free'], 'user', 0.90, false),

('Tamales (2 Tamales)', 'ingredient', 'Two pork tamales',
    210, 'g', 'serving (210g)', 210,
    420, 16.2, 47.6, 18.6,
    5.7, 2.9, 6.7, 45,
    760, 381, 81, 2.4,
    NULL, NULL, 'user', 0.89, false),

('Elote (Mexican Street Corn)', 'ingredient', 'Grilled corn with mayo, cheese, and chili',
    200, 'g', 'ear (200g)', 200,
    280, 8, 29, 16,
    4, 8, 5, 20,
    580, 350, 120, 1.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.89, false),

('Chile Relleno', 'ingredient', 'Stuffed poblano pepper with cheese',
    225, 'g', 'pepper (225g)', 225,
    365, 16, 23.6, 23.6,
    3.6, 5.8, 11.6, 145,
    710, 427, 382, 2,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.88, false),

-- ============================================================================
-- ITALIAN
-- ============================================================================

('Spaghetti Bolognese', 'ingredient', 'Spaghetti with meat sauce',
    400, 'g', 'serving (400g)', 400,
    520, 24, 68, 16,
    6, 12, 5, 50,
    680, 680, 80, 4,
    ARRAY['gluten'], NULL, 'user', 0.91, false),

('Fettuccine Alfredo', 'ingredient', 'Fettuccine with alfredo sauce',
    380, 'g', 'serving (380g)', 380,
    720, 18.9, 73.7, 38.9,
    3.7, 5.3, 23.2, 110,
    890, 263, 368, 2.6,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Chicken Parmesan', 'ingredient', 'Breaded chicken with marinara and cheese',
    350, 'g', 'serving (350g)', 350,
    580, 42.9, 42.3, 25.7,
    4.3, 8.6, 10, 135,
    1140, 660, 457, 3.4,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.91, false),

('Lasagna (Meat)', 'ingredient', 'Traditional meat lasagna',
    350, 'g', 'serving (350g)', 350,
    490, 28.6, 42.9, 22.9,
    4.3, 10, 11.4, 85,
    960, 600, 343, 3.4,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.92, false),

('Lasagna (Vegetable)', 'ingredient', 'Vegetable lasagna',
    340, 'g', 'serving (340g)', 340,
    410, 20.6, 47.1, 16.5,
    5.9, 11.8, 8.8, 55,
    850, 588, 412, 2.9,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Margherita Pizza (2 Slices)', 'ingredient', 'Two slices Margherita pizza',
    220, 'g', 'serving (220g)', 220,
    480, 18.2, 63.6, 16.8,
    3.6, 7.3, 7.3, 35,
    900, 318, 318, 3.2,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Ravioli (Cheese)', 'ingredient', 'Cheese ravioli with marinara',
    300, 'g', 'serving (300g)', 300,
    420, 18, 54, 15,
    4, 10, 7, 60,
    750, 450, 300, 2.7,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

('Penne Arrabbiata', 'ingredient', 'Penne with spicy tomato sauce',
    320, 'g', 'serving (320g)', 320,
    380, 11.9, 65.6, 8.1,
    5.6, 9.4, 1.2, 0,
    620, 525, 50, 2.9,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.90, false),

('Risotto (Mushroom)', 'ingredient', 'Creamy mushroom risotto',
    300, 'g', 'serving (300g)', 300,
    450, 12, 58.7, 18,
    2.7, 3.3, 9, 40,
    840, 450, 180, 1.8,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false),

('Tiramisu', 'ingredient', 'Classic tiramisu dessert',
    125, 'g', 'serving (125g)', 125,
    322, 6.4, 31.2, 18.4,
    0.8, 20, 10.4, 128,
    90, 136, 96, 0.8,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

-- ============================================================================
-- CHINESE
-- ============================================================================

('General Tsos Chicken', 'ingredient', 'Sweet and spicy fried chicken',
    280, 'g', 'serving (280g)', 280,
    580, 26.1, 58.9, 26.1,
    2.5, 28.6, 5, 80,
    1120, 393, 50, 2.5,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.91, false),

('Kung Pao Chicken', 'ingredient', 'Spicy chicken with peanuts',
    300, 'g', 'serving (300g)', 300,
    480, 30, 36, 24,
    4, 12, 4, 80,
    980, 540, 60, 2.7,
    ARRAY['nuts', 'soy'], NULL, 'user', 0.90, false),

('Sweet and Sour Chicken', 'ingredient', 'Fried chicken in sweet and sour sauce',
    280, 'g', 'serving (280g)', 280,
    550, 22.5, 68.2, 20.4,
    2.1, 36.8, 3.9, 70,
    680, 354, 43, 2,
    ARRAY['gluten'], NULL, 'user', 0.90, false),

('Beef and Broccoli', 'ingredient', 'Stir-fried beef with broccoli',
    320, 'g', 'serving (320g)', 320,
    420, 28.1, 28.8, 20.6,
    4.4, 8.8, 5, 70,
    1120, 643, 88, 3.2,
    ARRAY['soy'], NULL, 'user', 0.91, false),

('Mongolian Beef', 'ingredient', 'Stir-fried beef with scallions',
    280, 'g', 'serving (280g)', 280,
    520, 26.1, 42.5, 26.1,
    2.5, 20.7, 7.1, 75,
    1180, 464, 54, 2.9,
    ARRAY['soy'], NULL, 'user', 0.90, false),

('Moo Shu Pork (with Pancakes)', 'ingredient', 'Shredded pork with vegetables and pancakes',
    350, 'g', 'serving (350g)', 350,
    480, 24.3, 44.3, 22.9,
    5.1, 8.6, 5.1, 65,
    1020, 514, 97, 2.9,
    ARRAY['eggs', 'gluten', 'soy'], NULL, 'user', 0.89, false),

('Lo Mein (Chicken)', 'ingredient', 'Chicken lo mein noodles',
    350, 'g', 'serving (350g)', 350,
    520, 24.3, 68.6, 17.1,
    5.1, 8.6, 2.9, 60,
    1080, 457, 60, 3.1,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.90, false),

('Fried Rice (Chicken)', 'ingredient', 'Chicken fried rice',
    300, 'g', 'serving (300g)', 300,
    480, 18, 66, 16,
    3, 6, 3, 95,
    900, 270, 40, 2.1,
    ARRAY['eggs', 'soy'], NULL, 'user', 0.91, false),

('Spring Rolls (2 Rolls)', 'ingredient', 'Two vegetable spring rolls',
    140, 'g', 'serving (140g)', 140,
    280, 5.7, 34.3, 13,
    3.6, 3.6, 2.1, 0,
    560, 171, 36, 1.6,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

('Egg Rolls (2 Rolls)', 'ingredient', 'Two pork egg rolls',
    170, 'g', 'serving (170g)', 170,
    340, 11.2, 38.8, 15.9,
    3.5, 4.7, 3.5, 30,
    710, 224, 47, 2,
    ARRAY['eggs', 'gluten'], NULL, 'user', 0.90, false),

-- ============================================================================
-- JAPANESE
-- ============================================================================

('California Roll (8 Pieces)', 'ingredient', 'Eight pieces California sushi roll',
    220, 'g', 'serving (220g)', 220,
    280, 9.1, 45.5, 6.8,
    3.2, 6.8, 0.9, 20,
    590, 227, 68, 1.4,
    ARRAY['fish', 'gluten'], NULL, 'user', 0.92, false),

('Spicy Tuna Roll (8 Pieces)', 'ingredient', 'Eight pieces spicy tuna roll',
    240, 'g', 'serving (240g)', 240,
    320, 14.2, 47.5, 8.3,
    3.3, 6.7, 1.2, 25,
    680, 267, 75, 1.7,
    ARRAY['fish', 'eggs', 'gluten'], NULL, 'user', 0.91, false),

('Salmon Nigiri (4 Pieces)', 'ingredient', 'Four pieces salmon nigiri sushi',
    140, 'g', 'serving (140g)', 140,
    220, 14.3, 30, 4.3,
    1.4, 3.6, 0.7, 30,
    380, 257, 21, 0.9,
    ARRAY['fish'], ARRAY['gluten-free'], 'user', 0.91, false),

('Tuna Nigiri (4 Pieces)', 'ingredient', 'Four pieces tuna nigiri sushi',
    136, 'g', 'serving (136g)', 136,
    205, 16.9, 29.4, 1.5,
    1.5, 3.7, 0.4, 25,
    370, 265, 22, 0.9,
    ARRAY['fish'], ARRAY['gluten-free'], 'user', 0.91, false),

('Chicken Teriyaki Bowl', 'ingredient', 'Chicken teriyaki with rice',
    400, 'g', 'bowl (400g)', 400,
    560, 32, 76, 12,
    3, 24, 2, 85,
    1480, 560, 60, 3.2,
    ARRAY['soy'], NULL, 'user', 0.91, false),

('Beef Teriyaki Bowl', 'ingredient', 'Beef teriyaki with rice',
    420, 'g', 'bowl (420g)', 420,
    640, 34.3, 76.2, 20.5,
    3.3, 24.8, 6.7, 90,
    1520, 610, 67, 3.8,
    ARRAY['soy'], NULL, 'user', 0.91, false),

('Chicken Katsu', 'ingredient', 'Breaded fried chicken cutlet',
    200, 'g', 'serving (200g)', 200,
    480, 26, 38, 24,
    2, 4, 5, 85,
    720, 380, 40, 2.4,
    ARRAY['eggs', 'gluten'], NULL, 'user', 0.90, false),

('Ramen (Pork)', 'ingredient', 'Pork ramen with noodles and broth',
    500, 'g', 'bowl (500g)', 500,
    580, 28, 74, 18,
    5, 8, 6, 70,
    1680, 600, 80, 4,
    ARRAY['eggs', 'gluten', 'soy'], NULL, 'user', 0.91, false),

('Gyoza (6 Dumplings)', 'ingredient', 'Six pork dumplings',
    150, 'g', 'serving (150g)', 150,
    270, 11.3, 30, 11.3,
    2, 2.7, 3.3, 30,
    600, 193, 40, 1.7,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.90, false),

('Miso Soup', 'ingredient', 'Traditional miso soup',
    240, 'g', 'bowl (240g)', 240,
    50, 3.3, 6.2, 1.7,
    1.2, 2.5, 0.4, 0,
    920, 158, 42, 0.8,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

-- ============================================================================
-- THAI
-- ============================================================================

('Pad Thai (Chicken)', 'ingredient', 'Chicken pad Thai noodles',
    400, 'g', 'serving (400g)', 400,
    620, 28, 72, 24,
    4, 20, 4, 80,
    1280, 480, 80, 3.2,
    ARRAY['eggs', 'nuts', 'fish'], NULL, 'user', 0.91, false),

('Pad Thai (Shrimp)', 'ingredient', 'Shrimp pad Thai noodles',
    400, 'g', 'serving (400g)', 400,
    580, 26, 72, 20,
    4, 20, 3, 140,
    1320, 440, 80, 3,
    ARRAY['eggs', 'nuts', 'fish'], NULL, 'user', 0.91, false),

('Green Curry (Chicken)', 'ingredient', 'Thai green curry with chicken',
    380, 'g', 'serving (380g)', 380,
    520, 26.3, 34.2, 30.5,
    5.3, 11.8, 20.5, 75,
    1140, 660, 76, 3,
    NULL, NULL, 'user', 0.90, false),

('Red Curry (Chicken)', 'ingredient', 'Thai red curry with chicken',
    380, 'g', 'serving (380g)', 380,
    540, 27.4, 36.8, 31.6,
    5.3, 13.2, 21.1, 80,
    1180, 684, 79, 3.2,
    NULL, NULL, 'user', 0.90, false),

('Massaman Curry (Beef)', 'ingredient', 'Thai massaman curry with beef',
    400, 'g', 'serving (400g)', 400,
    650, 30, 48, 38,
    6, 18, 24, 85,
    1100, 760, 90, 3.8,
    ARRAY['nuts'], NULL, 'user', 0.89, false),

('Drunken Noodles (Pad Kee Mao)', 'ingredient', 'Spicy Thai basil noodles with chicken',
    380, 'g', 'serving (380g)', 380,
    560, 24.2, 68.4, 21.1,
    4.7, 10.5, 4.2, 75,
    1240, 526, 71, 3.4,
    ARRAY['soy'], NULL, 'user', 0.90, false),

('Tom Yum Soup (Shrimp)', 'ingredient', 'Spicy and sour Thai shrimp soup',
    350, 'g', 'bowl (350g)', 350,
    180, 15.7, 18.6, 5.7,
    2.9, 8.6, 1.4, 100,
    1050, 457, 57, 2,
    ARRAY['fish'], ARRAY['gluten-free'], 'user', 0.90, false),

('Larb Gai (Thai Chicken Salad)', 'ingredient', 'Spicy Thai chicken salad',
    250, 'g', 'serving (250g)', 250,
    280, 28, 16, 12,
    3, 6, 3, 85,
    880, 475, 50, 2.2,
    ARRAY['fish'], ARRAY['gluten-free'], 'user', 0.89, false),

-- ============================================================================
-- INDIAN
-- ============================================================================

('Chicken Tikka Masala', 'ingredient', 'Chicken in creamy tomato curry sauce',
    380, 'g', 'serving (380g)', 380,
    520, 30.4, 30.4, 30.4,
    5.3, 11.4, 15.2, 95,
    1100, 722, 152, 3.4,
    ARRAY['dairy'], NULL, 'user', 0.91, false),

('Butter Chicken', 'ingredient', 'Chicken in buttery tomato cream sauce',
    370, 'g', 'serving (370g)', 370,
    580, 28.9, 27, 38.9,
    4.3, 10.8, 21.6, 110,
    1040, 689, 135, 3.2,
    ARRAY['dairy'], NULL, 'user', 0.91, false),

('Chicken Curry', 'ingredient', 'Traditional chicken curry',
    350, 'g', 'serving (350g)', 350,
    420, 28.6, 25.7, 22.9,
    4.6, 8.6, 10, 85,
    980, 629, 100, 3.1,
    ARRAY['dairy'], NULL, 'user', 0.90, false),

('Lamb Vindaloo', 'ingredient', 'Spicy lamb curry',
    370, 'g', 'serving (370g)', 370,
    520, 32.4, 24.3, 32.4,
    5.1, 8.1, 13.5, 95,
    1160, 703, 92, 3.9,
    NULL, NULL, 'user', 0.89, false),

('Chana Masala', 'ingredient', 'Spiced chickpea curry',
    320, 'g', 'serving (320g)', 320,
    350, 13.8, 48.8, 11.9,
    11.9, 9.4, 1.9, 0,
    880, 608, 94, 4.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

('Saag Paneer', 'ingredient', 'Spinach curry with paneer cheese',
    300, 'g', 'serving (300g)', 300,
    380, 16, 18, 27,
    5, 7, 14, 60,
    820, 570, 300, 3.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false),

('Biryani (Chicken)', 'ingredient', 'Spiced basmati rice with chicken',
    400, 'g', 'serving (400g)', 400,
    560, 26, 68, 20,
    4, 6, 6, 80,
    1120, 560, 80, 3.2,
    ARRAY['dairy'], NULL, 'user', 0.91, false),

('Naan Bread', 'ingredient', 'Traditional Indian flatbread',
    90, 'g', 'piece (90g)', 90,
    262, 7.8, 44.4, 5.6,
    2.2, 3.3, 1.1, 0,
    422, 111, 56, 2.4,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Samosas (2 Pieces)', 'ingredient', 'Two vegetable samosas',
    130, 'g', 'serving (130g)', 130,
    280, 5.4, 33.8, 13.8,
    4.6, 3.8, 3.1, 0,
    520, 262, 31, 1.8,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

-- ============================================================================
-- MIDDLE EASTERN & MEDITERRANEAN
-- ============================================================================

('Falafel (4 Pieces)', 'ingredient', 'Four falafel balls',
    140, 'g', 'serving (140g)', 140,
    333, 13.3, 31.4, 17.9,
    7.1, 1.4, 2.1, 0,
    590, 398, 84, 3.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Chicken Shawarma Wrap', 'ingredient', 'Chicken shawarma in pita',
    300, 'g', 'wrap (300g)', 300,
    480, 32, 46, 18,
    5, 5, 5, 85,
    1080, 510, 120, 3.3,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Beef Shawarma Plate', 'ingredient', 'Beef shawarma with rice and salad',
    450, 'g', 'plate (450g)', 450,
    680, 38.7, 58.7, 30.2,
    7.8, 9, 10.9, 100,
    1340, 810, 135, 5,
    ARRAY['dairy'], NULL, 'user', 0.90, false),

('Gyro (Lamb)', 'ingredient', 'Greek lamb gyro sandwich',
    340, 'g', 'gyro (340g)', 340,
    620, 29.4, 50.3, 32.4,
    4.1, 8.2, 12.4, 90,
    1220, 559, 206, 4.1,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Greek Salad', 'ingredient', 'Traditional Greek salad with feta',
    280, 'g', 'salad (280g)', 280,
    220, 6.8, 15.4, 15.7,
    4.3, 8.9, 5.4, 25,
    720, 471, 154, 1.7,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Moussaka', 'ingredient', 'Greek eggplant and meat casserole',
    350, 'g', 'serving (350g)', 350,
    450, 22.9, 31.4, 25.7,
    7.1, 11.4, 11.4, 80,
    920, 714, 257, 3.1,
    ARRAY['dairy', 'eggs'], NULL, 'user', 0.89, false),

('Tabbouleh', 'ingredient', 'Bulgur wheat salad with herbs',
    180, 'g', 'serving (180g)', 180,
    198, 5, 27.2, 8.3,
    5.6, 2.2, 1.1, 0,
    360, 322, 28, 1.8,
    NULL, ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Kibbeh (3 Pieces)', 'ingredient', 'Three beef kibbeh',
    180, 'g', 'serving (180g)', 180,
    380, 18.9, 27.2, 22.2,
    3.3, 2.2, 8.3, 65,
    620, 344, 61, 2.9,
    NULL, NULL, 'user', 0.88, false);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ INTERNATIONAL FOODS SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Chicken Tacos (2 Tacos)', 'Chicken Burrito', 'Chicken Quesadilla',
    'Spaghetti Bolognese', 'Fettuccine Alfredo', 'Chicken Parmesan', 'Lasagna (Meat)',
    'General Tsos Chicken', 'Beef and Broccoli', 'Fried Rice (Chicken)',
    'California Roll (8 Pieces)', 'Chicken Teriyaki Bowl', 'Ramen (Pork)',
    'Pad Thai (Chicken)', 'Green Curry (Chicken)', 'Tom Yum Soup (Shrimp)',
    'Chicken Tikka Masala', 'Butter Chicken', 'Chana Masala', 'Biryani (Chicken)',
    'Falafel (4 Pieces)', 'Chicken Shawarma Wrap', 'Gyro (Lamb)', 'Greek Salad'
);
