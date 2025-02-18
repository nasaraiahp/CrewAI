-- sales_data.sql (SQLite database schema and data)

CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_category TEXT NOT NULL,
    sales_amount REAL NOT NULL,
    sales_region TEXT NOT NULL,
    sale_date DATE 
);

INSERT OR IGNORE INTO sales (product_name, product_category, sales_amount, sales_region, sale_date) VALUES
('Product A', 'Electronics', 1200, 'North', '2024-01-05'),
('Product B', 'Clothing', 800, 'East', '2024-01-12'),
('Product C', 'Electronics', 1500, 'West', '2024-01-19'),
('Product D', 'Furniture', 2000, 'South', '2024-01-26'),
('Product E', 'Clothing', 900, 'North', '2024-02-02'),
('Product F', 'Electronics', 1100, 'East', '2024-02-09'),
('Product G', 'Furniture', 1700, 'West', '2024-02-16'),
('Product H', 'Clothing', 750, 'South', '2024-02-23'),
('Product I', 'Electronics', 1400, 'North', '2024-03-01'),
('Product J', 'Furniture', 1900, 'East', '2024-03-08');