import os
import sqlite3
import pandas as pd

DB = "data/fraud.db"
OUT = "reports/sql_results"
os.makedirs(OUT, exist_ok=True)

if os.path.exists(DB):
    os.remove(DB)

con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys = ON")
con.executescript(open("sql/schema.sql").read())

cards = pd.read_csv("data/clean/cards_clean.csv", dtype={"card_id": str})
merchants = pd.read_csv("data/clean/merchants_clean.csv")
tx = pd.read_csv("data/clean/transactions_flagged.csv", dtype={"card_id": str})

tx["transaction_time"] = pd.to_datetime(tx["transaction_time"])
tx["date_key"] = tx["transaction_time"].dt.strftime("%Y%m%d").astype(int)
tx["transaction_time"] = tx["transaction_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

days = pd.to_datetime(tx["date_key"].astype(str), format="%Y%m%d").drop_duplicates().sort_values()
dates = pd.DataFrame({
    "date_key": days.dt.strftime("%Y%m%d").astype(int),
    "full_date": days.dt.strftime("%Y-%m-%d"),
    "month": days.dt.month,
    "year": days.dt.year,
    "weekday": days.dt.day_name(),
})

bad = ~tx["card_id"].isin(cards["card_id"]) | ~tx["merchant_id"].isin(merchants["merchant_id"])
if bad.sum() > 0:
    tx[bad].to_csv("reports/unmatched_transactions.csv", index=False)
    print("Payments with unknown card or merchant:", bad.sum(), "-> saved to reports/unmatched_transactions.csv")
tx = tx[~bad]

fact_cols = ["transaction_id", "card_id", "merchant_id", "date_key", "transaction_time", "hour",
             "amount", "channel", "city", "is_fraud", "flag_high_amount", "flag_odd_hour", "flag_velocity"]

cards.to_sql("dim_card", con, if_exists="append", index=False)
merchants.to_sql("dim_merchant", con, if_exists="append", index=False)
dates.to_sql("dim_date", con, if_exists="append", index=False)
tx[fact_cols].to_sql("fact_transaction", con, if_exists="append", index=False)

for table in ["dim_card", "dim_merchant", "dim_date", "fact_transaction"]:
    n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {n} rows")
print()

text = open("sql/queries.sql").read()
for part in text.split("-- name:")[1:]:
    name, sql = part.split("\n", 1)
    name = name.strip()
    result = pd.read_sql(sql.strip().rstrip(";"), con)
    result.to_csv(f"{OUT}/{name}.csv", index=False)
    print("==", name)
    print(result.to_string(index=False))
    print()

con.close()
print("Database saved to", DB, "and query results saved to", OUT)
