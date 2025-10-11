-- ============================================================================
-- MIGRATION 019: SEED BRANDED FROZEN FOODS
-- ============================================================================
-- Description: Popular branded frozen meals, pizzas, ice cream, snacks
-- Total items: ~70 items
-- Brands: Stouffers, Lean Cuisine, DiGiorno, Breyers, Haagen-Dazs, Hot Pockets
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

-- STOUFFER'S FROZEN MEALS
('Stouffers Macaroni and Cheese', 'meal', 'Stouffers classic mac and cheese frozen meal',
    100, 'g', 'tray (340g)', 340,
    118, 5, 13.8, 4.7,
    0.9, 1.5, 2.4, 15,
    324, 103, 88, 0.44,
    ARRAY['dairy', 'gluten', 'eggs'], ARRAY['vegetarian'], 'user', 0.94, false),

('Stouffers Lasagna with Meat Sauce', 'meal', 'Stouffers classic lasagna with meat',
    100, 'g', 'tray (283g)', 283,
    127, 6.7, 13.1, 4.6,
    1.4, 3.9, 2.1, 18,
    367, 181, 81, 0.85,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.93, false),

('Stouffers Baked Chicken Breast', 'meal', 'Stouffers baked chicken with gravy and sides',
    100, 'g', 'tray (251g)', 251,
    116, 7.2, 11.6, 4,
    2, 2.4, 1.6, 24,
    348, 164, 32, 0.8,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.92, false),

('Stouffers Meatloaf', 'meal', 'Stouffers homestyle meatloaf with mashed potatoes',
    100, 'g', 'tray (396g)', 396,
    101, 5.6, 9.1, 4.5,
    1.5, 2.5, 2, 20,
    333, 156, 28, 0.91,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.92, false),

('Stouffers Chicken Fettuccini Alfredo', 'meal', 'Stouffers chicken fettuccini alfredo',
    100, 'g', 'tray (283g)', 283,
    141, 7.1, 14.1, 5.3,
    1.4, 1.8, 2.8, 28,
    388, 141, 88, 0.71,
    ARRAY['dairy', 'gluten', 'eggs'], NULL, 'user', 0.92, false),

-- LEAN CUISINE
('Lean Cuisine Chicken with Basil Cream Sauce', 'meal', 'Lean Cuisine chicken pasta with basil',
    100, 'g', 'tray (255g)', 255,
    106, 6.7, 13.7, 2.4,
    2, 2.7, 0.8, 16,
    298, 157, 43, 0.67,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.93, false),

('Lean Cuisine Vermont White Cheddar Mac and Cheese', 'meal', 'Lean Cuisine mac and cheese',
    100, 'g', 'tray (283g)', 283,
    102, 4.6, 15.9, 2.1,
    1.8, 2.1, 1.1, 11,
    282, 113, 88, 0.53,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.93, false),

('Lean Cuisine Glazed Chicken', 'meal', 'Lean Cuisine glazed chicken with rice and veggies',
    100, 'g', 'tray (255g)', 255,
    102, 7.5, 16.5, 0.8,
    1.6, 6.3, 0.2, 18,
    290, 157, 24, 0.71,
    NULL, NULL, 'user', 0.92, false),

('Lean Cuisine Beef and Broccoli', 'meal', 'Lean Cuisine beef and broccoli',
    100, 'g', 'tray (255g)', 255,
    94, 7.1, 12.9, 1.6,
    2, 4.7, 0.4, 16,
    306, 196, 31, 0.94,
    ARRAY['soy', 'gluten'], NULL, 'user', 0.92, false),

('Lean Cuisine Chicken Teriyaki', 'meal', 'Lean Cuisine chicken teriyaki stir fry',
    100, 'g', 'tray (283g)', 283,
    95, 6.4, 15.5, 0.7,
    2.1, 6.4, 0.2, 14,
    291, 155, 28, 0.71,
    ARRAY['soy', 'gluten'], NULL, 'user', 0.92, false),

-- HEALTHY CHOICE
('Healthy Choice Chicken Fettuccini Alfredo', 'meal', 'Healthy Choice chicken alfredo',
    100, 'g', 'tray (248g)', 248,
    105, 6.5, 14.1, 2.4,
    2, 2.4, 0.8, 16,
    286, 145, 65, 0.65,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.92, false),

