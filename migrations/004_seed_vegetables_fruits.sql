-- ============================================================================
-- VEGETABLES & FRUITS - COMPREHENSIVE SEED DATA
-- ============================================================================
-- Purpose: All vegetables and fruits for nutrition tracking
-- Date: 2025-01-10
-- Total Items: ~100
-- ============================================================================

BEGIN;

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, cholesterol_mg,
    sodium_mg, potassium_mg, calcium_mg, iron_mg, vitamin_c_mg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES

-- ============================================================================
-- LEAFY GREENS
-- ============================================================================

('Kale (Raw)', 'ingredient', 'Raw kale leaves',
    100, 'g', '1 cup chopped (67g)', 67,
    49, 4.3, 8.8, 0.9,
    3.6, 2.3, 0.1, 0,
    38, 491, 150, 1.5, 120,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Spinach (Cooked)', 'ingredient', 'Boiled spinach',
    100, 'g', '1/2 cup (90g)', 90,
    23, 3.0, 3.8, 0.3,
    2.4, 0.4, 0.05, 0,
    70, 466, 136, 3.6, 9.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Romaine Lettuce', 'ingredient', 'Fresh romaine',
    100, 'g', '2 cups shredded (94g)', 94,
    17, 1.2, 3.3, 0.3,
    2.1, 1.2, 0.04, 0,
    8, 247, 33, 1.0, 4.0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Arugula', 'ingredient', 'Fresh arugula leaves',
    100, 'g', '2 cups (40g)', 40,
    25, 2.6, 3.7, 0.7,
    1.6, 2.1, 0.09, 0,
    27, 369, 160, 1.5, 15,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Mixed Salad Greens', 'ingredient', 'Spring mix blend',
    100, 'g', '2 cups (56g)', 56,
    21, 1.8, 3.9, 0.3,
    2.0, 1.8, 0.04, 0,
    15, 290, 40, 1.2, 18,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.93, true),

