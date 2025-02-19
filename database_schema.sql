-- sales_data.sql (MySQL table creation and data insertion)
CREATE DATABASE IF NOT EXISTS sales_dashboard;
USE sales_dashboard;

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    sales_date DATE NOT NULL,
    quantity INT NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    KEY idx_sales_date (sales_date),  -- Index for faster date-based queries
    KEY idx_product (product)      -- Index for faster product-based queries
);

INSERT INTO sales (product, sales_date, quantity, revenue) VALUES
('Product A', '2024-01-05', 10, 250.00),
('Product B', '2024-01-05', 5, 150.00),
('Product A', '2024-01-12', 15, 375.00),
('Product C', '2024-01-12', 20, 400.00),
('Product B', '2024-01-19', 8, 240.00),
('Product A', '2024-01-19', 12, 300.00),
('Product C', '2024-01-26', 25, 500.00),
('Product B', '2024-01-26', 10, 300.00);