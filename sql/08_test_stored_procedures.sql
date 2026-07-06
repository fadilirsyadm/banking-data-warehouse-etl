USE DWH;
GO

EXEC dbo.DailyTransaction
    @start_date = '2024-01-18',
    @end_date   = '2024-01-22';
GO

SELECT CustomerName
FROM dbo.DimCustomer
ORDER BY CustomerName;
GO

EXEC dbo.BalancePerCustomer
    @name = 'SHELLY';
GO