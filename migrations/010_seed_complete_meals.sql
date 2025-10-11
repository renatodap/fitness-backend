-- ============================================================================
-- MIGRATION 010: SEED COMPLETE MEALS & COMBOS
-- ============================================================================
-- Description: Complete meal combinations, bowls, platters, and meal kits
-- Categories: Breakfast combos, lunch bowls, dinner plates, meal prep favorites
-- Total items: ~60 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (full meal portion)
-- - Household serving typically = entire meal
-- - For multi-component meals, nutrition includes all parts
-- - Nutrition calculated: multiplier = gram_quantity / serving_size
-- ============================================================================

BEGIN;

-- ============================================================================
-- COMPLETE MEALS & COMBOS
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
-- BREAKFAST COMBOS
-- ============================================================================

('Scrambled Eggs with Toast and Bacon', 'ingredient', 'Two eggs, two strips bacon, one slice toast',
    180, 'g', 'meal (180g)', 180,
    380, 22, 24, 22,
    2, 4, 8, 410,
    920, 320, 80, 2.8,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.91, false),

('Oatmeal with Banana and Almonds', 'ingredient', 'Oatmeal, sliced banana, almonds, honey',
    350, 'g', 'bowl (350g)', 350,
    420, 13.3, 67.7, 12.3,
    9.1, 22.9, 1.4, 0,
    180, 742, 147, 3.1,
    ARRAY['nuts'], ARRAY['vegetarian'], 'user', 0.91, false),

