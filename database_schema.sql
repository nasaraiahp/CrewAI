CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

CREATE TABLE IF NOT EXISTS sales (
    ProductID INT PRIMARY KEY,  -- Add primary key
    Price DECIMAL(10, 2) NOT NULL, -- Add NOT NULL constraint
    LocationName VARCHAR(255) NOT NULL, -- Add NOT NULL constraint
    ProductName VARCHAR(255) NOT NULL -- Add NOT NULL constraint
);

INSERT INTO sales (Price, LocationName, ProductName, ProductID) VALUES
(10.99, 'New York', 'Product A', 1),
(15.50, 'Los Angeles', 'Product B', 2),
(12.75, 'Chicago', 'Product C', 3),
(10.99, 'New York', 'Product D', 4),
(18.20, 'Los Angeles', 'Product E', 5),
(14.00, 'Chicago', 'Product F', 6),
(9.99, 'Houston', 'Product G', 7),
(11.50, 'Houston', 'Product H', 8),
(16.75, 'Miami', 'Product I', 9),
(13.20, 'Miami', 'Product J', 10);