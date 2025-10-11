-- ============================================================================
-- MIGRATION 028: SEED BRAZILIAN DAIRY (LATICÍNIOS)
-- ============================================================================
-- Description: Common dairy products in Brazil with Portuguese names
-- Total items: ~40 items
-- Categories: Leites, Queijos, Iogurtes, Requeijão, Manteiga
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

-- LEITES (MILK)
('Leite Integral', 'ingredient', 'Whole milk',
    100, 'g', 'copo (244g)', 244,
    61, 3.2, 4.8, 3.3,
    0, 5.1, 1.9, 10,
    44, 143, 113, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.96, false),

('Leite Desnatado', 'ingredient', 'Skim milk',
    100, 'g', 'copo (245g)', 245,
    34, 3.4, 5, 0.2,
    0, 5.1, 0.1, 2,
    42, 156, 122, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.96, false),

('Leite Semidesnatado', 'ingredient', 'Low-fat milk',
    100, 'g', 'copo (244g)', 244,
    50, 3.3, 4.9, 2,
    0, 5.1, 1.2, 8,
    44, 150, 119, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.96, false),

('Leite Condensado', 'ingredient', 'Sweetened condensed milk',
    100, 'g', 'colher sopa (20g)', 20,
    321, 7.9, 54.4, 8.7,
    0, 54.4, 5.5, 34,
    127, 371, 284, 0.19,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Leite em Pó Integral', 'ingredient', 'Whole milk powder',
    100, 'g', 'colher sopa (8g)', 8,
    496, 26.3, 38.4, 26.7,
    0, 38.4, 16.7, 97,
    371, 1330, 912, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Leite Longa Vida Integral', 'ingredient', 'UHT whole milk',
    100, 'g', 'copo (244g)', 244,
    59, 3.1, 4.7, 3.2,
    0, 4.7, 1.9, 11,
    43, 140, 110, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.96, false),

-- QUEIJOS (CHEESE)
('Queijo Minas Frescal', 'ingredient', 'Fresh Minas cheese',
    100, 'g', 'fatia (30g)', 30,
    264, 17.4, 3.1, 20.8,
    0, 0.4, 13.4, 63,
    214, 54, 579, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Queijo Minas Padrão (Curado)', 'ingredient', 'Aged Minas cheese',
    100, 'g', 'fatia (30g)', 30,
    361, 24.4, 4, 28,
    0, 0.5, 17.9, 85,
    513, 71, 770, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Queijo Prato', 'ingredient', 'Prato cheese',
    100, 'g', 'fatia (30g)', 30,
    360, 25.6, 1.7, 28.5,
    0, 0, 17.9, 88,
    490, 90, 632, 0.4,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Queijo Mussarela', 'ingredient', 'Mozzarella cheese',
    100, 'g', 'fatia (28g)', 28,
    280, 27.5, 2.2, 17.1,
    0, 1.2, 10.9, 79,
    627, 95, 731, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.96, false),

('Queijo Parmesão Ralado', 'ingredient', 'Grated Parmesan cheese',
    100, 'g', 'colher sopa (5g)', 5,
    431, 38.5, 4.1, 28.6,
    0, 0.8, 19, 88,
    1602, 125, 1184, 0.82,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.96, false),

