-- ============================================================================
-- MIGRATION 014: SEED BREAD VARIETIES
-- ============================================================================
-- Description: All types of bread and bread products
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

('Brioche Bread', 'ingredient', 'Rich butter brioche bread',
    100, 'g', 'slice (40g)', 40,
    362, 10, 50, 12.9,
    2.6, 7.7, 7.1, 129,
    439, 129, 52, 3.23,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Ciabatta Bread', 'ingredient', 'Italian ciabatta bread',
    100, 'g', 'slice (50g)', 50,
    271, 9, 52, 2.6,
    2.3, 1.3, 0.5, 0,
    537, 127, 34, 3.4,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Focaccia Bread', 'ingredient', 'Italian focaccia with olive oil',
    100, 'g', 'piece (70g)', 70,
    280, 6.7, 43.3, 8.3,
    2, 1.7, 1.3, 0,
    667, 100, 50, 2.5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Pumpernickel Bread', 'ingredient', 'Dark German pumpernickel',
    100, 'g', 'slice (32g)', 32,
    250, 8.7, 47.5, 3.1,
    6.5, 0.9, 0.4, 0,
    603, 166, 44, 2.37,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('French Bread', 'ingredient', 'Traditional French baguette bread',
    100, 'g', 'slice (25g)', 25,
    275, 9, 53, 3.3,
    2.7, 3.5, 0.6, 0,
    597, 115, 69, 3.4,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Italian Bread', 'ingredient', 'White Italian bread',
    100, 'g', 'slice (30g)', 30,
    271, 9, 50, 3.5,
    2.3, 4, 0.7, 0,
    584, 122, 76, 3.5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Baguette', 'ingredient', 'French baguette',
    100, 'g', 'piece (60g)', 60,
    274, 9.2, 55.8, 1.5,
    2.3, 4.2, 0.3, 0,
    621, 115, 23, 3.6,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Flatbread (Plain)', 'ingredient', 'Mediterranean flatbread',
    100, 'g', 'piece (60g)', 60,
    275, 8, 52, 4,
    2, 2, 0.8, 0,
    520, 110, 40, 2.8,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Lavash Bread', 'ingredient', 'Armenian lavash flatbread',
    100, 'g', 'piece (50g)', 50,
    280, 9, 56, 1,
    2, 2, 0.2, 0,
    560, 115, 35, 3,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Challah Bread', 'ingredient', 'Jewish braided egg bread',
    100, 'g', 'slice (43g)', 43,
    292, 8.7, 50, 5.8,
    1.9, 6.8, 1.4, 47,
    220, 100, 42, 2.9,
    ARRAY['eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Ezekiel Bread', 'ingredient', 'Sprouted grain bread',
    100, 'g', 'slice (34g)', 34,
    246, 14, 42.5, 3.5,
    10.5, 0, 0.5, 0,
    246, 351, 88, 3.5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.93, false),

('Cornbread', 'ingredient', 'Southern style cornbread',
    100, 'g', 'piece (65g)', 65,
    326, 6.7, 47.7, 11.6,
    1.9, 13.3, 3, 59,
    551, 103, 107, 2.13,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Banana Bread', 'ingredient', 'Homemade banana bread',
    100, 'g', 'slice (60g)', 60,
    326, 4.3, 54.6, 10.5,
    1.7, 28.3, 2.1, 26,
    296, 158, 33, 1.38,
    ARRAY['dairy', 'eggs', 'gluten', 'nuts'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Zucchini Bread', 'ingredient', 'Homemade zucchini bread',
    100, 'g', 'slice (60g)', 60,
    310, 4, 51, 10,
    1.5, 28, 2, 25,
    280, 150, 30, 1.3,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Garlic Bread', 'ingredient', 'Garlic butter bread',
    100, 'g', 'slice (40g)', 40,
    350, 7, 40, 18,
    2, 3, 8, 20,
    600, 100, 50, 2.5,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Texas Toast', 'ingredient', 'Thick-sliced white bread toast',
    100, 'g', 'slice (40g)', 40,
    310, 8, 48, 10,
    2, 5, 2.5, 5,
    480, 95, 80, 2.8,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Dinner Roll', 'ingredient', 'Soft white dinner roll',
    100, 'g', 'roll (28g)', 28,
    289, 7.9, 50.5, 5.6,
    2.1, 7.9, 1.3, 13,
    405, 90, 79, 2.68,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Kaiser Roll', 'ingredient', 'Kaiser sandwich roll',
    100, 'g', 'roll (57g)', 57,
    293, 10, 56, 2.1,
    2.5, 5, 0.4, 0,
    528, 119, 105, 3.54,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Hamburger Bun (White)', 'ingredient', 'White hamburger bun',
    100, 'g', 'bun (52g)', 52,
    270, 8.7, 49.6, 3.5,
    2.6, 6.1, 0.9, 0,
    443, 122, 139, 3.04,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Hamburger Bun (Whole Wheat)', 'ingredient', 'Whole wheat hamburger bun',
    100, 'g', 'bun (52g)', 52,
    253, 11, 47.4, 3.2,
    6.3, 5.3, 0.5, 0,
    474, 242, 116, 2.84,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Hot Dog Bun', 'ingredient', 'White hot dog bun',
    100, 'g', 'bun (43g)', 43,
    277, 8.1, 51.6, 4.2,
    2.3, 9.3, 0.9, 0,
    488, 93, 116, 3.02,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Hoagie Roll', 'ingredient', 'Sub/hoagie roll',
    100, 'g', 'roll (85g)', 85,
    272, 9.4, 52.3, 2.6,
    2.4, 5.3, 0.5, 0,
    535, 122, 93, 3.41,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Pretzel Bun', 'ingredient', 'Soft pretzel hamburger bun',
    100, 'g', 'bun (60g)', 60,
    310, 10, 58, 4,
    2.5, 6, 0.8, 0,
    900, 130, 80, 3.5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Sandwich Thin (100 Calorie)', 'ingredient', 'Thin sandwich bun, 100 calories',
    100, 'g', 'bun (43g)', 43,
    233, 11.6, 41.9, 2.3,
    9.3, 4.7, 0, 0,
    465, 186, 116, 2.79,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Sliced White Bread', 'ingredient', 'Standard white sandwich bread',
    100, 'g', 'slice (25g)', 25,
    266, 7.6, 49.4, 3.3,
    2.4, 4.9, 0.6, 0,
    681, 100, 151, 2.85,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.96, true),

('Sliced Whole Wheat Bread', 'ingredient', 'Whole wheat sandwich bread',
    100, 'g', 'slice (28g)', 28,
    252, 12.5, 41.3, 4.2,
    6.8, 5.6, 0.8, 0,
    443, 248, 107, 2.71,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.96, true),

('Rye Bread', 'ingredient', 'Rye sandwich bread',
    100, 'g', 'slice (32g)', 32,
    259, 8.5, 48.3, 3.3,
    5.8, 3.9, 0.6, 0,
    603, 166, 73, 2.83,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Sourdough Bread', 'ingredient', 'Sourdough sandwich bread',
    100, 'g', 'slice (36g)', 36,
    289, 11.3, 56.2, 1.5,
    2.4, 1.7, 0.3, 0,
    622, 128, 69, 3.39,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Multigrain Bread', 'ingredient', 'Multigrain sandwich bread',
    100, 'g', 'slice (26g)', 26,
    265, 13.4, 43.3, 4.2,
    7.4, 6.4, 0.8, 0,
    476, 236, 103, 3.18,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Marble Rye Bread', 'ingredient', 'Marble rye bread',
    100, 'g', 'slice (32g)', 32,
    260, 8.5, 48, 3.5,
    6, 4, 0.6, 0,
    600, 165, 72, 2.8,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.93, false),

('Potato Bread', 'ingredient', 'Soft potato bread',
    100, 'g', 'slice (38g)', 38,
    266, 8, 50, 3.3,
    2.6, 6, 0.8, 3,
    542, 156, 92, 2.92,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Cinnamon Raisin Bread', 'ingredient', 'Cinnamon raisin bread',
    100, 'g', 'slice (26g)', 26,
    284, 8, 56.3, 3.4,
    3.6, 16.9, 0.5, 0,
    280, 206, 59, 2.84,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Gluten-Free Bread', 'ingredient', 'Gluten-free sandwich bread',
    100, 'g', 'slice (36g)', 36,
    250, 2.8, 40, 8.3,
    3.9, 3.9, 1.4, 25,
    333, 111, 56, 1.11,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Keto Bread', 'ingredient', 'Low-carb keto bread',
    100, 'g', 'slice (40g)', 40,
    188, 7.5, 7.5, 13.8,
    5, 2.5, 3.8, 38,
    338, 125, 75, 1.25,
    ARRAY['eggs', 'gluten', 'nuts'], ARRAY['vegetarian', 'keto'], 'user', 0.90, false),

('Cloud Bread', 'ingredient', 'Egg-based cloud bread',
    100, 'g', '3 pieces (60g)', 60,
    84, 10.5, 1.1, 4.2,
    0, 1.1, 1.3, 316,
    253, 79, 42, 0.84,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.89, false);

COMMIT;

SELECT '✅ BREAD VARIETIES SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Brioche Bread', 'Ciabatta Bread', 'French Bread', 'Baguette');
