# schema.sql
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    product TEXT NOT NULL PRIMARY KEY,
    sales_quantity INTEGER
);