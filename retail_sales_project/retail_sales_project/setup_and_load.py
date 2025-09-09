
"""
Setup & Load Script
- Creates SQLite DB
- Loads CSV into sales_raw
- Creates sales_clean with enriched fields
Update the CONFIG below to point to your Kaggle CSV, then run:
    python setup_and_load.py
"""
import os
import sqlite3
import pandas as pd

# ------------ CONFIG ------------
# TODO: Change this to your Kaggle CSV path
CSV_PATH = os.environ.get("RETAIL_CSV_PATH", "sample_data.csv")
DB_PATH = "retail_sales.db"
CHUNKSIZE = 100_000  # for very large CSVs; ignored if file is small
# -------------------------------

def ensure_db(conn):
    schema = """
    CREATE TABLE IF NOT EXISTS sales_raw (
        TransactionID TEXT,
        TransactionTime TEXT,
        ItemCode TEXT,
        ItemDescription TEXT,
        NumberOfItemsPurchased INTEGER,
        CostPerItem REAL,
        Country TEXT
    );
    """
    conn.executescript(schema)

def clean_and_enrich(conn):
    # Drop existing clean table to refresh
    conn.execute("DROP TABLE IF EXISTS sales_clean;")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS sales_clean AS
    SELECT
        TransactionID,
        datetime(TransactionTime) AS TransactionTime,
        ItemCode,
        ItemDescription,
        NumberOfItemsPurchased,
        CostPerItem,
        (NumberOfItemsPurchased * CostPerItem) AS TotalSales,
        Country,
        strftime('%Y', datetime(TransactionTime)) AS Year,
        strftime('%m', datetime(TransactionTime)) AS Month,
        date(datetime(TransactionTime)) AS TxnDate,
        strftime('%H', datetime(TransactionTime)) AS Hour
    FROM sales_raw
    WHERE TransactionID IS NOT NULL;
    """)

def load_csv(conn, csv_path):
    # Try chunked load; if it fails (small file), load directly
    try:
        for chunk in pd.read_csv(csv_path, chunksize=CHUNKSIZE):
            chunk.columns = [c.strip() for c in chunk.columns]
            chunk.to_sql("sales_raw", conn, if_exists="append", index=False)
    except ValueError:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip() for c in df.columns]
        df.to_sql("sales_raw", conn, if_exists="append", index=False)

def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}. Update CSV_PATH in this script.")
    conn = sqlite3.connect(DB_PATH)
    with conn:
        ensure_db(conn)
        # Fresh load: clear raw
        conn.execute("DELETE FROM sales_raw;")
        load_csv(conn, CSV_PATH)
        clean_and_enrich(conn)
    print(f"Done. SQLite DB created at: {DB_PATH} with tables sales_raw and sales_clean.")

if __name__ == "__main__":
    main()
