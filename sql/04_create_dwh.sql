USE master;
GO

IF DB_ID('DWH') IS NULL
BEGIN
    CREATE DATABASE DWH;
END
GO

USE DWH;
GO

IF OBJECT_ID('dbo.FactTransaction', 'U') IS NOT NULL DROP TABLE dbo.FactTransaction;
IF OBJECT_ID('dbo.DimAccount', 'U') IS NOT NULL DROP TABLE dbo.DimAccount;
IF OBJECT_ID('dbo.DimBranch', 'U') IS NOT NULL DROP TABLE dbo.DimBranch;
IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL DROP TABLE dbo.DimCustomer;
GO

CREATE TABLE dbo.DimCustomer (
    CustomerID      INT           NOT NULL PRIMARY KEY,
    CustomerName    NVARCHAR(255) NULL,
    Address         NVARCHAR(500) NULL,
    CityName        NVARCHAR(255) NULL,
    StateName       NVARCHAR(255) NULL,
    Age             INT           NULL,
    Gender          NVARCHAR(50)  NULL,
    Email           NVARCHAR(255) NULL
);

CREATE TABLE dbo.DimBranch (
    BranchID        INT           NOT NULL PRIMARY KEY,
    BranchName      NVARCHAR(255) NULL,
    BranchLocation  NVARCHAR(255) NULL
);

CREATE TABLE dbo.DimAccount (
    AccountID       INT           NOT NULL PRIMARY KEY,
    CustomerID      INT           NOT NULL,
    AccountType     NVARCHAR(100) NULL,
    Balance         DECIMAL(18,2) NULL,
    DateOpened      DATE          NULL,
    Status          NVARCHAR(50)  NULL,
    CONSTRAINT FK_DimAccount_DimCustomer
        FOREIGN KEY (CustomerID) REFERENCES dbo.DimCustomer(CustomerID)
);

CREATE TABLE dbo.FactTransaction (
    TransactionID    INT           NOT NULL PRIMARY KEY,
    AccountID        INT           NOT NULL,
    TransactionDate  DATETIME      NULL,
    Amount           DECIMAL(18,2) NULL,
    TransactionType  NVARCHAR(50)  NULL,
    BranchID         INT           NULL,
    CONSTRAINT FK_FactTransaction_DimAccount
        FOREIGN KEY (AccountID) REFERENCES dbo.DimAccount(AccountID),
    CONSTRAINT FK_FactTransaction_DimBranch
        FOREIGN KEY (BranchID) REFERENCES dbo.DimBranch(BranchID)
);
GO