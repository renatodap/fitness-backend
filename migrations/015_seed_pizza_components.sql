-- ============================================================================
-- MIGRATION 015: SEED PIZZA COMPONENTS
-- ============================================================================
-- Description: Pizza toppings, cheeses, sauces as individual trackable items
-- Total items: ~50 items
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
-- PIZZA MEATS
-- ============================================================================

('Pepperoni (Pizza Topping)', 'ingredient', 'Pepperoni slices for pizza',
    100, 'g', 'oz (28g)', 28,
    504, 22.7, 4.1, 44.3,
    0, 0, 15.5, 79,
    1881, 279, 27, 1.2,
    ARRAY['dairy'], ARRAY['keto'], 'usda', 0.95, true),

('Italian Sausage (Pizza Topping)', 'ingredient', 'Crumbled Italian sausage',
    100, 'g', 'oz (28g)', 28,
    344, 13.4, 3, 31.1,
    0, 0.4, 11.1, 65,
    1207, 184, 17, 1.16,
    NULL, ARRAY['keto'], 'usda', 0.94, true),

('Ground Beef (Pizza Topping)', 'ingredient', 'Seasoned ground beef for pizza',
    100, 'g', 'oz (28g)', 28,
    250, 26, 0, 17,
    0, 0, 6.8, 78,
    75, 318, 18, 2.6,
    NULL, ARRAY['gluten-free', 'keto'], 'user', 0.93, false),

('Bacon Bits (Pizza Topping)', 'ingredient', 'Real bacon pieces for pizza',
    100, 'g', 'tbsp (7g)', 7,
    541, 37.9, 1.7, 42,
    0, 0, 13.7, 107,
    2310, 565, 17, 1.44,
    NULL, ARRAY['gluten-free', 'keto'], 'usda', 0.94, true),

('Ham (Pizza Topping)', 'ingredient', 'Diced ham for pizza',
    100, 'g', 'oz (28g)', 28,
    145, 20.9, 1.5, 5.5,
    0, 1.5, 1.8, 53,
    1203, 287, 7, 0.91,
    NULL, ARRAY['gluten-free'], 'usda', 0.94, true),

('Canadian Bacon (Pizza Topping)', 'ingredient', 'Canadian bacon/back bacon slices',
    100, 'g', 'oz (28g)', 28,
    165, 21.8, 2.2, 7.7,
    0, 0, 2.5, 57,
    1455, 329, 11, 0.73,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Chicken (Pizza Topping)', 'ingredient', 'Grilled chicken pieces for pizza',
    100, 'g', 'oz (28g)', 28,
    165, 31, 0, 3.6,
    0, 0, 1, 85,
    74, 256, 15, 1.04,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Anchovies (Pizza Topping)', 'ingredient', 'Anchovy fillets for pizza',
    100, 'g', 'oz (28g)', 28,
    210, 28.9, 0, 9.7,
    0, 0, 2.2, 60,
    3668, 383, 147, 3.25,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.93, true),

('Meatball (Pizza Topping)', 'ingredient', 'Sliced meatballs for pizza',
    100, 'g', 'oz (28g)', 28,
    197, 12.5, 8.7, 12.5,
    0.9, 2.2, 4.8, 40,
    456, 194, 40, 1.4,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'usda', 0.92, true),

-- ============================================================================
-- PIZZA VEGETABLES
-- ============================================================================

