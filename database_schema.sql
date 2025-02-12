-- Create the table (Improved)
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY AUTO_INCREMENT, -- Add a primary key for efficient indexing and referencing
    Region VARCHAR(50) NOT NULL CHECK (Region IN ('North', 'South', 'East', 'West')), -- Constrain region values for data integrity
    Product VARCHAR(50) NOT NULL,
    Sales DECIMAL(10, 2) NOT NULL CHECK (Sales >= 0), -- Use DECIMAL for monetary values and ensure non-negative sales
    SaleDate DATE -- Add a date column to track sales over time
);


-- Insert data (Improved) - Example with SaleDate
INSERT INTO Sales (Region, Product, Sales, SaleDate) VALUES
('North', 'A', 1000.00, '2024-01-15'),
('North', 'B', 1500.00, '2024-01-20'),
('South', 'A', 2000.00, '2024-01-10'),
...


-- Queries (Improved - Example using SaleDate for more insightful analysis)

-- Query 1: Total Sales by Region and Month
SELECT Region, DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth, SUM(Sales) AS TotalSales
FROM Sales
GROUP BY Region, SaleMonth
ORDER BY Region, SaleMonth;

-- Query 2: Total Sales by Product and Month
SELECT Product, DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth, SUM(Sales) AS TotalSales
FROM Sales
GROUP BY Product, SaleMonth
ORDER BY Product, SaleMonth;

-- Query 3: Sales by Region, Product and Month
SELECT Region, Product, DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth, SUM(Sales) AS TotalSales
FROM Sales
GROUP BY Region, Product, SaleMonth
ORDER BY Region, Product, SaleMonth;

-- Query 4: Average Sales by Region and Month
SELECT Region, DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth, AVG(Sales) AS AverageSales
FROM Sales
GROUP BY Region, SaleMonth
ORDER BY Region, SaleMonth;