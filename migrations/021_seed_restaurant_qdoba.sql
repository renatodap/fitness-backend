-- ============================================================================
-- MIGRATION 021: SEED QDOBA MEXICAN EATS
-- ============================================================================
-- Description: Complete Qdoba menu items with accurate nutrition data
-- Total items: ~40 items
-- Categories: Entrees, proteins, bases, toppings, sauces, sides, drinks
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

-- ENTREE BASES
('Qdoba Burrito Bowl (Base Only)', 'ingredient', 'Qdoba burrito bowl with no toppings',
    100, 'g', 'bowl (220g)', 220,
    35, 1, 8, 0,
    1, 1, 0, 0,
    5, 40, 10, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Qdoba Burrito (Flour Tortilla)', 'ingredient', 'Qdoba 12-inch flour tortilla',
    100, 'g', 'tortilla (110g)', 110,
    290, 8, 50, 6,
    2, 2, 1.5, 0,
    700, 120, 80, 2.5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.93, false),

('Qdoba Taco (Soft Flour Tortilla)', 'ingredient', 'Qdoba soft flour taco shell',
    100, 'g', '3 tortillas (66g)', 66,
    295, 8, 51, 6,
    2, 2, 1.5, 0,
    710, 120, 80, 2.6,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Qdoba Taco (Crispy Corn Shell)', 'ingredient', 'Qdoba crispy corn taco shell',
    100, 'g', '3 shells (42g)', 42,
    357, 4.8, 57.1, 14.3,
    4.8, 2.4, 2.4, 0,
    190, 95, 48, 1.4,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

-- PROTEINS
('Qdoba Grilled Chicken', 'ingredient', 'Qdoba seasoned grilled chicken',
    100, 'g', 'serving (113g)', 113,
    150, 31, 2, 2.5,
    0, 1, 0.5, 85,
    620, 380, 20, 1.2,
    NULL, ARRAY['gluten-free'], 'user', 0.93, false),

('Qdoba Grilled Steak', 'ingredient', 'Qdoba marinated grilled steak',
    100, 'g', 'serving (113g)', 113,
    170, 28, 3, 5,
    0, 2, 2, 75,
    530, 420, 25, 2.8,
    NULL, ARRAY['gluten-free'], 'user', 0.93, false),

('Qdoba Ground Beef', 'ingredient', 'Qdoba seasoned ground beef',
    100, 'g', 'serving (113g)', 113,
    220, 21, 4, 13,
    0, 2, 5, 70,
    680, 350, 30, 2.4,
    NULL, ARRAY['gluten-free'], 'user', 0.92, false),

('Qdoba Pulled Pork', 'ingredient', 'Qdoba slow-cooked pulled pork',
    100, 'g', 'serving (113g)', 113,
    190, 26, 5, 7,
    0, 3, 2.5, 75,
    720, 370, 28, 1.8,
    NULL, ARRAY['gluten-free'], 'user', 0.92, false),

('Qdoba Fajita Vegetables', 'ingredient', 'Qdoba grilled peppers and onions',
    100, 'g', 'serving (85g)', 85,
    20, 0.5, 4, 0.5,
    1, 2, 0, 0,
    150, 120, 15, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Qdoba Vegetarian (Impossible)', 'ingredient', 'Qdoba Impossible plant-based meat',
    100, 'g', 'serving (113g)', 113,
    220, 18, 9, 13,
    3, 1, 7, 0,
    370, 440, 70, 3.6,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

-- RICE & BEANS
('Qdoba Cilantro Lime Rice', 'ingredient', 'Qdoba cilantro lime white rice',
    100, 'g', 'serving (127g)', 127,
    160, 3, 33, 2,
    0, 0, 0, 0,
    270, 55, 20, 1.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Qdoba Brown Rice', 'ingredient', 'Qdoba seasoned brown rice',
    100, 'g', 'serving (127g)', 127,
    150, 3.5, 30, 2.5,
    2, 0, 0, 0,
    250, 85, 15, 1.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Qdoba Black Beans', 'ingredient', 'Qdoba seasoned black beans',
    100, 'g', 'serving (127g)', 127,
    110, 7, 18, 1,
    6, 1, 0, 0,
    310, 280, 40, 2.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Qdoba Pinto Beans', 'ingredient', 'Qdoba seasoned pinto beans',
    100, 'g', 'serving (127g)', 127,
    115, 7, 19, 1,
    6, 1, 0, 0,
    320, 290, 45, 2.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

-- TOPPINGS
('Qdoba Shredded Cheese', 'ingredient', 'Qdoba three-cheese blend',
    100, 'g', 'serving (28g)', 28,
    357, 25, 3.6, 28.6,
    0, 0, 17.9, 89,
    643, 107, 714, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Qdoba Queso Blanco', 'ingredient', 'Qdoba white queso cheese sauce',
    100, 'g', 'serving (57g)', 57,
    140, 5, 7, 11,
    0, 4, 7, 35,
    580, 90, 150, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.92, false),

('Qdoba Queso Diablo', 'ingredient', 'Qdoba spicy cheese sauce',
    100, 'g', 'serving (57g)', 57,
    150, 5, 8, 11,
    0, 4, 7, 35,
    620, 95, 150, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.92, false),

('Qdoba Sour Cream', 'ingredient', 'Qdoba sour cream',
    100, 'g', 'serving (28g)', 28,
    214, 3.6, 7.1, 17.9,
    0, 3.6, 10.7, 54,
    71, 143, 107, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Qdoba Guacamole', 'ingredient', 'Qdoba fresh guacamole',
    100, 'g', 'serving (57g)', 57,
    105, 1.8, 7, 8.8,
    5.3, 0.9, 1.3, 0,
    175, 351, 9, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.94, false),

('Qdoba Pico de Gallo', 'ingredient', 'Qdoba fresh pico de gallo salsa',
    100, 'g', 'serving (57g)', 57,
    18, 0.9, 4.4, 0,
    0.9, 2.6, 0, 0,
    175, 140, 9, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.93, false),

('Qdoba Salsa Verde', 'ingredient', 'Qdoba green tomatillo salsa',
    100, 'g', 'serving (57g)', 57,
    26, 0.9, 6.1, 0,
    0.9, 3.5, 0, 0,
    350, 150, 10, 0.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.92, false),

('Qdoba Salsa Roja', 'ingredient', 'Qdoba red salsa',
    100, 'g', 'serving (57g)', 57,
    35, 1.8, 7, 0,
    1.8, 3.5, 0, 0,
    420, 175, 18, 0.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.92, false),

('Qdoba Corn Salsa', 'ingredient', 'Qdoba roasted corn salsa',
    100, 'g', 'serving (57g)', 57,
    70, 1.8, 14, 1.8,
    1.8, 5.3, 0, 0,
    175, 120, 9, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Qdoba Lettuce (Shredded)', 'ingredient', 'Qdoba shredded lettuce',
    100, 'g', 'serving (28g)', 28,
    14, 1.4, 2.9, 0.1,
    1.3, 0.8, 0, 0,
    10, 141, 36, 0.86,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Qdoba Jalapeños', 'ingredient', 'Qdoba pickled jalapeño slices',
    100, 'g', 'serving (28g)', 28,
    27, 0.9, 5.5, 0.4,
    2.8, 1.8, 0.1, 0,
    1135, 130, 16, 1.07,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

-- COMPLETE ENTREES
('Qdoba Chicken Burrito Bowl', 'restaurant', 'Qdoba burrito bowl with chicken, rice, beans, veggies, cheese, sour cream',
    100, 'g', 'bowl (510g)', 510,
    145, 11.4, 15.5, 4.7,
    2.4, 1.4, 1.8, 30,
    350, 240, 85, 1.5,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.91, false),

('Qdoba Steak Burrito (Large)', 'restaurant', 'Qdoba burrito with steak, rice, beans, cheese, sour cream, salsa',
    100, 'g', 'burrito (680g)', 680,
    175, 12.4, 21.6, 5.6,
    2.5, 1.8, 2.4, 38,
    480, 270, 100, 2.1,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Qdoba Veggie Bowl', 'restaurant', 'Qdoba bowl with fajita veggies, rice, black beans, guacamole, pico de gallo',
    100, 'g', 'bowl (480g)', 480,
    125, 4.8, 22, 3.3,
    4.8, 2.5, 0.4, 0,
    280, 220, 50, 1.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

('Qdoba Chicken Tacos (3 Soft)', 'restaurant', 'Three soft flour tacos with chicken, cheese, lettuce, pico de gallo',
    100, 'g', '3 tacos (340g)', 340,
    188, 13.8, 20.3, 5.9,
    1.8, 1.5, 2.1, 42,
    510, 240, 90, 1.6,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Qdoba Loaded Tortilla Soup', 'restaurant', 'Qdoba tortilla soup with chicken, tortilla strips, cheese',
    100, 'g', 'bowl (354g)', 354,
    127, 8.5, 11.6, 5.4,
    1.7, 2.5, 2.3, 28,
    595, 210, 95, 1.2,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.89, false),

-- SIDES & EXTRAS
('Qdoba Chips (Tortilla)', 'ingredient', 'Qdoba crispy tortilla chips',
    100, 'g', 'serving (113g)', 113,
    496, 7.1, 60.7, 25,
    5.4, 0.9, 3.6, 0,
    536, 196, 89, 1.79,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Qdoba Queso & Chips', 'restaurant', 'Qdoba chips with queso blanco',
    100, 'g', 'serving (170g)', 170,
    376, 6.5, 43.5, 19.4,
    3.5, 2.6, 6.5, 18,
    548, 162, 108, 1.2,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

('Qdoba Guacamole & Chips', 'restaurant', 'Qdoba chips with guacamole',
    100, 'g', 'serving (170g)', 170,
    371, 5.4, 42.4, 19.4,
    5.3, 0.9, 2.7, 0,
    441, 243, 62, 1.3,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Qdoba Mexican Street Corn', 'ingredient', 'Qdoba elote-style street corn',
    100, 'g', 'serving (142g)', 142,
    155, 3.5, 16.2, 9.2,
    1.4, 4.9, 4.2, 21,
    440, 165, 85, 0.6,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false),

-- BEVERAGES
('Qdoba Fountain Drink (Medium)', 'ingredient', 'Qdoba medium fountain soda',
    100, 'g', 'cup (21oz, 621g)', 621,
    42, 0, 11, 0,
    0, 11, 0, 0,
    18, 5, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Qdoba Agua Fresca (Mango)', 'ingredient', 'Qdoba mango agua fresca',
    100, 'g', 'cup (16oz, 473g)', 473,
    63, 0, 16, 0,
    0, 15, 0, 0,
    8, 20, 5, 0.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

('Qdoba Agua Fresca (Strawberry)', 'ingredient', 'Qdoba strawberry agua fresca',
    100, 'g', 'cup (16oz, 473g)', 473,
    59, 0, 15, 0,
    0, 14, 0, 0,
    8, 18, 5, 0.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

-- SAUCES & DRESSINGS
('Qdoba Chipotle Ranch Dressing', 'ingredient', 'Qdoba creamy chipotle ranch',
    100, 'g', 'serving (28g)', 28,
    429, 0, 7.1, 42.9,
    0, 7.1, 7.1, 21,
    643, 36, 36, 0,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Qdoba Habanero Salsa', 'ingredient', 'Qdoba spicy habanero hot sauce',
    100, 'g', 'serving (28g)', 28,
    36, 1.8, 7.1, 0,
    1.8, 3.6, 0, 0,
    536, 160, 18, 0.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.91, false),

('Qdoba Poblano Crema', 'ingredient', 'Qdoba creamy poblano sauce',
    100, 'g', 'serving (28g)', 28,
    357, 1.8, 7.1, 35.7,
    0, 3.6, 7.1, 21,
    536, 54, 36, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false);

COMMIT;

SELECT '✅ QDOBA MENU SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name LIKE 'Qdoba%';
