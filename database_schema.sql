CREATE TABLE IF NOT EXISTS sales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product TEXT NOT NULL,
  sales INTEGER NOT NULL
);

INSERT INTO sales (product, sales) VALUES
('Product A', 150),
('Product B', 200),
('Product C', 100),
('Product A', 50),
('Product B', 75),
('Product D', 120);