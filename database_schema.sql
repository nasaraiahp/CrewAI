-- schema.sql
CREATE TABLE IF NOT EXISTS sales (
    product TEXT NOT NULL,
    sales_amount REAL NOT NULL
);

INSERT OR IGNORE INTO sales (product, sales_amount) VALUES
('Product A', 1500),
('Product B', 2200),
('Product C', 1800),
('Product D', 2500),
('Product E', 1200);