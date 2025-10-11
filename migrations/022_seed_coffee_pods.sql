-- ============================================================================
-- MIGRATION 022: SEED COFFEE PODS & K-CUPS
-- ============================================================================
-- Description: Keurig K-Cups, coffee pods, instant coffee - INCLUDING YOUR GREAT VALUE CARAMEL CAPPUCCINO!
-- Total items: ~50 items
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
-- GREAT VALUE (WALMART) - YOUR COFFEE!
-- ============================================================================

('Great Value Caramel Cappuccino K-Cup', 'ingredient', 'Walmart Great Value caramel cappuccino K-cup pod',
    14, 'g', 'K-cup (14g)', 14,
    60, 1, 11, 1.5,
    0, 9, 1, 0,
    100, 30, 0, 0,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.93, false),

('Great Value French Vanilla K-Cup', 'ingredient', 'Walmart Great Value French vanilla K-cup',
    14, 'g', 'K-cup (14g)', 14,
    60, 1, 11, 1.5,
    0, 9, 1, 0,
    95, 30, 0, 0,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

('Great Value Colombian K-Cup', 'ingredient', 'Walmart Great Value Colombian coffee K-cup',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Great Value Donut Shop K-Cup', 'ingredient', 'Walmart Great Value donut shop blend K-cup',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- GREEN MOUNTAIN COFFEE
-- ============================================================================

('Green Mountain Breakfast Blend K-Cup', 'ingredient', 'Green Mountain breakfast blend coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 49, 2, 0.02,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Green Mountain French Vanilla K-Cup', 'ingredient', 'Green Mountain French vanilla flavored coffee',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 49, 2, 0.02,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Green Mountain Caramel Vanilla Cream K-Cup', 'ingredient', 'Green Mountain caramel vanilla cream',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 49, 2, 0.02,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- DUNKIN DONUTS K-CUPS
-- ============================================================================

('Dunkin Donuts Original Blend K-Cup', 'ingredient', 'Dunkin original blend coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Dunkin Donuts French Vanilla K-Cup', 'ingredient', 'Dunkin French vanilla flavored coffee',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Dunkin Donuts Hazelnut K-Cup', 'ingredient', 'Dunkin hazelnut flavored coffee',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- STARBUCKS K-CUPS
-- ============================================================================

('Starbucks Pike Place K-Cup', 'ingredient', 'Starbucks Pike Place roast',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Starbucks Veranda Blend K-Cup', 'ingredient', 'Starbucks Veranda blonde roast',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Starbucks French Roast K-Cup', 'ingredient', 'Starbucks French roast dark coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Starbucks Caramel K-Cup', 'ingredient', 'Starbucks caramel flavored coffee',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- MCCAFE K-CUPS
-- ============================================================================

('McCafe Premium Roast K-Cup', 'ingredient', 'McCafe premium roast coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('McCafe French Vanilla K-Cup', 'ingredient', 'McCafe French vanilla coffee',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.92, false),

-- ============================================================================
-- SPECIALTY K-CUPS (SWEET/FLAVORED)
-- ============================================================================

('Cafe Escapes Cafe Caramel K-Cup', 'ingredient', 'Cafe Escapes caramel coffee drink',
    15, 'g', 'K-cup (15g)', 15,
    60, 0.7, 11, 1.5,
    0, 9, 1.5, 0,
    85, 35, 0, 0,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

('Cafe Escapes Cafe Mocha K-Cup', 'ingredient', 'Cafe Escapes mocha coffee drink',
    15, 'g', 'K-cup (15g)', 15,
    60, 1, 11, 1.5,
    0, 9, 1.5, 0,
    85, 40, 0, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

('Cafe Escapes Cafe Vanilla K-Cup', 'ingredient', 'Cafe Escapes vanilla coffee drink',
    15, 'g', 'K-cup (15g)', 15,
    60, 0.7, 11, 1.5,
    0, 9, 1.5, 0,
    85, 35, 0, 0,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

('Swiss Miss Hot Cocoa K-Cup', 'ingredient', 'Swiss Miss hot chocolate K-cup',
    17, 'g', 'K-cup (17g)', 17,
    60, 1, 13, 1,
    1, 10, 0.5, 0,
    170, 70, 40, 0.4,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

-- ============================================================================
-- TEA K-CUPS
-- ============================================================================

('Twinings English Breakfast Tea K-Cup', 'ingredient', 'Twinings English breakfast tea pod',
    2, 'g', 'K-cup (2g)', 2,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Twinings Earl Grey Tea K-Cup', 'ingredient', 'Twinings Earl Grey tea pod',
    2, 'g', 'K-cup (2g)', 2,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Lipton Green Tea K-Cup', 'ingredient', 'Lipton green tea pod',
    2, 'g', 'K-cup (2g)', 2,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Celestial Seasonings Chai Tea K-Cup', 'ingredient', 'Celestial Seasonings chai tea pod',
    2, 'g', 'K-cup (2g)', 2,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- INSTANT COFFEE (NON-POD)
-- ============================================================================

('Nescafe Instant Coffee', 'ingredient', 'Nescafe classic instant coffee',
    100, 'g', 'tsp (2g)', 2,
    357, 14.3, 42.9, 0,
    0, 0, 0, 0,
    71, 3571, 143, 4.29,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'usda', 0.94, true),

('Folgers Instant Coffee', 'ingredient', 'Folgers instant coffee crystals',
    100, 'g', 'tsp (2g)', 2,
    357, 14.3, 42.9, 0,
    0, 0, 0, 0,
    71, 3571, 143, 4.29,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'usda', 0.93, true),

('Starbucks VIA Instant Coffee', 'ingredient', 'Starbucks VIA instant coffee packet',
    3, 'g', 'packet (3g)', 3,
    5, 0, 1, 0,
    0, 0, 0, 0,
    0, 15, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Nescafe 3-in-1 Coffee Mix', 'ingredient', 'Nescafe instant coffee with creamer and sugar',
    100, 'g', 'packet (20g)', 20,
    450, 5, 67.5, 17.5,
    0, 52.5, 15, 0,
    250, 300, 100, 0.5,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.91, false),

('Maxwell House International Cafe (French Vanilla)', 'ingredient', 'Maxwell House French vanilla instant coffee',
    100, 'g', 'tbsp (14g)', 14,
    429, 7.1, 64.3, 14.3,
    0, 57.1, 14.3, 0,
    214, 357, 71, 0.71,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.91, false),

('International Delight Iced Coffee', 'ingredient', 'International Delight ready-to-drink iced coffee',
    240, 'ml', 'bottle (240ml)', 240,
    190, 3, 29, 7,
    0, 28, 4.5, 20,
    120, 180, 100, 0.4,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

-- ============================================================================
-- SPECIALTY COFFEE DRINKS (POD-BASED)
-- ============================================================================

('Donut Shop Sweet and Creamy K-Cup', 'ingredient', 'Donut Shop sweet and creamy coffee',
    14, 'g', 'K-cup (14g)', 14,
    60, 1, 11, 1.5,
    0, 9, 1, 0,
    90, 30, 0, 0,
    ARRAY['dairy'], ARRAY['vegetarian'], 'user', 0.92, false),

('Folgers Gourmet Selections Caramel Drizzle K-Cup', 'ingredient', 'Folgers caramel drizzle flavored coffee',
    12, 'g', 'K-cup (12g)', 12,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.92, false),

('Eight OClock Coffee Original K-Cup', 'ingredient', 'Eight OClock original blend',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Peets Coffee Major Dickasons Blend K-Cup', 'ingredient', 'Peets Major Dickasons blend',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Caribou Coffee Caribou Blend K-Cup', 'ingredient', 'Caribou Coffee blend',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('NewmanS Own Organic Special Blend K-Cup', 'ingredient', 'Newmans Own organic coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- DECAF OPTIONS
-- ============================================================================

('Green Mountain Decaf K-Cup', 'ingredient', 'Green Mountain decaf coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 49, 2, 0.02,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Starbucks Decaf Pike Place K-Cup', 'ingredient', 'Starbucks decaf Pike Place',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Dunkin Donuts Decaf K-Cup', 'ingredient', 'Dunkin decaf coffee',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- ============================================================================
-- COLD BREW PODS
-- ============================================================================

('Starbucks Cold Brew K-Cup', 'ingredient', 'Starbucks cold brew coffee pod',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Dunkin Donuts Cold Brew K-Cup', 'ingredient', 'Dunkin cold brew coffee pod',
    10, 'g', 'K-cup (10g)', 10,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 50, 0, 0,
    NULL, ARRAY['vegan', 'vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false);

COMMIT;

SELECT '✅ COFFEE PODS SEEDED (INCLUDING YOUR GREAT VALUE CARAMEL CAPPUCCINO!)' as status, COUNT(*) as total_items
FROM foods WHERE name LIKE '%K-Cup%' OR name LIKE '%Instant Coffee%' OR name LIKE '%Great Value%Caramel%';
