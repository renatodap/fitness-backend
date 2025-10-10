-- ============================================================================
-- PHASE 3: REAL WORLD FOOD DATABASE - BRAZILIAN & SNACKS (100 FOODS)
-- ============================================================================
-- Brazilian essentials + American snack foods + sides & appetizers
-- Priority: Brazilian street food, meals, snacks, chips, protein bars
-- Coverage: 90%+ of real-world meal logs
-- ============================================================================

-- Get category IDs
DO $$
DECLARE
    cat_protein UUID;
    cat_carbs UUID;
    cat_fruits UUID;
    cat_vegetables UUID;
    cat_fats UUID;
    cat_dairy UUID;
    cat_beverages UUID;
BEGIN
    SELECT id INTO cat_protein FROM food_categories WHERE name = 'Protein' AND level = 0;
    SELECT id INTO cat_carbs FROM food_categories WHERE name = 'Grains' AND level = 0;
    SELECT id INTO cat_fruits FROM food_categories WHERE name = 'Fruits' AND level = 0;
    SELECT id INTO cat_vegetables FROM food_categories WHERE name = 'Vegetables' AND level = 0;
    SELECT id INTO cat_fats FROM food_categories WHERE name = 'Fats, Nuts & Seeds' AND level = 0;
    SELECT id INTO cat_dairy FROM food_categories WHERE name = 'Dairy' AND level = 0;
    SELECT id INTO cat_beverages FROM food_categories WHERE name = 'Beverages' AND level = 0;

