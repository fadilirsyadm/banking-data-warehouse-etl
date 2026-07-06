import os

import pyodbc
from dotenv import load_dotenv


load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER", "localhost")
SOURCE_DB = os.getenv("SOURCE_DB", "sample")
DWH_DB = os.getenv("DWH_DB", "DWH")
SQL_DRIVER = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")


def get_connection(database: str) -> pyodbc.Connection:
    conn_str = (
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(conn_str)


def get_source_connection() -> pyodbc.Connection:
    return get_connection(SOURCE_DB)


def get_dwh_connection() -> pyodbc.Connection:
    return get_connection(DWH_DB)