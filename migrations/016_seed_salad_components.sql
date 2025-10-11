-- ============================================================================
-- MIGRATION 016: SEED SALAD COMPONENTS
-- ============================================================================
-- Description: Salad greens, toppings, croutons, add-ons
-- Total items: ~40 items
-- ============================================================================

BEGIN;

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, cholesterol_mg,
    sodium_mg, potassium_mg, calcium_mg, iron_mg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES

-- ============================================================================
-- SALAD GREENS
-- ============================================================================

('Iceberg Lettuce', 'ingredient', 'Iceberg lettuce, chopped',
    100, 'g', 'cup (72g)', 72,
    14, 0.9, 3, 0.1,
    1.2, 1.97, 0, 0,
    10, 141, 18, 0.41,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Romaine Lettuce', 'ingredient', 'Romaine lettuce, chopped',
    100, 'g', 'cup (47g)', 47,
    17, 1.2, 3.3, 0.3,
    2.1, 1.2, 0, 0,
    8, 247, 33, 0.97,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Mixed Salad Greens', 'ingredient', 'Spring mix/mesclun greens',
    100, 'g', 'cup (55g)', 55,
    21, 1.8, 3.6, 0.4,
    1.8, 1.3, 0.1, 0,
    36, 364, 91, 1.45,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Butter Lettuce', 'ingredient', 'Butter/Boston lettuce',
    100, 'g', 'cup (55g)', 55,
    13, 1.4, 2.2, 0.2,
    1.1, 0.9, 0, 0,
    5, 238, 35, 1.24,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Red Leaf Lettuce', 'ingredient', 'Red leaf lettuce',
    100, 'g', 'cup (28g)', 28,
    16, 1.3, 2.3, 0.3,
    1, 0.5, 0, 0,
    25, 187, 33, 1.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Baby Spinach', 'ingredient', 'Fresh baby spinach leaves',
    100, 'g', 'cup (30g)', 30,
    23, 2.9, 3.6, 0.4,
    2.2, 0.4, 0.1, 0,
    79, 558, 99, 2.71,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Kale (Salad)', 'ingredient', 'Fresh kale, chopped',
    100, 'g', 'cup (67g)', 67,
    35, 2.9, 4.4, 1.5,
    4.1, 0.8, 0.2, 0,
    53, 348, 254, 1.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Arugula', 'ingredient', 'Fresh arugula/rocket leaves',
    100, 'g', 'cup (20g)', 20,
    25, 2.6, 3.7, 0.7,
    1.6, 2, 0.1, 0,
    27, 369, 160, 1.46,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Cabbage (Shredded)', 'ingredient', 'Shredded green cabbage',
    100, 'g', 'cup (89g)', 89,
    25, 1.3, 5.8, 0.1,
    2.5, 3.2, 0, 0,
    18, 170, 40, 0.47,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Coleslaw Mix (Dry)', 'ingredient', 'Shredded cabbage and carrot mix',
    100, 'g', 'cup (89g)', 89,
    31, 1.4, 7.1, 0.2,
    2.7, 4, 0, 0,
    22, 196, 42, 0.52,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

-- ============================================================================
-- SALAD TOPPINGS (VEGETABLES)
-- ============================================================================

('Cherry Tomatoes', 'ingredient', 'Cherry tomatoes, halved',
    100, 'g', 'cup (149g)', 149,
    18, 0.9, 3.9, 0.2,
    1.2, 2.6, 0, 0,
    5, 237, 10, 0.27,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Cucumbers (Sliced)', 'ingredient', 'Sliced cucumber',
    100, 'g', 'cup (104g)', 104,
    15, 0.7, 3.6, 0.1,
    0.5, 1.7, 0, 0,
    2, 147, 16, 0.28,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Red Onion (Sliced)', 'ingredient', 'Sliced red onion',
    100, 'g', 'cup (115g)', 115,
    40, 1.1, 9.3, 0.1,
    1.7, 4.2, 0, 0,
    4, 146, 23, 0.21,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Shredded Carrots', 'ingredient', 'Shredded carrots',
    100, 'g', 'cup (110g)', 110,
    41, 0.9, 9.6, 0.2,
    2.8, 4.7, 0, 0,
    69, 320, 33, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Bell Pepper Strips (Mixed)', 'ingredient', 'Mixed bell pepper strips',
    100, 'g', 'cup (92g)', 92,
    26, 1, 6, 0.3,
    2.1, 4.2, 0, 0,
    4, 211, 7, 0.43,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Radishes (Sliced)', 'ingredient', 'Sliced radishes',
    100, 'g', 'cup (116g)', 116,
    16, 0.7, 3.4, 0.1,
    1.6, 1.9, 0, 0,
    39, 233, 25, 0.34,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

-- ============================================================================
-- SALAD TOPPINGS (PROTEIN)
-- ============================================================================

('Bacon Bits (Real)', 'ingredient', 'Real bacon crumbles',
    100, 'g', 'tbsp (7g)', 7,
    541, 37.9, 1.7, 42,
    0, 0, 13.7, 107,
    2310, 565, 17, 1.44,
    NULL, ARRAY['gluten-free', 'keto'], 'usda', 0.94, true),

('Bacon Bits (Imitation)', 'ingredient', 'Imitation bacon bits',
    100, 'g', 'tbsp (7g)', 7,
    476, 28.6, 33.3, 23.8,
    4.8, 9.5, 4.8, 0,
    2571, 476, 95, 3.81,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian'], 'usda', 0.92, true),

('Hard Boiled Egg (Chopped)', 'ingredient', 'Chopped hard boiled egg',
    100, 'g', 'egg (50g)', 50,
    155, 12.6, 1.1, 10.6,
    0, 1.1, 3.3, 373,
    124, 126, 50, 1.19,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Grilled Chicken (Salad)', 'ingredient', 'Grilled chicken breast strips',
    100, 'g', 'oz (28g)', 28,
    165, 31, 0, 3.6,
    0, 0, 1, 85,
    74, 256, 15, 1.04,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Tuna (Salad Topping)', 'ingredient', 'Canned tuna, drained',
    100, 'g', 'oz (28g)', 28,
    128, 27.9, 0, 1.3,
    0, 0, 0.3, 42,
    247, 237, 14, 0.82,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Turkey Breast (Salad)', 'ingredient', 'Diced turkey breast',
    100, 'g', 'oz (28g)', 28,
    135, 30, 0, 1.7,
    0, 0, 0.5, 73,
    1104, 302, 13, 1.43,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Ham (Salad Topping)', 'ingredient', 'Diced deli ham',
    100, 'g', 'oz (28g)', 28,
    145, 20.9, 1.5, 5.5,
    0, 1.5, 1.8, 53,
    1203, 287, 7, 0.91,
    NULL, ARRAY['gluten-free'], 'usda', 0.94, true),

-- ============================================================================
-- CRUNCHY TOPPINGS
-- ============================================================================

('Croutons (Plain)', 'ingredient', 'Plain seasoned croutons',
    100, 'g', 'cup (30g)', 30,
    407, 11.3, 74.2, 6.5,
    4.8, 4.8, 1.6, 0,
    698, 129, 113, 3.55,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Croutons (Garlic)', 'ingredient', 'Garlic butter croutons',
    100, 'g', 'cup (30g)', 30,
    420, 10.7, 72, 8.9,
    4.3, 5, 2.1, 0,
    750, 125, 107, 3.4,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Tortilla Strips (Salad)', 'ingredient', 'Crispy tortilla strips',
    100, 'g', 'oz (28g)', 28,
    503, 7.1, 60.7, 25,
    5.4, 0.7, 3.2, 0,
    429, 179, 143, 1.43,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Wonton Strips (Salad)', 'ingredient', 'Fried wonton strips',
    100, 'g', 'oz (28g)', 28,
    460, 8, 62, 20,
    2, 2, 4, 10,
    580, 100, 40, 2.5,
    ARRAY['eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Sunflower Seeds (Salad)', 'ingredient', 'Roasted sunflower seeds',
    100, 'g', 'oz (28g)', 28,
    582, 19.3, 24.1, 49.8,
    11.1, 3.4, 4.5, 0,
    392, 645, 70, 3.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Sliced Almonds (Salad)', 'ingredient', 'Sliced almonds for salad',
    100, 'g', 'oz (28g)', 28,
    579, 21.2, 21.6, 49.9,
    12.5, 4.4, 3.8, 0,
    1, 733, 269, 3.71,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Pecans (Candied)', 'ingredient', 'Candied pecans for salad',
    100, 'g', 'oz (28g)', 28,
    710, 7.1, 60.7, 50,
    7.1, 46.4, 4.3, 0,
    143, 357, 57, 2.14,
    ARRAY['nuts'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Walnuts (Salad)', 'ingredient', 'Walnut pieces for salad',
    100, 'g', 'oz (28g)', 28,
    654, 15.2, 13.7, 65.2,
    6.7, 2.6, 6.1, 0,
    2, 441, 98, 2.91,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Chia Seeds (Salad)', 'ingredient', 'Chia seeds for salad',
    100, 'g', 'tbsp (12g)', 12,
    486, 16.5, 42.1, 30.7,
    34.4, 0, 3.3, 0,
    16, 407, 631, 7.72,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

-- ============================================================================
-- CHEESE & OTHER TOPPINGS
-- ============================================================================

('Shredded Cheddar (Salad)', 'ingredient', 'Shredded cheddar cheese',
    100, 'g', 'oz (28g)', 28,
    403, 24.9, 1.3, 33.1,
    0, 0.5, 21, 105,
    621, 98, 721, 0.68,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Crumbled Feta (Salad)', 'ingredient', 'Crumbled feta cheese',
    100, 'g', 'oz (28g)', 28,
    264, 14.2, 4.1, 21.3,
    0, 4.1, 14.9, 89,
    1116, 62, 493, 0.65,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Parmesan Shavings (Salad)', 'ingredient', 'Shaved parmesan cheese',
    100, 'g', 'oz (28g)', 28,
    431, 38.5, 4.1, 28.6,
    0, 0.9, 19.1, 88,
    1529, 125, 1184, 0.82,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Blue Cheese Crumbles (Salad)', 'ingredient', 'Blue cheese crumbles',
    100, 'g', 'oz (28g)', 28,
    353, 21.4, 2.3, 28.7,
    0, 0.5, 18.7, 75,
    1395, 256, 528, 0.31,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Avocado (Sliced)', 'ingredient', 'Sliced avocado for salad',
    100, 'g', 'avocado (136g)', 136,
    160, 2, 8.5, 14.7,
    6.7, 0.7, 2.1, 0,
    7, 485, 12, 0.55,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Dried Cranberries (Salad)', 'ingredient', 'Sweetened dried cranberries',
    100, 'g', 'oz (28g)', 28,
    325, 0.1, 82.4, 1.4,
    5.3, 72.6, 0.1, 0,
    5, 40, 8, 0.38,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Raisins (Salad)', 'ingredient', 'Raisins for salad',
    100, 'g', 'oz (28g)', 28,
    299, 3.1, 79.2, 0.5,
    3.7, 59.2, 0.1, 0,
    11, 749, 50, 1.88,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true);

COMMIT;

SELECT '✅ SALAD COMPONENTS SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Romaine Lettuce', 'Croutons (Plain)', 'Bacon Bits (Real)', 'Ranch Dressing');
