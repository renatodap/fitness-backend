-- ============================================================================
-- MIGRATION 006: SEED SNACKS & TREATS
-- ============================================================================
-- Description: Comprehensive snacks, treats, and packaged foods
-- Categories: Chips, crackers, cookies, candy, ice cream, bars, jerky, dried fruit
-- Total items: ~80 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (typically 100g)
-- - User inputs in servings (e.g., "1 bag chips") OR grams (e.g., "28g")
-- - Backend converts between servings↔grams using household_serving_grams
-- - Nutrition calculated: multiplier = gram_quantity / serving_size
-- - Each macronutrient: value * multiplier
-- ============================================================================

BEGIN;

-- ============================================================================
-- SNACKS & TREATS
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
-- CHIPS & SALTY SNACKS
-- ============================================================================

('Potato Chips (Regular)', 'ingredient', 'Regular salted potato chips',
    100, 'g', 'oz (28g)', 28,
    536, 6.6, 52.9, 34.6,
    4.4, 0.4, 3.1, 0,
    525, 1196, 23, 1.21,
    NULL, ARRAY['vegetarian'], 'usda', 0.95, true),

('Potato Chips (Baked)', 'ingredient', 'Baked potato chips, lower fat',
    100, 'g', 'oz (28g)', 28,
    464, 6.4, 75, 14.3,
    5.4, 3.6, 1.8, 0,
    714, 1393, 36, 2.14,
    NULL, ARRAY['vegetarian'], 'usda', 0.94, true),

('Tortilla Chips', 'ingredient', 'Corn tortilla chips, salted',
    100, 'g', 'oz (28g)', 28,
    503, 7.1, 60.7, 25,
    5.4, 0.7, 3.2, 0,
    429, 179, 143, 1.43,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Pita Chips', 'ingredient', 'Baked pita chips',
    100, 'g', 'oz (28g)', 28,
    446, 10.7, 64.3, 14.3,
    3.6, 3.6, 1.8, 0,
    607, 143, 36, 2.5,
    NULL, ARRAY['vegetarian'], 'usda', 0.93, true),

('Pretzels (Hard)', 'ingredient', 'Hard salted pretzels',
    100, 'g', 'oz (28g)', 28,
    381, 10, 79.2, 2.6,
    2.9, 2.1, 0.4, 0,
    1486, 137, 22, 3.42,
    NULL, ARRAY['vegetarian'], 'usda', 0.95, true),

('Popcorn (Air-Popped)', 'ingredient', 'Air-popped popcorn, plain',
    100, 'g', 'cup (8g)', 8,
    387, 12.9, 77.8, 4.5,
    14.5, 0.9, 0.6, 0,
    8, 329, 7, 3.19,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.96, true),

('Popcorn (Movie Butter)', 'ingredient', 'Popcorn with butter flavoring',
    100, 'g', 'cup (11g)', 11,
    500, 9.1, 57.1, 28.1,
    10, 0.5, 5, 0,
    972, 274, 11, 2.4,
    NULL, ARRAY['vegetarian'], 'usda', 0.93, true),

('Veggie Straws', 'ingredient', 'Vegetable straw snacks',
    100, 'g', 'oz (28g)', 28,
    500, 0, 66.7, 25,
    3.3, 3.3, 2.5, 0,
    800, 100, 0, 0.5,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false),

