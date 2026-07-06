import pandas as pd

from db import get_source_connection, get_dwh_connection
from utils import read_sql, load_dataframe


def extract_transform() -> pd.DataFrame:
    source_conn = get_source_connection()

    query = """
        SELECT
            account_id AS AccountID,
            customer_id AS CustomerID,
            account_type AS AccountType,
            balance AS Balance,
            date_opened AS DateOpened,
            status AS Status
        FROM dbo.account;
    """

    df = read_sql(source_conn, query)
    source_conn.close()

    df["AccountID"] = pd.to_numeric(df["AccountID"], errors="coerce").astype("Int64")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")
    df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    
    df["DateOpened"] = pd.to_datetime(
        df["DateOpened"],
        errors="coerce",
        dayfirst=True
    ).dt.date

    df["AccountType"] = df["AccountType"].apply(
        lambda x: x.upper().strip() if isinstance(x, str) else x
    )

    df["Status"] = df["Status"].apply(
        lambda x: x.upper().strip() if isinstance(x, str) else x
    )

    df = df.dropna(subset=["AccountID", "CustomerID"])
    df = df.drop_duplicates(subset=["AccountID"])

    return df


def load() -> None:
    df = extract_transform()

    dwh_conn = get_dwh_connection()
    load_dataframe(dwh_conn, "DimAccount", df)
    dwh_conn.close()


if __name__ == "__main__":
    load()