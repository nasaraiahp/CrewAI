CREATE TABLE SalesData (
    SalesID INT PRIMARY KEY AUTO_INCREMENT, -- Add a primary key for better data management
    Region VARCHAR(50) NOT NULL,
    Product VARCHAR(50) NOT NULL,
    Sales DECIMAL(10, 2) NOT NULL, -- Use DECIMAL for currency values
    SalesDate DATE NOT NULL,
    INDEX RegionIndex (Region),  -- Index for faster queries by region
    INDEX ProductIndex (Product), -- Index for faster queries by product
    INDEX SalesDateIndex (SalesDate) -- Index for faster queries by date
);