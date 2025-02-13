CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100) UNIQUE,  -- Adjust length as needed
    -- Other product details...
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY,
    ProductID INT,
    Quantity INT UNSIGNED, -- If quantities are never negative
    Price DECIMAL(10, 2),
    SaleDate DATE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE INDEX idx_sales_saledate ON Sales (SaleDate);
CREATE INDEX idx_sales_productid ON Sales (ProductID);