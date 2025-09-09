# Retail Sales Analysis & Reporting (Python + SQL + Excel)

This project analyzes retail sales data and generates Excel dashboards and a PowerPoint report.

## 1) Dataset
Use the Kaggle dataset mentioned in your brief (`RetailTransactionData`). Download the CSV and note its path.
For a quick test, a small `sample_data.csv` is included.

Expected fields:
- TransactionID
- TransactionTime
- ItemCode
- ItemDescription
- NumberOfItemsPurchased
- CostPerItem
- Country

## 2) Quickstart (SQLite-based)
1. Create a virtual environment (optional) and install deps:
   ```bash
   pip install pandas numpy matplotlib xlsxwriter python-pptx
   ```
2. Update the CSV path in `setup_and_load.py` (see the CONFIG section).
3. Run the loader to create SQLite DB and a cleaned table:
   ```bash
   python setup_and_load.py
   ```
4. Run the analysis to produce Excel & PPT reports in `outputs/`:
   ```bash
   python analysis_and_reports.py
   ```

Outputs include:
- `outputs/Retail_Sales_Report.xlsx`
- `outputs/Retail_Sales_Presentation.pptx`
- `outputs/images/` PNG charts

## 3) Swap in the Kaggle CSV
In `setup_and_load.py`, set `CSV_PATH` to your Kaggle CSV path. Re-run both scripts.

## 4) Optional: Load into MySQL or Postgres
A generic schema is provided in `schema.sql`. You can adapt DDL to your RDBMS.
