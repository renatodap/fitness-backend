-- ============================================================================
-- MIGRATION 020: SEED BRANDED PANTRY ITEMS
-- ============================================================================
-- Description: Popular branded pantry staples - sauces, soups, spreads, canned goods
-- Total items: ~60 items
-- Brands: Campbells, Prego, Heinz, Jif, Skippy, Hunts, Del Monte, etc.
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

-- PASTA SAUCES
('Prego Traditional Italian Sauce', 'ingredient', 'Prego traditional spaghetti sauce',
    100, 'g', 'cup (130g)', 130,
    54, 1.5, 10.8, 1.5,
    2.3, 6.9, 0, 0,
    385, 277, 23, 0.77,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Prego Meat Flavored Sauce', 'ingredient', 'Prego meat flavored pasta sauce',
    100, 'g', 'cup (130g)', 130,
    62, 2.3, 11.5, 1.5,
    2.3, 7.7, 0, 3,
    438, 285, 23, 0.85,
    NULL, ARRAY['gluten-free'], 'user', 0.93, false),

('Ragu Old World Style Traditional Sauce', 'ingredient', 'Ragu traditional pasta sauce',
    100, 'g', 'cup (125g)', 125,
    56, 1.6, 10.4, 1.6,
    2.4, 7.2, 0, 0,
    344, 280, 24, 0.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Classico Tomato and Basil Sauce', 'ingredient', 'Classico tomato basil pasta sauce',
    100, 'g', 'cup (125g)', 125,
    48, 1.6, 8, 1.6,
    2.4, 4.8, 0, 0,
    320, 280, 24, 0.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Newman's Own Marinara Sauce', 'ingredient', 'Newmans Own marinara pasta sauce',
    100, 'g', 'cup (124g)', 124,
    48, 1.6, 8.1, 1.6,
    2.4, 4.8, 0, 0,
    323, 274, 24, 0.81,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Rao's Homemade Marinara Sauce', 'ingredient', 'Raos homemade marinara sauce',
    100, 'g', 'cup (125g)', 125,
    56, 1.6, 5.6, 3.2,
    1.6, 4, 0.4, 0,
    296, 248, 24, 0.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- ALFREDO & CREAM SAUCES
('Prego Alfredo Sauce', 'ingredient', 'Prego classic alfredo sauce',
    100, 'g', 'cup (62g)', 62,
    306, 4.8, 9.7, 27.4,
    0, 3.2, 16.1, 65,
    758, 97, 129, 0.32,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Bertolli Alfredo Sauce', 'ingredient', 'Bertolli alfredo with aged parmesan',
    100, 'g', 'cup (61g)', 61,
    328, 4.9, 8.2, 29.5,
    0, 3.3, 18, 66,
    820, 98, 131, 0.33,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

-- CANNED SOUPS (Campbells, Progresso)
('Campbells Tomato Soup (Condensed)', 'ingredient', 'Campbells condensed tomato soup',
    100, 'g', 'cup prepared (253g)', 253,
    71, 1.6, 15.9, 0,
    1.6, 11.9, 0, 0,
    476, 238, 24, 1.19,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.95, false),

('Campbells Chicken Noodle Soup (Condensed)', 'ingredient', 'Campbells condensed chicken noodle soup',
    100, 'g', 'cup prepared (248g)', 248,
    50, 3.2, 6.5, 1.2,
    0.8, 0.8, 0.4, 10,
    373, 81, 16, 0.65,
    ARRAY['gluten'], NULL, 'user', 0.95, false),

('Campbells Cream of Mushroom Soup (Condensed)', 'ingredient', 'Campbells condensed cream of mushroom',
    100, 'g', 'cup prepared (248g)', 248,
    81, 1.6, 8.1, 4.8,
    0, 0.8, 2, 2,
    409, 81, 40, 0.4,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.94, false),

('Campbells Chunky Beef with Country Vegetables Soup', 'ingredient', 'Campbells Chunky beef vegetable soup',
    100, 'g', 'cup (245g)', 245,
    45, 2.9, 7.3, 0.8,
    1.2, 1.6, 0.4, 6,
    327, 147, 16, 0.73,
    NULL, NULL, 'user', 0.93, false),

('Progresso Traditional Chicken Noodle Soup', 'ingredient', 'Progresso chicken noodle soup',
    100, 'g', 'cup (245g)', 245,
    41, 3.3, 6.1, 0.8,
    0.8, 0.8, 0.4, 8,
    306, 98, 16, 0.65,
    ARRAY['gluten'], NULL, 'user', 0.94, false),

('Progresso Rich and Hearty Chicken and Homestyle Noodles', 'ingredient', 'Progresso rich and hearty chicken noodle',
    100, 'g', 'cup (245g)', 245,
    45, 3.3, 7.3, 0.8,
    0.8, 0.8, 0.4, 10,
    314, 98, 16, 0.73,
    ARRAY['gluten'], NULL, 'user', 0.94, false),

('Progresso Vegetable Classics Minestrone', 'ingredient', 'Progresso minestrone soup',
    100, 'g', 'cup (245g)', 245,
    41, 1.6, 8.2, 0.8,
    2, 2, 0, 0,
    306, 147, 24, 0.82,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.94, false),

-- PEANUT BUTTER
('Jif Creamy Peanut Butter', 'ingredient', 'Jif creamy peanut butter',
    100, 'g', 'tbsp (16g)', 16,
    588, 23.5, 23.5, 50,
    5.9, 11.8, 8.8, 0,
    471, 647, 59, 1.18,
    ARRAY['peanuts', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Jif Extra Crunchy Peanut Butter', 'ingredient', 'Jif extra crunchy peanut butter',
    100, 'g', 'tbsp (16g)', 16,
    588, 23.5, 23.5, 50,
    5.9, 11.8, 8.8, 0,
    471, 647, 59, 1.18,
    ARRAY['peanuts', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Skippy Creamy Peanut Butter', 'ingredient', 'Skippy creamy peanut butter',
    100, 'g', 'tbsp (16g)', 16,
    588, 23.5, 23.5, 50,
    5.9, 11.8, 8.8, 0,
    471, 647, 59, 1.18,
    ARRAY['peanuts', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Skippy Super Chunk Peanut Butter', 'ingredient', 'Skippy super chunk peanut butter',
    100, 'g', 'tbsp (16g)', 16,
    588, 23.5, 23.5, 50,
    5.9, 11.8, 8.8, 0,
    471, 647, 59, 1.18,
    ARRAY['peanuts', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Smuckers Natural Peanut Butter', 'ingredient', 'Smuckers natural creamy peanut butter',
    100, 'g', 'tbsp (16g)', 16,
    600, 26.7, 20, 53.3,
    6.7, 3.3, 8.3, 0,
    500, 667, 67, 1.33,
    ARRAY['peanuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- JELLY & JAM
('Smuckers Strawberry Jam', 'ingredient', 'Smuckers strawberry jam',
    100, 'g', 'tbsp (20g)', 20,
    250, 0, 65, 0,
    0, 60, 0, 0,
    25, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Smuckers Grape Jelly', 'ingredient', 'Smuckers grape jelly',
    100, 'g', 'tbsp (20g)', 20,
    250, 0, 65, 0,
    0, 60, 0, 0,
    30, 15, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Welchs Grape Jelly', 'ingredient', 'Welchs Concord grape jelly',
    100, 'g', 'tbsp (20g)', 20,
    250, 0, 65, 0,
    0, 60, 0, 0,
    25, 20, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

-- CONDIMENTS (Heinz, Hunts, French's)
('Heinz Tomato Ketchup', 'ingredient', 'Heinz tomato ketchup',
    100, 'g', 'tbsp (17g)', 17,
    107, 0, 28.6, 0,
    0, 23.8, 0, 0,
    952, 238, 10, 0.24,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Hunts Ketchup', 'ingredient', 'Hunts tomato ketchup',
    100, 'g', 'tbsp (17g)', 17,
    100, 0, 26.7, 0,
    0, 23.3, 0, 0,
    633, 200, 7, 0.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('French's Yellow Mustard', 'ingredient', 'Frenchs classic yellow mustard',
    100, 'g', 'tsp (5g)', 5,
    67, 3.3, 6.7, 3.3,
    3.3, 0, 0, 0,
    1333, 133, 67, 1.33,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Gulden's Spicy Brown Mustard', 'ingredient', 'Guldens spicy brown mustard',
    100, 'g', 'tsp (5g)', 5,
    100, 6.7, 6.7, 6.7,
    3.3, 0, 0, 0,
    1333, 167, 67, 1.67,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Heinz Yellow Mustard', 'ingredient', 'Heinz yellow mustard',
    100, 'g', 'tsp (5g)', 5,
    67, 3.3, 6.7, 3.3,
    3.3, 0, 0, 0,
    1333, 133, 67, 1.33,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Heinz 57 Sauce', 'ingredient', 'Heinz 57 steak sauce',
    100, 'g', 'tbsp (17g)', 17,
    133, 0, 33.3, 0,
    0, 26.7, 0, 0,
    933, 133, 13, 0.4,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.93, false),

('A1 Original Steak Sauce', 'ingredient', 'A1 original steak sauce',
    100, 'g', 'tbsp (17g)', 17,
    100, 0, 23.3, 0,
    0, 16.7, 0, 0,
    1833, 167, 17, 0.33,
    ARRAY['gluten'], ARRAY['vegetarian'], 'user', 0.94, false),

-- WORCESTERSHIRE & SOY SAUCE
('Lea and Perrins Worcestershire Sauce', 'ingredient', 'Lea & Perrins Worcestershire sauce',
    100, 'g', 'tsp (5g)', 5,
    67, 0, 16.7, 0,
    0, 6.7, 0, 0,
    5333, 267, 33, 1.67,
    ARRAY['gluten', 'fish'], NULL, 'user', 0.94, false),

('Kikkoman Soy Sauce', 'ingredient', 'Kikkoman naturally brewed soy sauce',
    100, 'g', 'tbsp (16g)', 16,
    53, 5.3, 7.9, 0,
    0, 1.3, 0, 0,
    5658, 158, 13, 1.32,
    ARRAY['soy', 'gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.95, false),

('Kikkoman Less Sodium Soy Sauce', 'ingredient', 'Kikkoman less sodium soy sauce',
    100, 'g', 'tbsp (16g)', 16,
    47, 4.7, 6.3, 0,
    0, 1.6, 0, 0,
    3553, 158, 13, 1.26,
    ARRAY['soy', 'gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.95, false),

-- MAYONNAISE
('Hellmann's Real Mayonnaise', 'ingredient', 'Hellmanns real mayonnaise',
    100, 'g', 'tbsp (14g)', 14,
    714, 0, 0, 78.6,
    0, 0, 11.9, 36,
    571, 36, 14, 0.07,
    ARRAY['eggs', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Hellmann's Light Mayonnaise', 'ingredient', 'Hellmanns light mayonnaise',
    100, 'g', 'tbsp (15g)', 15,
    333, 0, 13.3, 30,
    0, 6.7, 5, 20,
    1000, 67, 13, 0.07,
    ARRAY['eggs', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Dukes Real Mayonnaise', 'ingredient', 'Dukes real mayonnaise',
    100, 'g', 'tbsp (14g)', 14,
    714, 0, 0, 78.6,
    0, 0, 11.9, 50,
    429, 36, 14, 0.07,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Kraft Real Mayo', 'ingredient', 'Kraft real mayonnaise',
    100, 'g', 'tbsp (13g)', 13,
    769, 0, 0, 84.6,
    0, 0, 12.3, 38,
    615, 38, 15, 0.08,
    ARRAY['eggs', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

-- MIRACLE WHIP
('Miracle Whip Original', 'ingredient', 'Miracle Whip dressing',
    100, 'g', 'tbsp (15g)', 15,
    333, 0, 20, 26.7,
    0, 13.3, 4, 13,
    1000, 40, 13, 0.13,
    ARRAY['eggs', 'soy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

-- RELISH & PICKLES
('Heinz Sweet Pickle Relish', 'ingredient', 'Heinz sweet pickle relish',
    100, 'g', 'tbsp (15g)', 15,
    107, 0, 26.7, 0,
    0.7, 20, 0, 0,
    667, 67, 13, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Vlasic Dill Pickles', 'ingredient', 'Vlasic kosher dill pickles',
    100, 'g', 'pickle (28g)', 28,
    11, 0.4, 2.1, 0.1,
    0.7, 0.7, 0, 0,
    746, 93, 18, 0.36,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Claussen Dill Pickle Spears', 'ingredient', 'Claussen kosher dill pickle spears',
    100, 'g', 'spear (28g)', 28,
    7, 0.4, 1.4, 0.1,
    0.7, 0.7, 0, 0,
    746, 93, 18, 0.36,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- SALAD DRESSINGS
('Hidden Valley Ranch Dressing', 'ingredient', 'Hidden Valley original ranch dressing',
    100, 'g', 'tbsp (15g)', 15,
    467, 0, 6.7, 46.7,
    0, 3.3, 7.3, 13,
    1067, 67, 33, 0.13,
    ARRAY['eggs', 'dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Kraft Italian Dressing', 'ingredient', 'Kraft zesty Italian dressing',
    100, 'g', 'tbsp (16g)', 16,
    313, 0, 6.3, 31.3,
    0, 6.3, 5, 0,
    1563, 63, 13, 0.13,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Wishbone Italian Dressing', 'ingredient', 'Wishbone Italian dressing',
    100, 'g', 'tbsp (15g)', 15,
    400, 0, 6.7, 40,
    0, 6.7, 5.3, 0,
    1467, 67, 13, 0.13,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Ken's Steak House Chunky Blue Cheese', 'ingredient', 'Kens chunky blue cheese dressing',
    100, 'g', 'tbsp (16g)', 16,
    500, 3.1, 6.3, 50,
    0, 3.1, 9.4, 31,
    1250, 94, 125, 0.13,
    ARRAY['eggs', 'dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

-- CANNED TOMATOES
('Hunts Diced Tomatoes', 'ingredient', 'Hunts diced tomatoes',
    100, 'g', 'cup (121g)', 121,
    21, 0.8, 4.1, 0,
    0.8, 2.5, 0, 0,
    124, 124, 17, 0.41,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Hunts Tomato Sauce', 'ingredient', 'Hunts tomato sauce',
    100, 'g', 'cup (122g)', 122,
    20, 0.8, 4.1, 0,
    0.8, 2.5, 0, 0,
    131, 148, 16, 0.49,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Hunts Crushed Tomatoes', 'ingredient', 'Hunts crushed tomatoes',
    100, 'g', 'cup (121g)', 121,
    21, 0.8, 4.1, 0,
    0.8, 2.5, 0, 0,
    83, 132, 17, 0.41,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Muir Glen Organic Diced Tomatoes', 'ingredient', 'Muir Glen organic diced tomatoes',
    100, 'g', 'cup (121g)', 121,
    21, 0.8, 4.1, 0,
    0.8, 2.5, 0, 0,
    107, 124, 17, 0.41,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- CANNED BEANS
('Bush's Best Original Baked Beans', 'ingredient', 'Bushs original baked beans',
    100, 'g', 'cup (130g)', 130,
    115, 4.6, 21.5, 0.8,
    5.4, 10.8, 0, 0,
    354, 277, 46, 1.23,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Bush's Best Black Beans', 'ingredient', 'Bushs black beans',
    100, 'g', 'cup (130g)', 130,
    92, 6.2, 16.2, 0.8,
    6.2, 0, 0, 0,
    277, 277, 31, 1.54,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Bush's Best Pinto Beans', 'ingredient', 'Bushs pinto beans',
    100, 'g', 'cup (130g)', 130,
    92, 5.4, 16.9, 0.8,
    6.2, 0, 0, 0,
    277, 277, 31, 1.54,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- CANNED VEGETABLES
('Del Monte Cut Green Beans', 'ingredient', 'Del Monte cut green beans',
    100, 'g', 'cup (121g)', 121,
    17, 0.8, 3.3, 0,
    1.7, 1.7, 0, 0,
    248, 83, 25, 0.41,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Del Monte Sweet Corn', 'ingredient', 'Del Monte golden sweet corn',
    100, 'g', 'cup (125g)', 125,
    56, 1.6, 12, 0.8,
    1.6, 4.8, 0, 0,
    280, 120, 8, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Del Monte Sliced Carrots', 'ingredient', 'Del Monte sliced carrots',
    100, 'g', 'cup (122g)', 122,
    25, 0.8, 5.7, 0,
    1.6, 4.1, 0, 0,
    246, 123, 25, 0.41,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- CANNED TUNA
('StarKist Chunk Light Tuna in Water', 'ingredient', 'StarKist chunk light tuna',
    100, 'g', 'can (142g)', 142,
    92, 20.4, 0, 0.9,
    0, 0, 0.2, 42,
    247, 211, 14, 1.41,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'user', 0.95, false),

('StarKist Chunk Light Tuna in Oil', 'ingredient', 'StarKist chunk light tuna in oil',
    100, 'g', 'can (142g)', 142,
    140, 19.7, 0, 6.3,
    0, 0, 1.4, 42,
    247, 197, 14, 1.27,
    ARRAY['fish', 'soy'], ARRAY['gluten-free', 'paleo', 'keto'], 'user', 0.94, false),

('Bumble Bee Solid White Albacore Tuna in Water', 'ingredient', 'Bumble Bee white albacore tuna',
    100, 'g', 'can (142g)', 142,
    99, 21.1, 0, 1.4,
    0, 0, 0.4, 42,
    254, 218, 14, 1.48,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'user', 0.95, false);

COMMIT;

SELECT '✅ BRANDED PANTRY ITEMS SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Prego Traditional Italian Sauce', 'Heinz Tomato Ketchup', 'Jif Creamy Peanut Butter', 'Campbells Tomato Soup (Condensed)');
