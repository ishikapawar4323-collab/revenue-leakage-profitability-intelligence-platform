
SELECT COUNT(*) AS TOTAL_ROWS FROM REVENUE_TRANSACTIONS;
SELECT *
FROM revenue_transactions
LIMIT 10;
SELECT
MIN(OrderDate),
MAX(OrderDate)
FROM revenue_transactions;