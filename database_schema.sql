CREATE TABLE IF NOT EXISTS sales (
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    sales_quantity INTEGER NOT NULL
);

INSERT OR IGNORE INTO sales (product, category, sales_quantity) VALUES
('Product A', 'Electronics', 150),
('Product B', 'Clothing', 200),
('Product C', 'Electronics', 120),
('Product D', 'Books', 80),
('Product E', 'Clothing', 250),
('Product F', 'Books', 100);