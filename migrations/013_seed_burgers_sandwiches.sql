-- ============================================================================
-- MIGRATION 013: SEED BURGERS & SANDWICHES
-- ============================================================================
-- Description: All common burgers and sandwiches
-- Categories: Burgers (beef, turkey, veggie), Sandwiches (deli, grilled, specialty)
-- Total items: ~70 items
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
-- BURGERS (BEEF)
-- ============================================================================

('Hamburger (with Bun)', 'ingredient', 'Basic hamburger with bun',
    219, 'g', 'burger (219g)', 219,
    540, 34.3, 40.4, 24.7,
    2.3, 7.8, 9.1, 100,
    791, 479, 126, 4.5,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.93, false),

('Cheeseburger (with Bun)', 'ingredient', 'Cheeseburger with American cheese',
    248, 'g', 'burger (248g)', 248,
    630, 39.8, 41.4, 31.4,
    2.4, 8.1, 14.1, 130,
    1051, 538, 276, 4.7,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.93, false),

('Double Cheeseburger', 'ingredient', 'Double cheeseburger with two patties',
    340, 'g', 'burger (340g)', 340,
    820, 58.8, 42.6, 47.1,
    2.6, 8.8, 21.8, 190,
    1471, 735, 426, 6.5,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.92, false),

('Bacon Cheeseburger', 'ingredient', 'Cheeseburger with bacon',
    280, 'g', 'burger (280g)', 280,
    750, 44.6, 42.1, 42.1,
    2.5, 8.6, 17.9, 155,
    1321, 607, 293, 5.1,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.92, false),

