-- schema.sql
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_category TEXT NOT NULL,
    region TEXT NOT NULL,
    sales REAL NOT NULL
);

INSERT INTO sales (product_category, region, sales) VALUES
('Electronics', 'North', 1200),
('Electronics', 'East', 1800),
('Furniture', 'North', 800),
('Furniture', 'West', 1500),
('Clothing', 'South', 2200),
('Clothing', 'East', 1000),
('Electronics', 'West', 2500),
('Furniture', 'South', 1100),
('Clothing', 'North', 1400);