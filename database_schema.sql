CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

CREATE TABLE IF NOT EXISTS sales_data (
    product VARCHAR(255) NOT NULL,
    sales INT NOT NULL,
    sale_date DATE -- Add a date column to track sales over time
);

INSERT INTO sales_data (product, sales, sale_date) VALUES
('Product A', 1200, '2024-01-05'),  -- Example dates
('Product B', 850, '2024-01-05'),
('Product C', 1550, '2024-01-06'),
('Product D', 900, '2024-01-06'),
('Product E', 1100, '2024-01-07');