# Banking Data Warehouse: Python-Based ETL, Data Integration, and Stored Procedures

This repository contains a **Data Engineering final task project** for building a banking **Data Warehouse (DWH)** using **SQL Server**, **Python**, **Pandas**, **pyodbc**, and **SQL Server Stored Procedures**.

The project simulates a banking client that stores data across multiple sources and needs a centralized Data Warehouse to support faster reporting and analytics. The pipeline restores a sample SQL Server database, extracts data from SQL Server, CSV, and Excel sources, transforms the data using modular Python ETL scripts, loads it into dimension and fact tables, and creates reporting stored procedures.

---

## Project Background

A banking client has several data sources stored separately across database tables and transaction files. Because the extraction and integration process is not centralized, reporting and analysis are delayed.

This project solves the problem by creating an end-to-end ETL workflow that:

1. Restores the source database from `sample.bak`.
2. Extracts data from SQL Server, CSV, and Excel files.
3. Transforms and standardizes customer, account, branch, and transaction data.
4. Loads the processed data into a SQL Server Data Warehouse.
5. Creates stored procedures for reporting use cases.

---

## Tech Stack

| Category | Tools |
|---|---|
| Database | SQL Server, SQL Server Management Studio (SSMS) |
| Programming | Python |
| Data Processing | Pandas |
| Database Connector | pyodbc |
| File Processing | CSV, Excel, openpyxl |
| Configuration | python-dotenv |
| Reporting Logic | SQL Server Stored Procedures |

---

## Repository Structure

```text
banking-data-warehouse-etl/
|
|-- backup/
|   |-- sample.bak
|
|-- data/
|   |-- transaction_csv.csv
|   |-- transaction_excel.xlsx
|
|-- sql/
|   |-- 00_check_sample_tables.sql
|   |-- 01_check_sample_columns.sql
|   |-- 02_preview_source_data.sql
|   |-- 03_count_source_rows.sql
|   |-- 04_create_dwh.sql
|   |-- 05_check_dwh_tables.sql
|   |-- 06_validate_dwh_data.sql
|   |-- 07_create_stored_procedures.sql
|   |-- 08_test_stored_procedures.sql
|   |-- 09_check_stored_procedures.sql
|
|-- src/
|   |-- db.py
|   |-- utils.py
|   |-- etl_dim_customer.py
|   |-- etl_dim_branch.py
|   |-- etl_dim_account.py
|   |-- etl_fact_transaction.py
|   |-- run_all.py
|
|-- .env.example
|-- requirements.txt
|-- README.md
```

---

## Source Data

The project uses three main data sources:

| Source | File / Table | Description |
|---|---|---|
| SQL Server Backup | `backup/sample.bak` | Source database restored as `sample` |
| SQL Server Tables | `customer`, `city`, `state`, `account`, `branch`, `transaction_db` | Core banking source tables |
| CSV File | `data/transaction_csv.csv` | Additional transaction records |
| Excel File | `data/transaction_excel.xlsx` | Additional transaction records |

---

## Data Warehouse Design

Target database:

```text
DWH
```

The Data Warehouse consists of three dimension tables and one fact table:

| Table | Main Columns | Rows |
|---|---|---:|
| `DimCustomer` | `CustomerID`, `CustomerName`, `Address`, `CityName`, `StateName`, `Age`, `Gender`, `Email` | 20 |
| `DimAccount` | `AccountID`, `CustomerID`, `AccountType`, `Balance`, `DateOpened`, `Status` | 23 |
| `DimBranch` | `BranchID`, `BranchName`, `BranchLocation` | 5 |
| `FactTransaction` | `TransactionID`, `AccountID`, `TransactionDate`, `Amount`, `TransactionType`, `BranchID` | 25 |

### Table Relationship

```text
DimCustomer.CustomerID  -> DimAccount.CustomerID
DimAccount.AccountID    -> FactTransaction.AccountID
DimBranch.BranchID      -> FactTransaction.BranchID
```

---

## ETL Architecture

```text
SQL Server Backup (.bak)
        |
        v
Source Database: sample
        |
        v
Python ETL: Pandas + pyodbc
        |
        v
Data Transformation + Validation
        |
        v
Target Database: DWH
        |
        v
Stored Procedures for Reporting
```

The ETL process is modular. Each target table has its own ETL script, while `run_all.py` works as the main orchestrator.

### ETL Load Order

```text
1. DimCustomer
2. DimBranch
3. DimAccount
4. FactTransaction
```

This order is important because the fact table depends on valid foreign keys from the dimension tables.

---

## Transformation Summary

### 1. Customer Dimension

Script:

```text
src/etl_dim_customer.py
```

Main logic:

- Extracts data from `customer`, `city`, and `state` tables.
- Joins customer data with city and state data.
- Standardizes text columns using uppercase formatting.
- Removes duplicate records based on `CustomerID`.
- Loads the final result into `DWH.dbo.DimCustomer`.

### 2. Branch Dimension

Script:

```text
src/etl_dim_branch.py
```

Main logic:

- Extracts branch data from SQL Server.
- Renames columns into the DWH format.
- Standardizes branch name and location text.
- Removes duplicate records based on `BranchID`.
- Loads the final result into `DWH.dbo.DimBranch`.

### 3. Account Dimension

Script:

```text
src/etl_dim_account.py
```

Main logic:

- Extracts account data from SQL Server.
- Converts balance values into numeric format.
- Parses `DateOpened` into date format.
- Standardizes account type and status values.
- Removes duplicate records based on `AccountID`.
- Loads the final result into `DWH.dbo.DimAccount`.

### 4. Transaction Fact Table

Script:

```text
src/etl_fact_transaction.py
```

Main logic:

