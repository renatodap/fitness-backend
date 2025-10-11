-- ============================================================================
-- MIGRATION 011: SEED BEVERAGES
-- ============================================================================
-- Description: Comprehensive beverage database
-- Categories: Juices, sodas, energy drinks, sports drinks, coffee, tea, smoothies
-- Total items: ~50 items
--
-- HOW NUTRITION WORKS:
-- - Base nutrition stored per serving_size (typically 100ml or full serving)
-- - User inputs in servings (e.g., "1 can") OR ml
-- - For canned/bottled drinks, household_serving = full container
-- - Nutrition calculated: multiplier = ml_quantity / serving_size
-- ============================================================================

BEGIN;

-- ============================================================================
-- BEVERAGES
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
-- JUICES & FRUIT DRINKS
-- ============================================================================

('Orange Juice (100%)', 'ingredient', '100% pure orange juice',
    100, 'ml', 'cup (240ml)', 240,
    45, 0.7, 10.4, 0.2,
    0.2, 8.4, 0, 0,
    1, 200, 11, 0.2,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.96, true),

('Apple Juice (100%)', 'ingredient', '100% pure apple juice',
    100, 'ml', 'cup (240ml)', 240,
    46, 0.1, 11.3, 0.1,
    0.1, 10, 0, 0,
    4, 101, 8, 0.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Cranberry Juice Cocktail', 'ingredient', 'Sweetened cranberry juice cocktail',
    100, 'ml', 'cup (240ml)', 240,
    46, 0, 11.7, 0.1,
    0, 11.2, 0, 0,
    2, 15, 3, 0.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.94, true),

