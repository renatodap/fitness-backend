-- ============================================================================
-- MIGRATION 007: SEED CONDIMENTS & SAUCES
-- ============================================================================
-- Description: Comprehensive condiments, sauces, dressings, and flavor enhancers
-- Categories: Sauces, dressings, spreads, Asian sauces, dips, seasonings
-- Total items: ~60 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (typically 100g)
-- - User inputs in servings (e.g., "1 tbsp ketchup") OR grams (e.g., "17g")
-- - Backend converts between servings↔grams using household_serving_grams
-- - Nutrition calculated: multiplier = gram_quantity / serving_size
-- - Each macronutrient: value * multiplier
-- ============================================================================

BEGIN;

-- ============================================================================
-- CONDIMENTS & SAUCES
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
-- SAUCES & CONDIMENTS (BASIC)
-- ============================================================================

('Ketchup', 'ingredient', 'Tomato ketchup',
    100, 'g', 'tbsp (17g)', 17,
    101, 1.2, 25.8, 0.1,
    0.3, 21.3, 0, 0,
    907, 365, 15, 0.36,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.96, true),

('Mustard (Yellow)', 'ingredient', 'Yellow mustard',
    100, 'g', 'tsp (5g)', 5,
    66, 4, 5.3, 4,
    3.3, 2, 0.3, 0,
    1135, 138, 63, 1.17,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Dijon Mustard', 'ingredient', 'Dijon-style mustard',
    100, 'g', 'tsp (5g)', 5,
    67, 3.3, 6.7, 3.3,
    3.3, 0, 0, 0,
    1333, 133, 67, 1.33,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Mayonnaise (Full-Fat)', 'ingredient', 'Real mayonnaise',
    100, 'g', 'tbsp (14g)', 14,
    680, 0.9, 0.6, 75,
    0, 0.3, 10.2, 42,
    600, 21, 7, 0.14,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Mayonnaise (Light)', 'ingredient', 'Light mayonnaise',
    100, 'g', 'tbsp (15g)', 15,
    267, 0.7, 20, 20,
    0, 6.7, 3.3, 13,
    800, 27, 7, 0.13,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('BBQ Sauce', 'ingredient', 'Barbecue sauce, standard',
    100, 'g', 'tbsp (17g)', 17,
    172, 0.6, 40.8, 0.5,
    0.6, 33.9, 0.1, 0,
    815, 175, 23, 0.52,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Hot Sauce (Tabasco)', 'ingredient', 'Tabasco-style hot sauce',
    100, 'g', 'tsp (5g)', 5,
    12, 1.3, 0.8, 0.6,
    0.5, 0.4, 0.1, 0,
    2643, 80, 8, 0.32,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Sriracha', 'ingredient', 'Thai-style hot chili sauce',
    100, 'g', 'tsp (5g)', 5,
    93, 2, 20, 0.5,
    1.3, 13.3, 0.1, 0,
    2200, 200, 13, 0.67,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Worcestershire Sauce', 'ingredient', 'Worcestershire sauce',
    100, 'g', 'tsp (5g)', 5,
    78, 0, 19.5, 0,
    0, 13, 0, 0,
    1431, 136, 33, 1.43,
    ARRAY['fish'], ARRAY['gluten-free'], 'usda', 0.94, true),

('Vinegar (Balsamic)', 'ingredient', 'Balsamic vinegar',
    100, 'g', 'tbsp (16g)', 16,
    88, 0.5, 17.0, 0,
    0, 14.9, 0, 0,
    23, 112, 27, 0.72,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Vinegar (Apple Cider)', 'ingredient', 'Apple cider vinegar',
    100, 'g', 'tbsp (15g)', 15,
    21, 0, 0.9, 0,
    0, 0.4, 0, 0,
    5, 73, 7, 0.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

-- ============================================================================
-- SALAD DRESSINGS
-- ============================================================================

('Ranch Dressing', 'ingredient', 'Creamy ranch dressing',
    100, 'g', 'tbsp (15g)', 15,
    480, 0.7, 6.7, 50,
    0, 4, 7.3, 20,
    867, 67, 20, 0.13,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Caesar Dressing', 'ingredient', 'Creamy Caesar dressing',
    100, 'g', 'tbsp (15g)', 15,
    533, 1.3, 5.3, 56,
    0, 2.7, 9.3, 13,
    1067, 53, 33, 0.27,
    ARRAY['dairy', 'eggs', 'fish'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Italian Dressing', 'ingredient', 'Italian vinaigrette dressing',
    100, 'g', 'tbsp (15g)', 15,
    267, 0, 10, 26.7,
    0, 6.7, 4, 0,
    933, 40, 7, 0.13,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Blue Cheese Dressing', 'ingredient', 'Creamy blue cheese dressing',
    100, 'g', 'tbsp (15g)', 15,
    480, 4.7, 7.3, 50,
    0, 4.7, 9.3, 27,
    1093, 93, 87, 0.27,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Balsamic Vinaigrette', 'ingredient', 'Balsamic vinegar dressing',
    100, 'g', 'tbsp (15g)', 15,
    267, 0, 13.3, 26.7,
    0, 10.7, 4, 0,
    733, 93, 7, 0.27,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Honey Mustard Dressing', 'ingredient', 'Sweet honey mustard dressing',
    100, 'g', 'tbsp (15g)', 15,
    333, 0.7, 26.7, 26.7,
    0.7, 20, 4, 7,
    733, 53, 13, 0.27,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Thousand Island Dressing', 'ingredient', 'Thousand island dressing',
    100, 'g', 'tbsp (16g)', 16,
    400, 0.6, 15.6, 38.8,
    0.6, 12.5, 6.2, 25,
    675, 75, 19, 0.31,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- ASIAN SAUCES
-- ============================================================================

('Soy Sauce', 'ingredient', 'Traditional soy sauce',
    100, 'g', 'tbsp (16g)', 16,
    60, 10.5, 5.6, 0.1,
    0.8, 0.4, 0, 0,
    5586, 217, 20, 2.38,
    ARRAY['soy', 'gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.96, true),

('Soy Sauce (Low-Sodium)', 'ingredient', 'Reduced sodium soy sauce',
    100, 'g', 'tbsp (16g)', 16,
    48, 8.1, 4.8, 0,
    0.8, 0, 0, 0,
    2791, 217, 16, 1.89,
    ARRAY['soy', 'gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.95, true),

('Tamari (Gluten-Free)', 'ingredient', 'Gluten-free soy sauce',
    100, 'g', 'tbsp (16g)', 16,
    60, 10.5, 5.6, 0.1,
    0.8, 0.4, 0, 0,
    5586, 217, 20, 2.38,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Teriyaki Sauce', 'ingredient', 'Sweet teriyaki sauce',
    100, 'g', 'tbsp (18g)', 18,
    89, 5.6, 15.6, 0,
    0, 11.1, 0, 0,
    1944, 111, 11, 0.67,
    ARRAY['soy'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Hoisin Sauce', 'ingredient', 'Chinese hoisin sauce',
    100, 'g', 'tbsp (16g)', 16,
    220, 2.2, 47.3, 4.4,
    2.2, 33, 0.7, 0,
    1615, 242, 33, 1.1,
    ARRAY['soy'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Oyster Sauce', 'ingredient', 'Oyster-flavored sauce',
    100, 'g', 'tbsp (18g)', 18,
    51, 1.4, 11.1, 0,
    0, 8.3, 0, 0,
    2222, 111, 17, 0.56,
    ARRAY['fish'], ARRAY['gluten-free'], 'usda', 0.92, true),

('Sweet Chili Sauce', 'ingredient', 'Thai sweet chili sauce',
    100, 'g', 'tbsp (18g)', 18,
    200, 0, 48.9, 0.6,
    0.6, 40, 0.1, 0,
    1111, 56, 11, 0.33,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Fish Sauce', 'ingredient', 'Thai/Vietnamese fish sauce',
    100, 'g', 'tbsp (18g)', 18,
    35, 5.1, 3.9, 0,
    0, 0, 0, 0,
    5930, 89, 32, 1.11,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo'], 'usda', 0.94, true),

('Sesame Oil (Toasted)', 'ingredient', 'Toasted sesame oil for flavor',
    100, 'g', 'tsp (5g)', 5,
    884, 0, 0, 100,
    0, 0, 14.2, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

-- ============================================================================
-- MEXICAN SAUCES
-- ============================================================================

('Salsa (Red, Medium)', 'ingredient', 'Medium red salsa',
    100, 'g', 'tbsp (16g)', 16,
    28, 1.2, 6.2, 0.2,
    1.5, 3.7, 0, 0,
    430, 227, 18, 0.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Salsa Verde', 'ingredient', 'Green tomatillo salsa',
    100, 'g', 'tbsp (16g)', 16,
    20, 0.6, 4.4, 0.2,
    1.2, 2.5, 0, 0,
    400, 150, 12, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Guacamole', 'ingredient', 'Prepared guacamole dip',
    100, 'g', 'tbsp (15g)', 15,
    150, 1.9, 8.6, 13.5,
    6.7, 0.5, 2.1, 0,
    267, 415, 11, 0.48,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Pico de Gallo', 'ingredient', 'Fresh tomato salsa',
    100, 'g', 'serving (30g)', 30,
    25, 1, 5.3, 0.2,
    1.3, 3.3, 0, 0,
    333, 233, 13, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.93, true),

('Queso Dip', 'ingredient', 'Cheese dip for chips',
    100, 'g', 'serving (30g)', 30,
    300, 10, 10, 23.3,
    0, 3.3, 13.3, 50,
    900, 133, 267, 0.33,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.92, true),

-- ============================================================================
-- SPREADS & DIPS
-- ============================================================================

('Hummus (Classic)', 'ingredient', 'Classic chickpea hummus',
    100, 'g', 'tbsp (15g)', 15,
    177, 4.9, 14.3, 10.6,
    4, 0.3, 1.3, 0,
    269, 173, 38, 1.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Tzatziki Sauce', 'ingredient', 'Greek yogurt cucumber sauce',
    100, 'g', 'tbsp (15g)', 15,
    73, 4, 4.7, 4.7,
    0.7, 3.3, 2.7, 13,
    267, 133, 73, 0.27,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.93, true),

('Baba Ganoush', 'ingredient', 'Roasted eggplant dip',
    100, 'g', 'tbsp (15g)', 15,
    133, 3.3, 10, 10,
    4, 4, 1.3, 0,
    333, 267, 33, 1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Spinach Artichoke Dip', 'ingredient', 'Creamy spinach artichoke dip',
    100, 'g', 'serving (30g)', 30,
    233, 6.7, 10, 20,
    2, 3.3, 10, 40,
    600, 200, 167, 0.67,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.91, false),

('French Onion Dip', 'ingredient', 'Sour cream onion dip',
    100, 'g', 'tbsp (15g)', 15,
    200, 2.7, 6.7, 18.7,
    0.7, 4, 11.3, 40,
    533, 93, 60, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.92, true),

-- ============================================================================
-- PASTA & PIZZA SAUCES
-- ============================================================================

('Marinara Sauce', 'ingredient', 'Tomato marinara sauce',
    100, 'g', 'cup (250g)', 125,
    50, 1.8, 9.6, 1.4,
    2.5, 6.1, 0.2, 0,
    478, 410, 25, 0.82,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Alfredo Sauce', 'ingredient', 'Creamy alfredo sauce',
    100, 'g', 'cup (244g)', 122,
    180, 4.1, 8.2, 14.8,
    0.4, 2.9, 8.6, 41,
    656, 98, 123, 0.25,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Pesto Sauce', 'ingredient', 'Basil pesto sauce',
    100, 'g', 'tbsp (16g)', 16,
    500, 6.2, 6.2, 50,
    1.9, 1.2, 8.1, 12,
    812, 281, 250, 1.25,
    ARRAY['dairy', 'nuts'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Vodka Sauce', 'ingredient', 'Creamy tomato vodka sauce',
    100, 'g', 'cup (250g)', 125,
    100, 2, 12, 5,
    2, 8, 2.5, 10,
    480, 300, 40, 0.6,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Pizza Sauce', 'ingredient', 'Pizza tomato sauce',
    100, 'g', 'cup (249g)', 62,
    42, 1.6, 8.4, 0.8,
    2, 5.2, 0.1, 0,
    532, 364, 20, 0.88,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

-- ============================================================================
-- SPECIALTY SAUCES
-- ============================================================================

('Cocktail Sauce', 'ingredient', 'Seafood cocktail sauce',
    100, 'g', 'tbsp (17g)', 17,
    104, 1.2, 24.1, 0.3,
    0.6, 19.3, 0, 0,
    867, 241, 12, 0.42,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Tartar Sauce', 'ingredient', 'Creamy tartar sauce',
    100, 'g', 'tbsp (14g)', 14,
    533, 0.7, 6.7, 56.7,
    0.7, 4, 8, 40,
    1000, 47, 13, 0.13,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Hollandaise Sauce', 'ingredient', 'Classic hollandaise sauce',
    100, 'g', 'serving (30g)', 30,
    367, 5, 3.3, 36.7,
    0, 1.7, 21.7, 167,
    567, 100, 67, 0.67,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.93, true),

('Chimichurri', 'ingredient', 'Argentinian herb sauce',
    100, 'g', 'tbsp (15g)', 15,
    600, 1.3, 6.7, 66.7,
    2.7, 1.3, 10, 0,
    467, 267, 67, 1.33,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.92, true),

('Enchilada Sauce (Red)', 'ingredient', 'Red chili enchilada sauce',
    100, 'g', 'cup (250g)', 63,
    36, 1.2, 6.8, 1.2,
    1.6, 3.2, 0.2, 0,
    640, 240, 16, 0.72,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- COOKING BASES
-- ============================================================================

('Tomato Paste', 'ingredient', 'Concentrated tomato paste',
    100, 'g', 'tbsp (16g)', 16,
    82, 4.3, 18.9, 0.5,
    4.1, 12.2, 0.1, 0,
    59, 1014, 36, 2.98,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Tomato Sauce (Plain)', 'ingredient', 'Plain tomato sauce',
    100, 'g', 'cup (245g)', 123,
    29, 1.3, 6.7, 0.2,
    1.5, 4.4, 0, 0,
    321, 297, 16, 0.73,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Chicken Broth (Low-Sodium)', 'ingredient', 'Low-sodium chicken broth',
    100, 'g', 'cup (240g)', 120,
    5, 0.4, 0.5, 0.2,
    0, 0.2, 0, 0,
    208, 46, 4, 0.08,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Beef Broth (Low-Sodium)', 'ingredient', 'Low-sodium beef broth',
    100, 'g', 'cup (240g)', 120,
    8, 0.8, 0.4, 0.3,
    0, 0.2, 0.1, 0,
    208, 54, 8, 0.21,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Vegetable Broth (Low-Sodium)', 'ingredient', 'Low-sodium vegetable broth',
    100, 'g', 'cup (240g)', 120,
    8, 0.2, 1.9, 0,
    0, 0.8, 0, 0,
    192, 96, 8, 0.21,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Coconut Cream', 'ingredient', 'Thick coconut cream for cooking',
    100, 'g', 'tbsp (15g)', 15,
    330, 3.6, 6, 34.7,
    2.2, 3.3, 30.9, 0,
    14, 263, 18, 3.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ CONDIMENTS & SAUCES SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Ketchup', 'Mustard (Yellow)', 'Mayonnaise (Full-Fat)', 'BBQ Sauce', 'Sriracha',
    'Ranch Dressing', 'Caesar Dressing', 'Italian Dressing', 'Balsamic Vinaigrette',
    'Soy Sauce', 'Teriyaki Sauce', 'Hoisin Sauce', 'Sweet Chili Sauce',
    'Salsa (Red, Medium)', 'Guacamole', 'Hummus (Classic)', 'Tzatziki Sauce',
    'Marinara Sauce', 'Alfredo Sauce', 'Pesto Sauce', 'Pizza Sauce',
    'Tomato Paste', 'Chicken Broth (Low-Sodium)', 'Coconut Cream'
);
