-- ============================================================================
-- MIGRATION 017: SEED BRANDED PROTEIN PRODUCTS
-- ============================================================================
-- Description: Popular branded protein powders, bars, shakes, and supplements
-- Total items: ~60 items
-- Brands: Optimum Nutrition, Dymatize, Premier Protein, Quest, Clif, etc.
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

-- OPTIMUM NUTRITION (ON)
('Optimum Nutrition Gold Standard Whey (Double Rich Chocolate)', 'ingredient', 'ON Gold Standard 100% whey protein powder, chocolate',
    100, 'g', 'scoop (32g)', 32,
    381, 75, 12.5, 3.1,
    3.1, 3.1, 1.6, 156,
    406, 469, 281, 1.88,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Optimum Nutrition Gold Standard Whey (Vanilla Ice Cream)', 'ingredient', 'ON Gold Standard 100% whey protein powder, vanilla',
    100, 'g', 'scoop (32g)', 32,
    375, 75, 9.4, 3.1,
    3.1, 3.1, 1.6, 156,
    406, 469, 281, 1.88,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Optimum Nutrition Gold Standard Whey (Extreme Milk Chocolate)', 'ingredient', 'ON Gold Standard whey protein, milk chocolate',
    100, 'g', 'scoop (32g)', 32,
    381, 75, 12.5, 3.1,
    3.1, 3.1, 1.6, 156,
    406, 469, 281, 1.88,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Optimum Nutrition Gold Standard 100% Casein (Chocolate)', 'ingredient', 'ON casein protein powder, slow-digesting',
    100, 'g', 'scoop (34g)', 34,
    353, 70.6, 11.8, 2.9,
    2.9, 2.9, 1.5, 59,
    559, 618, 912, 0.88,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Optimum Nutrition Serious Mass (Chocolate)', 'ingredient', 'ON mass gainer protein powder',
    100, 'g', 'scoop (334g)', 334,
    377, 15, 75.4, 3,
    3, 15, 1.5, 75,
    150, 896, 299, 13.4,
    ARRAY['dairy', 'soy', 'eggs'], ARRAY['gluten-free'], 'user', 0.93, false),

