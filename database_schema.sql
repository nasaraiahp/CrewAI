-- schema.sql
CREATE TABLE IF NOT EXISTS sales (
    product TEXT NOT NULL,
    sales_quantity INTEGER NOT NULL,
    sales_region TEXT NOT NULL
);