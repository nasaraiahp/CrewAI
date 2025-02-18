-- create_tables.sql (no changes)
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    region TEXT NOT NULL,
    sales INTEGER NOT NULL
);


-- populate_data.sql (no changes)
INSERT INTO sales (product, region, sales) VALUES
('Product A', 'North', 1000),
('Product B', 'North', 1500),
('Product C', 'South', 2000),
('Product A', 'South', 1200),
('Product B', 'East', 800),
('Product C', 'East', 1800),
('Product A', 'West', 1500),
('Product B', 'West', 2200),
('Product C', 'North', 900);