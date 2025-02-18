CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    sales INTEGER NOT NULL
);

INSERT INTO sales (product, sales) VALUES
('Product A', 150),
('Product B', 200),
('Product C', 120),
('Product A', 80),
('Product B', 100),
('Product D', 250);