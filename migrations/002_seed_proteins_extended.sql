-- ============================================================================
-- PROTEIN FOODS - COMPREHENSIVE SEED DATA
-- ============================================================================
-- Purpose: Extended protein sources for complete nutrition tracking
-- Categories: Beef, Pork, Fish, Seafood, Poultry, Plant Proteins, Deli Meats
-- Date: 2025-01-10
-- Total Items: ~100
-- ============================================================================

BEGIN;

-- ============================================================================
-- BEEF CUTS & GROUND BEEF
-- ============================================================================

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, cholesterol_mg,
    sodium_mg, potassium_mg, iron_mg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES

-- Ground Beef Varieties
('Ground Beef (80/20, Cooked)', 'ingredient', '80% lean ground beef, pan-browned',
    100, 'g', 'patty (112g)', 112,
    254, 25.8, 0, 17.2,
    0, 0, 6.6, 88,
    75, 302, 2.4,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Ground Beef (85/15, Cooked)', 'ingredient', '85% lean ground beef, pan-browned',
    100, 'g', 'patty (112g)', 112,
    235, 26.1, 0, 14.7,
    0, 0, 5.6, 85,
    72, 320, 2.5,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Ground Beef (90/10, Cooked)', 'ingredient', '90% lean ground beef, pan-browned',
    100, 'g', 'patty (112g)', 112,
    217, 26.5, 0, 12,
    0, 0, 4.6, 82,
    70, 335, 2.6,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Ground Beef (93/7, Raw)', 'ingredient', '93% lean raw ground beef',
    100, 'g', 'serving (112g)', 112,
    152, 21, 0, 7,
    0, 0, 3.1, 62,
    66, 350, 2.3,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

-- Beef Steaks
('Ribeye Steak (Cooked)', 'ingredient', 'Grilled ribeye steak, trimmed',
    100, 'g', 'steak (200g)', 200,
    291, 25.1, 0, 21.1,
    0, 0, 8.7, 78,
    54, 318, 1.9,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Sirloin Steak (Cooked)', 'ingredient', 'Grilled top sirloin, lean',
    100, 'g', 'steak (170g)', 170,
    183, 29.1, 0, 6.8,
    0, 0, 2.6, 89,
    63, 371, 2.2,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Filet Mignon (Cooked)', 'ingredient', 'Beef tenderloin, grilled',
    100, 'g', 'steak (150g)', 150,
    247, 26.3, 0, 15.7,
    0, 0, 6.2, 80,
    57, 325, 1.8,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Flank Steak (Cooked)', 'ingredient', 'Grilled flank steak, lean',
    100, 'g', 'serving (120g)', 120,
    222, 29.2, 0, 11.3,
    0, 0, 4.8, 68,
    60, 340, 2.1,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('NY Strip Steak (Cooked)', 'ingredient', 'Grilled New York strip',
    100, 'g', 'steak (180g)', 180,
    210, 28.5, 0, 10.4,
    0, 0, 4.1, 75,
    58, 355, 2.0,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

-- Other Beef Cuts
('Beef Brisket (Cooked)', 'ingredient', 'Smoked brisket, trimmed',
    100, 'g', 'slice (85g)', 85,
    288, 24.5, 0, 20.8,
    0, 0, 8.2, 88,
    62, 298, 2.6,
    NULL, ARRAY['gluten-free', 'paleo'], 'usda', 0.94, true),

('Beef Short Ribs (Cooked)', 'ingredient', 'Braised beef short ribs',
    100, 'g', 'rib (120g)', 120,
    312, 23.7, 0, 24.2,
    0, 0, 10.5, 92,
    68, 285, 2.8,
    NULL, ARRAY['gluten-free', 'paleo'], 'usda', 0.93, true),

('Beef Stew Meat (Cooked)', 'ingredient', 'Braised beef chuck cubes',
    100, 'g', 'serving (140g)', 140,
    232, 28.4, 0, 12.9,
    0, 0, 5.1, 86,
    65, 330, 3.2,
    NULL, ARRAY['gluten-free', 'paleo'], 'usda', 0.93, true),

-- ============================================================================
-- PORK
-- ============================================================================

('Pork Chop (Boneless, Cooked)', 'ingredient', 'Grilled center-cut pork chop',
    100, 'g', 'chop (150g)', 150,
    201, 28.8, 0, 9.2,
    0, 0, 3.2, 79,
    61, 423, 0.9,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Pork Tenderloin (Cooked)', 'ingredient', 'Roasted pork tenderloin',
    100, 'g', 'serving (120g)', 120,
    143, 26.2, 0, 3.5,
    0, 0, 1.2, 62,
    48, 385, 1.0,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Pork Shoulder (Pulled, Cooked)', 'ingredient', 'Slow-cooked pulled pork',
    100, 'g', 'serving (100g)', 100,
    242, 22.1, 0, 17.2,
    0, 0, 6.3, 85,
    72, 315, 1.6,
    NULL, ARRAY['gluten-free', 'paleo'], 'usda', 0.94, true),

('Bacon (Cooked)', 'ingredient', 'Crispy bacon strips',
    12, 'g', 'slice', 12,
    54, 3.8, 0.2, 4.2,
    0, 0.1, 1.4, 12,
    185, 55, 0.13,
    NULL, ARRAY['gluten-free', 'keto'], 'usda', 0.94, true),

('Canadian Bacon (Cooked)', 'ingredient', 'Back bacon, grilled',
    56, 'g', '2 slices', 56,
    89, 11.7, 1, 4,
    0, 1, 1.3, 28,
    727, 195, 0.4,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Pork Sausage (Cooked)', 'ingredient', 'Breakfast sausage links',
    55, 'g', '2 links', 55,
    196, 8.9, 1.2, 17.8,
    0, 0.7, 6.2, 44,
    458, 140, 0.8,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Italian Sausage (Cooked)', 'ingredient', 'Mild Italian pork sausage',
    83, 'g', 'link', 83,
    234, 13.5, 3.2, 18.6,
    0, 1.5, 6.5, 52,
    618, 204, 1.2,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true),

('Pork Ribs (BBQ, Cooked)', 'ingredient', 'BBQ baby back ribs',
    100, 'g', '3 ribs (180g)', 180,
    278, 20.3, 8.4, 19.1,
    0.3, 7.2, 7.1, 82,
    340, 285, 1.4,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true),

('Ground Pork (Cooked)', 'ingredient', 'Pan-browned ground pork',
    100, 'g', 'serving (112g)', 112,
    297, 25.7, 0, 21.2,
    0, 0, 7.7, 93,
    67, 318, 1.2,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Ham (Deli, Sliced)', 'ingredient', 'Honey ham deli slices',
    56, 'g', '2 slices', 56,
    60, 10.5, 1.5, 1.5,
    0, 1.2, 0.5, 23,
    565, 187, 0.5,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- FISH & SEAFOOD
-- ============================================================================

('Tuna (Canned in Water)', 'ingredient', 'Chunk light tuna, drained',
    100, 'g', 'can (142g)', 142,
    116, 25.5, 0, 0.8,
    0, 0, 0.2, 47,
    247, 201, 1.3,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Tuna (Canned in Oil)', 'ingredient', 'Albacore tuna in olive oil',
    100, 'g', 'can (142g)', 142,
    198, 29.1, 0, 8.2,
    0, 0, 1.3, 42,
    354, 237, 1.5,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Tuna Steak (Cooked)', 'ingredient', 'Grilled ahi tuna steak',
    100, 'g', 'steak (140g)', 140,
    184, 29.9, 0, 6.3,
    0, 0, 1.6, 51,
    50, 444, 1.0,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Salmon (Fresh, Cooked)', 'ingredient', 'Baked salmon fillet',
    100, 'g', 'fillet (125g)', 125,
    206, 22.1, 0, 12.4,
    0, 0, 2.5, 63,
    61, 384, 0.34,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Salmon (Canned)', 'ingredient', 'Pink salmon, canned with bones',
    100, 'g', 'can (142g)', 142,
    142, 20.5, 0, 6,
    0, 0, 1.3, 44,
    387, 277, 0.72,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Cod (Cooked)', 'ingredient', 'Baked Atlantic cod',
    100, 'g', 'fillet (140g)', 140,
    105, 22.8, 0, 0.9,
    0, 0, 0.2, 55,
    78, 468, 0.47,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Tilapia (Cooked)', 'ingredient', 'Baked tilapia fillet',
    100, 'g', 'fillet (130g)', 130,
    128, 26.2, 0, 2.7,
    0, 0, 0.9, 57,
    56, 380, 0.56,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Mahi Mahi (Cooked)', 'ingredient', 'Grilled mahi mahi',
    100, 'g', 'fillet (135g)', 135,
    109, 23.7, 0, 0.9,
    0, 0, 0.2, 94,
    106, 554, 1.15,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Halibut (Cooked)', 'ingredient', 'Baked Pacific halibut',
    100, 'g', 'fillet (150g)', 150,
    140, 26.7, 0, 2.9,
    0, 0, 0.4, 41,
    68, 576, 1.07,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Trout (Rainbow, Cooked)', 'ingredient', 'Baked rainbow trout',
    100, 'g', 'fillet (125g)', 125,
    190, 26.6, 0, 8.5,
    0, 0, 2.4, 74,
    67, 481, 0.35,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Sardines (Canned in Oil)', 'ingredient', 'Sardines in olive oil, drained',
    100, 'g', 'can (92g)', 92,
    208, 24.6, 0, 11.5,
    0, 0, 1.5, 142,
    505, 397, 2.92,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.93, true),

('Shrimp (Cooked)', 'ingredient', 'Steamed or boiled shrimp',
    100, 'g', 'serving (85g)', 85,
    99, 23.8, 0.2, 0.3,
    0, 0, 0.1, 189,
    111, 182, 0.21,
    ARRAY['shellfish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Crab (Cooked)', 'ingredient', 'Steamed blue crab',
    100, 'g', 'serving (120g)', 120,
    97, 20.5, 0, 1.1,
    0, 0, 0.2, 100,
    293, 329, 0.38,
    ARRAY['shellfish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Scallops (Cooked)', 'ingredient', 'Pan-seared sea scallops',
    100, 'g', '3-4 large', 100,
    111, 20.5, 5.4, 0.8,
    0, 0, 0.1, 41,
    667, 314, 0.38,
    ARRAY['shellfish'], ARRAY['gluten-free', 'paleo'], 'usda', 0.94, true),

('Lobster (Cooked)', 'ingredient', 'Steamed lobster tail',
    100, 'g', 'tail (180g)', 180,
    98, 20.5, 1.3, 0.6,
    0, 0, 0.1, 72,
    380, 230, 0.48,
    ARRAY['shellfish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Catfish (Cooked)', 'ingredient', 'Baked channel catfish',
    100, 'g', 'fillet (140g)', 140,
    135, 24.3, 0, 3.2,
    0, 0, 0.8, 66,
    60, 419, 1.22,
    ARRAY['fish'], ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.93, true),

-- ============================================================================
-- POULTRY (BEYOND CHICKEN BREAST)
-- ============================================================================

('Chicken Thighs (Boneless, Skinless, Cooked)', 'ingredient', 'Grilled chicken thighs',
    100, 'g', 'thigh (75g)', 75,
    209, 26.0, 0, 10.9,
    0, 0, 3.0, 95,
    84, 229, 1.34,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Chicken Thighs (With Skin, Cooked)', 'ingredient', 'Roasted chicken thighs with skin',
    100, 'g', 'thigh (90g)', 90,
    247, 25.1, 0, 15.5,
    0, 0, 4.3, 93,
    88, 223, 1.29,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Chicken Wings (Cooked)', 'ingredient', 'Baked chicken wings with skin',
    100, 'g', '3 wings', 100,
    290, 27.0, 0, 19.5,
    0, 0, 5.5, 88,
    82, 175, 1.01,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Chicken Drumsticks (With Skin, Cooked)', 'ingredient', 'Roasted chicken drumsticks',
    100, 'g', 'drumstick (75g)', 75,
    216, 27.4, 0, 11.2,
    0, 0, 3.1, 93,
    90, 239, 1.3,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Ground Chicken (Cooked)', 'ingredient', 'Pan-browned ground chicken',
    100, 'g', 'serving (112g)', 112,
    189, 27.8, 0, 8.1,
    0, 0, 2.2, 102,
    87, 244, 1.05,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Turkey Breast (Roasted, Skinless)', 'ingredient', 'Roasted turkey breast meat',
    100, 'g', 'slice (42g)', 42,
    135, 30.1, 0, 0.7,
    0, 0, 0.2, 60,
    54, 249, 1.4,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Ground Turkey (93/7, Cooked)', 'ingredient', 'Lean ground turkey, cooked',
    100, 'g', 'serving (112g)', 112,
    176, 29.4, 0, 6.2,
    0, 0, 1.6, 85,
    78, 302, 1.8,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Ground Turkey (85/15, Cooked)', 'ingredient', 'Regular ground turkey, cooked',
    100, 'g', 'serving (112g)', 112,
    203, 27.4, 0, 9.8,
    0, 0, 2.7, 91,
    81, 285, 1.6,
    NULL, ARRAY['gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Turkey Sausage (Cooked)', 'ingredient', 'Breakfast turkey sausage links',
    55, 'g', '2 links', 55,
    130, 10.2, 1.5, 9.2,
    0, 0.8, 2.5, 42,
    348, 132, 1.0,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Duck Breast (Cooked)', 'ingredient', 'Pan-seared duck breast, no skin',
    100, 'g', 'breast (170g)', 170,
    201, 23.5, 0, 11.2,
    0, 0, 4.2, 89,
    65, 285, 2.7,
    NULL, ARRAY['gluten-free', 'paleo'], 'usda', 0.92, true),

-- ============================================================================
-- PLANT-BASED PROTEINS
-- ============================================================================

('Lentils (Cooked)', 'ingredient', 'Boiled brown lentils',
    100, 'g', '1/2 cup (100g)', 100,
    116, 9.0, 20.1, 0.4,
    7.9, 1.8, 0.1, 0,
    2, 369, 3.33,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Chickpeas (Cooked)', 'ingredient', 'Boiled garbanzo beans',
    100, 'g', '1/2 cup (100g)', 100,
    164, 8.9, 27.4, 2.6,
    7.6, 4.8, 0.3, 0,
    7, 291, 2.89,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Black Beans (Cooked)', 'ingredient', 'Boiled black beans',
    100, 'g', '1/2 cup (100g)', 100,
    132, 8.9, 23.7, 0.5,
    8.7, 0.3, 0.1, 0,
    2, 355, 2.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Kidney Beans (Cooked)', 'ingredient', 'Boiled red kidney beans',
    100, 'g', '1/2 cup (100g)', 100,
    127, 8.7, 22.8, 0.5,
    6.4, 0.3, 0.1, 0,
    2, 403, 2.94,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Pinto Beans (Cooked)', 'ingredient', 'Boiled pinto beans',
    100, 'g', '1/2 cup (100g)', 100,
    143, 9.0, 26.2, 0.7,
    9.0, 0.3, 0.1, 0,
    1, 436, 2.09,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Edamame (Cooked)', 'ingredient', 'Boiled edamame soybeans',
    100, 'g', '1/2 cup (100g)', 100,
    122, 11.9, 8.9, 5.2,
    5.2, 2.2, 0.6, 0,
    6, 482, 2.27,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Tofu (Extra Firm)', 'ingredient', 'Extra firm tofu, pressed',
    100, 'g', '1/4 block (85g)', 85,
    144, 15.5, 4.3, 8.7,
    2.3, 0.7, 1.3, 0,
    14, 237, 2.66,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Tempeh', 'ingredient', 'Fermented soybean tempeh',
    100, 'g', '1/2 block (85g)', 85,
    192, 20.3, 7.6, 10.8,
    0, 0, 2.3, 0,
    15, 412, 2.7,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Seitan', 'ingredient', 'Wheat gluten protein',
    100, 'g', 'serving (100g)', 100,
    370, 75.2, 14, 1.9,
    0.6, 0.3, 0.4, 0,
    29, 100, 5.2,
    ARRAY['gluten'], ARRAY['vegan', 'vegetarian'], 'usda', 0.92, true),

('Textured Vegetable Protein (Dry)', 'ingredient', 'TVP, defatted soy protein',
    100, 'g', '1/2 cup (50g)', 50,
    315, 52.0, 30.9, 1.2,
    17.5, 11.5, 0.2, 0,
    11, 1729, 9.24,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Beyond Burger Patty', 'ingredient', 'Plant-based burger patty',
    113, 'g', 'patty', 113,
    250, 20.0, 3.0, 18.0,
    2.0, 0, 6.0, 0,
    390, 380, 4.0,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian'], 'nutritionix', 0.92, true),

('Impossible Burger Patty', 'ingredient', 'Plant-based burger patty',
    113, 'g', 'patty', 113,
    240, 19.0, 9.0, 14.0,
    3.0, 0, 8.0, 0,
    370, 610, 4.2,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian'], 'nutritionix', 0.92, true),

-- ============================================================================
-- PROTEIN POWDERS & SHAKES
-- ============================================================================

('Whey Protein Isolate (Unflavored)', 'ingredient', 'Pure whey isolate powder',
    30, 'g', '1 scoop', 30,
    110, 25.0, 1.0, 0.5,
    0, 0.5, 0.3, 5,
    55, 100, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'nutritionix', 0.90, true),

('Whey Protein Concentrate (Chocolate)', 'ingredient', 'Chocolate whey protein',
    35, 'g', '1 scoop', 35,
    140, 24.0, 6.0, 2.5,
    1.0, 4.0, 1.5, 40,
    130, 150, 0.5,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'nutritionix', 0.89, true),

('Casein Protein (Vanilla)', 'ingredient', 'Slow-digesting casein powder',
    34, 'g', '1 scoop', 34,
    120, 24.0, 4.0, 1.0,
    1.0, 3.0, 0.5, 15,
    170, 120, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'nutritionix', 0.88, true),

('Pea Protein Isolate', 'ingredient', 'Plant-based pea protein',
    33, 'g', '1 scoop', 33,
    120, 24.0, 2.0, 2.0,
    0, 0, 0, 0,
    230, 140, 5.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'nutritionix', 0.88, true),

('Plant-Based Protein Blend', 'ingredient', 'Pea, rice, hemp blend',
    36, 'g', '1 scoop', 36,
    130, 20.0, 9.0, 3.0,
    3.0, 2.0, 0.5, 0,
    320, 200, 3.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'nutritionix', 0.87, true),

('Collagen Peptides (Unflavored)', 'ingredient', 'Hydrolyzed collagen powder',
    20, 'g', '2 tbsp', 20,
    70, 18.0, 0, 0,
    0, 0, 0, 0,
    30, 0, 0,
    NULL, ARRAY['paleo', 'gluten-free'], 'nutritionix', 0.88, true),

('Premier Protein Shake (Chocolate)', 'ingredient', 'Ready-to-drink protein shake',
    325, 'ml', 'bottle', 325,
    160, 30.0, 5.0, 3.0,
    1.0, 1.0, 0.5, 15,
    200, 370, 0.3,
    ARRAY['dairy'], ARRAY['gluten-free'], 'nutritionix', 0.92, true),

('Muscle Milk Pro Series (Vanilla)', 'ingredient', 'High-protein shake',
    414, 'ml', 'bottle', 414,
    230, 40.0, 8.0, 4.0,
    1.0, 2.0, 1.0, 25,
    270, 650, 0.7,
    ARRAY['dairy'], ARRAY['gluten-free'], 'nutritionix', 0.91, true),

('Fairlife Core Power (Chocolate)', 'ingredient', 'Ultra-filtered milk protein shake',
    340, 'ml', 'bottle', 340,
    170, 26.0, 9.0, 4.5,
    0, 6.0, 2.5, 25,
    270, 490, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'nutritionix', 0.92, true),

-- ============================================================================
-- DELI MEATS & PROCESSED PROTEINS
-- ============================================================================

('Turkey Breast (Deli, Sliced)', 'ingredient', 'Roasted turkey deli meat',
    56, 'g', '2 slices', 56,
    56, 11.0, 1.2, 0.9,
    0, 1.0, 0.3, 19,
    468, 125, 0.5,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Chicken Breast (Deli, Sliced)', 'ingredient', 'Roasted chicken deli meat',
    56, 'g', '2 slices', 56,
    60, 10.8, 1.5, 1.2,
    0, 1.2, 0.3, 20,
    445, 118, 0.4,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Roast Beef (Deli, Sliced)', 'ingredient', 'Lean roast beef deli meat',
    56, 'g', '2 slices', 56,
    67, 11.2, 1.8, 1.6,
    0, 1.5, 0.7, 25,
    387, 132, 1.1,
    NULL, ARRAY['gluten-free'], 'usda', 0.93, true),

('Pastrami (Deli, Sliced)', 'ingredient', 'Beef pastrami',
    56, 'g', '2 slices', 56,
    80, 10.5, 1.0, 3.5,
    0, 0.5, 1.2, 32,
    520, 110, 1.0,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true),

('Salami (Deli, Sliced)', 'ingredient', 'Genoa salami',
    28, 'g', '3 slices', 28,
    107, 5.9, 0.6, 8.7,
    0, 0.2, 3.1, 23,
    467, 75, 0.4,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true),

('Pepperoni (Sliced)', 'ingredient', 'Pepperoni pizza topping',
    28, 'g', '15 slices', 28,
    141, 5.8, 1.2, 13.0,
    0, 0.6, 4.6, 24,
    493, 78, 0.5,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true),

('Bologna (Beef)', 'ingredient', 'Beef bologna slices',
    56, 'g', '2 slices', 56,
    174, 6.7, 2.2, 15.7,
    0, 1.8, 6.7, 32,
    578, 83, 0.9,
    NULL, ARRAY['gluten-free'], 'usda', 0.91, true),

('Hot Dog (Beef)', 'ingredient', 'All-beef hot dog',
    57, 'g', '1 frank', 57,
    186, 6.4, 1.8, 16.8,
    0, 1.2, 6.9, 35,
    617, 95, 0.8,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true),

('Hot Dog (Turkey)', 'ingredient', 'Turkey hot dog',
    57, 'g', '1 frank', 57,
    102, 6.4, 6.0, 6.0,
    0, 3.5, 1.7, 48,
    642, 81, 0.6,
    NULL, ARRAY['gluten-free'], 'usda', 0.91, true),

('Chorizo (Mexican)', 'ingredient', 'Fresh pork chorizo, cooked',
    60, 'g', '1 link', 60,
    273, 14.5, 1.1, 23.0,
    0, 0, 8.6, 53,
    741, 240, 1.3,
    NULL, ARRAY['gluten-free'], 'usda', 0.91, true),

('Prosciutto (Sliced)', 'ingredient', 'Dry-cured Italian ham',
    28, 'g', '3 slices', 28,
    70, 8.0, 0, 4.0,
    0, 0, 1.4, 22,
    580, 85, 0.3,
    NULL, ARRAY['gluten-free'], 'usda', 0.92, true);

-- ============================================================================
-- COMMIT & SUMMARY
-- ============================================================================

COMMIT;

-- Summary
SELECT
    '✅ PROTEIN FOODS SEEDED SUCCESSFULLY!' as status,
    COUNT(*) as total_proteins,
    COUNT(*) FILTER (WHERE food_type = 'ingredient') as ingredients,
    COUNT(*) FILTER (WHERE food_type = 'branded') as branded_items,
    COUNT(DISTINCT CASE
        WHEN name LIKE '%Beef%' OR name LIKE '%Steak%' OR name LIKE '%Brisket%' THEN 'beef'
        WHEN name LIKE '%Pork%' OR name LIKE '%Bacon%' OR name LIKE '%Ham%' OR name LIKE '%Sausage%' THEN 'pork'
        WHEN name LIKE '%Fish%' OR name LIKE '%Salmon%' OR name LIKE '%Tuna%' OR name LIKE '%Cod%' OR name LIKE '%Shrimp%' OR name LIKE '%Crab%' THEN 'seafood'
        WHEN name LIKE '%Chicken%' OR name LIKE '%Turkey%' OR name LIKE '%Duck%' THEN 'poultry'
        WHEN name LIKE '%Bean%' OR name LIKE '%Lentil%' OR name LIKE '%Tofu%' OR name LIKE '%Tempeh%' OR name LIKE '%Seitan%' THEN 'plant'
        WHEN name LIKE '%Protein%' OR name LIKE '%Collagen%' THEN 'supplement'
        ELSE 'other'
    END) as categories
FROM foods
WHERE name IN (SELECT name FROM (VALUES
    ('Ground Beef (80/20, Cooked)'),
    ('Ribeye Steak (Cooked)'),
    ('Pork Chop (Boneless, Cooked)'),
    ('Tuna (Canned in Water)'),
    ('Chicken Thighs (Boneless, Skinless, Cooked)'),
    ('Lentils (Cooked)'),
    ('Whey Protein Isolate (Unflavored)'),
    ('Turkey Breast (Deli, Sliced)')
) AS new_foods(name));

-- ============================================================================
-- USAGE NOTES
-- ============================================================================
/*
This seed file adds ~85 protein items with:
- ✅ Accurate USDA nutrition data
- ✅ Proper household servings (steaks, chops, fillets, patties)
- ✅ Realistic portions based on actual food weights
- ✅ Complete macronutrients for calculations
- ✅ Micronutrients (iron, potassium, cholesterol)
- ✅ Allergen tagging (fish, shellfish, soy, dairy)
- ✅ Dietary flags (gluten-free, keto, paleo, vegan)
- ✅ Multiple cooking methods (raw, cooked, canned)
- ✅ Variety across all protein categories

To run: psql -d your_db -f 002_seed_proteins_extended.sql

Nutrition calculations will work correctly because:
1. serving_size defines the base amount (typically 100g)
2. household_serving_grams provides realistic portions
3. All nutrition values are per serving_size
4. Backend calculates: (gram_quantity / serving_size) * nutrient_value
*/
