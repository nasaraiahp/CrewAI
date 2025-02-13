CREATE TABLE Sales (
    SaleID INT PRIMARY KEY AUTO_INCREMENT,
    Product VARCHAR(255),
    Region VARCHAR(255),
    SaleDate DATE,
    Quantity INT,
    UnitPrice DECIMAL(10, 2)
);

INSERT INTO Sales (Product, Region, SaleDate, Quantity, UnitPrice) VALUES
('Product A', 'North', '2024-01-15', 10, 25.50),
('Product B', 'East', '2024-02-20', 5, 120.00),
('Product A', 'West', '2024-03-10', 20, 25.50),
('Product C', 'South', '2024-04-05', 15, 50.00),
('Product B', 'North', '2024-05-25', 8, 120.00),
('Product A', 'East', '2024-06-18', 12, 25.50),
('Product C', 'West', '2024-07-02', 25, 50.00),
('Product B', 'South', '2024-08-12', 10, 120.00);


-- Example Queries
-- Total Sales by Product
SELECT Product, SUM(Quantity * UnitPrice) AS TotalSalesValue
FROM Sales
GROUP BY Product;

-- Sales by Region
SELECT Region, SUM(Quantity * UnitPrice) AS TotalSalesValue
FROM Sales
GROUP BY Region;

-- Sales Trend over Time (Monthly)
SELECT DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth, SUM(Quantity * UnitPrice) AS MonthlySales
FROM Sales
GROUP BY SaleMonth
ORDER BY SaleMonth;