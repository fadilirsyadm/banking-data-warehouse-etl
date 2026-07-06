from db import get_dwh_connection
from utils import clear_all_dwh_tables

import etl_dim_customer
import etl_dim_branch
import etl_dim_account
import etl_fact_transaction


def main():
    print("[START] Full ETL process")

    dwh_conn = get_dwh_connection()
    clear_all_dwh_tables(dwh_conn)
    dwh_conn.close()

    etl_dim_customer.load()
    etl_dim_branch.load()
    etl_dim_account.load()
    etl_fact_transaction.load()

    print("[DONE] Full ETL process completed")


if __name__ == "__main__":
    main()