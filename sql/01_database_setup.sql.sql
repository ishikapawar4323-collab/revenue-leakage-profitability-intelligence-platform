
Use Revenue_Leakages_db;
Show Databases;

Drop database revenue_leakages;
Show databases;
Use revenue_leakages_db;
CREATE TABLE revenue_transactions (
    OrderID INT PRIMARY KEY,
    OrderDate DATETIME,
    CustomerID INT,
    Region VARCHAR(50),
    Category VARCHAR(100),
    Revenue DECIMAL(12,2),
    DiscountPct DECIMAL(5,2),
    Cost DECIMAL(12,2),
    FreightCost DECIMAL(12,2),
    Returned INT,
    ReturnCost DECIMAL(12,2),
    Profit DECIMAL(12,2)
);
Show tables;
Describe revenue_transactions;
Show tables;
SELECT DATABASE();
SHOW TABLES;
Drop Table revenue_transactions;
CREATE TABLE revenue_transactions (
    OrderID INT PRIMARY KEY,
    OrderDate DOUBLE,
    CustomerID INT,
    Region VARCHAR(50),
    Category VARCHAR(100),
    Revenue DECIMAL(12,2),
    DiscountPct DECIMAL(5,2),
    Cost DECIMAL(12,2),
    FreightCost DECIMAL(12,2),
    Returned INT,
    ReturnCost DECIMAL(12,2),
    Profit DECIMAL(12,2)
);



