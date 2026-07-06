import os
from pathlib import Path

import pandas as pd

from db import get_source_connection, get_dwh_connection
from utils import read_sql, load_dataframe


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

SOURCE_TRANSACTION_TABLE = os.getenv("SOURCE_TRANSACTION_TABLE", "transaction_db")


def normalize_transaction(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [col.strip().lower() for col in df.columns]

    df = df.rename(
        columns={
            "transaction_id": "TransactionID",
            "account_id": "AccountID",
            "transaction_date": "TransactionDate",
            "amount": "Amount",
            "transaction_type": "TransactionType",
            "branch_id": "BranchID",
        }
    )

    df = df[
        [
            "TransactionID",
            "AccountID",
            "TransactionDate",
            "Amount",
            "TransactionType",
            "BranchID",
        ]
    ]

    df["TransactionID"] = pd.to_numeric(df["TransactionID"], errors="coerce").astype("Int64")
    df["AccountID"] = pd.to_numeric(df["AccountID"], errors="coerce").astype("Int64")
    df["BranchID"] = pd.to_numeric(df["BranchID"], errors="coerce").astype("Int64")

    df["TransactionDate"] = pd.to_datetime(
        df["TransactionDate"],
        errors="coerce",
        dayfirst=True,
    )

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    df["TransactionType"] = df["TransactionType"].apply(
        lambda x: x.upper().strip() if isinstance(x, str) else x
    )

    df = df.dropna(subset=["TransactionID", "AccountID"])
    df = df.drop_duplicates(subset=["TransactionID"])

    return df


def extract_transform() -> pd.DataFrame:
    source_conn = get_source_connection()

    sql_query = f"""
        SELECT
            transaction_id,
            account_id,
            transaction_date,
            amount,
            transaction_type,
            branch_id
        FROM dbo.{SOURCE_TRANSACTION_TABLE};
    """

    transaction_sql = read_sql(source_conn, sql_query)
    source_conn.close()

    transaction_csv = pd.read_csv(DATA_DIR / "transaction_csv.csv")
    transaction_excel = pd.read_excel(DATA_DIR / "transaction_excel.xlsx")

    fact_sql = normalize_transaction(transaction_sql)
    fact_csv = normalize_transaction(transaction_csv)
    fact_excel = normalize_transaction(transaction_excel)

    fact = pd.concat(
        [fact_sql, fact_csv, fact_excel],
        ignore_index=True,
    )

    fact = fact.drop_duplicates(subset=["TransactionID"])

    return fact


def filter_valid_fact(fact: pd.DataFrame) -> pd.DataFrame:
    dwh_conn = get_dwh_connection()

    dim_account = read_sql(dwh_conn, "SELECT AccountID FROM dbo.DimAccount;")
    dim_branch = read_sql(dwh_conn, "SELECT BranchID FROM dbo.DimBranch;")

    dwh_conn.close()

    before = len(fact)

    valid_accounts = set(dim_account["AccountID"].dropna().astype(int))
    valid_branches = set(dim_branch["BranchID"].dropna().astype(int))

    fact = fact[fact["AccountID"].isin(valid_accounts)]
    fact = fact[fact["BranchID"].isin(valid_branches)]

    after = len(fact)

    if before != after:
        print(f"[WARN] Removed invalid FK rows from FactTransaction: {before - after}")

    return fact


def load() -> None:
    fact = extract_transform()
    fact = filter_valid_fact(fact)

    dwh_conn = get_dwh_connection()
    load_dataframe(dwh_conn, "FactTransaction", fact)
    dwh_conn.close()


if __name__ == "__main__":
    load()