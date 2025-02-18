CREATE TABLE IF NOT EXISTS sales (
    product TEXT NOT NULL,
    region TEXT NOT NULL,
    sales INTEGER NOT NULL
);

-- Wrap INSERTs in a transaction for efficiency
BEGIN TRANSACTION;
INSERT INTO sales (product, region, sales) VALUES
-- ... (rest of the insert statements)
COMMIT;