('Queijo Coalho', 'ingredient', 'Coalho cheese (grilling cheese)',
    100, 'g', 'espeto (60g)', 60,
    313, 22.8, 1.9, 24,
    0, 0, 15.4, 72,
    738, 62, 568, 0.3,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Queijo Parmesão em Lascas', 'ingredient', 'Shaved Parmesan cheese',
    100, 'g', 'lasca (10g)', 10,
    392, 35.8, 3.2, 25.8,
    0, 0.9, 17.3, 68,
    1529, 120, 1109, 0.82,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('Queijo Provolone', 'ingredient', 'Provolone cheese',
    100, 'g', 'fatia (28g)', 28,
    351, 25.6, 2.1, 26.6,
    0, 0.6, 17.1, 69,
    876, 138, 756, 0.52,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Queijo Gorgonzola', 'ingredient', 'Gorgonzola blue cheese',
    100, 'g', 'fatia (28g)', 28,
    353, 21.4, 2.3, 28.7,
    0, 0, 18.5, 70,
    1395, 256, 528, 0.43,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Queijo Cottage', 'ingredient', 'Cottage cheese',
    100, 'g', 'xícara (226g)', 226,
    98, 11.1, 3.4, 4.3,
    0, 2.7, 2.7, 17,
    364, 104, 83, 0.07,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.95, false),

('Queijo Ricota', 'ingredient', 'Ricotta cheese',
    100, 'g', 'fatia (40g)', 40,
    174, 11.3, 3.4, 13,
    0, 0.3, 8.3, 51,
    84, 125, 207, 0.44,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('Queijo Cream Cheese (Requeijão Cremoso)', 'ingredient', 'Cream cheese',
    100, 'g', 'colher sopa (15g)', 15,
    349, 5.9, 5.5, 34.9,
    0, 3.9, 21.9, 110,
    321, 138, 98, 0.38,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

-- REQUEIJÃO E CREMES
('Requeijão Cremoso', 'ingredient', 'Brazilian creamy cheese spread',
    100, 'g', 'colher sopa (15g)', 15,
    270, 9, 6, 24,
    0, 0, 15, 70,
    420, 90, 180, 0.2,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.94, false),

('Requeijão de Corte', 'ingredient', 'Sliceable requeijão cheese',
    100, 'g', 'fatia (30g)', 30,
    313, 18.8, 3.8, 25,
    0, 0, 16, 75,
    580, 95, 420, 0.25,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

('Catupiry Original', 'ingredient', 'Catupiry cream cheese',
    100, 'g', 'colher sopa (15g)', 15,
    243, 11.4, 4.3, 20,
    0, 0, 12.9, 64,
    486, 86, 271, 0.14,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- IOGURTES (YOGURT)
('Iogurte Natural Integral', 'ingredient', 'Whole milk plain yogurt',
    100, 'g', 'pote (170g)', 170,
    61, 3.5, 4.7, 3.3,
    0, 4.7, 2.1, 13,
    46, 155, 121, 0.05,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.96, false),

('Iogurte Natural Desnatado', 'ingredient', 'Low-fat plain yogurt',
    100, 'g', 'pote (170g)', 170,
    56, 5.7, 7.7, 0.2,
    0, 7.7, 0.1, 2,
    77, 255, 199, 0.09,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.96, false),

('Iogurte Grego Natural', 'ingredient', 'Greek yogurt plain',
    100, 'g', 'pote (170g)', 170,
    97, 9, 3.9, 5,
    0, 3.3, 3.2, 13,
    36, 141, 110, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('Iogurte com Frutas', 'ingredient', 'Fruit-flavored yogurt',
    100, 'g', 'pote (170g)', 170,
    85, 3.5, 14.8, 1.4,
    0, 13.8, 0.9, 6,
    60, 164, 127, 0.06,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Iogurte com Mel', 'ingredient', 'Honey yogurt',
    100, 'g', 'pote (170g)', 170,
    91, 3.3, 16.3, 1.5,
    0, 15.8, 0.9, 6,
    58, 158, 122, 0.05,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

('Yakult Original', 'ingredient', 'Yakult probiotic drink',
    100, 'g', 'frasco (80ml)', 80,
    65, 1.1, 14.7, 0,
    0, 14, 0, 0,
    30, 50, 40, 0.1,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

-- MANTEIGA E CREMES (BUTTER AND CREAM)
('Manteiga com Sal', 'ingredient', 'Salted butter',
    100, 'g', 'colher sopa (14g)', 14,
    717, 0.9, 0.1, 81.1,
    0, 0.1, 51.4, 215,
    714, 24, 24, 0.02,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.96, false),

('Manteiga sem Sal', 'ingredient', 'Unsalted butter',
    100, 'g', 'colher sopa (14g)', 14,
    717, 0.9, 0.1, 81.1,
    0, 0.1, 51.4, 215,
    11, 24, 24, 0.02,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.96, false),

('Margarina', 'ingredient', 'Margarine',
    100, 'g', 'colher sopa (14g)', 14,
    719, 0.2, 0.9, 80.5,
    0, 0.1, 15.5, 0,
    943, 42, 30, 0,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.95, false),

('Margarina Light', 'ingredient', 'Light margarine',
    100, 'g', 'colher sopa (14g)', 14,
    360, 0.2, 1, 40,
    0, 0, 8, 0,
    714, 40, 28, 0,
    ARRAY['soy'], ARRAY['vegan', 'vegetarian', 'gluten-free'], 'user', 0.94, false),

('Creme de Leite Fresco', 'ingredient', 'Heavy cream',
    100, 'g', 'colher sopa (15g)', 15,
    340, 2.1, 2.8, 36.1,
    0, 2.8, 22.5, 137,
    38, 75, 65, 0.03,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.95, false),

('Creme de Leite (Caixinha)', 'ingredient', 'Table cream (boxed)',
    100, 'g', 'caixinha (200g)', 200,
    193, 2.4, 4.8, 19.3,
    0, 3.4, 12.1, 61,
    51, 87, 77, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Nata', 'ingredient', 'Clotted cream',
    100, 'g', 'colher sopa (15g)', 15,
    450, 1.5, 2, 48,
    0, 2, 30, 180,
    40, 60, 50, 0.02,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.93, false),

-- LEITE FERMENTADO
('Coalhada', 'ingredient', 'Curdled milk drink',
    100, 'g', 'copo (200ml)', 200,
    50, 3.2, 6.2, 1.5,
    0, 6.2, 1, 8,
    45, 150, 115, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Kefir', 'ingredient', 'Kefir fermented milk',
    100, 'g', 'copo (240ml)', 240,
    44, 3.3, 4.5, 1.5,
    0.2, 4.5, 1, 8,
    40, 164, 120, 0.04,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.93, false),

-- DOCE DE LEITE
('Doce de Leite', 'ingredient', 'Dulce de leche',
    100, 'g', 'colher sopa (20g)', 20,
    315, 6.8, 55.5, 7.4,
    0, 55.5, 4.6, 24,
    129, 324, 251, 0.17,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false),

('Doce de Leite Pastoso', 'ingredient', 'Soft dulce de leche',
    100, 'g', 'colher sopa (20g)', 20,
    308, 6.5, 53.8, 7.2,
    0, 53.8, 4.5, 23,
    125, 318, 245, 0.16,
    ARRAY['dairy'], ARRAY['vegetarian', 'gluten-free'], 'user', 0.94, false);

COMMIT;

SELECT '✅ BRAZILIAN DAIRY SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Leite Integral', 'Queijo Minas Frescal', 'Iogurte Natural Integral', 'Requeijão Cremoso');
