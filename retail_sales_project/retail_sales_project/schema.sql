-- Raw table (staging)
CREATE TABLE IF NOT EXISTS sales_raw (
    TransactionID TEXT,
    TransactionTime TEXT,
    ItemCode TEXT,
    ItemDescription TEXT,
    NumberOfItemsPurchased INTEGER,
    CostPerItem REAL,
    Country TEXT
);

-- Cleaned + enriched table
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