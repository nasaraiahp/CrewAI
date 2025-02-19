CREATE TABLE IF NOT EXISTS sales (
    product TEXT PRIMARY KEY,
    sales INTEGER
);

INSERT OR REPLACE INTO sales (product, sales) VALUES
('Product A', 150),
('Product B', 200),
('Product C', 100),
('Product D', 250),
('Product E', 180);