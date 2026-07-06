import pandas as pd

from db import get_source_connection, get_dwh_connection
from utils import read_sql, load_dataframe


def extract_transform() -> pd.DataFrame:
    source_conn = get_source_connection()

    query = """
        SELECT
            c.customer_id AS CustomerID,
            c.customer_name AS CustomerName,
            c.address AS Address,
            ci.city_name AS CityName,
            s.state_name AS StateName,
            c.age AS Age,
            c.gender AS Gender,
            c.email AS Email
        FROM dbo.customer c
        LEFT JOIN dbo.city ci
            ON c.city_id = ci.city_id
        LEFT JOIN dbo.state s
            ON ci.state_id = s.state_id;
    """

    df = read_sql(source_conn, query)
    source_conn.close()

    text_columns = ["CustomerName", "Address", "CityName", "StateName", "Gender"]

    for col in text_columns:
        df[col] = df[col].apply(
            lambda x: x.upper().strip() if isinstance(x, str) else x
        )

    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")

    df = df.dropna(subset=["CustomerID"])
    df = df.drop_duplicates(subset=["CustomerID"])

    return df


def load() -> None:
    df = extract_transform()

    dwh_conn = get_dwh_connection()
    load_dataframe(dwh_conn, "DimCustomer", df)
    dwh_conn.close()


if __name__ == "__main__":
    load()