('Mushroom Swiss Burger', 'ingredient', 'Burger with sautéed mushrooms and Swiss cheese',
    300, 'g', 'burger (300g)', 300,
    680, 42, 43.3, 35.7,
    3, 9, 15, 135,
    920, 687, 320, 4.8,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

('BBQ Bacon Burger', 'ingredient', 'Burger with BBQ sauce, bacon, and cheddar',
    310, 'g', 'burger (310g)', 310,
    820, 46.5, 54.8, 44.8,
    3.2, 18.7, 18.7, 165,
    1580, 645, 306, 5.3,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

('Burger Patty Only (No Bun)', 'ingredient', 'Quarter pound beef patty, no bun',
    113, 'g', 'patty (113g)', 113,
    290, 28.3, 0, 19.5,
    0, 0, 7.1, 94,
    75, 407, 23, 2.7,
    NULL, ARRAY['gluten-free', 'keto'], 'usda', 0.95, true),

('Sliders (3 Mini Burgers)', 'ingredient', 'Three mini cheeseburger sliders',
    240, 'g', 'serving (240g)', 240,
    600, 36, 42, 30,
    2.4, 8.4, 13.5, 125,
    1000, 515, 264, 4.5,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

-- ============================================================================
-- BURGERS (ALTERNATIVE PROTEINS)
-- ============================================================================

('Turkey Burger (with Bun)', 'ingredient', 'Ground turkey burger with bun',
    219, 'g', 'burger (219g)', 219,
    440, 35.2, 41.1, 14.6,
    2.3, 7.8, 3.7, 85,
    820, 419, 110, 3.8,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.92, false),

('Chicken Burger (Grilled)', 'ingredient', 'Grilled chicken breast burger',
    230, 'g', 'burger (230g)', 230,
    420, 38.3, 42.6, 10.4,
    2.6, 8.3, 2.6, 90,
    880, 465, 96, 3.2,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.92, false),

('Chicken Burger (Crispy)', 'ingredient', 'Breaded fried chicken burger',
    240, 'g', 'burger (240g)', 240,
    580, 32.5, 50, 26.7,
    2.9, 8.8, 5.4, 80,
    1100, 425, 104, 3.6,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.91, false),

('Veggie Burger (with Bun)', 'ingredient', 'Plant-based veggie burger',
    219, 'g', 'burger (219g)', 219,
    380, 18.3, 45.7, 14.6,
    6.4, 8.2, 2.7, 0,
    750, 411, 137, 4.1,
    ARRAY['gluten', 'soy'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Black Bean Burger', 'ingredient', 'Black bean veggie burger with bun',
    219, 'g', 'burger (219g)', 219,
    360, 16.4, 49.3, 11,
    8.2, 7.8, 1.8, 0,
    680, 493, 123, 4.4,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Beyond Burger (with Bun)', 'ingredient', 'Beyond Meat plant-based burger',
    227, 'g', 'burger (227g)', 227,
    470, 25.1, 42.1, 21.1,
    4, 8.4, 6.2, 0,
    770, 429, 145, 5.3,
    ARRAY['gluten', 'soy'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Impossible Burger (with Bun)', 'ingredient', 'Impossible Foods plant-based burger',
    227, 'g', 'burger (227g)', 227,
    460, 24.7, 42.5, 20.4,
    3.5, 8.8, 7.5, 0,
    840, 418, 163, 5.7,
    ARRAY['gluten', 'soy'], ARRAY['vegan', 'vegetarian'], 'user', 0.92, false),

('Salmon Burger', 'ingredient', 'Grilled salmon burger with bun',
    219, 'g', 'burger (219g)', 219,
    420, 32.4, 42.5, 13.2,
    2.8, 7.8, 2.7, 65,
    740, 524, 109, 2.9,
    ARRAY['fish', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

('Bison Burger', 'ingredient', 'Bison burger with bun',
    219, 'g', 'burger (219g)', 219,
    480, 36.5, 40.6, 18.3,
    2.3, 7.8, 7.3, 95,
    750, 498, 118, 4.6,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.90, false),

('Lamb Burger', 'ingredient', 'Ground lamb burger with bun',
    219, 'g', 'burger (219g)', 219,
    560, 32.9, 40.8, 27.4,
    2.3, 7.8, 11.4, 105,
    820, 456, 126, 4.3,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.90, false),

-- ============================================================================
-- CLASSIC SANDWICHES
-- ============================================================================

('BLT Sandwich', 'ingredient', 'Bacon, lettuce, tomato sandwich',
    164, 'g', 'sandwich (164g)', 164,
    420, 14.6, 40.2, 21.3,
    2.4, 6.1, 6.1, 35,
    920, 268, 73, 2.9,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.92, false),

('Club Sandwich', 'ingredient', 'Turkey, bacon, lettuce, tomato triple-decker',
    313, 'g', 'sandwich (313g)', 313,
    590, 38.5, 55.3, 21.9,
    3.8, 9.4, 6.6, 95,
    1470, 563, 141, 4.7,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.92, false),

('Reuben Sandwich', 'ingredient', 'Corned beef, sauerkraut, Swiss, rye bread',
    286, 'g', 'sandwich (286g)', 286,
    640, 36.6, 46.2, 32.3,
    5.7, 8, 13.7, 120,
    1920, 460, 457, 3.7,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Grilled Cheese Sandwich', 'ingredient', 'Classic grilled cheese',
    119, 'g', 'sandwich (119g)', 119,
    390, 14.3, 35.7, 21.4,
    1.7, 4.8, 11.9, 60,
    780, 119, 357, 2.1,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Philly Cheesesteak', 'ingredient', 'Philly cheesesteak with peppers and onions',
    348, 'g', 'sandwich (348g)', 348,
    680, 40.6, 58.2, 29.6,
    3.8, 10.4, 13.9, 115,
    1520, 592, 348, 5.2,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Italian Sub', 'ingredient', 'Italian cold cut sub with salami, ham, provolone',
    283, 'g', 'sub (283g)', 283,
    640, 32.4, 50.3, 33.9,
    3.4, 8.5, 12.7, 95,
    1980, 396, 340, 3.7,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Meatball Sub', 'ingredient', 'Meatball marinara sub with cheese',
    350, 'g', 'sub (350g)', 350,
    680, 33.6, 70, 28,
    5.6, 14, 12.6, 85,
    1680, 700, 350, 5.6,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

('French Dip Sandwich', 'ingredient', 'Roast beef sandwich with au jus',
    283, 'g', 'sandwich (283g)', 283,
    540, 38.4, 50.8, 17, 2.8, 8.5, 6.8, 85,
    1420, 481, 113, 5.1,
    ARRAY['gluten'], NULL, 'user', 0.90, false),

('Monte Cristo Sandwich', 'ingredient', 'Ham and cheese sandwich, battered and fried',
    231, 'g', 'sandwich (231g)', 231,
    620, 30.9, 47.8, 33.2,
    2.3, 11.6, 14.8, 195,
    1460, 347, 416, 3.5,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.89, false),

('Pulled Pork Sandwich', 'ingredient', 'BBQ pulled pork sandwich',
    250, 'g', 'sandwich (250g)', 250,
    520, 30, 54, 20,
    3, 18, 6, 80,
    1180, 475, 100, 3.8,
    ARRAY['gluten'], NULL, 'user', 0.91, false),

-- ============================================================================
-- DELI SANDWICHES
-- ============================================================================

('Ham and Cheese Sandwich', 'ingredient', 'Deli ham and cheese on white bread',
    147, 'g', 'sandwich (147g)', 147,
    320, 19.7, 31.3, 12.2,
    1.5, 4.1, 5.4, 50,
    1020, 197, 197, 2.4,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'usda', 0.94, true),

('Turkey and Cheese Sandwich', 'ingredient', 'Deli turkey and cheese on white bread',
    147, 'g', 'sandwich (147g)', 147,
    310, 20.4, 31.3, 10.9,
    1.5, 4.1, 4.8, 45,
    980, 212, 191, 2.3,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.93, false),

('Roast Beef Sandwich', 'ingredient', 'Deli roast beef sandwich',
    164, 'g', 'sandwich (164g)', 164,
    340, 24.4, 33.5, 11,
    1.8, 4.9, 3.7, 55,
    880, 293, 85, 3.5,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.92, false),

('Pastrami Sandwich', 'ingredient', 'Pastrami on rye with mustard',
    180, 'g', 'sandwich (180g)', 180,
    380, 23.4, 38.7, 14.4,
    3.6, 5.4, 5.4, 65,
    1520, 289, 90, 3.2,
    ARRAY['gluten'], NULL, 'user', 0.91, false),

('Chicken Salad Sandwich', 'ingredient', 'Chicken salad sandwich on white bread',
    183, 'g', 'sandwich (183g)', 183,
    440, 20.8, 35.5, 24,
    1.8, 5.5, 4.4, 60,
    720, 256, 89, 2.6,
    ARRAY['eggs', 'gluten'], NULL, 'user', 0.92, false),

('Egg Salad Sandwich', 'ingredient', 'Egg salad sandwich on white bread',
    156, 'g', 'sandwich (156g)', 156,
    390, 12.8, 30.8, 23.4,
    1.6, 4.7, 5.3, 265,
    600, 134, 67, 2.1,
    ARRAY['eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Peanut Butter and Jelly Sandwich', 'ingredient', 'PB&J on white bread',
    100, 'g', 'sandwich (100g)', 100,
    350, 10, 48, 14,
    3, 18, 3, 0,
    380, 200, 60, 2,
    ARRAY['nuts', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Tuna Salad Sandwich', 'ingredient', 'Tuna salad sandwich on white bread',
    179, 'g', 'sandwich (179g)', 179,
    380, 20.7, 33, 17.9,
    1.8, 5, 3.6, 35,
    640, 246, 78, 2.4,
    ARRAY['eggs', 'fish', 'gluten'], NULL, 'usda', 0.93, true),

('Bologna Sandwich', 'ingredient', 'Bologna and cheese sandwich',
    128, 'g', 'sandwich (128g)', 128,
    360, 14.8, 31.3, 18.8,
    1.6, 4.1, 7.8, 45,
    1080, 156, 188, 2.1,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

-- ============================================================================
-- HOT SANDWICHES
-- ============================================================================

('Hot Dog (with Bun)', 'ingredient', 'All-beef hot dog in bun',
    100, 'g', 'hot dog (100g)', 100,
    290, 10.4, 22.9, 17.5,
    0.8, 5, 6.7, 35,
    810, 143, 54, 2.14,
    ARRAY['gluten', 'eggs'], NULL, 'usda', 0.94, true),

('Chili Dog', 'ingredient', 'Hot dog with chili and cheese',
    180, 'g', 'hot dog (180g)', 180,
    480, 18, 35.3, 29.4,
    2.9, 7.1, 11.8, 60,
    1260, 338, 162, 3.5,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.91, false),

('Corn Dog', 'ingredient', 'Battered hot dog on a stick',
    175, 'g', 'corn dog (175g)', 175,
    438, 16.6, 51.4, 19.4,
    0.6, 11.4, 5.1, 79,
    973, 263, 102, 2.63,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'usda', 0.93, true),

('Bratwurst (with Bun)', 'ingredient', 'Grilled bratwurst in bun',
    185, 'g', 'brat (185g)', 185,
    510, 18.5, 35.2, 32.6,
    1.9, 6.5, 11.1, 70,
    1180, 259, 85, 2.6,
    ARRAY['gluten', 'eggs'], NULL, 'user', 0.91, false),

('Sloppy Joe', 'ingredient', 'Ground beef in tangy sauce on bun',
    200, 'g', 'sandwich (200g)', 200,
    380, 20, 44, 14,
    2.4, 12, 5, 60,
    780, 380, 96, 3.2,
    ARRAY['gluten'], NULL, 'user', 0.91, false),

('Chicken Parm Sandwich', 'ingredient', 'Breaded chicken with marinara and mozzarella',
    300, 'g', 'sandwich (300g)', 300,
    680, 38.4, 60, 30,
    4.5, 11.7, 10.8, 105,
    1540, 570, 420, 4.2,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.91, false),

('Sausage and Peppers Sandwich', 'ingredient', 'Italian sausage with peppers and onions',
    300, 'g', 'sandwich (300g)', 300,
    620, 26.4, 52.8, 33,
    3.9, 9.6, 11.4, 75,
    1440, 510, 120, 3.9,
    ARRAY['gluten'], NULL, 'user', 0.90, false),

-- ============================================================================
-- SPECIALTY SANDWICHES
-- ============================================================================

('Banh Mi', 'ingredient', 'Vietnamese sandwich with pork, pickled vegetables',
    250, 'g', 'sandwich (250g)', 250,
    480, 22, 52, 20,
    3, 10, 5, 55,
    1120, 400, 80, 3.2,
    ARRAY['gluten'], NULL, 'user', 0.90, false),

('Cubano', 'ingredient', 'Cuban sandwich with pork, ham, Swiss, pickles',
    286, 'g', 'sandwich (286g)', 286,
    620, 38.9, 50.3, 28.6,
    2.9, 8.6, 12.3, 110,
    1860, 486, 400, 4,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Po Boy (Shrimp)', 'ingredient', 'New Orleans shrimp po boy',
    300, 'g', 'sandwich (300g)', 300,
    620, 24, 68.4, 27,
    3.6, 9, 5.4, 145,
    1380, 420, 120, 4.5,
    ARRAY['eggs', 'gluten'], NULL, 'user', 0.89, false),

('Gyro Sandwich', 'ingredient', 'Greek gyro wrap with tzatziki',
    250, 'g', 'gyro (250g)', 250,
    520, 24, 42, 26,
    3.5, 7, 10, 75,
    1050, 465, 170, 3.5,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('Falafel Wrap', 'ingredient', 'Falafel wrap with hummus and vegetables',
    280, 'g', 'wrap (280g)', 280,
    480, 16.1, 62.5, 19.6,
    11.2, 7, 3.6, 0,
    920, 560, 140, 5,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.91, false),

('Chicken Caesar Wrap', 'ingredient', 'Grilled chicken Caesar wrap',
    268, 'g', 'wrap (268g)', 268,
    520, 31.3, 39.6, 25.4,
    3.2, 4.3, 7.5, 85,
    1240, 429, 214, 2.9,
    ARRAY['dairy', 'eggs', 'fish', 'gluten'], NULL, 'user', 0.91, false),

('Buffalo Chicken Wrap', 'ingredient', 'Crispy buffalo chicken wrap with ranch',
    280, 'g', 'wrap (280g)', 280,
    600, 28, 48.4, 32.2,
    3.4, 5.6, 7.8, 75,
    1680, 420, 168, 3.2,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.90, false);

COMMIT;

SELECT
    '✅ BURGERS & SANDWICHES SEEDED!' as status,
    COUNT(*) as total_items,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Hamburger (with Bun)', 'Cheeseburger (with Bun)', 'Turkey Burger (with Bun)', 'Veggie Burger (with Bun)',
    'BLT Sandwich', 'Club Sandwich', 'Grilled Cheese Sandwich', 'Ham and Cheese Sandwich',
    'Peanut Butter and Jelly Sandwich', 'Hot Dog (with Bun)'
);