('Grape Juice (100%)', 'ingredient', '100% pure grape juice',
    100, 'ml', 'cup (240ml)', 240,
    60, 0.6, 14.7, 0.1,
    0.1, 14.2, 0, 0,
    5, 132, 9, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Pineapple Juice (100%)', 'ingredient', '100% pure pineapple juice',
    100, 'ml', 'cup (240ml)', 240,
    53, 0.4, 12.9, 0.1,
    0.2, 10.5, 0, 0,
    1, 130, 16, 0.3,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Tomato Juice', 'ingredient', 'Tomato juice with salt',
    100, 'ml', 'cup (240ml)', 240,
    17, 0.8, 4.2, 0,
    0.5, 3.4, 0, 0,
    269, 229, 10, 0.4,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

('Lemonade (Sweetened)', 'ingredient', 'Traditional sweetened lemonade',
    100, 'ml', 'cup (240ml)', 240,
    43, 0, 11.2, 0,
    0, 10.8, 0, 0,
    3, 10, 2, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- SODAS & CARBONATED DRINKS
-- ============================================================================

('Coca-Cola (Regular)', 'ingredient', 'Regular Coca-Cola soda',
    355, 'ml', 'can (355ml)', 355,
    140, 0, 39, 0,
    0, 39, 0, 0,
    45, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Coca-Cola Zero Sugar', 'ingredient', 'Zero sugar Coca-Cola',
    355, 'ml', 'can (355ml)', 355,
    0, 0, 0, 0,
    0, 0, 0, 0,
    40, 60, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Pepsi (Regular)', 'ingredient', 'Regular Pepsi soda',
    355, 'ml', 'can (355ml)', 355,
    150, 0, 41, 0,
    0, 41, 0, 0,
    30, 30, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Sprite', 'ingredient', 'Lemon-lime soda',
    355, 'ml', 'can (355ml)', 355,
    140, 0, 38, 0,
    0, 38, 0, 0,
    65, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Dr Pepper', 'ingredient', 'Dr Pepper soda',
    355, 'ml', 'can (355ml)', 355,
    150, 0, 40, 0,
    0, 39, 0, 0,
    55, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Mountain Dew', 'ingredient', 'Mountain Dew citrus soda',
    355, 'ml', 'can (355ml)', 355,
    170, 0, 46, 0,
    0, 46, 0, 0,
    60, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Ginger Ale', 'ingredient', 'Ginger ale soda',
    355, 'ml', 'can (355ml)', 355,
    124, 0, 32, 0,
    0, 31, 0, 0,
    25, 4, 11, 0.1,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

('Root Beer', 'ingredient', 'Root beer soda',
    355, 'ml', 'can (355ml)', 355,
    152, 0, 39, 0,
    0, 39, 0, 0,
    48, 0, 19, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'usda', 0.93, true),

-- ============================================================================
-- ENERGY DRINKS
-- ============================================================================

('Red Bull (Regular)', 'ingredient', 'Regular Red Bull energy drink',
    250, 'ml', 'can (250ml)', 250,
    112, 0.4, 27.6, 0,
    0, 27.2, 0, 0,
    105, 0, 0, 0,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Red Bull Sugar Free', 'ingredient', 'Sugar-free Red Bull',
    250, 'ml', 'can (250ml)', 250,
    10, 0.8, 2, 0,
    0, 0, 0, 0,
    105, 0, 0, 0,
    NULL, ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Monster Energy (Regular)', 'ingredient', 'Regular Monster energy drink',
    473, 'ml', 'can (473ml)', 473,
    210, 0, 54, 0,
    0, 52, 0, 0,
    370, 0, 0, 0,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'user', 0.92, false),

('Monster Zero Ultra', 'ingredient', 'Zero sugar Monster energy',
    473, 'ml', 'can (473ml)', 473,
    10, 0, 2, 0,
    0, 0, 0, 0,
    370, 0, 0, 0,
    NULL, ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.92, false),

('5-Hour Energy', 'ingredient', '5-Hour Energy shot',
    57, 'ml', 'bottle (57ml)', 57,
    4, 0, 0, 0,
    0, 0, 0, 0,
    18, 0, 0, 0,
    NULL, ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.90, false),

('Celsius (Peach Vibe)', 'ingredient', 'Celsius fitness energy drink',
    355, 'ml', 'can (355ml)', 355,
    10, 0, 2, 0,
    0, 0, 0, 0,
    15, 0, 50, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.91, false),

-- ============================================================================
-- SPORTS DRINKS
-- ============================================================================

('Gatorade (Regular)', 'ingredient', 'Regular Gatorade sports drink',
    355, 'ml', 'bottle (355ml)', 355,
    80, 0, 21, 0,
    0, 21, 0, 0,
    160, 45, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

('Gatorade Zero', 'ingredient', 'Zero sugar Gatorade',
    355, 'ml', 'bottle (355ml)', 355,
    5, 0, 1, 0,
    0, 0, 0, 0,
    160, 75, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Powerade (Regular)', 'ingredient', 'Regular Powerade sports drink',
    355, 'ml', 'bottle (355ml)', 355,
    80, 0, 21, 0,
    0, 21, 0, 0,
    150, 35, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Powerade Zero', 'ingredient', 'Zero sugar Powerade',
    355, 'ml', 'bottle (355ml)', 355,
    0, 0, 0, 0,
    0, 0, 0, 0,
    150, 35, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.92, false),

('BodyArmor (Regular)', 'ingredient', 'Regular BodyArmor sports drink',
    473, 'ml', 'bottle (473ml)', 473,
    70, 0, 18, 0,
    0, 16, 0, 0,
    65, 700, 0, 0,
    NULL, ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Coconut Water', 'ingredient', 'Natural coconut water',
    240, 'ml', 'carton (240ml)', 240,
    46, 1.7, 8.9, 0.5,
    2.6, 6.3, 0.4, 0,
    252, 600, 58, 0.7,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'usda', 0.95, true),

-- ============================================================================
-- COFFEE DRINKS
-- ============================================================================

('Black Coffee (Brewed)', 'ingredient', 'Regular brewed black coffee',
    240, 'ml', 'cup (240ml)', 240,
    2, 0.3, 0, 0,
    0, 0, 0, 0,
    5, 116, 5, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Coffee with Cream and Sugar', 'ingredient', 'Coffee with 2 cream, 2 sugar',
    250, 'ml', 'cup (250g)', 250,
    60, 0.8, 10, 2,
    0, 9, 1.2, 8,
    25, 136, 20, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.92, false),

('Latte (Grande, 2% Milk)', 'ingredient', 'Grande latte with 2% milk',
    473, 'ml', 'grande (473ml)', 473,
    190, 12.7, 19, 7.6,
    0, 18.1, 4.7, 25,
    170, 444, 380, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Cappuccino (Grande)', 'ingredient', 'Grande cappuccino with 2% milk',
    473, 'ml', 'grande (473ml)', 473,
    140, 10.1, 14.3, 5.1,
    0, 13.6, 3.2, 20,
    135, 354, 303, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.92, false),

('Mocha (Grande, 2% Milk)', 'ingredient', 'Grande mocha with 2% milk and whipped cream',
    473, 'ml', 'grande (473ml)', 473,
    360, 13.6, 44.1, 14.5,
    3, 35.2, 8.5, 40,
    180, 527, 406, 2.4,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Iced Coffee (Unsweetened)', 'ingredient', 'Iced coffee, no sweetener',
    473, 'ml', 'grande (473ml)', 473,
    5, 0.6, 0, 0,
    0, 0, 0, 0,
    10, 229, 10, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.94, false),

('Cold Brew Coffee', 'ingredient', 'Cold brew coffee, unsweetened',
    473, 'ml', 'grande (473ml)', 473,
    5, 0.6, 0, 0,
    0, 0, 0, 0,
    10, 229, 10, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'user', 0.94, false),

('Frappuccino (Caramel, Grande)', 'ingredient', 'Grande caramel frappuccino with whipped cream',
    473, 'ml', 'grande (473ml)', 473,
    420, 5.1, 66.5, 16.3,
    0, 63.6, 10.2, 55,
    230, 339, 203, 0.5,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.90, false),

-- ============================================================================
-- TEA & SPECIALTY DRINKS
-- ============================================================================

('Green Tea (Unsweetened)', 'ingredient', 'Brewed green tea, no sugar',
    240, 'ml', 'cup (240ml)', 240,
    2, 0.5, 0, 0,
    0, 0, 0, 0,
    2, 19, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Black Tea (Unsweetened)', 'ingredient', 'Brewed black tea, no sugar',
    240, 'ml', 'cup (240ml)', 240,
    2, 0, 0.7, 0,
    0, 0, 0, 0,
    7, 88, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo', 'keto'], 'usda', 0.96, true),

('Sweet Tea (Sweetened)', 'ingredient', 'Southern-style sweet iced tea',
    240, 'ml', 'cup (240ml)', 240,
    90, 0, 23, 0,
    0, 22, 0, 0,
    10, 88, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false),

('Chai Tea Latte (Grande)', 'ingredient', 'Grande chai tea latte with 2% milk',
    473, 'ml', 'grande (473ml)', 473,
    240, 6.8, 45.2, 4.7,
    0, 42.4, 2.8, 15,
    115, 288, 253, 0.5,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Matcha Latte (Grande)', 'ingredient', 'Grande matcha green tea latte',
    473, 'ml', 'grande (473ml)', 473,
    240, 12.7, 34, 7.6,
    1, 32.2, 4.7, 25,
    170, 444, 380, 0.7,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Kombucha (GTs Original)', 'ingredient', 'Original flavor kombucha',
    473, 'ml', 'bottle (473ml)', 473,
    60, 0, 14, 0,
    0, 7, 0, 0,
    10, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.91, false),

-- ============================================================================
-- PROTEIN SHAKES & SMOOTHIES
-- ============================================================================

('Protein Shake (Chocolate, Premade)', 'ingredient', 'Ready-to-drink chocolate protein shake',
    325, 'ml', 'bottle (325ml)', 325,
    160, 30, 5, 3,
    1, 3, 0.5, 20,
    210, 480, 500, 1.8,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.92, false),

('Protein Shake (Vanilla, Premade)', 'ingredient', 'Ready-to-drink vanilla protein shake',
    325, 'ml', 'bottle (325ml)', 325,
    160, 30, 5, 3,
    1, 3, 0.5, 20,
    210, 480, 500, 1.8,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.92, false),

('Smoothie (Strawberry Banana)', 'ingredient', 'Strawberry banana smoothie',
    450, 'ml', 'medium (450g)', 450,
    280, 6.7, 60, 2.2,
    5.8, 48.9, 0.7, 5,
    120, 622, 222, 0.9,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false),

('Smoothie (Green Detox)', 'ingredient', 'Green smoothie with spinach, apple, banana',
    450, 'ml', 'medium (450g)', 450,
    220, 4.9, 50.7, 2.2,
    8, 33.8, 0.4, 0,
    85, 756, 133, 1.8,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

('Smoothie (Tropical)', 'ingredient', 'Tropical fruit smoothie (mango, pineapple, coconut)',
    450, 'ml', 'medium (450g)', 450,
    260, 3.1, 58.7, 4.5,
    5.4, 45.8, 3.1, 0,
    50, 603, 89, 0.9,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.90, false),

('Smoothie (Protein Berry)', 'ingredient', 'Mixed berry protein smoothie',
    450, 'ml', 'medium (450g)', 450,
    340, 24, 52, 4.5,
    7.2, 38.7, 1.4, 10,
    180, 648, 270, 1.4,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.91, false);

COMMIT;

-- ============================================================================
-- VERIFICATION QUERY
-- ============================================================================

SELECT
    '✅ BEVERAGES SEEDED!' as status,
    COUNT(*) as total_items,
    COUNT(*) FILTER (WHERE household_serving_unit IS NOT NULL) as items_with_household_servings,
    COUNT(DISTINCT food_type) as food_types,
    ROUND(AVG(data_quality_score)::numeric, 2) as avg_quality_score
FROM foods
WHERE name IN (
    'Orange Juice (100%)', 'Apple Juice (100%)', 'Coca-Cola (Regular)', 'Coca-Cola Zero Sugar',
    'Red Bull (Regular)', 'Monster Energy (Regular)', 'Gatorade (Regular)', 'Gatorade Zero',
    'Black Coffee (Brewed)', 'Latte (Grande, 2% Milk)', 'Green Tea (Unsweetened)', 'Sweet Tea (Sweetened)',
    'Protein Shake (Chocolate, Premade)', 'Smoothie (Strawberry Banana)', 'Coconut Water'
);
