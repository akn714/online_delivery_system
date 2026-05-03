-- =========================================
-- 1. SEED CATEGORIES
-- =========================================

INSERT INTO categories (name) VALUES
('Grocery'),
('Stationary'),
('Fruits'),
('Non-Veg');

-- =========================================
-- 2. ADD GROCERY ITEMS
-- =========================================

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'White Bread', 20, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Bhuja Chana', 27, '250gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Maggie (Small - 75g)', 15, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Maggie (Family Pack - 400g)', 56, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Moongfali', 42, '250gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Soyabean (Packet)', 10, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Soyabean (Open - Small)', 27, '250gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Macaroni / Pasta', 20, '250gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Sugar (Chini)', 15, '250gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Glucose D (200g)', 56, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Glucose D (400g)', 89, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Jam (Small)', 25, 'box' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Jam (Big)', 90, 'bottle' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Colgate (Small)', 20, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Colgate (Medium)', 70, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Colgate (Big)', 130, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Closeup (Small)', 20, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Closeup (Big)', 55, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Sensodyne Toothpaste', 140, 'piece' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Coffee (Nescafe - 50g)', 10, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Coffee (Nescafe - 100g)', 124, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Coffee (Nescafe - 200g)', 235, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Mustard Oil (Sarso Tel)', 180, 'liter' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Fortune Oil', 190, 'liter' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Garam Masala (Whole)', 20, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Garam Masala (Packet)', 10, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Kacha Chana', 80, 'kg' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Makhana', 130, '100 gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Kaju (Cashew)', 100, '100 gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Badam (Almond)', 100, '100 gm' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pista (Packet)', 350, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Lassi (250ml)', 24, 'tetrapack' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Buttermilk (200ml)', 14, 'packet' FROM categories WHERE name='Grocery';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Buttermilk (1L)', 65, 'packet' FROM categories WHERE name='Grocery';

-- =========================================
-- 3. ADD STATIONARY ITEMS
-- =========================================

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Practical File (Physics - 30 Pages)', 30, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Practical File (Physics - 60 Pages)', 60, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Practical File (Chemistry - 30 Pages)', 30, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Practical File (Chemistry - 60 Pages)', 60, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Practical File (General - 30 Pages)', 30, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Practical File (General - 60 Pages)', 60, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pen (Blue, Cheap)', 4, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pen (Black, Cheap)', 4, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pen (Blue, Medium)', 5, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pen (Black, Medium)', 5, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pen (Blue, Good)', 10, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pen (Black, Good)', 10, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pencil', 5, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Eraser', 5, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Sharpener', 5, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Drawing Book (A3 - 36 pages)', 90, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Drawing Book (A3 - 56 pages)', 110, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'A4 Size Pages (500 sheets)', 200, 'pack' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Stapler', 50, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Staple Pins', 10, 'box' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Sticky Notes', 20, 'pack' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Fevicol (Small)', 10, 'bottle' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Fevicol (Medium)', 20, 'bottle' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Fevicol (Big)', 50, 'bottle' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Double-Sided Tape (Small)', 5, 'roll' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Double-Sided Tape (Big)', 10, 'roll' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Spiral Notebook (Plain - 100 Pages)', 80, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Spiral Notebook (Plain - 200 Pages)', 100, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Spiral Notebook (Lined - 100 Pages)', 80, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Register (A4 Rough - 100 Pages)', 30, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Register (A4 Rough - 200 Pages)', 40, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Graph Book', 10, 'piece' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Cello Tape', 5, 'roll' FROM categories WHERE name='Stationary';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Highlighter', 20, 'piece' FROM categories WHERE name='Stationary';

-- =========================================
-- 4. ADD FRUITS
-- =========================================

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Banana', 40, 'kg' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Pomegranate (Anaar)', 80, '500gm' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Mango', 100, 'kg' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Apple', 100, '500gm' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Papaya (Papita)', 60, 'kg' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Kiwi', 50, 'piece' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Coconut (Nariyal)', 70, 'piece' FROM categories WHERE name='Fruits';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Grapes (Angoor)', 40, '250gm' FROM categories WHERE name='Fruits';

-- =========================================
-- 5. ADD NON-VEG
-- =========================================

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Eggs (30 pieces)', 180, 'tray' FROM categories WHERE name='Non-Veg';

INSERT INTO items (category_id, name, price, unit)
SELECT id, 'Raw Chicken (500g)', 120, 'packet' FROM categories WHERE name='Non-Veg';