('Mushrooms (Pizza Topping)', 'ingredient', 'Sliced mushrooms for pizza',
    100, 'g', 'oz (28g)', 28,
    22, 3.1, 3.3, 0.3,
    1, 2, 0, 0,
    5, 318, 3, 0.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Green Peppers (Pizza Topping)', 'ingredient', 'Sliced green bell peppers',
    100, 'g', 'oz (28g)', 28,
    20, 0.9, 4.6, 0.2,
    1.7, 2.4, 0, 0,
    3, 175, 10, 0.34,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Red Peppers (Pizza Topping)', 'ingredient', 'Sliced red bell peppers',
    100, 'g', 'oz (28g)', 28,
    26, 1, 6, 0.3,
    2.1, 4.2, 0, 0,
    4, 211, 7, 0.43,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Onions (Pizza Topping)', 'ingredient', 'Sliced onions for pizza',
    100, 'g', 'oz (28g)', 28,
    40, 1.1, 9.3, 0.1,
    1.7, 4.2, 0, 0,
    4, 146, 23, 0.21,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Black Olives (Pizza Topping)', 'ingredient', 'Sliced black olives',
    100, 'g', 'oz (28g)', 28,
    115, 0.8, 6.3, 10.7,
    3.2, 0, 1.4, 0,
    872, 8, 88, 3.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Green Olives (Pizza Topping)', 'ingredient', 'Sliced green olives',
    100, 'g', 'oz (28g)', 28,
    145, 1, 3.8, 15.3,
    3.3, 0.5, 2, 0,
    1556, 42, 52, 0.49,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Tomatoes (Pizza Topping)', 'ingredient', 'Fresh tomato slices',
    100, 'g', 'oz (28g)', 28,
    18, 0.9, 3.9, 0.2,
    1.2, 2.6, 0, 0,
    5, 237, 10, 0.27,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Spinach (Pizza Topping)', 'ingredient', 'Fresh spinach for pizza',
    100, 'g', 'oz (28g)', 28,
    23, 2.9, 3.6, 0.4,
    2.2, 0.4, 0.1, 0,
    79, 558, 99, 2.71,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Jalapeños (Pizza Topping)', 'ingredient', 'Sliced jalapeño peppers',
    100, 'g', 'oz (28g)', 28,
    29, 0.9, 6.5, 0.4,
    2.8, 4.1, 0, 0,
    3, 248, 12, 0.25,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Banana Peppers (Pizza Topping)', 'ingredient', 'Pickled banana pepper rings',
    100, 'g', 'oz (28g)', 28,
    27, 1.7, 4.2, 0.5,
    1.8, 1.95, 0.1, 0,
    1480, 211, 13, 0.86,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Pineapple (Pizza Topping)', 'ingredient', 'Pineapple chunks for pizza',
    100, 'g', 'oz (28g)', 28,
    50, 0.5, 13.1, 0.1,
    1.4, 9.9, 0, 0,
    1, 109, 13, 0.29,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Roasted Garlic (Pizza Topping)', 'ingredient', 'Roasted garlic cloves',
    100, 'g', 'oz (28g)', 28,
    149, 6.4, 33.1, 0.5,
    2.1, 1, 0.1, 0,
    17, 401, 181, 1.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Sun-Dried Tomatoes (Pizza Topping)', 'ingredient', 'Sun-dried tomato pieces',
    100, 'g', 'oz (28g)', 28,
    258, 14.1, 55.8, 2.97,
    12.3, 37.6, 0.4, 0,
    2095, 3427, 110, 9.09,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Artichoke Hearts (Pizza Topping)', 'ingredient', 'Marinated artichoke hearts',
    100, 'g', 'oz (28g)', 28,
    53, 3.3, 11.9, 0.2,
    5.4, 1, 0, 0,
    386, 370, 44, 1.28,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- PIZZA CHEESES
-- ============================================================================

('Mozzarella (Pizza, Shredded)', 'ingredient', 'Shredded mozzarella for pizza',
    100, 'g', 'oz (28g)', 28,
    280, 27.5, 2.2, 17.1,
    0, 1.2, 10.9, 79,
    627, 95, 731, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Mozzarella (Fresh, Sliced)', 'ingredient', 'Fresh mozzarella slices',
    100, 'g', 'oz (28g)', 28,
    280, 18.6, 3.1, 22.4,
    0, 1, 13.2, 60,
    373, 76, 409, 0.15,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Parmesan (Pizza, Grated)', 'ingredient', 'Grated parmesan for pizza',
    100, 'g', 'tbsp (5g)', 5,
    431, 38.5, 4.1, 28.6,
    0, 0.9, 19.1, 88,
    1529, 125, 1184, 0.82,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Ricotta (Pizza)', 'ingredient', 'Ricotta cheese for white pizza',
    100, 'g', 'oz (28g)', 28,
    174, 11.3, 3.0, 13,
    0, 0.3, 8.3, 51,
    84, 105, 207, 0.38,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Provolone (Pizza)', 'ingredient', 'Provolone cheese slices',
    100, 'g', 'oz (28g)', 28,
    351, 25.6, 2.1, 26.6,
    0, 0.6, 17.1, 69,
    876, 138, 756, 0.52,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Cheddar (Pizza, Shredded)', 'ingredient', 'Shredded cheddar for pizza',
    100, 'g', 'oz (28g)', 28,
    403, 24.9, 1.3, 33.1,
    0, 0.5, 21, 105,
    621, 98, 721, 0.68,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Feta (Pizza)', 'ingredient', 'Crumbled feta for pizza',
    100, 'g', 'oz (28g)', 28,
    264, 14.2, 4.1, 21.3,
    0, 4.1, 14.9, 89,
    1116, 62, 493, 0.65,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Goat Cheese (Pizza)', 'ingredient', 'Goat cheese crumbles',
    100, 'g', 'oz (28g)', 28,
    364, 21.6, 2.5, 29.8,
    0, 2.5, 20.6, 79,
    515, 158, 298, 1.62,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Gorgonzola (Pizza)', 'ingredient', 'Gorgonzola blue cheese',
    100, 'g', 'oz (28g)', 28,
    353, 21.4, 2.3, 28.7,
    0, 0.5, 18.7, 75,
    1395, 256, 528, 0.31,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Fontina (Pizza)', 'ingredient', 'Fontina cheese for pizza',
    100, 'g', 'oz (28g)', 28,
    389, 25.6, 1.6, 31.1,
    0, 1.6, 19.2, 116,
    800, 60, 550, 0.23,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.93, true),

('Vegan Cheese (Pizza)', 'ingredient', 'Plant-based mozzarella shreds',
    100, 'g', 'oz (28g)', 28,
    286, 0, 7.1, 28.6,
    0, 0, 21.4, 0,
    536, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

-- ============================================================================
-- PIZZA SAUCES & BASES
-- ============================================================================

('Pizza Sauce (Red)', 'ingredient', 'Traditional tomato pizza sauce',
    100, 'g', 'cup (249g)', 62,
    42, 1.6, 8.4, 0.8,
    2, 5.2, 0.1, 0,
    532, 364, 20, 0.88,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('White Pizza Sauce (Alfredo)', 'ingredient', 'Alfredo sauce for white pizza',
    100, 'g', 'cup (244g)', 61,
    180, 4.1, 8.2, 14.8,
    0.4, 2.9, 8.6, 41,
    656, 98, 123, 0.25,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Pesto (Pizza)', 'ingredient', 'Basil pesto for pizza',
    100, 'g', 'tbsp (16g)', 16,
    500, 6.2, 6.2, 50,
    1.9, 1.2, 8.1, 12,
    812, 281, 250, 1.25,
    ARRAY['dairy', 'nuts'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('BBQ Sauce (Pizza)', 'ingredient', 'BBQ sauce for pizza',
    100, 'g', 'tbsp (17g)', 17,
    172, 0.6, 40.8, 0.5,
    0.6, 33.9, 0.1, 0,
    815, 175, 23, 0.52,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Ranch Dressing (Pizza Drizzle)', 'ingredient', 'Ranch for pizza drizzle',
    100, 'g', 'tbsp (15g)', 15,
    480, 0.7, 6.7, 50,
    0, 4, 7.3, 20,
    867, 67, 20, 0.13,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Buffalo Sauce (Pizza)', 'ingredient', 'Buffalo wing sauce for pizza',
    100, 'g', 'tbsp (15g)', 15,
    33, 0, 6.7, 0.7,
    0, 3.3, 0, 0,
    2933, 67, 7, 0.13,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.92, false),

('Garlic Oil (Pizza)', 'ingredient', 'Garlic-infused olive oil',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 13.8, 0,
    2, 2, 1, 0.56,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- PIZZA CRUSTS
-- ============================================================================

('Pizza Dough (Unbaked)', 'ingredient', 'Raw pizza dough',
    100, 'g', 'oz (28g)', 28,
    275, 9, 53, 3.3,
    2.7, 3.5, 0.6, 0,
    597, 115, 69, 3.4,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.94, true),

('Cauliflower Pizza Crust (Prebaked)', 'ingredient', 'Cauliflower pizza crust',
    100, 'g', 'crust (150g)', 150,
    160, 6.7, 20, 6.7,
    3.3, 3.3, 2.7, 33,
    400, 200, 133, 1.33,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.91, false),

('Gluten-Free Pizza Crust', 'ingredient', 'Gluten-free pizza crust',
    100, 'g', 'crust (130g)', 130,
    250, 3.8, 46.2, 5.4,
    3.8, 1.5, 0.8, 0,
    385, 115, 46, 1.15,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false);

COMMIT;

SELECT '✅ PIZZA COMPONENTS SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name LIKE '%Pizza%' OR name IN ('Pepperoni (Pizza Topping)', 'Mozzarella (Pizza, Shredded)');
