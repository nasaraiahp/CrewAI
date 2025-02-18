-- schema.sql
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    product TEXT UNIQUE,  -- Added UNIQUE constraint
    sales_quantity INTEGER
);