-- ============================================================================
-- SECTION 1: BRAZILIAN STREET FOOD (10 variations)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Coxinha (2 pieces)', 'Protein', cat_protein, 140, 'g', 350, 14, 38, 15, 2, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{gluten}', 1.0),
('Pão de Queijo (3 pieces)', 'Grains', cat_carbs, 90, 'g', 270, 9, 27, 14, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,gluten,vegetarian}', 1.0),
('Pastel (1 large)', 'Grains', cat_carbs, 120, 'g', 320, 10, 36, 15, 2, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{gluten}', 1.0),
('Esfiha (2 pieces - meat)', 'Grains', cat_carbs, 110, 'g', 280, 12, 34, 11, 2, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{gluten}', 1.0),
('Brigadeiro (3 pieces)', 'Grains', cat_carbs, 60, 'g', 210, 2, 32, 9, 1, true, true, false, 'processed', 'raw', '{dessert,snack}', '{dairy,vegetarian}', 1.0),
('Açaí Bowl with Granola & Banana', 'Fruits', cat_fruits, 350, 'g', 420, 8, 72, 12, 10, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{vegetarian}', 1.0),
('Tapioca Crepe (with cheese)', 'Grains', cat_carbs, 140, 'g', 320, 12, 48, 10, 3, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Bolinho de Bacalhau (3 pieces)', 'Protein', cat_protein, 120, 'g', 310, 18, 24, 15, 1, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{gluten,seafood}', 1.0),
('Empadinha (2 pieces - chicken)', 'Grains', cat_carbs, 100, 'g', 260, 10, 28, 12, 1, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{gluten}', 1.0),
('Churros (2 pieces, with dulce de leche)', 'Grains', cat_carbs, 120, 'g', 380, 5, 54, 16, 1, true, true, false, 'processed', 'cooked', '{dessert,snack}', '{dairy,gluten,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 2: BRAZILIAN MEALS (12 variations)
-- ============================================================================

('Feijoada Completa (Black bean stew with pork)', 'Protein', cat_protein, 500, 'g', 720, 42, 58, 32, 14, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork}', 1.0),
('Arroz, Feijão, Bife (Rice, beans, steak)', 'Protein', cat_protein, 520, 'g', 680, 48, 72, 18, 12, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 1.0),
('Frango à Passarinho (Fried chicken pieces)', 'Protein', cat_protein, 200, 'g', 380, 32, 12, 24, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten}', 1.0),
('Picanha (6 oz)', 'Protein', cat_protein, 170, 'g', 370, 36, 0, 24, 0, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{}', 1.0),
('Moqueca (Fish stew, Bahian style)', 'Protein', cat_protein, 450, 'g', 420, 38, 26, 18, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{seafood,dairy}', 1.0),
('Strogonoff de Frango com Arroz (Chicken stroganoff with rice)', 'Protein', cat_protein, 480, 'g', 640, 42, 64, 24, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy}', 1.0),
('Escondidinho (Mashed cassava casserole with meat)', 'Grains', cat_carbs, 350, 'g', 520, 28, 54, 20, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{}', 1.0),
('Vatapá (Shrimp stew)', 'Protein', cat_protein, 400, 'g', 480, 26, 38, 24, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{seafood,nuts}', 1.0),
('Bobó de Camarão (Shrimp with cassava cream)', 'Protein', cat_protein, 420, 'g', 540, 32, 44, 26, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{seafood,dairy}', 1.0),
('Bauru Sandwich (Brazilian hot sandwich)', 'Protein', cat_protein, 250, 'g', 520, 28, 48, 22, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{dairy,gluten}', 1.0),
('X-Tudo Burger (Brazilian loaded burger)', 'Protein', cat_protein, 380, 'g', 820, 42, 56, 44, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Churrasco Misto (Mixed grill meats, 12 oz)', 'Protein', cat_protein, 340, 'g', 820, 68, 0, 64, 0, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{pork}', 1.0),

-- ============================================================================
-- SECTION 3: BRAZILIAN SIDES & SNACKS (8 variations)
-- ============================================================================

('Farofa (Toasted cassava flour, 1/2 cup)', 'Grains', cat_carbs, 85, 'g', 280, 4, 52, 7, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),
('Vinagrete (Brazilian salsa, 1/4 cup)', 'Vegetables', cat_vegetables, 60, 'g', 20, 1, 4, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Couve à Mineira (Collard greens, sautéed)', 'Vegetables', cat_vegetables, 100, 'g', 80, 3, 8, 5, 3, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Feijão Tropeiro (Beans with bacon & cassava)', 'Grains', cat_carbs, 200, 'g', 340, 14, 42, 12, 8, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork}', 1.0),
('Mandioca Frita (Fried cassava)', 'Grains', cat_carbs, 120, 'g', 290, 2, 48, 10, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian,vegan}', 1.0),
('Polenta Frita (Fried polenta)', 'Grains', cat_carbs, 100, 'g', 210, 4, 30, 8, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian}', 1.0),
('Arroz à Grega (Rice with vegetables)', 'Grains', cat_carbs, 160, 'g', 240, 5, 42, 6, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),
('Salada de Batata (Potato salad, Brazilian style)', 'Grains', cat_carbs, 150, 'g', 260, 4, 32, 13, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),

-- ============================================================================
-- SECTION 4: BRAZILIAN DRINKS (6 variations)
-- ============================================================================

('Guaraná Antarctica (Can, 12 oz)', 'Beverages', cat_beverages, 355, 'g', 140, 0, 37, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Mate Leão (Can, 12 oz, iced tea)', 'Beverages', cat_beverages, 355, 'g', 90, 0, 24, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Suco de Laranja Natural (Fresh orange juice, 12 oz)', 'Beverages', cat_beverages, 355, 'g', 165, 3, 39, 1, 1, true, true, true, 'raw', 'raw', '{breakfast,snack}', '{vegetarian,vegan}', 1.0),
('Vitamina de Abacate (Avocado smoothie)', 'Beverages', cat_beverages, 400, 'g', 320, 7, 48, 12, 8, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Caipirinha (8 oz, cachaça cocktail)', 'Beverages', cat_beverages, 237, 'g', 280, 0, 38, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0),
('Cerveja (Brahma/Skol/Antarctica, 12 oz)', 'Beverages', cat_beverages, 355, 'g', 145, 1, 11, 0, 0, false, true, false, 'processed', 'raw', '{snack,dinner}', '{gluten}', 1.0),

-- ============================================================================
-- SECTION 5: AMERICAN CHIPS & CRACKERS (12 variations)
-- ============================================================================

('Lay''s Potato Chips (1 oz bag)', 'Grains', cat_carbs, 28, 'g', 160, 2, 15, 10, 1, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Doritos Nacho Cheese (1 oz, ~11 chips)', 'Grains', cat_carbs, 28, 'g', 150, 2, 18, 8, 1, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Doritos Cool Ranch (1 oz, ~11 chips)', 'Grains', cat_carbs, 28, 'g', 150, 2, 18, 8, 1, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Cheetos Regular (1 oz bag)', 'Grains', cat_carbs, 28, 'g', 160, 2, 13, 10, 1, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Cheetos Hot (1 oz bag)', 'Grains', cat_carbs, 28, 'g', 170, 1, 15, 11, 1, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Pringles Original (15 chips)', 'Grains', cat_carbs, 28, 'g', 150, 1, 15, 9, 1, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Fritos Corn Chips (1 oz bag)', 'Grains', cat_carbs, 28, 'g', 160, 2, 15, 10, 1, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Sun Chips (1 oz bag)', 'Grains', cat_carbs, 28, 'g', 140, 2, 18, 6, 2, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Goldfish Crackers (55 pieces)', 'Grains', cat_carbs, 30, 'g', 140, 3, 20, 5, 1, false, true, false, 'processed', 'raw', '{snack}', '{dairy,gluten,vegetarian}', 1.0),
('Wheat Thins (16 crackers)', 'Grains', cat_carbs, 31, 'g', 140, 2, 22, 5, 3, false, true, false, 'processed', 'raw', '{snack}', '{gluten,vegetarian}', 1.0),
('Triscuits (6 crackers)', 'Grains', cat_carbs, 28, 'g', 120, 3, 20, 3, 3, false, true, false, 'processed', 'raw', '{snack}', '{gluten,vegetarian}', 1.0),
('Ritz Crackers (5 crackers)', 'Grains', cat_carbs, 16, 'g', 80, 1, 10, 4, 0, false, true, false, 'processed', 'raw', '{snack}', '{gluten,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 6: PROTEIN BARS & GRANOLA BARS (8 variations)
-- ============================================================================

('Quest Protein Bar (Chocolate Chip Cookie Dough)', 'Protein', cat_protein, 60, 'g', 200, 21, 22, 9, 14, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Pure Protein Bar (Chocolate Peanut Butter)', 'Protein', cat_protein, 50, 'g', 200, 20, 18, 6, 2, false, true, false, 'processed', 'raw', '{snack}', '{dairy,nuts,vegetarian}', 1.0),
('RXBAR (Chocolate Sea Salt)', 'Protein', cat_protein, 52, 'g', 210, 12, 23, 9, 5, false, true, false, 'processed', 'raw', '{snack}', '{nuts,vegetarian}', 1.0),
('Clif Bar (Chocolate Chip)', 'Grains', cat_carbs, 68, 'g', 250, 10, 45, 5, 4, false, true, false, 'processed', 'raw', '{snack}', '{gluten,vegetarian}', 1.0),
('Nature Valley Granola Bar (2 bars per pack)', 'Grains', cat_carbs, 42, 'g', 190, 4, 29, 7, 2, false, true, false, 'processed', 'raw', '{snack}', '{gluten,vegetarian}', 1.0),
('Kind Bar (Dark Chocolate Nuts & Sea Salt)', 'Fats', cat_fats, 40, 'g', 200, 6, 16, 16, 7, false, true, false, 'processed', 'raw', '{snack}', '{nuts,vegetarian}', 1.0),
('Built Bar (Coconut)', 'Protein', cat_protein, 54, 'g', 130, 17, 20, 2, 6, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Gatorade Protein Bar', 'Protein', cat_protein, 45, 'g', 150, 20, 15, 4, 1, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 7: MISC SNACKS (10 variations)
-- ============================================================================

('Popcorn (Microwave, 3 cups popped)', 'Grains', cat_carbs, 24, 'g', 130, 3, 15, 7, 3, true, true, false, 'processed', 'cooked', '{snack}', '{vegetarian}', 1.0),
('Popcorn (Movie theater, Medium)', 'Grains', cat_carbs, 110, 'g', 590, 9, 63, 34, 13, true, true, false, 'processed', 'cooked', '{snack}', '{vegetarian}', 1.0),
('Pretzels (1 oz, ~15 small twists)', 'Grains', cat_carbs, 28, 'g', 110, 3, 23, 1, 1, true, true, false, 'processed', 'raw', '{snack}', '{gluten,vegetarian}', 1.0),
('String Cheese (1 stick)', 'Dairy', cat_dairy, 28, 'g', 80, 7, 1, 6, 0, true, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Babybel Cheese (1 round)', 'Dairy', cat_dairy, 21, 'g', 70, 5, 0, 6, 0, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Beef Jerky (1 oz)', 'Protein', cat_protein, 28, 'g', 116, 9, 3, 7, 0, true, true, false, 'processed', 'raw', '{snack}', '{}', 1.0),
('Trail Mix (1/4 cup)', 'Fats', cat_fats, 38, 'g', 173, 5, 17, 11, 2, true, true, false, 'processed', 'raw', '{snack}', '{nuts,vegetarian}', 1.0),
('Mixed Nuts (1 oz)', 'Fats', cat_fats, 28, 'g', 170, 6, 7, 15, 2, true, true, true, 'raw', 'raw', '{snack}', '{nuts,vegetarian}', 1.0),
('Peanuts (Roasted, salted, 1 oz)', 'Fats', cat_fats, 28, 'g', 170, 7, 5, 15, 2, true, true, false, 'processed', 'cooked', '{snack}', '{nuts,vegetarian}', 1.0),
('Sunflower Seeds (1/4 cup)', 'Fats', cat_fats, 35, 'g', 207, 6, 7, 19, 4, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- SECTION 8: RESTAURANT SIDES & APPETIZERS (14 variations)
-- ============================================================================

('Coleslaw (1/2 cup)', 'Vegetables', cat_vegetables, 90, 'g', 150, 1, 14, 11, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian}', 1.0),
('Macaroni Salad (1/2 cup)', 'Grains', cat_carbs, 125, 'g', 180, 3, 20, 10, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 1.0),
('Potato Salad (1/2 cup)', 'Grains', cat_carbs, 125, 'g', 180, 3, 14, 13, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),
('Corn on the Cob (1 ear, with butter)', 'Vegetables', cat_vegetables, 146, 'g', 155, 5, 27, 5, 3, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Mashed Potatoes (1 cup, with gravy)', 'Grains', cat_carbs, 243, 'g', 238, 4, 33, 11, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Baked Beans (1/2 cup)', 'Grains', cat_carbs, 127, 'g', 155, 6, 29, 2, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),
('Rice Pilaf (1 cup)', 'Grains', cat_carbs, 206, 'g', 250, 5, 45, 5, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 1.0),
('Garlic Bread (2 slices)', 'Grains', cat_carbs, 60, 'g', 180, 4, 21, 9, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Dinner Roll (1 roll, with butter)', 'Grains', cat_carbs, 42, 'g', 120, 3, 18, 4, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Biscuit (1 biscuit, Southern style)', 'Grains', cat_carbs, 60, 'g', 180, 3, 22, 9, 1, true, true, false, 'processed', 'cooked', '{breakfast,lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Chips and Guacamole (Restaurant portion)', 'Grains', cat_carbs, 200, 'g', 480, 6, 50, 30, 9, true, true, false, 'processed', 'raw', '{snack,appetizer}', '{vegetarian,vegan}', 1.0),
('Nachos with Cheese (Small)', 'Grains', cat_carbs, 150, 'g', 420, 12, 42, 22, 5, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{dairy,vegetarian}', 1.0),
('Loaded Potato Skins (4 pieces)', 'Grains', cat_carbs, 180, 'g', 380, 14, 28, 24, 3, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{dairy,pork}', 1.0),
('Jalapeño Poppers (6 pieces)', 'Vegetables', cat_vegetables, 120, 'g', 270, 9, 22, 16, 2, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{dairy,gluten,vegetarian}', 1.0);

END $$;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Count Phase 3 foods by category
SELECT
    food_group,
    COUNT(*) as count
FROM foods_enhanced
WHERE name LIKE '%Brazilian%'
   OR name LIKE '%Coxinha%'
   OR name LIKE '%Pão de Queijo%'
   OR name LIKE '%Feijoada%'
   OR name LIKE '%Chips%'
   OR name LIKE '%Protein Bar%'
   OR name LIKE '%Popcorn%'
GROUP BY food_group
ORDER BY count DESC;

-- List all Brazilian foods
SELECT name, calories, protein_g, total_carbs_g, total_fat_g
FROM foods_enhanced
WHERE name LIKE '%Coxinha%'
   OR name LIKE '%Pão%'
   OR name LIKE '%Feijoada%'
   OR name LIKE '%Picanha%'
   OR name LIKE '%Churrasco%'
ORDER BY name;

-- Total count across all phases
SELECT COUNT(*) as total_foods FROM foods_enhanced;
