CREATE TABLE Sales (
    Region VARCHAR(50) NOT NULL CHECK (Region IN ('North', 'South', 'East', 'West')), -- Enforce valid regions
    Product VARCHAR(50) NOT NULL CHECK (Product IN ('A', 'B', 'C')), -- Enforce valid products
    Sales INT NOT NULL CHECK (Sales >= 0) -- Ensure sales are non-negative
);

-- Use parameterized INSERT statements to prevent SQL injection (though not strictly necessary here as values are hardcoded)
INSERT INTO Sales (Region, Product, Sales) VALUES
('North', 'A', 1000), ('North', 'B', 1500), ('South', 'A', 2000),
('South', 'C', 1200), ('East', 'B', 800), ('East', 'C', 1800),
('West', 'A', 1100), ('West', 'B', 900), ('West', 'C', 2500);

-- The existing queries are generally fine.  Adding indexes could improve performance if the dataset is large.
CREATE INDEX idx_region ON Sales (Region);
CREATE INDEX idx_product ON Sales (Product);