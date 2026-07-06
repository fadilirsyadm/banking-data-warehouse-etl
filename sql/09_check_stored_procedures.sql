USE DWH;
GO

SELECT 
    name AS ProcedureName,
    create_date,
    modify_date
FROM sys.procedures
WHERE name IN ('DailyTransaction', 'BalancePerCustomer')
ORDER BY name;