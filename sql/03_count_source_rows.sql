USE sample;
GO

SELECT 'customer' AS TableName, COUNT(*) AS TotalRows FROM customer
UNION ALL
SELECT 'city', COUNT(*) FROM city
UNION ALL
SELECT 'state', COUNT(*) FROM state
UNION ALL
SELECT 'account', COUNT(*) FROM account
UNION ALL
SELECT 'branch', COUNT(*) FROM branch
UNION ALL
SELECT 'transaction_db', COUNT(*) FROM transaction_db;