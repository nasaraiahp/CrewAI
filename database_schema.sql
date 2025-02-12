-- No significant changes needed.  Using UPPERCASE for SQL keywords is common practice for readability.
CREATE TABLE Sales (
    Region VARCHAR(50) NOT NULL,
    Product VARCHAR(50) NOT NULL,
    Sales INT NOT NULL
);

INSERT INTO Sales (Region, Product, Sales) VALUES
('North', 'A', 100),
('North', 'B', 150),
('South', 'A', 200),
('South', 'B', 120),
('East', 'A', 80),
('East', 'B', 100),
('West', 'A', 180),
('West', 'B', 90);

-- Queries remain the same. Consider adding indexes if the Sales table becomes very large.