-- ============================================================================
-- MIGRATION 005: SEED FATS & DAIRY FOODS
-- ============================================================================
-- Description: Comprehensive fats and dairy products for nutrition tracking
-- Categories: Cooking oils, nuts, seeds, nut butters, cheese, yogurt, milk, butter
-- Total items: ~70 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (typically 100g)
-- - User inputs in servings (e.g., "1 tbsp oil") OR grams (e.g., "14g")
-- - Backend converts between servings↔grams using household_serving_grams
-- - Nutrition calculated: multiplier = gram_quantity / serving_size
-- - Each macronutrient: value * multiplier
--
-- Critical Fields:
-- - serving_size (required): Base amount for nutrition (e.g., 100)
-- - serving_unit (required): Unit for serving_size (e.g., 'g')
-- - household_serving_unit (optional): User-friendly name (e.g., 'tbsp', 'oz')
-- - household_serving_grams (optional): Grams per household serving (e.g., 14g for tbsp)
-- - ALL macros: calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g, sodium_mg
-- ============================================================================

BEGIN;

-- ============================================================================
-- FATS & DAIRY FOODS
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
-- COOKING OILS & FATS
-- ============================================================================

('Olive Oil (Extra Virgin)', 'ingredient', 'Extra virgin olive oil, cold-pressed',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 13.8, 0,
    0, 2, 1, 0.56,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Coconut Oil', 'ingredient', 'Refined or virgin coconut oil',
    100, 'g', 'tbsp (14g)', 14,
    862, 0, 0, 100,
    0, 0, 82.5, 0,
    0, 0, 0, 0.05,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Avocado Oil', 'ingredient', 'Refined avocado oil for cooking',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 11.6, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Vegetable Oil', 'ingredient', 'Generic vegetable oil blend',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 7.2, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Canola Oil', 'ingredient', 'Canola oil for cooking',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 7.4, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Sesame Oil', 'ingredient', 'Toasted sesame oil for flavor',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 14.2, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Grapeseed Oil', 'ingredient', 'Light grapeseed oil',
    100, 'g', 'tbsp (14g)', 14,
    884, 0, 0, 100,
    0, 0, 9.6, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- NUTS (RAW & ROASTED)
-- ============================================================================

('Almonds (Raw)', 'ingredient', 'Raw almonds, whole',
    100, 'g', 'oz (28g)', 28,
    579, 21.2, 21.6, 49.9,
    12.5, 4.4, 3.8, 0,
    1, 733, 269, 3.71,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Cashews (Roasted)', 'ingredient', 'Dry roasted cashews, salted',
    100, 'g', 'oz (28g)', 28,
    553, 15.3, 32.7, 43.9,
    3.3, 7.8, 7.8, 0,
    308, 565, 45, 6.05,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Walnuts (Raw)', 'ingredient', 'Raw walnuts, halves',
    100, 'g', 'oz (28g)', 28,
    654, 15.2, 13.7, 65.2,
    6.7, 2.6, 6.1, 0,
    2, 441, 98, 2.91,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Pecans (Raw)', 'ingredient', 'Raw pecan halves',
    100, 'g', 'oz (28g)', 28,
    691, 9.2, 13.9, 72,
    9.6, 4, 6.2, 0,
    0, 410, 70, 2.53,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Pistachios (Roasted)', 'ingredient', 'Roasted pistachios, salted',
    100, 'g', 'oz (28g)', 28,
    562, 20.3, 27.5, 45.4,
    10.3, 7.7, 5.4, 0,
    428, 1042, 107, 4.03,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Macadamia Nuts', 'ingredient', 'Dry roasted macadamia nuts',
    100, 'g', 'oz (28g)', 28,
    718, 7.9, 13.8, 75.8,
    8.6, 4.6, 12, 0,
    5, 368, 85, 3.69,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Peanuts (Roasted)', 'ingredient', 'Dry roasted peanuts, salted',
    100, 'g', 'oz (28g)', 28,
    587, 23.7, 21.3, 49.7,
    8.4, 4.9, 6.8, 0,
    459, 634, 54, 1.58,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.96, true),

('Brazil Nuts', 'ingredient', 'Raw Brazil nuts',
    100, 'g', 'oz (28g)', 28,
    656, 14.3, 12.3, 66.4,
    7.5, 2.3, 15.1, 0,
    3, 659, 160, 2.43,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

-- ============================================================================
-- SEEDS
-- ============================================================================

('Chia Seeds', 'ingredient', 'Dried chia seeds',
    100, 'g', 'tbsp (12g)', 12,
    486, 16.5, 42.1, 30.7,
    34.4, 0, 3.3, 0,
    16, 407, 631, 7.72,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Flaxseed (Ground)', 'ingredient', 'Ground flaxseed meal',
    100, 'g', 'tbsp (7g)', 7,
    534, 18.3, 28.9, 42.2,
    27.3, 1.6, 3.7, 0,
    30, 813, 255, 5.73,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Pumpkin Seeds (Pepitas)', 'ingredient', 'Roasted pumpkin seeds, salted',
    100, 'g', 'oz (28g)', 28,
    559, 30.2, 14.7, 49,
    6, 1.4, 8.7, 0,
    7, 788, 46, 8.07,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Sunflower Seeds', 'ingredient', 'Dry roasted sunflower seeds, salted',
    100, 'g', 'oz (28g)', 28,
    582, 19.3, 24.1, 49.8,
    11.1, 3.4, 4.5, 0,
    392, 645, 70, 3.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Hemp Hearts', 'ingredient', 'Shelled hemp seeds',
    100, 'g', 'tbsp (10g)', 10,
    553, 31.6, 8.7, 48.8,
    4, 1.5, 4.6, 0,
    5, 1200, 70, 7.95,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Sesame Seeds', 'ingredient', 'Toasted sesame seeds',
    100, 'g', 'tbsp (9g)', 9,
    565, 16.9, 25.7, 48,
    16.9, 0.5, 6.7, 0,
    39, 406, 131, 7.78,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

-- ============================================================================
-- NUT & SEED BUTTERS
-- ============================================================================

('Peanut Butter (Creamy)', 'ingredient', 'Creamy peanut butter, standard',
    100, 'g', 'tbsp (16g)', 16,
    588, 25, 20, 50,
    6, 9.2, 10.3, 0,
    17, 649, 43, 1.87,
    ARRAY['nuts'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.96, true),

('Peanut Butter (Natural)', 'ingredient', 'Natural peanut butter, no added sugar',
    100, 'g', 'tbsp (16g)', 16,
    598, 24.1, 21.6, 51.1,
    5.7, 10.5, 6.9, 0,
    476, 745, 54, 2.17,
    ARRAY['nuts'], ARRAY['vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Almond Butter', 'ingredient', 'Creamy almond butter',
    100, 'g', 'tbsp (16g)', 16,
    614, 21.2, 18.8, 55.5,
    10.3, 4.4, 4.2, 0,
    7, 748, 347, 3.49,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Cashew Butter', 'ingredient', 'Creamy cashew butter',
    100, 'g', 'tbsp (16g)', 16,
    587, 17.6, 27.6, 49.4,
    2, 8.5, 9.8, 0,
    15, 546, 43, 5,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Sunflower Seed Butter', 'ingredient', 'Creamy sunflower seed butter',
    100, 'g', 'tbsp (16g)', 16,
    617, 20, 20, 55,
    6.7, 8.3, 5.7, 0,
    360, 689, 67, 3.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- CHEESE (HARD & SEMI-HARD)
-- ============================================================================

('Cheddar Cheese', 'ingredient', 'Sharp cheddar cheese',
    100, 'g', 'oz (28g)', 28,
    403, 24.9, 1.3, 33.1,
    0, 0.5, 21, 105,
    621, 98, 721, 0.68,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Mozzarella (Part-Skim)', 'ingredient', 'Part-skim mozzarella cheese',
    100, 'g', 'oz (28g)', 28,
    254, 24.3, 3.1, 15.9,
    0, 1.2, 9.3, 54,
    373, 95, 731, 0.23,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Swiss Cheese', 'ingredient', 'Swiss cheese slices',
    100, 'g', 'oz (28g)', 28,
    380, 26.9, 5.4, 27.8,
    0, 1.3, 17.8, 92,
    192, 77, 791, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Parmesan (Grated)', 'ingredient', 'Grated parmesan cheese',
    100, 'g', 'tbsp (5g)', 5,
    431, 38.5, 4.1, 28.6,
    0, 0.9, 19.1, 88,
    1529, 125, 1184, 0.82,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Feta Cheese', 'ingredient', 'Crumbled feta cheese',
    100, 'g', 'oz (28g)', 28,
    264, 14.2, 4.1, 21.3,
    0, 4.1, 14.9, 89,
    1116, 62, 493, 0.65,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Goat Cheese (Soft)', 'ingredient', 'Soft goat cheese (chevre)',
    100, 'g', 'oz (28g)', 28,
    364, 21.6, 2.5, 29.8,
    0, 2.5, 20.6, 79,
    515, 158, 298, 1.62,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Cream Cheese', 'ingredient', 'Regular cream cheese',
    100, 'g', 'tbsp (15g)', 15,
    342, 5.9, 5.5, 34.2,
    0, 3.2, 19.3, 110,
    321, 138, 98, 0.37,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Cottage Cheese (Low-Fat 2%)', 'ingredient', 'Low-fat cottage cheese',
    100, 'g', 'cup (226g)', 226,
    86, 11.1, 4.3, 2.3,
    0, 4.1, 1.4, 9,
    330, 84, 91, 0.14,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Ricotta Cheese (Part-Skim)', 'ingredient', 'Part-skim ricotta cheese',
    100, 'g', 'cup (246g)', 246,
    138, 11.4, 5.1, 7.9,
    0, 0.3, 4.9, 31,
    125, 125, 272, 0.44,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.95, true),

('Blue Cheese (Crumbled)', 'ingredient', 'Crumbled blue cheese',
    100, 'g', 'oz (28g)', 28,
    353, 21.4, 2.3, 28.7,
    0, 0.5, 18.7, 75,
    1395, 256, 528, 0.31,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

-- ============================================================================
-- YOGURT & CULTURED DAIRY
-- ============================================================================

('Greek Yogurt (Plain, Nonfat)', 'ingredient', 'Plain nonfat Greek yogurt',
    100, 'g', 'cup (170g)', 170,
    59, 10.2, 3.6, 0.4,
    0, 3.2, 0.1, 5,
    36, 141, 110, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Greek Yogurt (Plain, 2%)', 'ingredient', 'Plain 2% Greek yogurt',
    100, 'g', 'cup (170g)', 170,
    73, 9.9, 3.9, 1.9,
    0, 3.6, 1.2, 10,
    36, 141, 115, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Greek Yogurt (Plain, Full-Fat)', 'ingredient', 'Plain full-fat Greek yogurt',
    100, 'g', 'cup (170g)', 170,
    97, 9, 3.6, 5,
    0, 3.2, 3.2, 17,
    35, 141, 100, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Regular Yogurt (Plain, Low-Fat)', 'ingredient', 'Plain low-fat regular yogurt',
    100, 'g', 'cup (245g)', 245,
    63, 5.2, 7, 1.6,
    0, 7, 1, 6,
    70, 234, 183, 0.08,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Skyr (Icelandic Yogurt)', 'ingredient', 'Plain nonfat skyr',
    100, 'g', 'cup (170g)', 170,
    63, 11, 4, 0.2,
    0, 4, 0.1, 5,
    60, 150, 150, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Kefir (Plain, Low-Fat)', 'ingredient', 'Plain low-fat kefir',
    100, 'g', 'cup (243g)', 243,
    41, 3.3, 4.5, 1,
    0, 4.5, 0.6, 5,
    40, 151, 120, 0.05,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- MILK & MILK ALTERNATIVES
-- ============================================================================

('Whole Milk (3.25%)', 'ingredient', 'Whole milk, vitamin D added',
    100, 'g', 'cup (244g)', 244,
    61, 3.2, 4.8, 3.3,
    0, 5.1, 1.9, 12,
    43, 151, 113, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.96, true),

('2% Milk', 'ingredient', 'Reduced-fat milk (2%)',
    100, 'g', 'cup (244g)', 244,
    50, 3.3, 4.7, 2,
    0, 5.1, 1.2, 8,
    44, 150, 117, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.96, true),

('Skim Milk (Nonfat)', 'ingredient', 'Nonfat skim milk',
    100, 'g', 'cup (245g)', 245,
    34, 3.4, 5, 0.2,
    0, 5.1, 0.1, 2,
    42, 156, 122, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'usda', 0.96, true),

('Oat Milk (Unsweetened)', 'ingredient', 'Unsweetened oat milk',
    100, 'g', 'cup (240g)', 240,
    42, 1.3, 6.7, 1.5,
    0.8, 2.5, 0.2, 0,
    100, 129, 120, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Almond Milk (Unsweetened)', 'ingredient', 'Unsweetened almond milk',
    100, 'g', 'cup (240g)', 240,
    13, 0.4, 0.6, 1.1,
    0.2, 0, 0.1, 0,
    63, 67, 120, 0.28,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Soy Milk (Unsweetened)', 'ingredient', 'Unsweetened soy milk',
    100, 'g', 'cup (240g)', 240,
    33, 2.9, 1.2, 1.8,
    0.4, 0.4, 0.2, 0,
    38, 118, 120, 0.4,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Coconut Milk (Beverage, Unsweetened)', 'ingredient', 'Unsweetened coconut milk beverage',
    100, 'g', 'cup (240g)', 240,
    19, 0, 1.8, 1.9,
    0, 0.8, 1.7, 0,
    13, 46, 120, 0.14,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

('Cashew Milk (Unsweetened)', 'ingredient', 'Unsweetened cashew milk',
    100, 'g', 'cup (240g)', 240,
    17, 0.4, 1.3, 1.5,
    0, 0, 0.2, 0,
    83, 21, 120, 0.14,
    ARRAY['nuts'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.92, true),

-- ============================================================================
-- BUTTER & SPREADS
-- ============================================================================

('Butter (Salted)', 'ingredient', 'Salted butter',
    100, 'g', 'tbsp (14g)', 14,
    717, 0.9, 0.1, 81.1,
    0, 0.1, 51.4, 215,
    576, 24, 24, 0.02,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Butter (Unsalted)', 'ingredient', 'Unsalted butter',
    100, 'g', 'tbsp (14g)', 14,
    717, 0.9, 0.1, 81.1,
    0, 0.1, 51.4, 215,
    11, 24, 24, 0.02,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'usda', 0.96, true),

('Ghee (Clarified Butter)', 'ingredient', 'Clarified butter (ghee)',
    100, 'g', 'tbsp (13g)', 13,
    876, 0, 0, 99.5,
    0, 0, 61.9, 256,
    0, 5, 4, 0,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Vegan Butter (Plant-Based)', 'ingredient', 'Plant-based vegan butter spread',
    100, 'g', 'tbsp (14g)', 14,
    714, 0, 0, 80,
    0, 0, 28, 0,
    714, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

-- ============================================================================
-- SPECIALTY FATS
-- ============================================================================

('Avocado (Hass)', 'ingredient', 'Fresh Hass avocado',
    100, 'g', 'avocado (136g)', 136,
    160, 2, 8.5, 14.7,
    6.7, 0.7, 2.1, 0,
    7, 485, 12, 0.55,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Olives (Kalamata)', 'ingredient', 'Kalamata olives, pitted',
    100, 'g', 'oz (28g)', 28,
    115, 0.8, 6.3, 10.7,
    3.2, 0, 1.4, 0,
    872, 8, 88, 3.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Olives (Green)', 'ingredient', 'Green olives, pitted',
    100, 'g', 'oz (28g)', 28,
    145, 1, 3.8, 15.3,
    3.3, 0.5, 2, 0,
    1556, 42, 52, 0.49,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ FATS & DAIRY SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Olive Oil (Extra Virgin)', 'Coconut Oil', 'Avocado Oil', 'Vegetable Oil', 'Canola Oil',
    'Almonds (Raw)', 'Cashews (Roasted)', 'Walnuts (Raw)', 'Pecans (Raw)', 'Pistachios (Roasted)',
    'Chia Seeds', 'Flaxseed (Ground)', 'Pumpkin Seeds (Pepitas)', 'Sunflower Seeds',
    'Peanut Butter (Creamy)', 'Peanut Butter (Natural)', 'Almond Butter', 'Cashew Butter',
    'Cheddar Cheese', 'Mozzarella (Part-Skim)', 'Swiss Cheese', 'Parmesan (Grated)', 'Feta Cheese',
    'Greek Yogurt (Plain, Nonfat)', 'Greek Yogurt (Plain, 2%)', 'Greek Yogurt (Plain, Full-Fat)',
    'Whole Milk (3.25%)', '2% Milk', 'Skim Milk (Nonfat)', 'Oat Milk (Unsweetened)', 'Almond Milk (Unsweetened)',
    'Butter (Salted)', 'Butter (Unsalted)', 'Ghee (Clarified Butter)', 'Avocado (Hass)'
);
