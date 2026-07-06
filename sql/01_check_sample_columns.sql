USE sample;
GO

-- SELECT * FROM INFORMATION_SCHEMA.COLUMNS;

SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    ORDINAL_POSITION
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN (
    'customer',
    'city',
    'state',
    'account',
    'branch',
    'transaction_db'
)
ORDER BY TABLE_NAME, ORDINAL_POSITION;