('Collard Greens (Cooked)', 'ingredient', 'Boiled collard greens',
    100, 'g', '1/2 cup (95g)', 95,
    33, 2.5, 5.7, 0.4,
    2.8, 0.9, 0.06, 0,
    20, 169, 141, 0.9, 18.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Swiss Chard (Cooked)', 'ingredient', 'Sautéed swiss chard',
    100, 'g', '1/2 cup (88g)', 88,
    20, 1.9, 4.1, 0.1,
    2.1, 1.1, 0.02, 0,
    179, 379, 58, 2.3, 18,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

-- ============================================================================
-- CRUCIFEROUS VEGETABLES
-- ============================================================================

('Broccoli (Raw)', 'ingredient', 'Fresh broccoli florets',
    100, 'g', '1 cup (91g)', 91,
    34, 2.8, 6.6, 0.4,
    2.6, 1.7, 0.04, 0,
    33, 316, 47, 0.73, 89.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Cauliflower (Raw)', 'ingredient', 'Fresh cauliflower',
    100, 'g', '1 cup chopped (107g)', 107,
    25, 1.9, 5.0, 0.3,
    2.0, 1.9, 0.03, 0,
    30, 299, 22, 0.42, 48.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Brussels Sprouts (Cooked)', 'ingredient', 'Roasted Brussels sprouts',
    100, 'g', '1/2 cup (78g)', 78,
    36, 2.6, 7.1, 0.5,
    2.6, 2.2, 0.06, 0,
    16, 317, 36, 1.2, 62,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Cabbage (Green, Raw)', 'ingredient', 'Fresh green cabbage',
    100, 'g', '1 cup shredded (89g)', 89,
    25, 1.3, 5.8, 0.1,
    2.5, 3.2, 0.01, 0,
    18, 170, 40, 0.47, 36.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Red Cabbage (Raw)', 'ingredient', 'Fresh red cabbage',
    100, 'g', '1 cup shredded (89g)', 89,
    31, 1.4, 7.4, 0.2,
    2.1, 3.8, 0.02, 0,
    27, 243, 45, 0.8, 57,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Bok Choy (Cooked)', 'ingredient', 'Stir-fried bok choy',
    100, 'g', '1 cup (170g)', 170,
    12, 1.6, 1.8, 0.2,
    1.0, 0.8, 0.03, 0,
    58, 371, 93, 0.6, 26,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

-- ============================================================================
-- ROOT VEGETABLES
-- ============================================================================

('Carrots (Raw)', 'ingredient', 'Raw baby carrots',
    100, 'g', '1 medium (61g)', 61,
    41, 0.93, 9.6, 0.24,
    2.8, 4.74, 0.04, 0,
    69, 320, 33, 0.3, 5.9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Beets (Cooked)', 'ingredient', 'Boiled beets',
    100, 'g', '1/2 cup sliced (85g)', 85,
    44, 1.7, 10.0, 0.2,
    2.0, 7.96, 0.03, 0,
    77, 305, 16, 0.79, 3.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Turnips (Cooked)', 'ingredient', 'Boiled turnips',
    100, 'g', '1/2 cup (78g)', 78,
    22, 0.9, 5.1, 0.1,
    2.0, 3.0, 0.01, 0,
    16, 177, 30, 0.18, 11.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.93, true),

('Parsnips (Cooked)', 'ingredient', 'Roasted parsnips',
    100, 'g', '1/2 cup (78g)', 78,
    75, 1.2, 18.0, 0.3,
    4.9, 4.8, 0.05, 0,
    8, 367, 29, 0.59, 13,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.93, true),

('Radishes', 'ingredient', 'Fresh radishes',
    100, 'g', '1 cup sliced (116g)', 116,
    16, 0.68, 3.4, 0.1,
    1.6, 1.86, 0.03, 0,
    39, 233, 25, 0.34, 14.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

-- ============================================================================
-- SQUASH & GOURDS
-- ============================================================================

('Zucchini (Raw)', 'ingredient', 'Fresh zucchini',
    100, 'g', '1 medium (196g)', 196,
    17, 1.2, 3.1, 0.3,
    1.0, 2.5, 0.08, 0,
    8, 261, 16, 0.37, 17.9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Yellow Squash (Cooked)', 'ingredient', 'Sautéed yellow squash',
    100, 'g', '1/2 cup sliced (90g)', 90,
    20, 0.9, 4.3, 0.2,
    1.4, 2.3, 0.04, 0,
    2, 192, 24, 0.35, 10,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Butternut Squash (Cooked)', 'ingredient', 'Roasted butternut squash',
    100, 'g', '1/2 cup cubed (103g)', 103,
    40, 0.9, 10.5, 0.1,
    3.2, 2.2, 0.02, 0,
    4, 284, 41, 0.6, 15.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Acorn Squash (Baked)', 'ingredient', 'Baked acorn squash',
    100, 'g', '1/2 squash (105g)', 105,
    56, 1.1, 14.6, 0.1,
    2.3, 0, 0.03, 0,
    4, 437, 44, 0.93, 11,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Spaghetti Squash (Cooked)', 'ingredient', 'Baked spaghetti squash',
    100, 'g', '1 cup (155g)', 155,
    31, 0.6, 7.0, 0.6,
    1.5, 2.8, 0.13, 0,
    17, 108, 23, 0.31, 3.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Pumpkin (Canned)', 'ingredient', 'Pure pumpkin puree',
    100, 'g', '1/2 cup (122g)', 122,
    34, 1.1, 8.1, 0.3,
    3.6, 3.2, 0.18, 0,
    3, 262, 21, 1.4, 4.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

-- ============================================================================
-- NIGHTSHADES
-- ============================================================================

('Tomato (Roma)', 'ingredient', 'Fresh Roma tomato',
    100, 'g', '1 medium (62g)', 62,
    18, 0.9, 3.9, 0.2,
    1.2, 2.6, 0.03, 0,
    5, 237, 10, 0.27, 13.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Cherry Tomatoes', 'ingredient', 'Fresh cherry tomatoes',
    100, 'g', '1 cup (149g)', 149,
    18, 0.9, 3.9, 0.2,
    1.2, 2.6, 0.03, 0,
    5, 237, 10, 0.27, 13.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Grape Tomatoes', 'ingredient', 'Fresh grape tomatoes',
    100, 'g', '1/2 cup (75g)', 75,
    18, 0.9, 3.9, 0.2,
    1.2, 2.6, 0.03, 0,
    5, 237, 10, 0.27, 13.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Bell Pepper (Green)', 'ingredient', 'Fresh green bell pepper',
    100, 'g', '1 medium (119g)', 119,
    20, 0.86, 4.6, 0.2,
    1.7, 2.4, 0.03, 0,
    3, 175, 10, 0.34, 80.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Bell Pepper (Yellow)', 'ingredient', 'Fresh yellow bell pepper',
    100, 'g', '1 medium (119g)', 119,
    27, 1.0, 6.3, 0.2,
    0.9, 5.0, 0.03, 0,
    2, 212, 11, 0.46, 183.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Eggplant (Cooked)', 'ingredient', 'Grilled eggplant',
    100, 'g', '1/2 cup (50g)', 50,
    35, 0.8, 8.7, 0.2,
    2.5, 3.2, 0.04, 0,
    1, 123, 6, 0.12, 1.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Jalapeño Peppers', 'ingredient', 'Fresh jalapeños',
    100, 'g', '1 pepper (14g)', 14,
    29, 0.9, 6.5, 0.4,
    2.8, 4.1, 0.04, 0,
    3, 248, 12, 0.25, 118.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

-- ============================================================================
-- OTHER VEGETABLES
-- ============================================================================

('Cucumber (With Peel)', 'ingredient', 'Fresh cucumber',
    100, 'g', '1/2 medium (150g)', 150,
    15, 0.65, 3.6, 0.1,
    0.5, 1.67, 0.04, 0,
    2, 147, 16, 0.28, 2.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Celery', 'ingredient', 'Fresh celery stalks',
    100, 'g', '2 medium stalks (80g)', 80,
    14, 0.69, 3.0, 0.2,
    1.6, 1.34, 0.04, 0,
    80, 260, 40, 0.2, 3.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Onion (Yellow)', 'ingredient', 'Fresh yellow onion',
    100, 'g', '1 medium (110g)', 110,
    40, 1.1, 9.3, 0.1,
    1.7, 4.2, 0.04, 0,
    4, 146, 23, 0.21, 7.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Red Onion', 'ingredient', 'Fresh red onion',
    100, 'g', '1 medium (110g)', 110,
    40, 1.1, 9.3, 0.1,
    1.7, 4.2, 0.04, 0,
    4, 146, 23, 0.21, 7.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Green Onions (Scallions)', 'ingredient', 'Fresh scallions',
    100, 'g', '1 cup chopped (100g)', 100,
    32, 1.8, 7.3, 0.2,
    2.6, 2.3, 0.03, 0,
    16, 276, 72, 1.48, 18.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Garlic', 'ingredient', 'Fresh garlic cloves',
    3, 'g', '1 clove', 3,
    4, 0.2, 1.0, 0.01,
    0.06, 0.03, 0, 0,
    1, 12, 5, 0.05, 0.9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Mushrooms (White, Raw)', 'ingredient', 'Fresh button mushrooms',
    100, 'g', '1 cup sliced (70g)', 70,
    22, 3.1, 3.3, 0.3,
    1.0, 2.0, 0.05, 0,
    5, 318, 3, 0.5, 2.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Portobello Mushroom', 'ingredient', 'Large portobello cap',
    100, 'g', '1 cap (84g)', 84,
    22, 2.1, 3.9, 0.4,
    1.3, 2.5, 0.05, 0,
    9, 364, 3, 0.3, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.94, true),

('Asparagus (Cooked)', 'ingredient', 'Steamed asparagus',
    100, 'g', '5-6 spears (90g)', 90,
    22, 2.4, 4.1, 0.2,
    2.1, 1.3, 0.05, 0,
    14, 224, 23, 0.91, 7.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Green Beans (Cooked)', 'ingredient', 'Steamed green beans',
    100, 'g', '3/4 cup (100g)', 100,
    35, 1.8, 7.9, 0.1,
    3.4, 1.4, 0.03, 0,
    1, 209, 37, 0.74, 9.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Corn (Yellow, Cooked)', 'ingredient', 'Boiled sweet corn',
    100, 'g', '1/2 cup kernels (82g)', 82,
    96, 3.4, 21.0, 1.5,
    2.4, 4.5, 0.23, 0,
    15, 270, 2, 0.52, 6.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

('Peas (Green, Frozen, Cooked)', 'ingredient', 'Cooked frozen peas',
    100, 'g', '2/3 cup (100g)', 100,
    84, 5.4, 15.6, 0.2,
    5.5, 5.9, 0.04, 0,
    3, 192, 22, 1.5, 9.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.95, true),

-- ============================================================================
-- BERRIES
-- ============================================================================

('Blueberries (Fresh)', 'ingredient', 'Fresh blueberries',
    100, 'g', '1 cup (148g)', 148,
    57, 0.74, 14.5, 0.33,
    2.4, 10.0, 0.03, 0,
    1, 77, 6, 0.28, 9.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Strawberries (Fresh)', 'ingredient', 'Fresh strawberries',
    100, 'g', '1 cup sliced (166g)', 166,
    32, 0.67, 7.68, 0.3,
    2.0, 4.89, 0.02, 0,
    1, 153, 16, 0.41, 58.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Raspberries (Fresh)', 'ingredient', 'Fresh raspberries',
    100, 'g', '1 cup (123g)', 123,
    52, 1.2, 11.9, 0.65,
    6.5, 4.4, 0.02, 0,
    1, 151, 25, 0.69, 26.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Blackberries (Fresh)', 'ingredient', 'Fresh blackberries',
    100, 'g', '1 cup (144g)', 144,
    43, 1.4, 9.6, 0.5,
    5.3, 4.9, 0.01, 0,
    1, 162, 29, 0.62, 21,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Cranberries (Fresh)', 'ingredient', 'Fresh cranberries',
    100, 'g', '1 cup whole (100g)', 100,
    46, 0.39, 12.2, 0.13,
    4.6, 4.04, 0.01, 0,
    2, 85, 8, 0.25, 13.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

-- ============================================================================
-- STONE FRUITS
-- ============================================================================

('Peach', 'ingredient', 'Fresh peach',
    100, 'g', '1 medium (150g)', 150,
    39, 0.91, 9.5, 0.25,
    1.5, 8.4, 0.02, 0,
    0, 190, 6, 0.25, 6.6,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Nectarine', 'ingredient', 'Fresh nectarine',
    100, 'g', '1 medium (142g)', 142,
    44, 1.1, 10.6, 0.3,
    1.7, 7.9, 0.02, 0,
    0, 201, 6, 0.28, 5.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Plum', 'ingredient', 'Fresh plum',
    100, 'g', '1 medium (66g)', 66,
    46, 0.7, 11.4, 0.3,
    1.4, 9.9, 0.02, 0,
    0, 157, 6, 0.17, 9.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Apricot', 'ingredient', 'Fresh apricot',
    100, 'g', '3 medium (105g)', 105,
    48, 1.4, 11.1, 0.4,
    2.0, 9.2, 0.03, 0,
    1, 259, 13, 0.39, 10,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Cherries (Sweet)', 'ingredient', 'Fresh sweet cherries',
    100, 'g', '1 cup (154g)', 154,
    63, 1.1, 16.0, 0.2,
    2.1, 12.8, 0.04, 0,
    0, 222, 13, 0.36, 7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

-- ============================================================================
-- TROPICAL FRUITS
-- ============================================================================

('Mango', 'ingredient', 'Fresh mango',
    100, 'g', '1 cup diced (165g)', 165,
    60, 0.82, 15.0, 0.38,
    1.6, 13.7, 0.09, 0,
    1, 168, 11, 0.16, 36.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Pineapple', 'ingredient', 'Fresh pineapple',
    100, 'g', '1 cup chunks (165g)', 165,
    50, 0.54, 13.1, 0.12,
    1.4, 9.85, 0.01, 0,
    1, 109, 13, 0.29, 47.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Papaya', 'ingredient', 'Fresh papaya',
    100, 'g', '1 cup cubed (145g)', 145,
    43, 0.47, 10.8, 0.26,
    1.7, 7.82, 0.08, 0,
    8, 182, 20, 0.25, 60.9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Kiwi', 'ingredient', 'Fresh kiwi fruit',
    100, 'g', '2 medium (150g)', 150,
    61, 1.1, 14.7, 0.5,
    3.0, 9.0, 0.03, 0,
    3, 312, 34, 0.31, 92.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Dragon Fruit', 'ingredient', 'Fresh dragon fruit',
    100, 'g', '1/2 fruit (200g)', 200,
    60, 1.2, 13.0, 0,
    3.0, 9.8, 0, 0,
    0, 270, 8, 0.4, 9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.92, true),

-- ============================================================================
-- MELONS
-- ============================================================================

('Watermelon', 'ingredient', 'Fresh watermelon',
    100, 'g', '1 cup diced (152g)', 152,
    30, 0.61, 7.55, 0.15,
    0.4, 6.2, 0.02, 0,
    1, 112, 7, 0.24, 8.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Cantaloupe', 'ingredient', 'Fresh cantaloupe',
    100, 'g', '1 cup diced (160g)', 160,
    34, 0.84, 8.2, 0.19,
    0.9, 7.9, 0.05, 0,
    16, 267, 9, 0.21, 36.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Honeydew Melon', 'ingredient', 'Fresh honeydew',
    100, 'g', '1 cup diced (170g)', 170,
    36, 0.54, 9.1, 0.14,
    0.8, 8.1, 0.04, 0,
    18, 228, 6, 0.17, 18,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

-- ============================================================================
-- CITRUS
-- ============================================================================

('Orange', 'ingredient', 'Fresh orange',
    131, 'g', '1 medium orange', 131,
    62, 1.2, 15.4, 0.2,
    3.1, 12.2, 0.02, 0,
    0, 237, 52, 0.13, 69.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Grapefruit', 'ingredient', 'Fresh grapefruit',
    100, 'g', '1/2 medium (123g)', 123,
    42, 0.77, 10.7, 0.14,
    1.6, 6.9, 0.02, 0,
    0, 135, 22, 0.08, 31.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Lemon', 'ingredient', 'Fresh lemon',
    58, 'g', '1 medium lemon', 58,
    17, 0.6, 5.4, 0.2,
    1.6, 1.5, 0.02, 0,
    1, 80, 15, 0.3, 30.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Lime', 'ingredient', 'Fresh lime',
    67, 'g', '1 medium lime', 67,
    20, 0.5, 7.1, 0.1,
    1.9, 1.1, 0.01, 0,
    1, 68, 22, 0.4, 19.5,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.95, true),

('Tangerine', 'ingredient', 'Fresh tangerine',
    100, 'g', '1 medium (88g)', 88,
    53, 0.81, 13.3, 0.31,
    1.8, 10.6, 0.04, 0,
    2, 166, 37, 0.15, 26.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

-- ============================================================================
-- OTHER FRUITS
-- ============================================================================

('Apple (Fuji)', 'ingredient', 'Fresh Fuji apple',
    182, 'g', '1 medium apple', 182,
    95, 0.5, 25.0, 0.3,
    4.4, 19.0, 0.05, 0,
    2, 195, 11, 0.22, 8.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Grapes (Red)', 'ingredient', 'Fresh red grapes',
    100, 'g', '1 cup (151g)', 151,
    69, 0.72, 18.1, 0.16,
    0.9, 15.5, 0.05, 0,
    2, 191, 10, 0.36, 3.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Pear', 'ingredient', 'Fresh pear',
    100, 'g', '1 medium (178g)', 178,
    57, 0.36, 15.2, 0.14,
    3.1, 9.8, 0.02, 0,
    1, 116, 9, 0.18, 4.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Banana (Small)', 'ingredient', 'Small banana',
    101, 'g', '1 small banana', 101,
    90, 1.1, 23.1, 0.3,
    2.6, 12.3, 0.11, 0,
    1, 361, 5, 0.27, 8.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Pomegranate', 'ingredient', 'Fresh pomegranate seeds',
    100, 'g', '1/2 cup arils (87g)', 87,
    83, 1.7, 18.7, 1.2,
    4.0, 13.7, 0.12, 0,
    3, 236, 10, 0.3, 10.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.94, true),

('Fig (Fresh)', 'ingredient', 'Fresh fig',
    50, 'g', '1 medium fig', 50,
    37, 0.4, 9.6, 0.15,
    1.5, 8.0, 0.03, 0,
    0, 116, 18, 0.19, 1.0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.93, true);

COMMIT;

SELECT
    '✅ VEGETABLES & FRUITS SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(DISTINCT CASE
        WHEN name LIKE '%Lettuce%' OR name LIKE '%Spinach%' OR name LIKE '%Kale%' OR name LIKE '%Arugula%' THEN 'leafy greens'
        WHEN name LIKE '%Broccoli%' OR name LIKE '%Cauliflower%' OR name LIKE '%Cabbage%' OR name LIKE '%Brussels%' THEN 'cruciferous'
        WHEN name LIKE '%berry%' OR name LIKE '%berries%' THEN 'berries'
        WHEN name LIKE '%Melon%' THEN 'melons'
        WHEN name LIKE '%Orange%' OR name LIKE '%Lemon%' OR name LIKE '%Lime%' OR name LIKE '%Grapefruit%' THEN 'citrus'
        ELSE 'other'
    END) as categories
FROM foods
WHERE (name LIKE '%Spinach%' OR name LIKE '%Broccoli%' OR name LIKE '%berry%'
    OR name LIKE '%Apple%' OR name LIKE '%Tomato%' OR name LIKE '%Carrot%');
