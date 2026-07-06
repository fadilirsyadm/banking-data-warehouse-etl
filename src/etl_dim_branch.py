import pandas as pd

from db import get_source_connection, get_dwh_connection
from utils import read_sql, load_dataframe


def extract_transform() -> pd.DataFrame:
    source_conn = get_source_connection()

    query = """
        SELECT
            branch_id AS BranchID,
            branch_name AS BranchName,
            branch_location AS BranchLocation
        FROM dbo.branch;
    """

    df = read_sql(source_conn, query)
    source_conn.close()

    df["BranchID"] = pd.to_numeric(df["BranchID"], errors="coerce").astype("Int64")

    df["BranchName"] = df["BranchName"].apply(
        lambda x: x.upper().strip() if isinstance(x, str) else x
    )

    df["BranchLocation"] = df["BranchLocation"].apply(
        lambda x: x.upper().strip() if isinstance(x, str) else x
    )

    df = df.dropna(subset=["BranchID"])
    df = df.drop_duplicates(subset=["BranchID"])

    return df


def load() -> None:
    df = extract_transform()

    dwh_conn = get_dwh_connection()
    load_dataframe(dwh_conn, "DimBranch", df)
    dwh_conn.close()


if __name__ == "__main__":
    load()