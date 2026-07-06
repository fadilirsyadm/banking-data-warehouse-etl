import pandas as pd
import pyodbc


def read_sql(conn: pyodbc.Connection, query: str) -> pd.DataFrame:
    return pd.read_sql(query, conn)


def clean_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if hasattr(value, "item"):
        return value.item()

    return value


def load_dataframe(conn: pyodbc.Connection, table_name: str, df: pd.DataFrame) -> None:
    columns = list(df.columns)
    column_sql = ", ".join([f"[{col}]" for col in columns])
    placeholders = ", ".join(["?"] * len(columns))

    insert_sql = f"""
        INSERT INTO dbo.{table_name} ({column_sql})
        VALUES ({placeholders})
    """

    records = [
        tuple(clean_value(value) for value in row)
        for row in df.itertuples(index=False, name=None)
    ]

    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany(insert_sql, records)
    conn.commit()

    print(f"[OK] Loaded {table_name}: {len(df)} rows")


def clear_table(conn: pyodbc.Connection, table_name: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.{table_name};")
    conn.commit()

    print(f"[OK] Cleared {table_name}")


def clear_all_dwh_tables(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM dbo.FactTransaction;")
    cursor.execute("DELETE FROM dbo.DimAccount;")
    cursor.execute("DELETE FROM dbo.DimBranch;")
    cursor.execute("DELETE FROM dbo.DimCustomer;")

    conn.commit()

    print("[OK] Cleared all DWH tables")