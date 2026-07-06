USE DWH;
GO

CREATE OR ALTER PROCEDURE dbo.DailyTransaction
    @start_date DATE,
    @end_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        CAST(TransactionDate AS DATE) AS TransactionDate,
        COUNT(TransactionID) AS TotalTransactions,
        SUM(Amount) AS TotalAmount
    FROM dbo.FactTransaction
    WHERE CAST(TransactionDate AS DATE) BETWEEN @start_date AND @end_date
    GROUP BY CAST(TransactionDate AS DATE)
    ORDER BY CAST(TransactionDate AS DATE);
END;
GO

CREATE OR ALTER PROCEDURE dbo.BalancePerCustomer
    @name NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        c.CustomerName,
        a.AccountID,
        a.AccountType,
        a.Balance AS InitialBalance,
        ISNULL(SUM(
            CASE
                WHEN f.TransactionType IN ('DEPOSIT') THEN f.Amount
                WHEN f.TransactionType IN ('WITHDRAWAL', 'PAYMENT') THEN -f.Amount
                WHEN f.TransactionType IN ('TRANSFER') THEN f.Amount
                ELSE 0
            END
        ), 0) AS TransactionAdjustment,
        a.Balance + ISNULL(SUM(
            CASE
                WHEN f.TransactionType IN ('DEPOSIT') THEN f.Amount
                WHEN f.TransactionType IN ('WITHDRAWAL', 'PAYMENT') THEN -f.Amount
                WHEN f.TransactionType IN ('TRANSFER') THEN f.Amount
                ELSE 0
            END
        ), 0) AS CurrentBalance
    FROM dbo.DimCustomer c
    INNER JOIN dbo.DimAccount a
        ON c.CustomerID = a.CustomerID
    LEFT JOIN dbo.FactTransaction f
        ON a.AccountID = f.AccountID
    WHERE 
        c.CustomerName LIKE '%' + UPPER(@name) + '%'
        AND a.Status = 'ACTIVE'
    GROUP BY
        c.CustomerName,
        a.AccountID,
        a.AccountType,
        a.Balance
    ORDER BY
        c.CustomerName,
        a.AccountID;
END;
GO