CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    sales INTEGER NOT NULL,
    region TEXT NOT NULL,
    UNIQUE(product, region) -- Example: Ensure unique product/region combinations
);
-- ... rest of the insert statements ...