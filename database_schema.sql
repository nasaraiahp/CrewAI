-- schema.sql
CREATE TABLE IF NOT EXISTS sales (
    product TEXT PRIMARY KEY,
    sales INTEGER
);

INSERT OR IGNORE INTO sales (product, sales) VALUES
('Product A', 100),
('Product B', 150),
('Product C', 75),
('Product D', 200),
('Product E', 120);