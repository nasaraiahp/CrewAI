-- Create the table (add primary key or unique constraint if applicable)
CREATE TABLE Sales (
    SalesID INT PRIMARY KEY AUTO_INCREMENT, -- Added a primary key
    Region VARCHAR(50) NOT NULL,
    Product VARCHAR(50) NOT NULL,
    Sales INT NOT NULL,
    Date DATE NOT NULL
);

-- Insert sample data
INSERT INTO Sales (Region, Product, Sales, Date) VALUES
('North', 'A', 100, '2023-01-01'),
('North', 'B', 150, '2023-01-01'),
('South', 'A', 200, '2023-01-01'),
('South', 'B', 250, '2023-01-01'),
('North', 'A', 120, '2023-01-08'),
('North', 'B', 180, '2023-01-08'),
('South', 'A', 220, '2023-01-08'),
('South', 'B', 280, '2023-01-08');


-- Queries for charts (using aliases for clarity)
-- Query 1: Total sales by region
SELECT Region, SUM(Sales) AS TotalSalesByRegion FROM Sales GROUP BY Region;

-- Query 2: Total sales by product
SELECT Product, SUM(Sales) AS TotalSalesByProduct FROM Sales GROUP BY Product;

-- Query 3: Sales trend over time
SELECT Date, SUM(Sales) AS TotalSalesByDate FROM Sales GROUP BY Date ORDER BY Date;

-- Query 4: Average sales per region per product
SELECT Region, Product, AVG(Sales) AS AverageSalesByRegionProduct
FROM Sales 
GROUP BY Region, Product;