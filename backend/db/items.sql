-- =========================================
-- 1. CREATE TABLES
-- =========================================

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    price INT NOT NULL,
    unit VARCHAR(50) NOT NULL
);

-- =========================================
-- 2. ENABLE ROW LEVEL SECURITY
-- =========================================

ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- =========================================
-- 3. POLICIES (READ ONLY FOR FRONTEND)
-- =========================================

CREATE POLICY "Public can read categories"
ON categories
FOR SELECT
USING (true);

CREATE POLICY "Public can read items"
ON items
FOR SELECT
USING (true);