('Protein Pancakes with Berries', 'ingredient', 'Three protein pancakes with mixed berries',
    280, 'g', 'meal (280g)', 280,
    480, 32.1, 58.9, 13.6,
    7.1, 18.6, 3.6, 185,
    680, 457, 179, 2.9,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

('Greek Yogurt Parfait', 'ingredient', 'Greek yogurt, granola, berries, honey',
    300, 'g', 'parfait (300g)', 300,
    380, 22, 54, 10,
    6, 32, 3, 20,
    140, 480, 240, 2.1,
    ARRAY['dairy', 'gluten', 'nuts'], ARRAY['vegetarian'], 'user', 0.92, false),

('Avocado Toast with Egg', 'ingredient', 'Whole wheat toast, avocado, poached egg',
    220, 'g', 'serving (220g)', 220,
    400, 16.4, 36.4, 22.7,
    10.9, 3.6, 5, 185,
    520, 659, 77, 2.9,
    ARRAY['eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.92, false),

('Breakfast Burrito (Egg and Sausage)', 'ingredient', 'Egg, sausage, cheese, peppers in tortilla',
    280, 'g', 'burrito (280g)', 280,
    540, 24.3, 38.6, 30,
    4.3, 3.6, 12.9, 300,
    1100, 386, 257, 3.1,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.91, false),

('Breakfast Hash (Potatoes, Eggs, Peppers)', 'ingredient', 'Potato hash with eggs and vegetables',
    350, 'g', 'serving (350g)', 350,
    420, 18.9, 42.9, 18.9,
    6.3, 5.7, 5.1, 370,
    720, 840, 100, 3.2,
    ARRAY['eggs'], ARRAY['gluten-free'], 'user', 0.90, false),

('Smoothie Bowl (Acai)', 'ingredient', 'Acai smoothie bowl with toppings',
    320, 'g', 'bowl (320g)', 320,
    380, 8.1, 65.6, 11.9,
    12.5, 35.6, 2.5, 0,
    85, 625, 125, 2.2,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

('Bagel with Cream Cheese and Lox', 'ingredient', 'Bagel, cream cheese, smoked salmon',
    180, 'g', 'serving (180g)', 180,
    440, 23.9, 50, 15.6,
    2.8, 6.7, 6.7, 55,
    1120, 322, 89, 3.1,
    ARRAY['dairy', 'eggs', 'fish', 'gluten'], NULL, 'user', 0.91, false),

('French Toast with Syrup', 'ingredient', 'Three slices French toast with maple syrup',
    260, 'g', 'serving (260g)', 260,
    520, 13.8, 78.5, 16.9,
    3.1, 38.5, 5.4, 185,
    560, 231, 154, 2.8,
    ARRAY['dairy', 'eggs', 'gluten'], ARRAY['vegetarian'], 'user', 0.90, false),

-- ============================================================================
-- LUNCH BOWLS & SALADS
-- ============================================================================

('Chicken Caesar Salad', 'ingredient', 'Grilled chicken Caesar salad with croutons',
    340, 'g', 'salad (340g)', 340,
    480, 36.8, 20.6, 30.9,
    4.1, 4.4, 7.9, 100,
    1140, 544, 221, 2.4,
    ARRAY['dairy', 'eggs', 'fish', 'gluten'], NULL, 'user', 0.92, false),

('Cobb Salad', 'ingredient', 'Cobb salad with chicken, bacon, egg, avocado',
    380, 'g', 'salad (380g)', 380,
    540, 40.8, 15.2, 38,
    8.4, 6.8, 11.4, 285,
    1260, 874, 183, 2.9,
    ARRAY['dairy', 'eggs'], ARRAY['gluten-free'], 'user', 0.92, false),

('Chicken Burrito Bowl', 'ingredient', 'Chicken, rice, beans, salsa, cheese',
    450, 'g', 'bowl (450g)', 450,
    620, 38.7, 66.7, 20,
    12.2, 6.7, 7.8, 95,
    1280, 1022, 244, 4.9,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.92, false),

('Steak Burrito Bowl', 'ingredient', 'Steak, rice, beans, guacamole, salsa',
    480, 'g', 'bowl (480g)', 480,
    720, 40, 70, 30,
    13, 8, 11, 105,
    1420, 1104, 250, 5.6,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.91, false),

('Buddha Bowl (Quinoa, Chickpeas, Veggies)', 'ingredient', 'Quinoa bowl with roasted vegetables',
    420, 'g', 'bowl (420g)', 420,
    480, 18.1, 68.6, 16.7,
    14.3, 12.4, 2.4, 0,
    680, 924, 119, 5.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

('Poke Bowl (Tuna)', 'ingredient', 'Tuna poke bowl with rice and vegetables',
    420, 'g', 'bowl (420g)', 420,
    520, 32.4, 64.3, 12.9,
    7.1, 9.5, 2.4, 40,
    1100, 762, 76, 3.3,
    ARRAY['fish', 'soy'], ARRAY['gluten-free'], 'user', 0.91, false),

('Poke Bowl (Salmon)', 'ingredient', 'Salmon poke bowl with rice and edamame',
    440, 'g', 'bowl (440g)', 440,
    580, 34.1, 65.9, 17,
    8.2, 10.2, 3.4, 55,
    1120, 843, 86, 3.6,
    ARRAY['fish', 'soy'], ARRAY['gluten-free'], 'user', 0.91, false),

('Grain Bowl (Farro, Roasted Chicken)', 'ingredient', 'Farro grain bowl with chicken and vegetables',
    400, 'g', 'bowl (400g)', 400,
    520, 32, 56, 18,
    10, 8, 4, 85,
    880, 720, 100, 3.8,
    ARRAY['gluten'], NULL, 'user', 0.90, false),

('Tuna Salad Sandwich', 'ingredient', 'Tuna salad on whole wheat with lettuce',
    240, 'g', 'sandwich (240g)', 240,
    420, 24, 40.8, 17.5,
    6, 6.7, 3.1, 40,
    920, 384, 96, 3.1,
    ARRAY['eggs', 'fish', 'gluten'], NULL, 'user', 0.91, false),

('Chicken Wrap (Grilled)', 'ingredient', 'Grilled chicken wrap with vegetables',
    280, 'g', 'wrap (280g)', 280,
    440, 30.4, 42.9, 15.7,
    5.7, 5, 4.3, 80,
    1020, 514, 114, 2.9,
    ARRAY['gluten'], NULL, 'user', 0.91, false),

-- ============================================================================
-- DINNER PLATES
-- ============================================================================

('Grilled Chicken Breast with Broccoli and Rice', 'ingredient', 'Chicken breast, steamed broccoli, brown rice',
    450, 'g', 'plate (450g)', 450,
    480, 42.7, 54.7, 8,
    7.6, 3.6, 1.8, 95,
    480, 1013, 91, 2.9,
    NULL, ARRAY['gluten-free'], 'user', 0.93, false),

('Grilled Salmon with Asparagus and Quinoa', 'ingredient', 'Grilled salmon, asparagus, quinoa',
    420, 'g', 'plate (420g)', 420,
    560, 38.1, 46.7, 21,
    8.4, 5.5, 4.2, 70,
    420, 1092, 97, 4.4,
    ARRAY['fish'], ARRAY['gluten-free'], 'user', 0.92, false),

('Steak with Sweet Potato and Green Beans', 'ingredient', 'Sirloin steak, roasted sweet potato, green beans',
    480, 'g', 'plate (480g)', 480,
    620, 44.2, 52.1, 24,
    9.1, 14.4, 8.6, 110,
    560, 1296, 115, 5.3,
    NULL, ARRAY['gluten-free', 'paleo'], 'user', 0.92, false),

('Baked Cod with Roasted Vegetables', 'ingredient', 'Baked cod, mixed roasted vegetables',
    400, 'g', 'plate (400g)', 400,
    380, 34, 36, 11,
    8, 14, 2, 75,
    520, 1000, 120, 2.8,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo'], 'user', 0.91, false),

('Turkey Meatloaf with Mashed Potatoes', 'ingredient', 'Turkey meatloaf, mashed potatoes, gravy',
    450, 'g', 'plate (450g)', 450,
    580, 36.7, 58.7, 20,
    5.8, 9, 7.8, 130,
    1180, 1013, 135, 4,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.90, false),

('Pork Chop with Apple and Brussels Sprouts', 'ingredient', 'Pork chop, sautéed apples, roasted Brussels sprouts',
    420, 'g', 'plate (420g)', 420,
    520, 38.1, 38.1, 22.9,
    8.4, 16.7, 7.1, 100,
    640, 1008, 92, 3.1,
    NULL, ARRAY['gluten-free', 'paleo'], 'user', 0.91, false),

('Chicken Stir-Fry with Brown Rice', 'ingredient', 'Chicken and vegetable stir-fry with brown rice',
    450, 'g', 'plate (450g)', 450,
    540, 34.7, 64, 15.6,
    7.6, 11.1, 2.7, 85,
    1060, 778, 98, 3.6,
    ARRAY['soy'], NULL, 'user', 0.91, false),

('Beef Stir-Fry with Noodles', 'ingredient', 'Beef and vegetable stir-fry with noodles',
    450, 'g', 'plate (450g)', 450,
    620, 34.7, 66.7, 22.2,
    6.7, 11.1, 6.7, 90,
    1140, 733, 89, 4.2,
    ARRAY['gluten', 'soy'], NULL, 'user', 0.90, false),

('Shrimp Scampi with Pasta', 'ingredient', 'Shrimp scampi in garlic butter over pasta',
    400, 'g', 'plate (400g)', 400,
    580, 32, 58, 24,
    4, 6, 10, 220,
    1180, 520, 120, 3.2,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.91, false),

('BBQ Ribs with Coleslaw and Cornbread', 'ingredient', 'BBQ pork ribs, coleslaw, cornbread',
    480, 'g', 'plate (480g)', 480,
    840, 38.4, 67.2, 48,
    6.7, 28.8, 17.3, 150,
    1680, 768, 173, 4.3,
    ARRAY['dairy', 'eggs', 'gluten'], NULL, 'user', 0.89, false),

-- ============================================================================
-- MEAL PREP FAVORITES
-- ============================================================================

('Chicken and Broccoli Meal Prep', 'ingredient', 'Grilled chicken, broccoli, brown rice (meal prep portion)',
    400, 'g', 'container (400g)', 400,
    420, 38, 48, 7,
    7, 3, 1.5, 85,
    450, 900, 80, 2.6,
    NULL, ARRAY['gluten-free'], 'user', 0.92, false),

('Turkey and Sweet Potato Meal Prep', 'ingredient', 'Ground turkey, roasted sweet potato, green beans',
    420, 'g', 'container (420g)', 420,
    480, 36.8, 50.4, 12.6,
    9.2, 13.4, 3.4, 90,
    560, 1134, 109, 3.8,
    NULL, ARRAY['gluten-free', 'paleo'], 'user', 0.91, false),

('Beef and Veggie Meal Prep', 'ingredient', 'Lean beef, mixed vegetables, quinoa',
    430, 'g', 'container (430g)', 430,
    540, 38.7, 52.9, 18.1,
    9, 9, 6, 95,
    620, 1032, 107, 5.2,
    NULL, ARRAY['gluten-free'], 'user', 0.91, false),

('Salmon and Asparagus Meal Prep', 'ingredient', 'Baked salmon, roasted asparagus, wild rice',
    400, 'g', 'container (400g)', 400,
    520, 36, 44, 19,
    7, 5, 3.5, 65,
    400, 1040, 92, 4,
    ARRAY['fish'], ARRAY['gluten-free'], 'user', 0.92, false),

('Chicken Fajita Bowl Meal Prep', 'ingredient', 'Chicken fajitas, cauliflower rice, peppers',
    380, 'g', 'container (380g)', 380,
    380, 34.2, 28.5, 15.2,
    7.6, 10.6, 3.8, 85,
    760, 874, 91, 2.7,
    NULL, ARRAY['gluten-free', 'paleo'], 'user', 0.91, false),

('Shrimp and Zucchini Meal Prep', 'ingredient', 'Garlic shrimp, zucchini noodles, tomatoes',
    350, 'g', 'container (350g)', 350,
    320, 30.1, 22.4, 12.6,
    5.6, 9.8, 2.1, 215,
    920, 784, 119, 2.5,
    NULL, ARRAY['gluten-free', 'paleo'], 'user', 0.90, false),

('Tofu and Veggie Meal Prep', 'ingredient', 'Baked tofu, roasted vegetables, brown rice',
    400, 'g', 'container (400g)', 400,
    420, 18, 58, 14,
    9, 10, 2, 0,
    560, 720, 200, 3.6,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

('Chicken Curry Meal Prep', 'ingredient', 'Chicken curry with vegetables and rice',
    420, 'g', 'container (420g)', 420,
    540, 33.6, 58.8, 17.6,
    6.7, 10.1, 6.7, 85,
    980, 882, 126, 3.8,
    ARRAY['dairy'], NULL, 'user', 0.90, false),

('Beef Taco Bowl Meal Prep', 'ingredient', 'Seasoned beef, cauliflower rice, salsa, cheese',
    380, 'g', 'container (380g)', 380,
    480, 32.3, 24.7, 30.4,
    6.8, 6.8, 14.4, 100,
    920, 722, 247, 3.4,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.91, false),

('Greek Chicken Meal Prep', 'ingredient', 'Greek chicken, cucumber salad, quinoa, hummus',
    420, 'g', 'container (420g)', 420,
    520, 36.2, 48.1, 18.6,
    9.5, 8.1, 3.8, 85,
    840, 966, 126, 4.2,
    NULL, NULL, 'user', 0.91, false),

-- ============================================================================
-- FAST CASUAL BOWLS & PLATTERS
-- ============================================================================

('Mediterranean Platter', 'ingredient', 'Falafel, hummus, tabbouleh, pita',
    450, 'g', 'platter (450g)', 450,
    680, 22.5, 88.2, 27,
    16.2, 10.8, 3.6, 0,
    1240, 900, 180, 6.3,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'user', 0.90, false),

('Chicken Shawarma Platter', 'ingredient', 'Chicken shawarma, rice, salad, hummus, pita',
    550, 'g', 'platter (550g)', 550,
    780, 44, 82.5, 28.6,
    10.5, 11, 7.7, 110,
    1540, 1155, 198, 5.5,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.90, false),

('Korean BBQ Bowl', 'ingredient', 'Korean BBQ beef, rice, kimchi, vegetables',
    450, 'g', 'bowl (450g)', 450,
    620, 34.7, 68, 22.2,
    6.7, 16, 7.8, 90,
    1380, 822, 100, 4.2,
    ARRAY['soy'], NULL, 'user', 0.90, false),

('Teriyaki Chicken Bowl', 'ingredient', 'Teriyaki chicken, rice, steamed vegetables',
    450, 'g', 'bowl (450g)', 450,
    580, 34.7, 76, 13.3,
    5.8, 24, 2.7, 85,
    1520, 689, 76, 3.6,
    ARRAY['soy'], NULL, 'user', 0.91, false),

('Acai Bowl (Large)', 'ingredient', 'Acai base with granola, fruit, nuts, honey',
    420, 'g', 'bowl (420g)', 420,
    520, 11.9, 83.3, 16.7,
    14.3, 47.6, 4.8, 0,
    120, 840, 167, 3.1,
    ARRAY['nuts'], ARRAY['vegetarian'], 'user', 0.91, false),

('Protein Power Bowl', 'ingredient', 'Grilled chicken, quinoa, black beans, avocado',
    460, 'g', 'bowl (460g)', 460,
    620, 42.6, 56.5, 23.5,
    15.2, 6.5, 4.8, 95,
    780, 1196, 130, 5.3,
    NULL, ARRAY['gluten-free'], 'user', 0.92, false),

('Vegan Power Bowl', 'ingredient', 'Tofu, quinoa, roasted vegetables, tahini',
    440, 'g', 'bowl (440g)', 440,
    520, 22.7, 56.8, 22.7,
    13.6, 12.3, 3.4, 0,
    680, 1012, 205, 5.7,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

('Southwest Chicken Bowl', 'ingredient', 'Chicken, black beans, corn, peppers, avocado',
    450, 'g', 'bowl (450g)', 450,
    580, 38.7, 54, 22,
    13.5, 8, 5.4, 95,
    980, 1080, 135, 4.5,
    NULL, ARRAY['gluten-free'], 'user', 0.91, false),

('BBQ Chicken Platter', 'ingredient', 'BBQ chicken, mac and cheese, coleslaw',
    480, 'g', 'platter (480g)', 480,
    740, 42.2, 64.8, 33.6,
    5.8, 22.6, 14.4, 155,
    1680, 768, 288, 3.4,
    ARRAY['dairy', 'gluten'], NULL, 'user', 0.89, false),

('Fish and Chips', 'ingredient', 'Battered fish, french fries, tartar sauce',
    480, 'g', 'plate (480g)', 480,
    840, 34.6, 86.4, 43.2,
    7.7, 5.8, 7.7, 90,
    1440, 1104, 115, 3.4,
    ARRAY['eggs', 'fish', 'gluten'], NULL, 'user', 0.90, false);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ COMPLETE MEALS SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Scrambled Eggs with Toast and Bacon', 'Oatmeal with Banana and Almonds', 'Avocado Toast with Egg',
    'Chicken Caesar Salad', 'Cobb Salad', 'Chicken Burrito Bowl', 'Buddha Bowl (Quinoa, Chickpeas, Veggies)',
    'Grilled Chicken Breast with Broccoli and Rice', 'Grilled Salmon with Asparagus and Quinoa',
    'Steak with Sweet Potato and Green Beans', 'Chicken and Broccoli Meal Prep',
    'Mediterranean Platter', 'Korean BBQ Bowl', 'Protein Power Bowl'
);
