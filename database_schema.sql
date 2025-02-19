-- sales_data.db (SQLite database schema - no security changes needed for this simple example)
CREATE TABLE sales_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    sales INTEGER NOT NULL
);

INSERT INTO sales_data (product, sales) VALUES
('Product A', 1500),
('Product B', 1200),
('Product C', 2000),
('Product D', 800),
('Product E', 1600);