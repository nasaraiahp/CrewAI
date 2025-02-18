CREATE TABLE IF NOT EXISTS sales (
    product TEXT,
    category TEXT,
    sales_quantity INTEGER
);

DELETE FROM sales; -- Clear existing data for demo

INSERT INTO sales VALUES
    ('Product A', 'Electronics', 150),
    ('Product B', 'Clothing', 200),
    ('Product C', 'Electronics', 100),
    ('Product D', 'Books', 120),
    ('Product E', 'Clothing', 80);