Use revenue_leakages_db;
SELECT COUNT(*) AS TOTAL_ROWS FROM REVENUE_TRANSACTIONS;
SELECT
    Category,
    ROUND(SUM(Revenue),2) AS Revenue,
    ROUND(SUM(Profit),2) AS Profit,
    ROUND((SUM(Profit)/SUM(Revenue))*100,2) AS Profit_Margin_Pct
FROM revenue_transactions
GROUP BY Category
ORDER BY Profit_Margin_Pct DESC;
SELECT
    Region,
    ROUND(SUM(Profit),2) AS Profit
FROM revenue_transactions
GROUP BY Region
ORDER BY Profit DESC;
SELECT
    ROUND(SUM(ReturnCost),2) AS Return_Leakage,
    ROUND(SUM(Revenue * DiscountPct/100),2) AS Discount_Leakage,
    ROUND(SUM(Revenue),2) AS Revenue,
    ROUND(
        (SUM(ReturnCost) +
            SUM(Revenue * DiscountPct/100)
        ) / SUM(Revenue) * 100
    ,2) AS Leakage_Percentage
FROM revenue_transactions;
SELECT
    OrderID,
    Revenue,
    Profit
FROM revenue_transactions
ORDER BY Revenue DESC
LIMIT 10;
SELECT
    OrderID,
    Revenue,
    Cost,
    Profit
FROM revenue_transactions
ORDER BY Profit ASC
LIMIT 10;
SELECT
    Region,
    SUM(Profit) AS Profit,
    RANK() OVER(
        ORDER BY SUM(Profit) DESC
    ) AS Region_Rank
FROM revenue_transactions
GROUP BY Region;
WITH customer_profit AS (
    SELECT
        CustomerID,
        SUM(Revenue) AS Revenue,
        SUM(Profit) AS Profit
    FROM revenue_transactions
    GROUP BY CustomerID
)
SELECT *
FROM customer_profit
ORDER BY Profit DESC;
SELECT
    CustomerID,
    SUM(Profit) AS Profit,
    RANK() OVER(
        ORDER BY SUM(Profit) DESC
    ) AS Customer_Rank
FROM revenue_transactions
GROUP BY CustomerID;
SELECT
    CustomerID,
    COUNT(OrderID) AS Orders,
    ROUND(SUM(Revenue),2) AS Lifetime_Revenue,
    ROUND(SUM(Profit),2) AS Lifetime_Profit
FROM revenue_transactions
GROUP BY CustomerID
ORDER BY Lifetime_Profit DESC;
SELECT
    Region,
    ROUND(
        SUM(ReturnCost)
        + SUM(Revenue*DiscountPct/100)
    ,2) AS Total_Leakage,
    RANK() OVER(
        ORDER BY
        SUM(ReturnCost)
        + SUM(Revenue*DiscountPct/100)
        DESC
    ) AS Leakage_Rank
FROM revenue_transactions
GROUP BY Region;
SELECT
    Category,
    ROUND(SUM(Revenue),2) AS Revenue,
    ROUND(SUM(Profit),2) AS Profit
FROM revenue_transactions
GROUP BY Category
HAVING SUM(Profit) < 0;