('Cheese Puffs', 'ingredient', 'Crunchy cheese puffs',
    100, 'g', 'oz (28g)', 28,
    571, 7.1, 53.6, 35.7,
    0, 3.6, 7.1, 7,
    1071, 143, 71, 0.71,
    ARRAY['dairy'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Doritos (Nacho Cheese)', 'ingredient', 'Nacho cheese flavored tortilla chips',
    100, 'g', 'oz (28g)', 28,
    500, 7.1, 64.3, 21.4,
    3.6, 3.6, 2.9, 0,
    607, 214, 143, 1.43,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

-- ============================================================================
-- CRACKERS
-- ============================================================================

('Saltine Crackers', 'ingredient', 'Plain salted saltine crackers',
    100, 'g', 'cracker (3g)', 3,
    421, 8.4, 73.7, 10.5,
    2.1, 1.1, 1.6, 0,
    1105, 116, 105, 4.21,
    NULL, ARRAY['vegetarian'], 'usda', 0.95, true),

('Wheat Thins', 'ingredient', 'Whole wheat crackers',
    100, 'g', 'crackers (16 pieces, 29g)', 29,
    483, 8.6, 65.5, 20.7,
    6.9, 6.9, 3.4, 0,
    828, 276, 69, 3.1,
    NULL, ARRAY['vegetarian'], 'usda', 0.94, true),

('Ritz Crackers', 'ingredient', 'Buttery round crackers',
    100, 'g', 'crackers (5 pieces, 16g)', 16,
    500, 6.2, 62.5, 25,
    3.1, 6.2, 6.2, 0,
    750, 125, 62, 2.5,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.91, false),

('Triscuit', 'ingredient', 'Whole grain wheat crackers',
    100, 'g', 'crackers (6 pieces, 28g)', 28,
    429, 10.7, 71.4, 10.7,
    10.7, 0, 1.8, 0,
    536, 214, 36, 3.2,
    NULL, ARRAY['vegetarian'], 'usda', 0.94, true),

('Graham Crackers', 'ingredient', 'Honey graham crackers',
    100, 'g', 'sheet (14g)', 14,
    423, 6.2, 76.2, 9.5,
    2.9, 28.6, 1.4, 0,
    476, 143, 48, 2.86,
    NULL, ARRAY['vegetarian'], 'usda', 0.94, true),

('Rice Cakes (Plain)', 'ingredient', 'Plain puffed rice cakes',
    100, 'g', 'cake (9g)', 9,
    387, 8.1, 80.6, 3.2,
    3.2, 0, 0.6, 0,
    323, 129, 16, 1.29,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

-- ============================================================================
-- COOKIES & SWEET BAKED GOODS
-- ============================================================================

('Chocolate Chip Cookies', 'ingredient', 'Standard chocolate chip cookies',
    100, 'g', 'cookie (12g)', 12,
    488, 5.6, 66.7, 22.2,
    2.2, 38.9, 11.1, 17,
    389, 167, 56, 2.22,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Oreo Cookies', 'ingredient', 'Chocolate sandwich cookies with cream',
    100, 'g', 'cookie (11g)', 11,
    480, 4, 68, 20,
    4, 40, 4, 0,
    480, 160, 40, 3.6,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Oatmeal Raisin Cookies', 'ingredient', 'Oatmeal cookies with raisins',
    100, 'g', 'cookie (15g)', 15,
    447, 6.2, 69.2, 16.9,
    3.1, 36.9, 3.8, 23,
    400, 246, 46, 1.85,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Brownie (Unfrosted)', 'ingredient', 'Chocolate brownie, no frosting',
    100, 'g', 'brownie (56g)', 56,
    405, 4.8, 52.4, 19.1,
    2.4, 35.7, 4.8, 48,
    238, 190, 48, 1.9,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Sugar Cookie', 'ingredient', 'Plain sugar cookies',
    100, 'g', 'cookie (14g)', 14,
    471, 5.9, 64.7, 20.6,
    1.2, 29.4, 5.9, 29,
    412, 59, 29, 2.35,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Shortbread Cookies', 'ingredient', 'Buttery shortbread cookies',
    100, 'g', 'cookie (8g)', 8,
    502, 5.8, 63.5, 24.8,
    1.5, 19.4, 15.5, 58,
    388, 77, 39, 2.13,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

-- ============================================================================
-- CANDY & CHOCOLATE
-- ============================================================================

('Milk Chocolate Bar', 'ingredient', 'Milk chocolate candy bar',
    100, 'g', 'bar (43g)', 43,
    535, 7.7, 59.6, 29.8,
    3.5, 52.6, 17.5, 21,
    79, 385, 189, 2.28,
    ARRAY['dairy'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Dark Chocolate (70-85%)', 'ingredient', 'Dark chocolate, high cacao',
    100, 'g', 'square (10g)', 10,
    598, 7.8, 45.8, 42.6,
    10.9, 24, 24.5, 2,
    20, 715, 73, 11.9,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'usda', 0.96, true),

('M&Ms (Plain)', 'ingredient', 'Milk chocolate candies with shell',
    100, 'g', 'pack (47.9g)', 48,
    492, 4.9, 70.5, 21.3,
    2.5, 65.6, 12.3, 8,
    74, 246, 123, 1.64,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.91, false),

('Reeses Peanut Butter Cups', 'ingredient', 'Chocolate peanut butter cups',
    100, 'g', 'cup (21g)', 21,
    515, 10.3, 54.6, 30.9,
    3.1, 49.5, 11.3, 5,
    412, 371, 62, 1.55,
    ARRAY['dairy', 'nuts'], ARRAY['vegetarian'], 'user', 0.92, false),

('Snickers Bar', 'ingredient', 'Chocolate, caramel, peanut candy bar',
    100, 'g', 'bar (52.7g)', 53,
    488, 8.1, 59.3, 24.4,
    2.3, 47.7, 9.3, 5,
    244, 326, 93, 0.93,
    ARRAY['dairy', 'nuts'], ARRAY['vegetarian'], 'user', 0.91, false),

('Skittles', 'ingredient', 'Fruit-flavored chewy candies',
    100, 'g', 'pack (61g)', 61,
    405, 0, 90.7, 4.4,
    0, 74.4, 4.2, 0,
    9, 2, 2, 0.09,
    NULL, ARRAY['vegetarian'], 'user', 0.90, false),

('Gummy Bears', 'ingredient', 'Fruit-flavored gummy candies',
    100, 'g', 'serving (40g)', 40,
    325, 6.9, 76.7, 0,
    0, 46.2, 0, 0,
    23, 5, 3, 0.12,
    NULL, ARRAY['vegetarian'], 'usda', 0.94, true),

('Sour Patch Kids', 'ingredient', 'Sour then sweet gummy candies',
    100, 'g', 'serving (56g)', 56,
    357, 0, 89.3, 0,
    0, 71.4, 0, 0,
    36, 0, 0, 0,
    NULL, ARRAY['vegetarian'], 'user', 0.89, false),

-- ============================================================================
-- ICE CREAM & FROZEN TREATS
-- ============================================================================

('Vanilla Ice Cream (Regular)', 'ingredient', 'Regular vanilla ice cream',
    100, 'g', 'cup (66g)', 66,
    207, 3.5, 23.6, 11,
    0.7, 21.2, 6.8, 44,
    80, 199, 128, 0.09,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Chocolate Ice Cream', 'ingredient', 'Regular chocolate ice cream',
    100, 'g', 'cup (66g)', 66,
    216, 3.8, 28.2, 11,
    1.6, 25.4, 6.5, 34,
    76, 249, 109, 0.93,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Ben & Jerrys (Average)', 'ingredient', 'Premium ice cream, average flavor',
    100, 'g', 'cup (106g)', 106,
    250, 4, 28, 14,
    1, 24, 9, 55,
    75, 200, 120, 0.5,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian'], 'user', 0.90, false),

('Halo Top (Low-Calorie)', 'ingredient', 'Low-calorie high-protein ice cream',
    100, 'g', 'cup (88g)', 88,
    114, 6.8, 18.2, 2.3,
    4.5, 6.8, 1.1, 23,
    159, 159, 114, 0.23,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Frozen Yogurt (Vanilla)', 'ingredient', 'Vanilla frozen yogurt',
    100, 'g', 'cup (72g)', 72,
    159, 4, 24.4, 4.9,
    0.7, 23.5, 2.8, 7,
    71, 188, 134, 0.22,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Popsicle (Fruit)', 'ingredient', 'Fruit-flavored ice pop',
    100, 'g', 'pop (77g)', 77,
    67, 0, 16.9, 0,
    0, 13.3, 0, 0,
    15, 1, 1, 0.01,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Ice Cream Sandwich', 'ingredient', 'Vanilla ice cream between chocolate cookies',
    100, 'g', 'sandwich (71g)', 71,
    237, 3.5, 35.1, 8.8,
    1.8, 21.1, 4.4, 18,
    175, 140, 88, 1.23,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

-- ============================================================================
-- PROTEIN & SNACK BARS
-- ============================================================================

('Clif Bar (Chocolate Chip)', 'ingredient', 'Energy bar with whole grains',
    100, 'g', 'bar (68g)', 68,
    412, 8.8, 67.6, 11.8,
    8.8, 38.2, 2.9, 0,
    294, 353, 88, 5.29,
    ARRAY['gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.92, false),

('Quest Bar (Chocolate Chip)', 'ingredient', 'High-protein low-sugar bar',
    100, 'g', 'bar (60g)', 60,
    333, 33.3, 40, 11.7,
    26.7, 1.7, 5, 0,
    583, 333, 333, 3.33,
    ARRAY['dairy', 'nuts', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('RX Bar (Chocolate Sea Salt)', 'ingredient', 'Whole food protein bar',
    100, 'g', 'bar (52g)', 52,
    385, 19.2, 46.2, 13.5,
    9.6, 25, 1.9, 0,
    385, 385, 58, 1.92,
    ARRAY['eggs', 'nuts'], ARRAY['gluten-free', 'paleo'], 'user', 0.92, false),

('Kind Bar (Dark Chocolate Nuts)', 'ingredient', 'Nut and dark chocolate bar',
    100, 'g', 'bar (40g)', 40,
    500, 12.5, 45, 30,
    7.5, 20, 5, 0,
    250, 375, 75, 2.5,
    ARRAY['nuts'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Nature Valley Granola Bar', 'ingredient', 'Crunchy granola bar',
    100, 'g', 'bar (42g)', 42,
    476, 7.1, 64.3, 19,
    4.8, 28.6, 3.6, 0,
    476, 214, 48, 2.14,
    ARRAY['gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.90, false),

-- ============================================================================
-- JERKY & DRIED MEAT
-- ============================================================================

('Beef Jerky (Original)', 'ingredient', 'Traditional beef jerky',
    100, 'g', 'oz (28g)', 28,
    410, 33.2, 10.5, 25.6,
    1.1, 7.9, 10.5, 80,
    1691, 565, 21, 4.21,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Turkey Jerky', 'ingredient', 'Lean turkey jerky',
    100, 'g', 'oz (28g)', 28,
    328, 50, 10, 7.8,
    0, 7.8, 1.6, 94,
    1875, 469, 31, 3.75,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.93, true),

('Pepperoni Sticks', 'ingredient', 'Cured pepperoni snack sticks',
    100, 'g', 'stick (14g)', 14,
    504, 22.7, 4.1, 44.3,
    0, 0, 15.5, 79,
    1881, 279, 27, 1.2,
    ARRAY['dairy'], ARRAY['gluten-free', 'keto'], 'usda', 0.93, true),

-- ============================================================================
-- DRIED FRUIT
-- ============================================================================

('Raisins (Seedless)', 'ingredient', 'Dried seedless raisins',
    100, 'g', 'small box (43g)', 43,
    299, 3.1, 79.2, 0.5,
    3.7, 59.2, 0.1, 0,
    11, 749, 50, 1.88,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Dried Cranberries (Sweetened)', 'ingredient', 'Sweetened dried cranberries',
    100, 'g', 'serving (40g)', 40,
    325, 0.1, 82.4, 1.4,
    5.3, 72.6, 0.1, 0,
    5, 40, 8, 0.38,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Dried Apricots', 'ingredient', 'Dried apricot halves',
    100, 'g', 'apricot (8g)', 8,
    241, 3.4, 62.6, 0.5,
    7.3, 53.4, 0, 0,
    10, 1162, 55, 2.66,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Dates (Medjool)', 'ingredient', 'Dried Medjool dates, pitted',
    100, 'g', 'date (24g)', 24,
    277, 1.8, 75, 0.2,
    6.7, 66.5, 0, 0,
    1, 696, 64, 0.9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Dried Mango (Sweetened)', 'ingredient', 'Sweetened dried mango slices',
    100, 'g', 'serving (40g)', 40,
    319, 1.8, 78.6, 1.2,
    3.6, 66.3, 0.4, 0,
    18, 284, 18, 0.48,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Banana Chips', 'ingredient', 'Fried banana chips',
    100, 'g', 'oz (28g)', 28,
    519, 2.3, 58.4, 33.6,
    7.7, 35.3, 28.5, 0,
    6, 536, 18, 1.04,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Dried Figs', 'ingredient', 'Dried fig halves',
    100, 'g', 'fig (8g)', 8,
    249, 3.3, 63.9, 0.9,
    9.8, 47.9, 0.1, 0,
    10, 680, 162, 2.03,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

-- ============================================================================
-- MISC PACKAGED SNACKS
-- ============================================================================

('Trail Mix (Nuts & Dried Fruit)', 'ingredient', 'Mixed nuts, seeds, and dried fruit',
    100, 'g', 'oz (28g)', 28,
    462, 13.8, 44.9, 29.4,
    7.1, 27.6, 4.5, 0,
    118, 531, 67, 2.38,
    ARRAY['nuts'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Granola (With Raisins)', 'ingredient', 'Granola with oats and raisins',
    100, 'g', 'cup (61g)', 61,
    471, 10.3, 64.7, 20.1,
    6.5, 21.8, 3.6, 0,
    288, 336, 77, 2.83,
    ARRAY['gluten', 'nuts'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Fruit Snacks (Gummy)', 'ingredient', 'Fruit-flavored gummy snacks',
    100, 'g', 'pouch (26g)', 26,
    333, 0, 83.3, 0,
    0, 50, 0, 0,
    50, 17, 17, 0.17,
    NULL, ARRAY['vegetarian'], 'usda', 0.92, true),

('Goldfish Crackers', 'ingredient', 'Cheddar goldfish crackers',
    100, 'g', 'serving (30g)', 30,
    500, 10, 63.3, 20,
    3.3, 6.7, 3.3, 0,
    833, 167, 167, 2.67,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Pudding Cup (Chocolate)', 'ingredient', 'Ready-to-eat chocolate pudding',
    100, 'g', 'cup (113g)', 113,
    115, 2.7, 20.4, 3.1,
    0.9, 17.7, 1.8, 7,
    150, 159, 106, 0.35,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Rice Krispies Treats', 'ingredient', 'Marshmallow crispy rice bar',
    100, 'g', 'bar (22g)', 22,
    400, 4.5, 81.8, 4.5,
    0.9, 36.4, 2.3, 0,
    409, 64, 18, 4.55,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.90, false);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ SNACKS & TREATS SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Potato Chips (Regular)', 'Tortilla Chips', 'Pretzels (Hard)', 'Popcorn (Air-Popped)',
    'Saltine Crackers', 'Wheat Thins', 'Graham Crackers', 'Rice Cakes (Plain)',
    'Chocolate Chip Cookies', 'Oreo Cookies', 'Brownie (Unfrosted)',
    'Milk Chocolate Bar', 'Dark Chocolate (70-85%)', 'M&Ms (Plain)', 'Snickers Bar',
    'Vanilla Ice Cream (Regular)', 'Chocolate Ice Cream', 'Frozen Yogurt (Vanilla)',
    'Clif Bar (Chocolate Chip)', 'Quest Bar (Chocolate Chip)', 'RX Bar (Chocolate Sea Salt)',
    'Beef Jerky (Original)', 'Turkey Jerky', 'Raisins (Seedless)', 'Dried Cranberries (Sweetened)',
    'Trail Mix (Nuts & Dried Fruit)', 'Granola (With Raisins)'
);