-- DYMATIZE
('Dymatize ISO 100 Whey Protein Isolate (Gourmet Chocolate)', 'ingredient', 'Dymatize hydrolyzed whey protein isolate, chocolate',
    100, 'g', 'scoop (31g)', 31,
    371, 80.6, 6.5, 0,
    0, 3.2, 0, 161,
    548, 484, 258, 0.65,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Dymatize ISO 100 Whey Protein Isolate (Gourmet Vanilla)', 'ingredient', 'Dymatize hydrolyzed whey protein isolate, vanilla',
    100, 'g', 'scoop (31g)', 31,
    371, 80.6, 6.5, 0,
    0, 3.2, 0, 161,
    548, 484, 258, 0.65,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Dymatize Elite 100% Whey Protein (Rich Chocolate)', 'ingredient', 'Dymatize whey protein blend, chocolate',
    100, 'g', 'scoop (33g)', 33,
    364, 75.8, 9.1, 3,
    3, 3, 1.5, 152,
    424, 455, 273, 1.82,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- PREMIER PROTEIN
('Premier Protein Shake (Chocolate)', 'ingredient', 'Premier Protein ready-to-drink shake, chocolate',
    100, 'g', 'shake (325ml)', 325,
    62, 9.2, 3.1, 0.9,
    0.9, 0.3, 0, 6,
    62, 123, 154, 1.85,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Premier Protein Shake (Vanilla)', 'ingredient', 'Premier Protein ready-to-drink shake, vanilla',
    100, 'g', 'shake (325ml)', 325,
    62, 9.2, 3.1, 0.9,
    0.9, 0.3, 0, 6,
    62, 123, 154, 1.85,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Premier Protein Shake (Caramel)', 'ingredient', 'Premier Protein ready-to-drink shake, caramel',
    100, 'g', 'shake (325ml)', 325,
    62, 9.2, 3.1, 0.9,
    0.9, 0.3, 0, 6,
    62, 123, 154, 1.85,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Premier Protein Shake (Cafe Latte)', 'ingredient', 'Premier Protein coffee shake, cafe latte',
    100, 'g', 'shake (325ml)', 325,
    62, 9.2, 3.1, 0.9,
    0.9, 0.3, 0, 6,
    77, 123, 154, 1.85,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Premier Protein Bar (Chocolate Peanut Butter)', 'ingredient', 'Premier Protein bar, chocolate peanut butter',
    100, 'g', 'bar (72g)', 72,
    278, 27.8, 34.7, 6.9,
    6.9, 2.8, 2.8, 7,
    278, 236, 139, 3.47,
    ARRAY['dairy', 'peanuts', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Premier Protein Bar (Cookies and Cream)', 'ingredient', 'Premier Protein bar, cookies and cream',
    100, 'g', 'bar (72g)', 72,
    278, 27.8, 36.1, 5.6,
    5.6, 2.8, 2.8, 7,
    278, 236, 139, 3.47,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- QUEST NUTRITION
('Quest Protein Bar (Chocolate Chip Cookie Dough)', 'ingredient', 'Quest protein bar, chocolate chip cookie dough',
    100, 'g', 'bar (60g)', 60,
    333, 33.3, 40, 13.3,
    23.3, 1.7, 6.7, 8,
    467, 300, 167, 3,
    ARRAY['dairy', 'soy', 'nuts'], ARRAY['gluten-free'], 'user', 0.94, false),

('Quest Protein Bar (Cookies and Cream)', 'ingredient', 'Quest protein bar, cookies and cream',
    100, 'g', 'bar (60g)', 60,
    333, 35, 38.3, 13.3,
    23.3, 1.7, 6.7, 8,
    467, 317, 167, 3,
    ARRAY['dairy', 'soy', 'nuts'], ARRAY['gluten-free'], 'user', 0.94, false),

('Quest Protein Bar (Birthday Cake)', 'ingredient', 'Quest protein bar, birthday cake flavor',
    100, 'g', 'bar (60g)', 60,
    333, 35, 40, 13.3,
    23.3, 1.7, 6.7, 8,
    417, 267, 167, 3,
    ARRAY['dairy', 'soy', 'nuts'], ARRAY['gluten-free'], 'user', 0.93, false),

('Quest Protein Powder (Vanilla Milkshake)', 'ingredient', 'Quest protein powder, vanilla',
    100, 'g', 'scoop (31g)', 31,
    387, 80.6, 9.7, 3.2,
    3.2, 0, 0, 161,
    645, 484, 258, 0.65,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Quest Protein Chips (BBQ)', 'ingredient', 'Quest high-protein BBQ chips',
    100, 'g', 'bag (32g)', 32,
    313, 31.3, 31.3, 12.5,
    18.8, 3.1, 3.1, 0,
    1250, 469, 313, 2.19,
    ARRAY['dairy', 'soy'], NULL, 'user', 0.92, false),

('Quest Protein Chips (Sour Cream and Onion)', 'ingredient', 'Quest high-protein sour cream chips',
    100, 'g', 'bag (32g)', 32,
    313, 31.3, 31.3, 12.5,
    18.8, 3.1, 3.1, 0,
    1250, 469, 313, 2.19,
    ARRAY['dairy', 'soy'], NULL, 'user', 0.92, false),

-- MUSCLE MILK
('Muscle Milk Pro Series Protein Shake (Knockout Chocolate)', 'ingredient', 'Muscle Milk protein shake, chocolate',
    100, 'g', 'bottle (414ml)', 414,
    77, 12.3, 3.9, 1,
    1, 1.9, 0, 10,
    77, 308, 192, 0.77,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Muscle Milk Pro Series Protein Shake (Vanilla Creme)', 'ingredient', 'Muscle Milk protein shake, vanilla',
    100, 'g', 'bottle (414ml)', 414,
    77, 12.3, 3.9, 1,
    1, 1.9, 0, 10,
    77, 308, 192, 0.77,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Muscle Milk Protein Bar (Chocolate Peanut Butter)', 'ingredient', 'Muscle Milk protein bar, peanut butter',
    100, 'g', 'bar (58g)', 58,
    310, 27.6, 34.5, 10.3,
    3.4, 17.2, 5.2, 10,
    310, 310, 172, 3.45,
    ARRAY['dairy', 'peanuts', 'soy'], ARRAY['gluten-free'], 'user', 0.93, false),

-- CLIF BUILDER'S BAR
('Clif Builder Bar (Chocolate)', 'ingredient', 'Clif Builders protein bar, chocolate',
    100, 'g', 'bar (68g)', 68,
    353, 29.4, 44.1, 11.8,
    5.9, 23.5, 4.4, 0,
    353, 265, 147, 3.53,
    ARRAY['dairy', 'soy', 'nuts'], NULL, 'user', 0.93, false),

('Clif Builder Bar (Chocolate Peanut Butter)', 'ingredient', 'Clif Builders protein bar, peanut butter',
    100, 'g', 'bar (68g)', 68,
    353, 29.4, 44.1, 11.8,
    5.9, 23.5, 4.4, 0,
    353, 265, 147, 3.53,
    ARRAY['dairy', 'peanuts', 'soy'], NULL, 'user', 0.93, false),

('Clif Builder Bar (Cookies and Cream)', 'ingredient', 'Clif Builders protein bar, cookies and cream',
    100, 'g', 'bar (68g)', 68,
    353, 29.4, 44.1, 11.8,
    5.9, 23.5, 4.4, 0,
    353, 265, 147, 3.53,
    ARRAY['dairy', 'soy', 'nuts'], NULL, 'user', 0.93, false),

-- PURE PROTEIN
('Pure Protein Bar (Chocolate Peanut Butter)', 'ingredient', 'Pure Protein bar, chocolate peanut butter',
    100, 'g', 'bar (50g)', 50,
    400, 40, 34, 12,
    4, 4, 4, 10,
    400, 280, 200, 3.6,
    ARRAY['dairy', 'peanuts', 'soy'], ARRAY['gluten-free'], 'user', 0.93, false),

('Pure Protein Bar (Chocolate Deluxe)', 'ingredient', 'Pure Protein bar, chocolate deluxe',
    100, 'g', 'bar (50g)', 50,
    400, 40, 36, 10,
    4, 4, 4, 10,
    400, 280, 200, 3.6,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.93, false),

('Pure Protein Shake (Vanilla Cream)', 'ingredient', 'Pure Protein ready-to-drink shake, vanilla',
    100, 'g', 'bottle (325ml)', 325,
    62, 10.8, 3.1, 0.5,
    0.5, 0.5, 0, 6,
    92, 154, 154, 1.85,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- ORGAIN
('Orgain Organic Protein Powder (Chocolate)', 'ingredient', 'Orgain organic plant-based protein, chocolate',
    100, 'g', 'scoop (46g)', 46,
    326, 43.5, 32.6, 6.5,
    15.2, 2.2, 0, 0,
    587, 913, 261, 9.78,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Orgain Organic Protein Powder (Vanilla)', 'ingredient', 'Orgain organic plant-based protein, vanilla',
    100, 'g', 'scoop (46g)', 46,
    326, 43.5, 32.6, 6.5,
    15.2, 2.2, 0, 0,
    587, 913, 261, 9.78,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Orgain Organic Protein Shake (Chocolate)', 'ingredient', 'Orgain ready-to-drink protein shake, chocolate',
    100, 'g', 'bottle (325ml)', 325,
    62, 6.2, 7.7, 1.5,
    1.5, 3.1, 0, 0,
    92, 154, 154, 1.85,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

-- VEGA
('Vega Protein and Greens (Vanilla)', 'ingredient', 'Vega plant-based protein with greens, vanilla',
    100, 'g', 'scoop (33g)', 33,
    364, 45.5, 24.2, 6.1,
    9.1, 0, 0, 0,
    758, 606, 303, 5.45,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Vega Sport Premium Protein (Chocolate)', 'ingredient', 'Vega sport plant-based protein, chocolate',
    100, 'g', 'scoop (45g)', 45,
    333, 55.6, 22.2, 4.4,
    4.4, 0, 0, 0,
    667, 778, 222, 7.78,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Vega One All-in-One Shake (Berry)', 'ingredient', 'Vega One nutritional shake, berry',
    100, 'g', 'scoop (42g)', 42,
    357, 35.7, 35.7, 10.7,
    14.3, 0, 1.8, 0,
    571, 714, 357, 10.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

-- BODYARMOR & CORE POWER
('Core Power High Protein Shake (Chocolate)', 'ingredient', 'Core Power milk protein shake, chocolate',
    100, 'g', 'bottle (414ml)', 414,
    62, 10.1, 5.3, 1.2,
    0.5, 4.8, 0.7, 15,
    58, 145, 145, 0.36,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Core Power High Protein Shake (Vanilla)', 'ingredient', 'Core Power milk protein shake, vanilla',
    100, 'g', 'bottle (414ml)', 414,
    62, 10.1, 5.3, 1.2,
    0.5, 4.8, 0.7, 15,
    58, 145, 145, 0.36,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Core Power Elite (Chocolate)', 'ingredient', 'Core Power Elite high protein shake, 42g protein',
    100, 'g', 'bottle (414ml)', 414,
    72, 12.1, 4.3, 1.7,
    0.5, 3.9, 1, 20,
    77, 174, 174, 0.43,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- FAIRLIFE & MUSCLE MILK SMOOTHIES
('Fairlife Core Power Protein Shake (Strawberry Banana)', 'ingredient', 'Fairlife Core Power protein shake, strawberry banana',
    100, 'g', 'bottle (414ml)', 414,
    62, 10.1, 5.3, 1.2,
    0.5, 4.8, 0.7, 15,
    58, 145, 145, 0.36,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- NAKED JUICE PROTEIN
('Naked Juice Protein Smoothie (Protein Zone)', 'ingredient', 'Naked Juice protein smoothie with whey',
    100, 'g', 'bottle (450ml)', 450,
    62, 6.2, 9.8, 0.4,
    0.9, 8, 0.2, 4,
    27, 107, 53, 0.36,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.93, false),

-- SPORTS NUTRITION (PRE-WORKOUT, POST-WORKOUT)
('C4 Original Pre-Workout (Fruit Punch)', 'ingredient', 'C4 pre-workout powder, fruit punch',
    100, 'g', 'scoop (6.5g)', 6.5,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

('Optimum Nutrition Amino Energy (Watermelon)', 'ingredient', 'ON amino energy drink powder, watermelon',
    100, 'g', 'scoop (9g)', 9,
    222, 55.6, 11.1, 0,
    0, 0, 0, 0,
    556, 111, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

-- ENSURE & BOOST (Medical nutrition)
('Ensure Original (Vanilla)', 'ingredient', 'Ensure nutrition shake, vanilla',
    100, 'g', 'bottle (237ml)', 237,
    105, 3.8, 14.3, 2.4,
    0, 6.3, 0.4, 2,
    84, 168, 105, 1.89,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Ensure Original (Chocolate)', 'ingredient', 'Ensure nutrition shake, chocolate',
    100, 'g', 'bottle (237ml)', 237,
    105, 3.8, 14.3, 2.4,
    0, 6.3, 0.4, 2,
    84, 168, 105, 1.89,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Ensure High Protein (Vanilla)', 'ingredient', 'Ensure high protein nutrition shake, vanilla',
    100, 'g', 'bottle (237ml)', 237,
    63, 6.3, 4.2, 0.6,
    0, 2.5, 0.2, 3,
    84, 189, 126, 1.89,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Boost Original (Chocolate)', 'ingredient', 'Boost nutrition drink, chocolate',
    100, 'g', 'bottle (237ml)', 237,
    101, 4.2, 16, 1.7,
    0, 8, 0.4, 4,
    59, 168, 126, 1.89,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Boost High Protein (Vanilla)', 'ingredient', 'Boost high protein drink, vanilla',
    100, 'g', 'bottle (237ml)', 237,
    97, 8, 11.8, 1.3,
    0, 6.3, 0.4, 8,
    67, 189, 168, 1.89,
    ARRAY['dairy', 'soy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- GNARCOTIC PROTEIN FOODS (HIGH PROTEIN PRODUCTS)
('Built Bar (Coconut)', 'ingredient', 'Built Bar protein bar, coconut',
    100, 'g', 'bar (56g)', 56,
    196, 30.4, 32.1, 5.4,
    10.7, 0, 3.6, 9,
    357, 232, 179, 2.68,
    ARRAY['dairy', 'soy', 'nuts'], ARRAY['gluten-free'], 'user', 0.92, false),

('Built Bar (Double Chocolate)', 'ingredient', 'Built Bar protein bar, double chocolate',
    100, 'g', 'bar (56g)', 56,
    196, 30.4, 32.1, 5.4,
    10.7, 0, 3.6, 9,
    357, 232, 179, 2.68,
    ARRAY['dairy', 'soy', 'nuts'], ARRAY['gluten-free'], 'user', 0.92, false),

-- COLLAGEN PEPTIDES
('Vital Proteins Collagen Peptides (Unflavored)', 'ingredient', 'Vital Proteins collagen peptide powder',
    100, 'g', 'scoop (20g)', 20,
    350, 90, 0, 0,
    0, 0, 0, 0,
    400, 0, 0, 0,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'user', 0.93, false),

('Sports Research Collagen Peptides (Unflavored)', 'ingredient', 'Sports Research collagen powder',
    100, 'g', 'scoop (11g)', 11,
    364, 90.9, 0, 0,
    0, 0, 0, 0,
    455, 0, 0, 0,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'user', 0.93, false),

-- EGG WHITE PROTEIN
('MuscleEgg Liquid Egg Whites', 'ingredient', 'MuscleEgg 100% liquid egg whites',
    100, 'g', 'cup (243g)', 243,
    52, 11, 0.8, 0.2,
    0, 0.4, 0, 0,
    166, 176, 7, 0.08,
    ARRAY['eggs'], ARRAY['gluten-free', 'paleo'], 'user', 0.94, false),

-- BEEF PROTEIN
('Carnivor Beef Protein Isolate (Chocolate)', 'ingredient', 'MuscleMeds Carnivor beef protein isolate',
    100, 'g', 'scoop (36.3g)', 36.3,
    330, 68.9, 16.5, 0,
    0, 0, 0, 0,
    688, 275, 55, 2.75,
    NULL, ARRAY['gluten-free', 'paleo'], 'user', 0.92, false);

COMMIT;

SELECT '✅ BRANDED PROTEIN PRODUCTS SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Optimum Nutrition Gold Standard Whey (Double Rich Chocolate)', 'Premier Protein Shake (Chocolate)', 'Quest Protein Bar (Chocolate Chip Cookie Dough)', 'Dymatize ISO 100 Whey Protein Isolate (Gourmet Chocolate)');
