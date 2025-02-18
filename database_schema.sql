CREATE TABLE sales (
    product_id INTEGER PRIMARY KEY, -- Removed AUTOINCREMENT for clarity; INTEGER PRIMARY KEY implies AUTOINCREMENT in SQLite
    product_name TEXT NOT NULL CHECK (length(product_name) > 0), -- Add a check for non-empty product names
    category TEXT NOT NULL CHECK (length(category) > 0), -- Add a check for non-empty categories
    sales_quantity INTEGER NOT NULL CHECK (sales_quantity >= 0), -- Ensure sales quantity is non-negative
    sales_revenue REAL NOT NULL CHECK (sales_revenue >= 0) -- Ensure sales revenue is non-negative
);

INSERT INTO sales (product_name, category, sales_quantity, sales_revenue) VALUES
('Product A', 'Electronics', 120, 25000.00),
('Product B', 'Clothing', 200, 15000.00),
('Product C', 'Books', 80, 8000.00),
('Product D', 'Electronics', 150, 30000.00),
('Product E', 'Clothing', 250, 20000.00),
('Product F', 'Books', 50, 4000.00),
('Product G', 'Electronics', 100, 22000.00),
('Product H', 'Clothing', 180, 12000.00);