- Extracts transaction data from SQL Server table `transaction_db`.
- Reads additional transaction records from CSV and Excel files.
- Normalizes transaction schemas across all sources.
- Combines transaction data using `pandas.concat()`.
- Removes duplicate transactions based on `TransactionID`.
- Validates foreign keys before loading into the fact table.
- Loads the final result into `DWH.dbo.FactTransaction`.

---

## Stored Procedures

The project includes two stored procedures for reporting.

| Stored Procedure | Parameter | Business Purpose | Output |
|---|---|---|---|
| `dbo.DailyTransaction` | `@start_date`, `@end_date` | Aggregates daily transaction count and total amount within a selected date range | `TransactionDate`, `TotalTransactions`, `TotalAmount` |
| `dbo.BalancePerCustomer` | `@name` | Calculates current balance for active customer accounts based on transaction movement | `CustomerName`, `AccountID`, `AccountType`, `InitialBalance`, `CurrentBalance` |

### DailyTransaction Example

```sql
EXEC dbo.DailyTransaction
    @start_date = '2024-01-18',
    @end_date   = '2024-01-22';
```

### BalancePerCustomer Example

```sql
EXEC dbo.BalancePerCustomer
    @name = 'SHELLY';
```

Balance formula:

```text
CurrentBalance = InitialBalance + DEPOSIT - WITHDRAWAL - PAYMENT + TRANSFER
```

---

## Environment Configuration

Create a local `.env` file based on `.env.example`.

Example:

```env
SQL_SERVER=localhost
SOURCE_DB=sample
DWH_DB=DWH
SQL_DRIVER=ODBC Driver 18 for SQL Server
SOURCE_TRANSACTION_TABLE=transaction_db
```

---

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Check installed ODBC drivers:

```powershell
python -c "import pyodbc; print(pyodbc.drivers())"
```

Make sure one of these drivers is available:

```text
ODBC Driver 18 for SQL Server
ODBC Driver 17 for SQL Server
```

---

## How to Run the Project

### 1. Restore Source Database

Restore this backup file using SSMS:

```text
backup/sample.bak
```

Restore it as:

```text
sample
```

### 2. Inspect Source Database

Run these SQL scripts in SSMS:

```text
sql/00_check_sample_tables.sql
sql/01_check_sample_columns.sql
sql/02_preview_source_data.sql
sql/03_count_source_rows.sql
```

### 3. Create Data Warehouse

Run:

```text
sql/04_create_dwh.sql
```

Then validate the created tables:

```text
sql/05_check_dwh_tables.sql
```

Expected DWH tables:

```text
DimCustomer
DimBranch
DimAccount
FactTransaction
```

### 4. Run Python ETL

Run the main ETL orchestrator:

```powershell
python src/run_all.py
```

Expected output:

```text
[START] Full ETL process
[OK] Cleared all DWH tables
[OK] Loaded DimCustomer: 20 rows
[OK] Loaded DimBranch: 5 rows
[OK] Loaded DimAccount: 23 rows
[OK] Loaded FactTransaction: 25 rows
[DONE] Full ETL process completed
```

### 5. Validate DWH Result

Run:

```text
sql/06_validate_dwh_data.sql
```

Expected result:

| Table | Total Rows |
|---|---:|
| `DimCustomer` | 20 |
| `DimBranch` | 5 |
| `DimAccount` | 23 |
| `FactTransaction` | 25 |

### 6. Create Stored Procedures

Run:

```text
sql/07_create_stored_procedures.sql
```

### 7. Test Stored Procedures

Run:

```text
sql/08_test_stored_procedures.sql
sql/09_check_stored_procedures.sql
```

---

## SQL Scripts

| File | Description |
|---|---|
| `00_check_sample_tables.sql` | Checks available tables in the restored `sample` database |
| `01_check_sample_columns.sql` | Checks source database columns |
| `02_preview_source_data.sql` | Previews source table records |
| `03_count_source_rows.sql` | Counts source table rows |
| `04_create_dwh.sql` | Creates the target DWH database and tables |
| `05_check_dwh_tables.sql` | Checks created DWH tables |
| `06_validate_dwh_data.sql` | Validates ETL output in the DWH |
| `07_create_stored_procedures.sql` | Creates reporting stored procedures |
| `08_test_stored_procedures.sql` | Tests stored procedure execution |
| `09_check_stored_procedures.sql` | Checks stored procedure metadata |

---

## Python Scripts

| File | Description |
|---|---|
| `db.py` | Creates SQL Server connections for source and target databases |
| `utils.py` | Provides helper functions for SQL reading, value cleaning, loading, and table clearing |
| `etl_dim_customer.py` | Loads `DimCustomer` |
| `etl_dim_branch.py` | Loads `DimBranch` |
| `etl_dim_account.py` | Loads `DimAccount` |
| `etl_fact_transaction.py` | Loads `FactTransaction` from SQL Server, CSV, and Excel |
| `run_all.py` | Runs the complete ETL process in the correct order |

---

## Final Output

After running the full ETL process, the DWH contains:

```text
DimCustomer      20 rows
DimBranch        5 rows
DimAccount       23 rows
FactTransaction  25 rows
```

Available stored procedures:

```text
dbo.DailyTransaction
dbo.BalancePerCustomer
```

---

## Notes

- Restore `sample.bak` before running the Python ETL pipeline.
- Keep CSV and Excel files inside the `data/` folder.
- Run the ETL from the project root directory.
- If a connection error occurs, check `SQL_SERVER`, `SQL_DRIVER`, and database names in `.env`.

---

## Author

**Fadil Irsyad Muhammad**  
Data Engineer Project-Based Internship - ID/X Partners x Rakamin Academy
