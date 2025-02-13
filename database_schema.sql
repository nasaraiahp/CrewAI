# create_table.sql
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

CREATE TABLE IF NOT EXISTS sales (
    Product_Id INT PRIMARY KEY,
    Product_Name VARCHAR(255),
    Price DECIMAL(10, 2),
    Location_Name VARCHAR(255)
);

INSERT INTO sales (Product_Id, Product_Name, Price, Location_Name) VALUES
    (1, 'Laptop', 1200, 'New York'),
    (2, 'Mouse', 25, 'Los Angeles'),
    (3, 'Keyboard', 75, 'Chicago'),
    (4, 'Monitor', 300, 'New York'),
    (5, 'Webcam', 50, 'Los Angeles'),
    (6, 'Printer', 200, 'Chicago'),
    (7, 'Tablet', 350, 'New York'),
    (8, 'Smartphone', 1000, 'Houston'),
    (9, 'Charger', 20, 'Miami'),
    (10, 'Speaker', 150, 'Dallas');