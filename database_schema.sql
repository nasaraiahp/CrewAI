CREATE TABLE sales (
    Price REAL,
    LocationName TEXT,
    ProductName TEXT,
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT -- Added primary key and autoincrement
);

INSERT INTO sales (Price, LocationName, ProductName) VALUES -- Removed ProductID from insert to utilize autoincrement
(10.5, 'New York', 'Laptop'),
(25, 'London', 'Tablet'),
(15, 'New York', 'Mouse'),
(30, 'Paris', 'Keyboard'),
(20, 'London', 'Monitor'),
(12, 'New York', 'Webcam'),
(35, 'Paris', 'Printer'),
(18, 'London', 'Charger'),
(22, 'New York', 'Speaker'),
(28, 'Paris', 'Headset');


-- Example query for plotting Price Count vs. Location Name:
SELECT LocationName, COUNT(*) AS PriceCount
FROM sales
GROUP BY LocationName;