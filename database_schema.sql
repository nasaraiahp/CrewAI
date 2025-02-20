-- sales_data.db (SQLite database schema and dummy data)

CREATE TABLE sales (
    product TEXT PRIMARY KEY,
    sales INTEGER
);

-- Example table for regional sales, adjust as needed.
CREATE TABLE regional_sales (
    region TEXT,
    sales INTEGER
);


INSERT INTO sales (product, sales) VALUES
('Product A', 1500),
('Product B', 1200),
('Product C', 800),
('Product D', 2000),
('Product E', 1600);

-- Add example data for Regional sales. Relate it to your 'sales' data or adapt as necessary for your project.
INSERT INTO regional_sales (region, sales) VALUES
('North', 500), ('North', 750),
('South', 400), ('South', 650),
('East', 300), ('East', 550),
('West', 700), ('West', 750); -- Example data