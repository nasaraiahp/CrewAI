CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    sale_date DATE NOT NULL,
    quantity INT NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    INDEX product_idx (product)  -- Index for faster queries on product
);

INSERT INTO sales (product, sale_date, quantity, revenue) VALUES
('Product A', '2024-01-05', 10, 250.00),
('Product B', '2024-01-05', 5, 120.00),
('Product A', '2024-01-12', 15, 375.00),
('Product C', '2024-01-12', 8, 200.00),
('Product B', '2024-01-19', 7, 175.00),
('Product A', '2024-01-19', 12, 300.00),
('Product C', '2024-01-26', 10, 250.00),
('Product B', '2024-01-26', 6, 150.00);