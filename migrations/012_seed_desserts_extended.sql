-- ============================================================================
-- MIGRATION 012: SEED EXTENDED DESSERTS
-- ============================================================================
-- Description: Comprehensive dessert coverage - cakes, pies, donuts, more ice cream
-- Categories: Cakes, pies, donuts, cupcakes, pastries, puddings, more ice cream flavors
-- Total items: ~80 items
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
-- CAKES
-- ============================================================================

('Chocolate Cake (with Frosting)', 'ingredient', 'Chocolate cake with chocolate frosting',
    100, 'g', 'slice (95g)', 95,
    371, 4.7, 52.1, 16.4,
    1.9, 37.4, 5.6, 55,
    299, 152, 47, 2.35,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Vanilla Cake (with Frosting)', 'ingredient', 'Vanilla cake with vanilla frosting',
    100, 'g', 'slice (95g)', 95,
    378, 3.8, 54.5, 16.8,
    0.8, 40.5, 6.8, 58,
    318, 83, 45, 1.52,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Red Velvet Cake', 'ingredient', 'Red velvet cake with cream cheese frosting',
    100, 'g', 'slice (100g)', 100,
    390, 4.5, 53, 18,
    1.5, 38, 7, 60,
    340, 120, 50, 1.8,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Carrot Cake (with Cream Cheese Frosting)', 'ingredient', 'Carrot cake with cream cheese frosting',
    100, 'g', 'slice (111g)', 111,
    408, 4.6, 48.5, 22.7,
    1.8, 35.2, 4.3, 46,
    299, 182, 39, 1.36,
    ARRAY['dairy', 'eggs', 'gluten', 'nuts'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Cheesecake (Plain)', 'ingredient', 'New York style cheesecake',
    100, 'g', 'slice (125g)', 125,
    321, 5.5, 25.5, 22.5,
    0.9, 19.8, 12.5, 103,
    332, 98, 63, 0.36,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Cheesecake (Strawberry)', 'ingredient', 'Cheesecake with strawberry topping',
    100, 'g', 'slice (125g)', 125,
    300, 5, 28, 18,
    1, 22, 10, 95,
    310, 110, 65, 0.4,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Pound Cake', 'ingredient', 'Classic butter pound cake',
    100, 'g', 'slice (80g)', 80,
    389, 5.6, 55.6, 16.7,
    1.1, 33.3, 8.9, 133,
    289, 78, 56, 1.78,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Angel Food Cake', 'ingredient', 'Light angel food cake',
    100, 'g', 'slice (50g)', 50,
    258, 5.9, 58.3, 0.2,
    0.5, 42.7, 0, 0,
    643, 68, 42, 0.34,
    ARRAY['eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('German Chocolate Cake', 'ingredient', 'German chocolate cake with coconut pecan frosting',
    100, 'g', 'slice (100g)', 100,
    420, 5, 55, 21,
    2, 40, 9, 65,
    320, 150, 55, 2,
    ARRAY['dairy', 'eggs', 'gluten', 'nuts'], ARRAY['vegetarian'], 'user', 0.91, false),

('Lemon Cake', 'ingredient', 'Lemon cake with lemon frosting',
    100, 'g', 'slice (95g)', 95,
    370, 4, 52, 17,
    0.8, 38, 6.5, 55,
    310, 95, 45, 1.5,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

-- ============================================================================
-- PIES
-- ============================================================================

('Apple Pie', 'ingredient', 'Traditional apple pie',
    100, 'g', 'slice (125g)', 125,
    237, 2, 34.3, 11,
    1.6, 16, 4.4, 0,
    266, 71, 11, 0.8,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Pumpkin Pie', 'ingredient', 'Pumpkin pie with crust',
    100, 'g', 'slice (109g)', 109,
    243, 4.4, 31.9, 10.8,
    2.5, 18.4, 3.7, 46,
    288, 173, 65, 1.02,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Pecan Pie', 'ingredient', 'Pecan pie',
    100, 'g', 'slice (113g)', 113,
    466, 5.2, 59.5, 23.6,
    2.4, 31.9, 4.1, 55,
    308, 95, 30, 1.41,
    ARRAY['dairy', 'eggs', 'gluten', 'nuts'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Cherry Pie', 'ingredient', 'Cherry pie',
    100, 'g', 'slice (125g)', 125,
    260, 2.4, 40, 11.2,
    0.8, 18.4, 2.8, 0,
    288, 80, 16, 0.8,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Blueberry Pie', 'ingredient', 'Blueberry pie',
    100, 'g', 'slice (125g)', 125,
    243, 2, 36.5, 10.5,
    1.4, 17.2, 2.6, 0,
    272, 56, 10, 0.7,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Lemon Meringue Pie', 'ingredient', 'Lemon meringue pie',
    100, 'g', 'slice (127g)', 127,
    268, 1.8, 47.2, 8.7,
    1, 29.9, 2.2, 51,
    165, 50, 15, 0.5,
    ARRAY['eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Key Lime Pie', 'ingredient', 'Key lime pie',
    100, 'g', 'slice (100g)', 100,
    330, 4, 42, 17,
    0.8, 32, 8, 80,
    220, 85, 70, 0.6,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Chocolate Cream Pie', 'ingredient', 'Chocolate cream pie',
    100, 'g', 'slice (113g)', 113,
    301, 2.7, 38.1, 15.9,
    1.8, 22.1, 6.2, 6,
    135, 144, 50, 1.08,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Banana Cream Pie', 'ingredient', 'Banana cream pie',
    100, 'g', 'slice (100g)', 100,
    290, 3.5, 38, 14,
    1, 22, 6, 30,
    200, 180, 55, 0.7,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

-- ============================================================================
-- DONUTS & PASTRIES
-- ============================================================================

('Glazed Donut', 'ingredient', 'Classic glazed donut',
    100, 'g', 'donut (60g)', 60,
    452, 4.8, 51.6, 25.8,
    1.6, 27.4, 6.5, 19,
    379, 58, 37, 1.61,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Chocolate Frosted Donut', 'ingredient', 'Donut with chocolate frosting',
    100, 'g', 'donut (65g)', 65,
    460, 5, 54, 25,
    2, 30, 7, 20,
    390, 75, 40, 2,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.93, false),

('Boston Cream Donut', 'ingredient', 'Boston cream filled donut',
    100, 'g', 'donut (85g)', 85,
    400, 4.7, 49.4, 21.2,
    1.2, 28.2, 9.4, 24,
    341, 82, 41, 1.29,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Jelly Donut', 'ingredient', 'Jelly filled donut',
    100, 'g', 'donut (85g)', 85,
    380, 4.5, 51, 18,
    1.5, 26, 5, 18,
    360, 65, 35, 1.4,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Old Fashioned Donut', 'ingredient', 'Old fashioned cake donut',
    100, 'g', 'donut (55g)', 55,
    420, 4.5, 49.1, 23.6,
    1.8, 23.6, 7.3, 25,
    364, 55, 36, 1.82,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Donut Holes (Glazed)', 'ingredient', 'Glazed donut holes',
    100, 'g', '4 holes (52g)', 52,
    450, 5, 52, 24,
    1.5, 28, 6.5, 20,
    380, 60, 38, 1.6,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Croissant (Plain)', 'ingredient', 'Butter croissant',
    100, 'g', 'croissant (67g)', 67,
    406, 8.2, 45.8, 21,
    2.6, 9.7, 11.3, 67,
    477, 125, 37, 2.24,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.95, true),

('Chocolate Croissant', 'ingredient', 'Chocolate filled croissant',
    100, 'g', 'croissant (80g)', 80,
    430, 7.5, 50, 22,
    3, 16, 12, 60,
    460, 150, 45, 2.5,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Danish (Cheese)', 'ingredient', 'Cheese danish pastry',
    100, 'g', 'danish (91g)', 91,
    371, 6.4, 43.5, 19.4,
    1.3, 17.7, 9.7, 52,
    319, 82, 60, 1.54,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Danish (Fruit)', 'ingredient', 'Fruit danish pastry',
    100, 'g', 'danish (94g)', 94,
    335, 4.8, 45.1, 15.9,
    1.6, 20.6, 4.8, 19,
    320, 70, 33, 1.28,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Cinnamon Roll (with Icing)', 'ingredient', 'Cinnamon roll with icing',
    100, 'g', 'roll (85g)', 85,
    365, 5.9, 51.8, 15.3,
    1.8, 27.1, 5.9, 35,
    329, 94, 48, 1.88,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Eclair (Chocolate)', 'ingredient', 'Chocolate eclair with cream filling',
    100, 'g', 'eclair (100g)', 100,
    295, 6.2, 35.9, 14.5,
    1.4, 19.3, 6.9, 127,
    337, 117, 77, 1.24,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

-- ============================================================================
-- CUPCAKES
-- ============================================================================

('Vanilla Cupcake (with Frosting)', 'ingredient', 'Vanilla cupcake with vanilla frosting',
    100, 'g', 'cupcake (50g)', 50,
    380, 4, 54, 17,
    0.8, 40, 7, 58,
    320, 85, 46, 1.5,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Chocolate Cupcake (with Frosting)', 'ingredient', 'Chocolate cupcake with chocolate frosting',
    100, 'g', 'cupcake (50g)', 50,
    370, 4.5, 52, 16.5,
    2, 37, 5.5, 55,
    300, 155, 48, 2.3,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Red Velvet Cupcake', 'ingredient', 'Red velvet cupcake with cream cheese frosting',
    100, 'g', 'cupcake (55g)', 55,
    390, 4.5, 53, 18,
    1.5, 38, 7, 60,
    340, 120, 50, 1.8,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

-- ============================================================================
-- ICE CREAM & FROZEN DESSERTS (Additional Flavors)
-- ============================================================================

('Chocolate Mint Ice Cream', 'ingredient', 'Mint chocolate chip ice cream',
    100, 'g', 'cup (66g)', 66,
    216, 3.8, 26.3, 11,
    1.2, 23.8, 6.5, 34,
    76, 249, 109, 0.6,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Cookies and Cream Ice Cream', 'ingredient', 'Cookies and cream ice cream',
    100, 'g', 'cup (66g)', 66,
    228, 3.5, 28.1, 11.4,
    0.9, 23.7, 6.7, 36,
    116, 186, 116, 0.7,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'usda', 0.94, true),

('Strawberry Ice Cream', 'ingredient', 'Strawberry ice cream',
    100, 'g', 'cup (66g)', 66,
    192, 3.2, 27.6, 8,
    0.9, 25.4, 4.5, 29,
    80, 199, 120, 0.14,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Cookie Dough Ice Cream', 'ingredient', 'Chocolate chip cookie dough ice cream',
    100, 'g', 'cup (66g)', 66,
    250, 4, 32, 12,
    1, 26, 7, 40,
    90, 200, 120, 0.8,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.91, false),

('Rocky Road Ice Cream', 'ingredient', 'Rocky road ice cream with nuts and marshmallows',
    100, 'g', 'cup (66g)', 66,
    240, 4.5, 31.8, 11.4,
    1.8, 27.3, 5.5, 32,
    80, 227, 123, 1,
    ARRAY['dairy', 'eggs', 'nuts'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Butter Pecan Ice Cream', 'ingredient', 'Butter pecan ice cream',
    100, 'g', 'cup (66g)', 66,
    240, 3.6, 23.6, 15.5,
    0.9, 20, 7.3, 38,
    136, 182, 109, 0.36,
    ARRAY['dairy', 'eggs', 'nuts'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Neapolitan Ice Cream', 'ingredient', 'Neapolitan ice cream (chocolate, vanilla, strawberry)',
    100, 'g', 'cup (66g)', 66,
    201, 3.5, 25.3, 10,
    0.8, 22.8, 5.9, 33,
    78, 203, 116, 0.5,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Coffee Ice Cream', 'ingredient', 'Coffee flavored ice cream',
    100, 'g', 'cup (66g)', 66,
    216, 3.8, 28.2, 11,
    0.7, 25.4, 6.5, 34,
    76, 249, 109, 0.93,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Sherbet (Orange)', 'ingredient', 'Orange sherbet',
    100, 'g', 'cup (74g)', 74,
    147, 1.1, 30.4, 2,
    2, 22.5, 1.2, 5,
    38, 99, 52, 0.15,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Sorbet (Fruit)', 'ingredient', 'Fruit sorbet, dairy-free',
    100, 'g', 'cup (74g)', 74,
    130, 0.5, 34.1, 0,
    1, 28.7, 0, 0,
    5, 53, 5, 0.27,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Gelato (Vanilla)', 'ingredient', 'Italian vanilla gelato',
    100, 'g', 'cup (88g)', 88,
    200, 4, 25, 10,
    0.5, 22, 6, 35,
    70, 180, 120, 0.2,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Fudgsicle', 'ingredient', 'Chocolate fudge ice pop',
    100, 'g', 'pop (65g)', 65,
    108, 3.1, 21.5, 1.5,
    3.1, 15.4, 0.8, 3,
    92, 277, 92, 0.46,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Creamsicle', 'ingredient', 'Orange cream ice pop',
    100, 'g', 'pop (63g)', 63,
    127, 1.6, 22.2, 3.2,
    0, 17.5, 1.6, 6,
    38, 63, 32, 0,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- PUDDINGS & OTHER DESSERTS
-- ============================================================================

('Vanilla Pudding', 'ingredient', 'Vanilla pudding cup',
    100, 'g', 'cup (113g)', 113,
    111, 2.7, 19.5, 2.7,
    0, 16.8, 1.8, 9,
    159, 133, 106, 0.09,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Tapioca Pudding', 'ingredient', 'Tapioca pudding',
    100, 'g', 'cup (113g)', 113,
    114, 2.7, 19.5, 2.7,
    0.9, 16.8, 1.8, 9,
    150, 124, 97, 0.18,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Rice Pudding', 'ingredient', 'Rice pudding with raisins',
    100, 'g', 'cup (113g)', 113,
    116, 2.7, 20.4, 2.7,
    0.9, 13.3, 1.8, 9,
    82, 115, 88, 0.35,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Jello (Regular)', 'ingredient', 'Fruit flavored gelatin dessert',
    100, 'g', 'cup (99g)', 99,
    62, 1.6, 14.2, 0,
    0, 14.2, 0, 0,
    57, 1, 2, 0,
    NULL, ARRAY['vegetarian'], 'usda', 0.94, true),

('Jello (Sugar-Free)', 'ingredient', 'Sugar-free gelatin dessert',
    100, 'g', 'cup (99g)', 99,
    8, 1.6, 0, 0,
    0, 0, 0, 0,
    57, 1, 2, 0,
    NULL, ARRAY['vegetarian', 'keto'], 'usda', 0.94, true),

('Flan', 'ingredient', 'Caramel custard flan',
    100, 'g', 'slice (90g)', 90,
    140, 4.4, 22.2, 4.4,
    0, 20, 2.2, 80,
    70, 124, 88, 0.4,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Creme Brulee', 'ingredient', 'French vanilla custard with caramelized sugar',
    100, 'g', 'serving (100g)', 100,
    260, 4, 22, 18,
    0, 20, 11, 240,
    60, 100, 80, 0.4,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false),

('Chocolate Mousse', 'ingredient', 'Chocolate mousse',
    100, 'g', 'cup (85g)', 85,
    203, 2.4, 22.4, 12.2,
    1.2, 18.3, 7.3, 88,
    73, 122, 49, 0.73,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Cobbler (Peach)', 'ingredient', 'Peach cobbler',
    100, 'g', 'serving (139g)', 139,
    210, 2.2, 34.5, 7.9,
    1.4, 19.4, 1.4, 0,
    252, 144, 20, 0.86,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.93, true),

('Cobbler (Berry)', 'ingredient', 'Mixed berry cobbler',
    100, 'g', 'serving (139g)', 139,
    215, 2.3, 35.4, 8.1,
    2.3, 18.5, 1.5, 0,
    260, 154, 22, 0.92,
    ARRAY['gluten'], ARRAY['vegetarian'], 'usda', 0.93, true);

COMMIT;

SELECT
    '✅ EXTENDED DESSERTS SEEDED!' as status,
    COUNT(*) as total_items,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Chocolate Cake (with Frosting)', 'Vanilla Cake (with Frosting)', 'Red Velvet Cake', 'Cheesecake (Plain)',
    'Apple Pie', 'Pumpkin Pie', 'Pecan Pie', 'Cherry Pie',
    'Glazed Donut', 'Chocolate Frosted Donut', 'Boston Cream Donut',
    'Vanilla Cupcake (with Frosting)', 'Chocolate Cupcake (with Frosting)',
    'Chocolate Mint Ice Cream', 'Cookies and Cream Ice Cream', 'Cookie Dough Ice Cream'
);