('Healthy Choice Cafe Steamers Grilled Chicken Pesto', 'meal', 'Healthy Choice pesto chicken',
    100, 'g', 'tray (283g)', 283,
    106, 7.1, 12.4, 2.8,
    2.5, 2.5, 0.7, 18,
    298, 159, 53, 0.88,
    ARRAY['dairy', 'gluten', 'nuts'], NULL, 'user', 0.91, false),

-- DIGIORNO PIZZA
('DiGiorno Rising Crust Four Cheese Pizza', 'meal', 'DiGiorno frozen four cheese pizza',
    100, 'g', 'pizza (269g)', 269,
    248, 11.5, 31.2, 8.9,
    2.2, 5.6, 4.1, 19,
    633, 152, 215, 1.67,
    ARRAY['dairy', 'gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.93, false),

('DiGiorno Rising Crust Pepperoni Pizza', 'meal', 'DiGiorno frozen pepperoni pizza',
    100, 'g', 'pizza (282g)', 282,
    266, 11.7, 31.2, 10.3,
    2.1, 5.3, 4.6, 21,
    723, 163, 199, 1.77,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.93, false),

('DiGiorno Rising Crust Supreme Pizza', 'meal', 'DiGiorno frozen supreme pizza',
    100, 'g', 'pizza (318g)', 318,
    245, 10.7, 29.6, 9.1,
    2.2, 5.3, 3.8, 18,
    654, 189, 189, 1.73,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.92, false),

('DiGiorno Stuffed Crust Five Cheese Pizza', 'meal', 'DiGiorno stuffed crust cheese pizza',
    100, 'g', 'pizza (289g)', 289,
    256, 12.1, 30.6, 9.7,
    2.1, 5.5, 4.8, 23,
    679, 152, 241, 1.66,
    ARRAY['dairy', 'gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.93, false),

-- RED BARON PIZZA
('Red Baron Classic Crust Pepperoni Pizza', 'meal', 'Red Baron frozen pepperoni pizza',
    100, 'g', 'pizza (311g)', 311,
    289, 12.5, 31.7, 12.2,
    2.6, 5.8, 5.4, 25,
    725, 160, 193, 1.93,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.93, false),

('Red Baron Brick Oven Crust Four Cheese Pizza', 'meal', 'Red Baron four cheese pizza',
    100, 'g', 'pizza (296g)', 296,
    270, 12.8, 32.4, 9.5,
    2.4, 6.1, 4.7, 23,
    676, 155, 209, 1.86,
    ARRAY['dairy', 'gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.93, false),

-- HOT POCKETS
('Hot Pockets Ham and Cheese', 'meal', 'Hot Pockets ham and cheese sandwich',
    100, 'g', 'pocket (127g)', 127,
    228, 7.9, 28.3, 8.7,
    1.6, 3.9, 3.9, 24,
    630, 126, 142, 1.57,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.93, false),

('Hot Pockets Pepperoni Pizza', 'meal', 'Hot Pockets pepperoni pizza sandwich',
    100, 'g', 'pocket (127g)', 127,
    236, 9.4, 30.7, 8.7,
    1.6, 5.5, 3.9, 20,
    630, 157, 150, 1.89,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.93, false),

('Hot Pockets Philly Steak and Cheese', 'meal', 'Hot Pockets Philly steak sandwich',
    100, 'g', 'pocket (127g)', 127,
    228, 7.9, 28.3, 8.7,
    1.6, 3.9, 3.9, 24,
    630, 157, 142, 1.89,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.92, false),

-- BAGEL BITES
('Bagel Bites Cheese and Pepperoni', 'meal', 'Bagel Bites mini pizza bagels',
    100, 'g', '4 pieces (88g)', 88,
    261, 10.2, 36.4, 8,
    2.3, 4.5, 3.4, 14,
    557, 136, 159, 1.7,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.93, false),

-- TOTINOS PIZZA ROLLS
('Totinos Pizza Rolls (Pepperoni)', 'meal', 'Totinos pepperoni pizza rolls',
    100, 'g', '6 rolls (85g)', 85,
    282, 8.2, 38.8, 10.6,
    2.4, 3.5, 3.5, 12,
    541, 129, 94, 1.76,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.93, false),

('Totinos Pizza Rolls (Combination)', 'meal', 'Totinos combination pizza rolls',
    100, 'g', '6 rolls (85g)', 85,
    282, 8.2, 38.8, 10.6,
    2.4, 3.5, 3.5, 12,
    541, 129, 94, 1.76,
    ARRAY['dairy', 'gluten', 'soy'], NULL, 'user', 0.93, false),

-- CHICKEN NUGGETS & TENDERS
('Tyson Chicken Nuggets', 'ingredient', 'Tyson frozen breaded chicken nuggets',
    100, 'g', '5 pieces (84g)', 84,
    286, 13.1, 17.9, 17.9,
    1.2, 0, 3.6, 36,
    548, 179, 24, 1.19,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.94, false),

('Tyson Chicken Tenders', 'ingredient', 'Tyson frozen breaded chicken tenders',
    100, 'g', '3 pieces (84g)', 84,
    274, 14.3, 17.9, 15.5,
    1.2, 0, 2.4, 36,
    524, 190, 24, 1.19,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.94, false),

('Perdue Simply Smart Chicken Breast Nuggets', 'ingredient', 'Perdue breaded chicken breast nuggets',
    100, 'g', '5 pieces (84g)', 84,
    250, 16.7, 16.7, 13.1,
    1.2, 0, 2.4, 40,
    476, 214, 24, 1.43,
    ARRAY['gluten'], NULL, 'user', 0.93, false),

-- FISH STICKS & FILLETS
('Gortons Fish Sticks', 'ingredient', 'Gortons breaded fish sticks',
    100, 'g', '6 sticks (114g)', 114,
    202, 10.5, 20.2, 8.8,
    0.9, 1.8, 1.8, 26,
    351, 175, 18, 0.88,
    ARRAY['gluten', 'fish'], NULL, 'user', 0.93, false),

('Gortons Beer Battered Fish Fillets', 'ingredient', 'Gortons beer battered fish fillets',
    100, 'g', 'fillet (99g)', 99,
    232, 11.1, 18.2, 12.1,
    1, 1, 2, 30,
    505, 192, 20, 1.01,
    ARRAY['gluten', 'fish'], NULL, 'user', 0.93, false),

('Mrs. Pauls Fish Sticks', 'ingredient', 'Mrs. Pauls breaded fish sticks',
    100, 'g', '6 sticks (114g)', 114,
    193, 9.6, 19.3, 8.8,
    0.9, 1.8, 1.8, 24,
    368, 167, 18, 0.88,
    ARRAY['gluten', 'fish'], NULL, 'user', 0.93, false),

-- FROZEN BREAKFAST
('Eggo Homestyle Waffles', 'ingredient', 'Eggo frozen waffles',
    100, 'g', '2 waffles (70g)', 70,
    286, 7.1, 50, 7.1,
    1.4, 5.7, 1.4, 29,
    643, 143, 214, 3.57,
    ARRAY['dairy', 'eggs', 'gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.94, false),

('Eggo Buttermilk Pancakes', 'ingredient', 'Eggo frozen buttermilk pancakes',
    100, 'g', '3 pancakes (104g)', 104,
    240, 4.8, 44.2, 4.8,
    1, 9.6, 1, 19,
    577, 115, 96, 2.88,
    ARRAY['dairy', 'eggs', 'gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.93, false),

('Jimmy Dean Sausage, Egg and Cheese Biscuit', 'meal', 'Jimmy Dean frozen breakfast sandwich',
    100, 'g', 'sandwich (142g)', 142,
    296, 11.3, 21.8, 17.6,
    0.7, 2.1, 7, 113,
    775, 169, 141, 1.55,
    ARRAY['dairy', 'eggs', 'gluten', 'soy'], NULL, 'user', 0.92, false),

('Jimmy Dean Delights Turkey Sausage, Egg White and Cheese Muffin', 'meal', 'Jimmy Dean Delights breakfast sandwich',
    100, 'g', 'sandwich (127g)', 127,
    197, 15, 19.7, 5.5,
    3.1, 1.6, 2.4, 55,
    551, 213, 197, 1.57,
    ARRAY['dairy', 'eggs', 'gluten', 'soy'], NULL, 'user', 0.93, false),

-- ICE CREAM (Breyers, Haagen-Dazs, Ben & Jerry's)
('Breyers Natural Vanilla Ice Cream', 'ingredient', 'Breyers natural vanilla ice cream',
    100, 'g', 'cup (66g)', 66,
    197, 3, 22.7, 10.6,
    0, 21.2, 6.1, 30,
    61, 167, 106, 0.15,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Breyers Natural Chocolate Ice Cream', 'ingredient', 'Breyers natural chocolate ice cream',
    100, 'g', 'cup (66g)', 66,
    197, 3, 24.2, 10.6,
    1.5, 21.2, 6.1, 30,
    76, 182, 106, 0.76,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Haagen-Dazs Vanilla Ice Cream', 'ingredient', 'Haagen-Dazs vanilla ice cream',
    100, 'g', 'cup (106g)', 106,
    270, 4.7, 23.3, 17.4,
    0, 20.9, 10.5, 116,
    70, 209, 140, 0.47,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Haagen-Dazs Chocolate Ice Cream', 'ingredient', 'Haagen-Dazs chocolate ice cream',
    100, 'g', 'cup (106g)', 106,
    264, 4.7, 24.5, 16.0,
    2.8, 21.7, 9.4, 94,
    66, 302, 132, 0.94,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Haagen-Dazs Coffee Ice Cream', 'ingredient', 'Haagen-Dazs coffee ice cream',
    100, 'g', 'cup (106g)', 106,
    258, 4.7, 21.7, 17.0,
    0, 20.8, 10.4, 113,
    75, 236, 142, 0.47,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Haagen-Dazs Caramel Cone Ice Cream', 'ingredient', 'Haagen-Dazs caramel cone ice cream',
    100, 'g', 'cup (82g)', 82,
    304, 4.9, 32.9, 16.5,
    1.2, 26.8, 9.8, 85,
    134, 220, 110, 0.73,
    ARRAY['dairy', 'eggs', 'gluten', 'nuts'], ARRAY['vegetarian'], 'user', 0.94, false),

('Ben and Jerrys Half Baked Ice Cream', 'ingredient', 'Ben & Jerrys Half Baked ice cream',
    100, 'g', 'cup (106g)', 106,
    283, 4.7, 34.9, 14.2,
    0.9, 28.3, 8.5, 47,
    94, 236, 113, 1.42,
    ARRAY['dairy', 'eggs', 'gluten', 'soy'], ARRAY['vegetarian'], 'user', 0.93, false),

('Ben and Jerrys Cherry Garcia Ice Cream', 'ingredient', 'Ben & Jerrys Cherry Garcia ice cream',
    100, 'g', 'cup (106g)', 106,
    245, 3.8, 28.3, 12.3,
    0.9, 23.6, 7.5, 57,
    57, 217, 113, 0.57,
    ARRAY['dairy', 'eggs'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Ben and Jerrys Chunky Monkey Ice Cream', 'ingredient', 'Ben & Jerrys Chunky Monkey ice cream',
    100, 'g', 'cup (106g)', 106,
    283, 4.7, 31.1, 15.1,
    0.9, 25.5, 8.5, 47,
    57, 264, 113, 0.94,
    ARRAY['dairy', 'eggs', 'nuts'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Ben and Jerrys Phish Food Ice Cream', 'ingredient', 'Ben & Jerrys Phish Food ice cream',
    100, 'g', 'cup (106g)', 106,
    283, 4.7, 35.8, 13.2,
    0.9, 30.2, 7.5, 38,
    85, 264, 113, 1.42,
    ARRAY['dairy', 'eggs', 'gluten', 'fish'], ARRAY['vegetarian'], 'user', 0.92, false),

-- POPSICLES & FROZEN TREATS
('Outshine Strawberry Fruit Bars', 'ingredient', 'Outshine real fruit strawberry bars',
    100, 'g', 'bar (77g)', 77,
    52, 0, 14.3, 0,
    1.3, 10.4, 0, 0,
    13, 52, 13, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Klondike Original Vanilla Ice Cream Bar', 'ingredient', 'Klondike vanilla ice cream bar',
    100, 'g', 'bar (133g)', 133,
    301, 3, 30.8, 18,
    0.8, 24.1, 12.8, 15,
    68, 150, 90, 0.6,
    ARRAY['dairy', 'soy'], ARRAY['vegetarian'], 'user', 0.93, false),

('Fudgsicle Original Fudge Pops', 'ingredient', 'Fudgsicle original fudge ice pops',
    100, 'g', 'pop (65g)', 65,
    92, 3.1, 18.5, 1.5,
    3.1, 13.8, 0.8, 3,
    123, 231, 92, 0.92,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

-- FROZEN VEGETABLES (with sauce)
('Birds Eye Steamfresh Broccoli and Cheese Sauce', 'ingredient', 'Birds Eye broccoli with cheese sauce',
    100, 'g', 'cup (142g)', 142,
    56, 2.1, 6.3, 2.1,
    2.1, 2.1, 1.1, 5,
    282, 211, 63, 0.42,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Green Giant Steamers Broccoli and Cheese Sauce', 'ingredient', 'Green Giant broccoli with cheese sauce',
    100, 'g', 'cup (142g)', 142,
    56, 2.1, 6.3, 2.1,
    2.1, 2.1, 1.1, 5,
    296, 211, 63, 0.42,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

-- FROZEN POTATOES
('Ore-Ida Golden Crinkles French Fries', 'ingredient', 'Ore-Ida frozen crinkle cut fries',
    100, 'g', '3oz (84g)', 84,
    143, 2.4, 23.8, 4.8,
    2.4, 0, 0.6, 0,
    238, 381, 12, 0.71,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Ore-Ida Tater Tots', 'ingredient', 'Ore-Ida frozen tater tots',
    100, 'g', '9 pieces (84g)', 84,
    179, 2.4, 23.8, 8.3,
    2.4, 0, 1.2, 0,
    476, 357, 12, 0.71,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Ore-Ida Extra Crispy Fast Food Fries', 'ingredient', 'Ore-Ida extra crispy fries',
    100, 'g', '3oz (84g)', 84,
    179, 2.4, 25, 8.3,
    2.4, 0, 1.2, 0,
    262, 381, 12, 0.71,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

-- APPETIZERS
('TGI Fridays Mozzarella Sticks', 'ingredient', 'TGI Fridays frozen mozzarella sticks',
    100, 'g', '3 sticks (84g)', 84,
    298, 13.1, 27.4, 14.3,
    1.2, 2.4, 6, 36,
    690, 143, 310, 1.19,
    ARRAY['dairy', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('TGI Fridays Loaded Potato Skins', 'ingredient', 'TGI Fridays frozen loaded potato skins',
    100, 'g', '3 pieces (85g)', 85,
    247, 8.2, 21.2, 14.1,
    1.2, 1.2, 5.9, 24,
    565, 306, 118, 0.71,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('TGI Fridays Boneless Chicken Bites', 'ingredient', 'TGI Fridays frozen boneless wings',
    100, 'g', '4 pieces (84g)', 84,
    238, 13.1, 17.9, 13.1,
    1.2, 2.4, 2.4, 36,
    595, 179, 24, 1.19,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.91, false),

-- VEGGIE BURGERS & PLANT-BASED
('MorningStar Farms Grillers Original Veggie Burger', 'ingredient', 'MorningStar veggie burger patty',
    100, 'g', 'patty (71g)', 71,
    176, 21.1, 9.9, 7,
    4.2, 1.4, 1.4, 0,
    634, 352, 70, 2.82,
    ARRAY['soy', 'gluten', 'eggs'], ARRAY['vegetarian'], 'user', 0.93, false),

('Beyond Burger Frozen Patties', 'ingredient', 'Beyond Meat plant-based burger patties',
    100, 'g', 'patty (113g)', 113,
    221, 17.7, 5.3, 15,
    2.7, 0, 5.3, 0,
    354, 442, 27, 3.54,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Impossible Burger Frozen Patties', 'ingredient', 'Impossible Foods plant-based burger patties',
    100, 'g', 'patty (113g)', 113,
    212, 17.7, 8, 12.4,
    2.7, 0, 7.1, 0,
    327, 389, 62, 3.54,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false);

COMMIT;

SELECT '✅ BRANDED FROZEN FOODS SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Stouffers Macaroni and Cheese', 'DiGiorno Rising Crust Pepperoni Pizza', 'Hot Pockets Pepperoni Pizza', 'Haagen-Dazs Vanilla Ice Cream');
