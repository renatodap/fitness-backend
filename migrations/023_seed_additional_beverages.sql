-- ============================================================================
-- MIGRATION 023: SEED ADDITIONAL BEVERAGES
-- ============================================================================
-- Description: Additional sodas, juices, milk varieties, energy drinks, sports drinks
-- Total items: ~50 items
-- Brands: Coca-Cola, Pepsi, Fanta, Minute Maid, Tropicana, Gatorade, etc.
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

-- ADDITIONAL SODAS
('Fanta Orange Soda', 'ingredient', 'Fanta orange soda',
    100, 'g', 'can (355ml)', 355,
    46, 0, 12.3, 0,
    0, 12.3, 0, 0,
    18, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Fanta Grape Soda', 'ingredient', 'Fanta grape soda',
    100, 'g', 'can (355ml)', 355,
    50, 0, 13.3, 0,
    0, 13.3, 0, 0,
    21, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('7-Up Lemon Lime Soda', 'ingredient', '7-Up lemon lime soda',
    100, 'g', 'can (355ml)', 355,
    42, 0, 11, 0,
    0, 11, 0, 0,
    13, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Sprite Lemon Lime Soda', 'ingredient', 'Sprite lemon lime soda',
    100, 'g', 'can (355ml)', 355,
    42, 0, 11, 0,
    0, 11, 0, 0,
    13, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Sprite Zero Sugar', 'ingredient', 'Sprite zero sugar lemon lime soda',
    100, 'g', 'can (355ml)', 355,
    0, 0, 0, 0,
    0, 0, 0, 0,
    21, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Orange Crush Soda', 'ingredient', 'Orange Crush orange soda',
    100, 'g', 'can (355ml)', 355,
    50, 0, 13.3, 0,
    0, 13.3, 0, 0,
    25, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Grape Crush Soda', 'ingredient', 'Grape Crush grape soda',
    100, 'g', 'can (355ml)', 355,
    54, 0, 14.4, 0,
    0, 14.4, 0, 0,
    25, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Cream Soda (A&W)', 'ingredient', 'A&W cream soda',
    100, 'g', 'can (355ml)', 355,
    50, 0, 13.3, 0,
    0, 13.3, 0, 0,
    29, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Barq's Root Beer', 'ingredient', 'Barqs root beer',
    100, 'g', 'can (355ml)', 355,
    46, 0, 12.3, 0,
    0, 12.3, 0, 0,
    21, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Sunkist Orange Soda', 'ingredient', 'Sunkist orange soda',
    100, 'g', 'can (355ml)', 355,
    54, 0, 14.4, 0,
    0, 14.4, 0, 0,
    25, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Mellow Yellow Soda', 'ingredient', 'Mellow Yellow citrus soda',
    100, 'g', 'can (355ml)', 355,
    50, 0, 13.3, 0,
    0, 13.3, 0, 0,
    21, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

-- FLAVORED SPARKLING WATER
('LaCroix Sparkling Water (Pamplemousse)', 'ingredient', 'LaCroix grapefruit sparkling water',
    100, 'g', 'can (355ml)', 355,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('LaCroix Sparkling Water (Lime)', 'ingredient', 'LaCroix lime sparkling water',
    100, 'g', 'can (355ml)', 355,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('Perrier Sparkling Water', 'ingredient', 'Perrier natural sparkling mineral water',
    100, 'g', 'bottle (330ml)', 330,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('San Pellegrino Sparkling Water', 'ingredient', 'San Pellegrino sparkling natural mineral water',
    100, 'g', 'bottle (500ml)', 500,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('Bubly Sparkling Water (Strawberry)', 'ingredient', 'Bubly strawberry sparkling water',
    100, 'g', 'can (355ml)', 355,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

-- MILK VARIETIES
('Fairlife Whole Milk', 'ingredient', 'Fairlife ultra-filtered whole milk',
    100, 'g', 'cup (240ml)', 240,
    63, 5.4, 5, 2.5,
    0, 5, 1.7, 8,
    58, 192, 167, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Fairlife 2% Reduced Fat Milk', 'ingredient', 'Fairlife ultra-filtered 2% milk',
    100, 'g', 'cup (240ml)', 240,
    50, 5.4, 5, 1.1,
    0, 5, 0.8, 8,
    54, 192, 167, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Fairlife Fat Free Skim Milk', 'ingredient', 'Fairlife ultra-filtered skim milk',
    100, 'g', 'cup (240ml)', 240,
    33, 5.4, 5, 0,
    0, 5, 0, 4,
    46, 192, 167, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Lactaid Whole Milk', 'ingredient', 'Lactaid lactose-free whole milk',
    100, 'g', 'cup (240ml)', 240,
    63, 3.3, 5, 3.3,
    0, 5, 2.1, 13,
    50, 142, 125, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Lactaid 2% Reduced Fat Milk', 'ingredient', 'Lactaid lactose-free 2% milk',
    100, 'g', 'cup (240ml)', 240,
    50, 3.3, 5, 2.1,
    0, 5, 1.3, 8,
    50, 142, 125, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Lactaid Fat Free Skim Milk', 'ingredient', 'Lactaid lactose-free fat free milk',
    100, 'g', 'cup (240ml)', 240,
    33, 3.3, 5, 0,
    0, 5, 0, 2,
    50, 142, 125, 0,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.95, false),

('Chocolate Milk (Whole)', 'ingredient', 'Whole chocolate milk',
    100, 'g', 'cup (240ml)', 240,
    83, 3.3, 10.8, 3.3,
    0.8, 10, 2.1, 13,
    63, 167, 117, 0.25,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.94, false),

('TruMoo Chocolate Milk (Lowfat)', 'ingredient', 'TruMoo 1% lowfat chocolate milk',
    100, 'g', 'cup (240ml)', 240,
    67, 3.3, 10, 1.1,
    0, 9.2, 0.8, 5,
    63, 167, 117, 0.25,
    ARRAY['dairy'], ARRAY['gluten-free'], 'user', 0.94, false),

-- JUICE BOXES & POUCHES
('Capri Sun Fruit Punch', 'ingredient', 'Capri Sun fruit punch juice drink',
    100, 'g', 'pouch (177ml)', 177,
    28, 0, 7.3, 0,
    0, 6.2, 0, 0,
    11, 17, 6, 0.06,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Capri Sun Pacific Cooler', 'ingredient', 'Capri Sun Pacific cooler juice drink',
    100, 'g', 'pouch (177ml)', 177,
    28, 0, 7.3, 0,
    0, 6.2, 0, 0,
    11, 17, 6, 0.06,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Honest Kids Apple Juice', 'ingredient', 'Honest Kids organic apple juice drink',
    100, 'g', 'pouch (177ml)', 177,
    17, 0, 4.5, 0,
    0, 4, 0, 0,
    6, 17, 6, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

-- ORANGE JUICE (BRANDED)
('Tropicana Pure Premium Orange Juice', 'ingredient', 'Tropicana pure premium orange juice',
    100, 'g', 'cup (240ml)', 240,
    46, 0.8, 10.8, 0,
    0, 8.3, 0, 0,
    0, 192, 10, 0.21,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Minute Maid Original Orange Juice', 'ingredient', 'Minute Maid original orange juice',
    100, 'g', 'cup (240ml)', 240,
    46, 0.8, 11.3, 0,
    0, 9.2, 0, 0,
    4, 183, 8, 0.17,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Simply Orange Juice', 'ingredient', 'Simply Orange pure squeezed orange juice',
    100, 'g', 'cup (240ml)', 240,
    46, 0.8, 10.8, 0,
    0, 8.8, 0, 0,
    0, 192, 10, 0.21,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- APPLE JUICE (BRANDED)
('Mott's 100% Apple Juice', 'ingredient', 'Motts 100% apple juice',
    100, 'g', 'cup (240ml)', 240,
    48, 0, 11.7, 0,
    0, 10.8, 0, 0,
    8, 117, 8, 0.25,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Martinelli's Apple Juice', 'ingredient', 'Martinellis 100% apple juice',
    100, 'g', 'bottle (296ml)', 296,
    50, 0, 12.5, 0,
    0, 11.7, 0, 0,
    8, 125, 8, 0.25,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

-- CRANBERRY JUICE
('Ocean Spray Cranberry Juice Cocktail', 'ingredient', 'Ocean Spray cranberry juice cocktail',
    100, 'g', 'cup (240ml)', 240,
    46, 0, 11.7, 0,
    0, 11.7, 0, 0,
    4, 25, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Ocean Spray Diet Cranberry Juice', 'ingredient', 'Ocean Spray diet cranberry juice',
    100, 'g', 'cup (240ml)', 240,
    4, 0, 1.3, 0,
    0, 0, 0, 0,
    29, 25, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

-- LEMONADE
('Minute Maid Lemonade', 'ingredient', 'Minute Maid lemonade',
    100, 'g', 'cup (240ml)', 240,
    46, 0, 12.1, 0,
    0, 11.3, 0, 0,
    8, 13, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Simply Lemonade', 'ingredient', 'Simply Lemonade all natural lemonade',
    100, 'g', 'cup (240ml)', 240,
    50, 0, 12.5, 0,
    0, 11.7, 0, 0,
    4, 17, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Country Time Lemonade', 'ingredient', 'Country Time lemonade drink mix prepared',
    100, 'g', 'cup (240ml)', 240,
    25, 0, 6.7, 0,
    0, 6.7, 0, 0,
    4, 8, 4, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

-- ICED TEA (BRANDED)
('Lipton Iced Tea (Lemon)', 'ingredient', 'Lipton lemon iced tea',
    100, 'g', 'bottle (500ml)', 500,
    29, 0, 7.5, 0,
    0, 7.5, 0, 0,
    42, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Arizona Green Tea with Ginseng and Honey', 'ingredient', 'Arizona green tea with ginseng',
    100, 'g', 'can (680ml)', 680,
    29, 0, 7.5, 0,
    0, 7.5, 0, 0,
    42, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Arizona Arnold Palmer Half and Half', 'ingredient', 'Arizona Arnold Palmer iced tea lemonade',
    100, 'g', 'can (680ml)', 680,
    33, 0, 8.8, 0,
    0, 8.3, 0, 0,
    42, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Snapple Lemon Tea', 'ingredient', 'Snapple lemon iced tea',
    100, 'g', 'bottle (473ml)', 473,
    38, 0, 9.5, 0,
    0, 9.5, 0, 0,
    4, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Snapple Peach Tea', 'ingredient', 'Snapple peach iced tea',
    100, 'g', 'bottle (473ml)', 473,
    33, 0, 8.3, 0,
    0, 8.3, 0, 0,
    4, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Pure Leaf Sweet Tea', 'ingredient', 'Pure Leaf sweet tea',
    100, 'g', 'bottle (547ml)', 547,
    33, 0, 8.3, 0,
    0, 8.3, 0, 0,
    4, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Pure Leaf Unsweetened Black Tea', 'ingredient', 'Pure Leaf unsweetened black tea',
    100, 'g', 'bottle (547ml)', 547,
    0, 0, 0, 0,
    0, 0, 0, 0,
    4, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

-- VITAMIN WATER & ENHANCED DRINKS
('Vitaminwater Zero Sugar (XXX)', 'ingredient', 'Vitaminwater zero sugar acai-blueberry-pomegranate',
    100, 'g', 'bottle (591ml)', 591,
    0, 0, 0.8, 0,
    0, 0, 0, 0,
    0, 25, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Vitaminwater Essential (Orange)', 'ingredient', 'Vitaminwater essential orange',
    100, 'g', 'bottle (591ml)', 591,
    42, 0, 11.3, 0,
    0, 11.3, 0, 0,
    0, 25, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.93, false),

-- COCONUT WATER
('Vita Coco Coconut Water', 'ingredient', 'Vita Coco pure coconut water',
    100, 'g', 'bottle (330ml)', 330,
    19, 0, 4.5, 0,
    0, 3.8, 0, 0,
    30, 215, 19, 0.19,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'user', 0.95, false),

('Zico Coconut Water', 'ingredient', 'Zico natural coconut water',
    100, 'g', 'bottle (414ml)', 414,
    17, 0.4, 3.9, 0,
    0, 3.5, 0, 0,
    30, 215, 17, 0.17,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'paleo'], 'user', 0.95, false),

-- ALOE DRINKS
('ALO Drink Original Aloe Vera', 'ingredient', 'ALO drink original aloe vera with honey',
    100, 'g', 'bottle (500ml)', 500,
    21, 0, 5.4, 0,
    0.4, 4.6, 0, 0,
    38, 8, 4, 0.08,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.92, false);

COMMIT;

SELECT '✅ ADDITIONAL BEVERAGES SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Fanta Orange Soda', 'Tropicana Pure Premium Orange Juice', 'Fairlife 2% Reduced Fat Milk', 'LaCroix Sparkling Water (Pamplemousse)');
