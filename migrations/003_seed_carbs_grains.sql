-- ============================================================================
-- CARBS & GRAINS - COMPREHENSIVE SEED DATA
-- ============================================================================
-- Purpose: Breads, pasta, rice, potatoes, cereals, grains, baked goods
-- Date: 2025-01-10
-- Total Items: ~80
-- ============================================================================

BEGIN;

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, cholesterol_mg,
    sodium_mg, potassium_mg, iron_mg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES

-- ============================================================================
-- BREAD & BREAD PRODUCTS
-- ============================================================================

('White Bread (Sliced)', 'ingredient', 'Enriched white bread',
    28, 'g', 'slice', 28,
    75, 2.3, 14.2, 0.9,
    0.7, 1.4, 0.2, 0,
    147, 33, 0.9,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Whole Wheat Bread (100%)', 'ingredient', '100% whole wheat bread',
    28, 'g', 'slice', 28,
    69, 3.5, 11.6, 1.1,
    1.9, 1.4, 0.24, 0,
    132, 70, 0.9,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Sourdough Bread', 'ingredient', 'Traditional sourdough',
    28, 'g', 'slice', 28,
    73, 3.0, 14.1, 0.5,
    0.7, 0.5, 0.1, 0,
    174, 44, 1.0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Rye Bread', 'ingredient', 'Dark rye bread',
    32, 'g', 'slice', 32,
    83, 2.7, 15.5, 1.1,
    1.9, 1.0, 0.2, 0,
    211, 53, 0.9,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Multigrain Bread', 'ingredient', '7-grain bread',
    28, 'g', 'slice', 28,
    69, 3.5, 12.0, 1.1,
    1.9, 2.0, 0.2, 0,
    127, 69, 0.9,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Bagel (Plain)', 'ingredient', 'Plain bagel',
    95, 'g', 'bagel', 95,
    257, 10.0, 50.4, 1.5,
    2.1, 5.0, 0.3, 0,
    475, 105, 3.5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('English Muffin', 'ingredient', 'Whole wheat English muffin',
    57, 'g', 'muffin', 57,
    134, 5.8, 26.2, 1.5,
    4.4, 1.6, 0.2, 0,
    218, 106, 1.6,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Pita Bread (White)', 'ingredient', 'White pita pocket',
    60, 'g', 'pita', 60,
    165, 5.5, 33.4, 0.7,
    1.3, 0.6, 0.1, 0,
    322, 72, 1.6,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Pita Bread (Whole Wheat)', 'ingredient', 'Whole wheat pita',
    64, 'g', 'pita', 64,
    170, 6.3, 35.2, 1.7,
    4.7, 0.7, 0.3, 0,
    340, 109, 1.9,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Naan Bread', 'ingredient', 'Indian flatbread',
    90, 'g', 'piece', 90,
    262, 7.6, 45.4, 5.1,
    2.0, 3.6, 1.3, 23,
    419, 115, 2.8,
    ARRAY['gluten', 'dairy'], ARRAY['vegetarian'], 'usda', 0.92, true),

('Tortilla (Flour, 8-inch)', 'ingredient', 'Flour tortilla',
    49, 'g', 'tortilla', 49,
    146, 3.9, 24.3, 3.7,
    1.5, 1.0, 1.0, 0,
    391, 70, 1.6,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Tortilla (Corn, 6-inch)', 'ingredient', 'Corn tortilla',
    26, 'g', 'tortilla', 26,
    52, 1.4, 10.7, 0.7,
    1.5, 0.3, 0.1, 0,
    12, 40, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Croissant (Plain)', 'ingredient', 'Butter croissant',
    67, 'g', 'croissant', 67,
    272, 5.5, 31.0, 14.1,
    1.7, 7.0, 8.2, 45,
    424, 88, 1.8,
    ARRAY['gluten', 'dairy'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Dinner Roll', 'ingredient', 'Soft white dinner roll',
    43, 'g', 'roll', 43,
    120, 3.7, 20.6, 2.4,
    1.1, 2.8, 0.6, 0,
    206, 41, 1.3,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Hamburger Bun', 'ingredient', 'Sesame seed bun',
    50, 'g', 'bun', 50,
    140, 4.7, 24.4, 2.4,
    1.5, 3.5, 0.5, 0,
    241, 61, 1.8,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Hot Dog Bun', 'ingredient', 'Long hot dog bun',
    43, 'g', 'bun', 43,
    120, 4.1, 21.6, 2.0,
    0.9, 3.2, 0.5, 0,
    206, 44, 1.5,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

-- ============================================================================
-- PASTA
-- ============================================================================

('Spaghetti (Cooked)', 'ingredient', 'Regular spaghetti, boiled',
    100, 'g', '1/2 cup (70g)', 70,
    131, 5.0, 25.0, 1.1,
    1.8, 0.56, 0.2, 0,
    1, 44, 0.91,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Penne (Cooked)', 'ingredient', 'Penne pasta, boiled',
    100, 'g', '1 cup (107g)', 107,
    131, 5.0, 25.0, 1.1,
    1.8, 0.56, 0.2, 0,
    1, 44, 0.91,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Fettuccine (Cooked)', 'ingredient', 'Fettuccine pasta, boiled',
    100, 'g', '1/2 cup (70g)', 70,
    131, 5.0, 25.0, 1.1,
    1.8, 0.56, 0.2, 0,
    1, 44, 0.91,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Whole Wheat Pasta (Cooked)', 'ingredient', 'Whole wheat spaghetti',
    100, 'g', '1/2 cup (70g)', 70,
    124, 5.3, 26.5, 0.5,
    3.9, 0.8, 0.1, 0,
    3, 62, 1.1,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Protein Pasta (Cooked)', 'ingredient', 'Chickpea or lentil pasta',
    100, 'g', '1/2 cup (70g)', 70,
    160, 11.0, 27.0, 2.5,
    5.0, 2.0, 0.3, 0,
    5, 280, 2.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Egg Noodles (Cooked)', 'ingredient', 'Wide egg noodles',
    100, 'g', '1/2 cup (80g)', 80,
    138, 4.5, 25.2, 2.1,
    1.2, 0.4, 0.4, 29,
    8, 45, 1.5,
    ARRAY['gluten', 'eggs'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Lasagna Noodles (Cooked)', 'ingredient', 'Lasagna sheets',
    100, 'g', '1 sheet (35g)', 35,
    135, 4.7, 25.9, 1.5,
    1.8, 0.9, 0.3, 0,
    2, 50, 1.0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.93, true),

('Macaroni (Cooked)', 'ingredient', 'Elbow macaroni',
    100, 'g', '1 cup (140g)', 140,
    131, 5.0, 25.0, 1.1,
    1.8, 0.56, 0.2, 0,
    1, 44, 0.91,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Orzo (Cooked)', 'ingredient', 'Rice-shaped pasta',
    100, 'g', '1/2 cup (85g)', 85,
    130, 4.3, 26.1, 0.9,
    1.3, 0.5, 0.1, 0,
    1, 40, 0.8,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.93, true),

('Ramen Noodles (Cooked)', 'ingredient', 'Fresh ramen noodles',
    100, 'g', 'serving (150g)', 150,
    138, 4.5, 27.3, 0.6,
    1.2, 0.2, 0.1, 0,
    60, 30, 0.9,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.92, true),

-- ============================================================================
-- RICE
-- ============================================================================

('White Rice (Long Grain, Cooked)', 'ingredient', 'Fluffy long grain white rice',
    100, 'g', '1/2 cup (79g)', 79,
    130, 2.7, 28.2, 0.3,
    0.4, 0.05, 0.1, 0,
    1, 35, 0.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Brown Rice (Long Grain, Cooked)', 'ingredient', 'Cooked brown rice',
    100, 'g', '1/2 cup (98g)', 98,
    112, 2.3, 23.5, 0.8,
    1.8, 0.35, 0.2, 0,
    3, 79, 0.52,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Jasmine Rice (Cooked)', 'ingredient', 'Thai jasmine white rice',
    100, 'g', '1/2 cup (79g)', 79,
    129, 2.7, 27.9, 0.2,
    0.4, 0, 0.05, 0,
    1, 35, 0.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Basmati Rice (Cooked)', 'ingredient', 'Indian basmati rice',
    100, 'g', '1/2 cup (79g)', 79,
    121, 2.5, 25.2, 0.4,
    0.4, 0.1, 0.1, 0,
    1, 37, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Wild Rice (Cooked)', 'ingredient', 'Cooked wild rice',
    100, 'g', '1/2 cup (82g)', 82,
    101, 4.0, 21.3, 0.3,
    1.8, 0.7, 0.05, 0,
    3, 101, 0.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Arborio Rice (Cooked)', 'ingredient', 'Risotto rice',
    100, 'g', '1/2 cup (80g)', 80,
    130, 2.4, 28.7, 0.1,
    0.6, 0, 0, 0,
    1, 25, 0.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Sushi Rice (Cooked)', 'ingredient', 'Seasoned sushi rice',
    100, 'g', '1/2 cup (75g)', 75,
    140, 2.5, 30.8, 0.2,
    0.3, 4.0, 0, 0,
    280, 30, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Instant Rice (Cooked)', 'ingredient', 'Minute rice, prepared',
    100, 'g', '1/2 cup (82g)', 82,
    123, 2.5, 26.9, 0.2,
    0.6, 0.1, 0.05, 0,
    5, 22, 0.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.91, true),

('Fried Rice (Restaurant Style)', 'dish', 'Vegetable fried rice',
    100, 'g', '1 cup (198g)', 198,
    163, 3.2, 25.8, 5.6,
    1.2, 1.5, 0.8, 42,
    460, 88, 1.0,
    ARRAY['eggs', 'soy'], ARRAY['vegetarian'], 'usda', 0.88, true),

-- ============================================================================
-- POTATOES
-- ============================================================================

('Russet Potato (Baked)', 'ingredient', 'Baked russet with skin',
    100, 'g', 'medium (173g)', 173,
    93, 2.5, 21.2, 0.1,
    2.2, 1.2, 0.03, 0,
    6, 544, 1.0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Red Potato (Boiled)', 'ingredient', 'Boiled red potatoes',
    100, 'g', 'small (90g)', 90,
    89, 1.9, 20.1, 0.1,
    1.8, 1.3, 0.03, 0,
    7, 379, 0.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Yukon Gold Potato (Roasted)', 'ingredient', 'Roasted Yukon gold',
    100, 'g', 'medium (150g)', 150,
    110, 2.3, 24.5, 0.9,
    2.0, 1.5, 0.1, 0,
    8, 455, 0.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Mashed Potatoes (With Butter & Milk)', 'dish', 'Creamy mashed potatoes',
    100, 'g', '1/2 cup (105g)', 105,
    113, 2.0, 16.9, 4.2,
    1.5, 1.8, 2.6, 12,
    333, 284, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.92, true),

('French Fries (Fast Food)', 'dish', 'Deep fried french fries',
    100, 'g', 'medium (117g)', 117,
    312, 3.4, 41.4, 14.5,
    3.8, 0.2, 2.3, 0,
    210, 579, 0.7,
    NULL, ARRAY['vegan', 'vegetarian'], 'usda', 0.91, true),

('Hash Browns', 'dish', 'Shredded fried hash browns',
    100, 'g', '1 patty (65g)', 65,
    265, 2.6, 35.1, 12.5,
    2.9, 0.9, 1.9, 0,
    534, 365, 0.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.90, true),

('Tater Tots', 'dish', 'Fried potato nuggets',
    100, 'g', '9 pieces (84g)', 84,
    227, 2.8, 29.1, 11.0,
    2.6, 0.7, 1.7, 0,
    513, 377, 0.8,
    NULL, ARRAY['vegetarian'], 'usda', 0.89, true),

('Potato Chips (Regular)', 'ingredient', 'Classic potato chips',
    28, 'g', '1 oz (15 chips)', 28,
    152, 2.0, 15.0, 10.0,
    1.1, 0.1, 3.1, 0,
    149, 361, 0.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- CEREALS & OATS
-- ============================================================================

('Oatmeal (Cooked with Water)', 'ingredient', 'Plain cooked oats',
    100, 'g', '1/2 cup (117g)', 117,
    71, 2.5, 12.0, 1.5,
    1.7, 0.3, 0.3, 0,
    4, 70, 0.9,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Steel Cut Oats (Cooked)', 'ingredient', 'Irish oatmeal',
    100, 'g', '1/2 cup (125g)', 125,
    71, 2.5, 12.3, 1.4,
    2.0, 0.4, 0.2, 0,
    3, 61, 1.0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Instant Oatmeal (Plain)', 'ingredient', 'Quick oats, prepared',
    100, 'g', 'packet (28g dry)', 28,
    68, 2.4, 12.0, 1.4,
    1.7, 0.4, 0.2, 0,
    49, 61, 4.2,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.93, true),

('Cheerios (Original)', 'ingredient', 'Whole grain oat cereal',
    28, 'g', '1 cup', 28,
    100, 3.0, 20.0, 2.0,
    3.0, 1.0, 0.5, 0,
    140, 95, 8.1,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Corn Flakes', 'ingredient', 'Toasted corn flakes',
    28, 'g', '1 cup', 28,
    100, 2.0, 24.0, 0,
    1.0, 3.0, 0, 0,
    200, 25, 8.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Frosted Flakes', 'ingredient', 'Sugar frosted corn flakes',
    31, 'g', '3/4 cup', 31,
    110, 1.0, 28.0, 0,
    0, 12.0, 0, 0,
    150, 25, 8.1,
    NULL, ARRAY['vegetarian'], 'usda', 0.92, true),

('Raisin Bran', 'ingredient', 'Bran flakes with raisins',
    59, 'g', '1 cup', 59,
    190, 5.0, 46.0, 1.5,
    7.0, 18.0, 0, 0,
    210, 340, 16.2,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.93, true),

('Granola (Plain)', 'ingredient', 'Rolled oats granola',
    50, 'g', '1/2 cup', 50,
    229, 5.8, 32.5, 9.5,
    4.3, 10.5, 1.5, 0,
    14, 205, 1.6,
    ARRAY['gluten', 'nuts'], ARRAY['vegetarian'], 'usda', 0.92, true),

('Grape-Nuts', 'ingredient', 'Wheat and barley nuggets',
    58, 'g', '1/2 cup', 58,
    208, 6.7, 47.1, 1.0,
    7.0, 10.7, 0.2, 0,
    354, 239, 16.2,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.92, true),

-- ============================================================================
-- OTHER GRAINS
-- ============================================================================

('Quinoa (Cooked)', 'ingredient', 'Cooked quinoa',
    100, 'g', '1/2 cup (93g)', 93,
    120, 4.4, 21.3, 1.9,
    2.8, 0.87, 0.23, 0,
    7, 172, 1.49,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Couscous (Cooked)', 'ingredient', 'Moroccan couscous',
    100, 'g', '1/2 cup (78g)', 78,
    112, 3.8, 23.2, 0.2,
    1.4, 0.1, 0.03, 0,
    5, 58, 0.4,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Bulgur (Cooked)', 'ingredient', 'Cracked wheat bulgur',
    100, 'g', '1/2 cup (91g)', 91,
    83, 3.1, 18.6, 0.2,
    4.5, 0.1, 0.04, 0,
    5, 68, 0.96,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Farro (Cooked)', 'ingredient', 'Ancient wheat grain',
    100, 'g', '1/2 cup (85g)', 85,
    123, 5.0, 26.4, 0.8,
    3.5, 0.6, 0.1, 0,
    3, 145, 1.0,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.93, true),

('Barley (Cooked)', 'ingredient', 'Pearl barley',
    100, 'g', '1/2 cup (79g)', 79,
    123, 2.3, 28.2, 0.4,
    3.8, 0.3, 0.08, 0,
    3, 93, 1.3,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Polenta (Cooked)', 'ingredient', 'Cooked cornmeal',
    100, 'g', '1/2 cup (125g)', 125,
    70, 1.6, 15.4, 0.3,
    0.7, 0.2, 0.04, 0,
    236, 25, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Grits (Cooked)', 'ingredient', 'Southern hominy grits',
    100, 'g', '1/2 cup (121g)', 121,
    59, 1.4, 12.9, 0.2,
    0.5, 0.2, 0.03, 0,
    154, 27, 0.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

-- ============================================================================
-- BAKED GOODS & PASTRIES
-- ============================================================================

('Blueberry Muffin', 'dish', 'Bakery-style blueberry muffin',
    113, 'g', 'muffin', 113,
    426, 6.2, 60.7, 17.7,
    2.6, 30.3, 3.6, 45,
    381, 107, 2.0,
    ARRAY['gluten', 'eggs', 'dairy'], ARRAY['vegetarian'], 'usda', 0.91, true),

('Chocolate Chip Muffin', 'dish', 'Chocolate chip muffin',
    113, 'g', 'muffin', 113,
    467, 6.8, 61.0, 21.7,
    2.3, 34.5, 5.3, 53,
    396, 132, 2.3,
    ARRAY['gluten', 'eggs', 'dairy'], ARRAY['vegetarian'], 'usda', 0.90, true),

('Banana Bread (Slice)', 'dish', 'Homemade banana bread',
    60, 'g', 'slice', 60,
    196, 2.6, 32.8, 6.3,
    0.7, 18.3, 1.3, 26,
    181, 80, 0.7,
    ARRAY['gluten', 'eggs'], ARRAY['vegetarian'], 'usda', 0.90, true),

('Pancake (Plain)', 'dish', 'Buttermilk pancake',
    38, 'g', '4-inch pancake', 38,
    86, 2.4, 11.0, 3.5,
    0.4, 2.2, 0.8, 11,
    167, 43, 0.7,
    ARRAY['gluten', 'eggs', 'dairy'], ARRAY['vegetarian'], 'usda', 0.92, true),

('Waffle (Plain)', 'dish', 'Belgian waffle',
    75, 'g', 'waffle', 75,
    218, 6.0, 25.0, 10.6,
    1.7, 3.9, 2.1, 52,
    383, 119, 1.6,
    ARRAY['gluten', 'eggs', 'dairy'], ARRAY['vegetarian'], 'usda', 0.92, true),

('Donut (Glazed)', 'dish', 'Glazed yeast donut',
    60, 'g', 'donut', 60,
    269, 3.6, 31.3, 14.5,
    0.9, 12.6, 3.5, 4,
    257, 65, 1.0,
    ARRAY['gluten', 'eggs'], ARRAY['vegetarian'], 'usda', 0.90, true),

('Cinnamon Roll', 'dish', 'Frosted cinnamon roll',
    85, 'g', 'roll', 85,
    330, 4.6, 49.5, 12.7,
    1.4, 24.0, 3.0, 13,
    340, 81, 1.7,
    ARRAY['gluten', 'dairy'], ARRAY['vegetarian'], 'usda', 0.89, true),

('Scone (Plain)', 'dish', 'British cream scone',
    65, 'g', 'scone', 65,
    235, 4.5, 32.5, 10.0,
    1.2, 8.5, 6.2, 35,
    321, 82, 1.5,
    ARRAY['gluten', 'dairy', 'eggs'], ARRAY['vegetarian'], 'usda', 0.90, true);

COMMIT;

SELECT
    '✅ CARBS & GRAINS SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(DISTINCT CASE
        WHEN name LIKE '%Bread%' OR name LIKE '%Bun%' OR name LIKE '%Roll%' THEN 'bread'
        WHEN name LIKE '%Pasta%' OR name LIKE '%Noodle%' THEN 'pasta'
        WHEN name LIKE '%Rice%' THEN 'rice'
        WHEN name LIKE '%Potato%' THEN 'potato'
        WHEN name LIKE '%Oat%' OR name LIKE '%Cereal%' THEN 'cereal'
        ELSE 'other'
    END) as categories
FROM foods
WHERE name LIKE '%Bread%' OR name LIKE '%Pasta%' OR name LIKE '%Rice%' OR name LIKE '%Potato%'
   OR name LIKE '%Oat%' OR name LIKE '%Cereal%' OR name LIKE '%Muffin%';
