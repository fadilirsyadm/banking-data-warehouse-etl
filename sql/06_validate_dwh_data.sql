USE DWH;
GO

SELECT 'DimCustomer' AS TableName, COUNT(*) AS TotalRows FROM dbo.DimCustomer
UNION ALL
SELECT 'DimBranch', COUNT(*) FROM dbo.DimBranch
UNION ALL
SELECT 'DimAccount', COUNT(*) FROM dbo.DimAccount
UNION ALL
SELECT 'FactTransaction', COUNT(*) FROM dbo.FactTransaction;
GO

SELECT TOP 10 * FROM dbo.DimCustomer;
SELECT TOP 10 * FROM dbo.DimBranch;
SELECT TOP 10 * FROM dbo.DimAccount;
SELECT TOP 10 * FROM dbo.FactTransaction;
GO

SELECT
    TransactionID,
    COUNT(*) AS DuplicateCount
FROM dbo.FactTransaction
GROUP BY TransactionID
HAVING COUNT(*) > 1;
GO