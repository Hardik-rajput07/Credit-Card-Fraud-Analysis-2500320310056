# clean_data.py
# Reads the 3 raw files from data/raw, fixes the data problems,
# and saves clean files in data/clean.
#
# - Every fix is counted and written to reports/data_quality_log.csv
#   (columns: issue, rule_applied, rows_affected).
# - No row is dropped silently: every removed row is saved in
#   data/clean/rejected_rows.csv with the reason it was removed.
#
# Run from the repo folder:  python src/clean_data.py

import os
import pandas as pd

RAW = "data/raw/"
CLEAN = "data/clean/"
LOG_FILE = "reports/data_quality_log.csv"

os.makedirs(CLEAN, exist_ok=True)
os.makedirs("reports", exist_ok=True)

log = []       # one entry for each fix
rejected = []  # rows that were removed, with the reason


def add_log(issue, rule, rows):
    log.append({"issue": issue, "rule_applied": rule, "rows_affected": int(rows)})
    print(f"{rows:>6} rows | {issue}")


def reject(df, mask, file, reason):
    # save the removed rows before removing them
    removed = df[mask].copy()
    removed.insert(0, "reason", reason)
    removed.insert(0, "file", file)
    rejected.append(removed)
    return df[~mask]


def clean_text(column, style):
    # remove extra spaces, then fix capital letters
    column = column.str.strip()
    if style == "title":
        return column.str.title()   # delhi -> Delhi
    return column.str.lower()       # GROCERY -> grocery


def count_changed(old, new):
    # how many values were changed (empty values are not counted)
    return ((old != new) & old.notna()).sum()


# ================= 1. Load =================
cards = pd.read_csv(RAW + "cards.csv")
merchants = pd.read_csv(RAW + "merchants.csv")
tx = pd.read_csv(RAW + "transactions.csv")
start_rows = {"cards": len(cards), "merchants": len(merchants), "transactions": len(tx)}


# ================= 2. cards.csv =================
mask = cards.duplicated()
add_log("cards: duplicate rows", "keep the first copy, remove the repeats", mask.sum())
cards = reject(cards, mask, "cards", "duplicate row")

new = clean_text(cards["card_type"], "title").replace({"Rupay": "RuPay"})
add_log("cards: card_type with wrong case or spaces",
        "strip spaces and use one spelling (Visa, Mastercard, RuPay)",
        count_changed(cards["card_type"], new))
cards["card_type"] = new

mask = cards["credit_limit"] < 0
add_log("cards: negative credit_limit",
        "a limit cannot be negative, so set it to empty", mask.sum())
cards.loc[mask, "credit_limit"] = None

median_limit = cards["credit_limit"].median()
add_log("cards: empty credit_limit",
        f"fill with the median limit ({median_limit:.0f})", cards["credit_limit"].isna().sum())
cards["credit_limit"] = cards["credit_limit"].fillna(median_limit)

add_log("cards: empty home_city", "fill with 'Unknown'", cards["home_city"].isna().sum())
cards["home_city"] = cards["home_city"].fillna("Unknown")


# ================= 3. merchants.csv =================
mask = merchants.duplicated()
add_log("merchants: duplicate rows", "keep the first copy, remove the repeats", mask.sum())
merchants = reject(merchants, mask, "merchants", "duplicate row")

new = clean_text(merchants["merchant_category"], "lower")
add_log("merchants: merchant_category with wrong case or spaces",
        "strip spaces and make all small letters", count_changed(merchants["merchant_category"], new))
merchants["merchant_category"] = new

add_log("merchants: empty city", "fill with 'Unknown'", merchants["city"].isna().sum())
merchants["city"] = merchants["city"].fillna("Unknown")


# ================= 4. transactions.csv =================
mask = tx.duplicated()
add_log("transactions: duplicate rows", "keep the first copy, remove the repeats", mask.sum())
tx = reject(tx, mask, "transactions", "duplicate row")

# Dates come in 2 formats: 2025-01-05 14:03:22 and 05-01-2025 14:03
format1 = pd.to_datetime(tx["transaction_time"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
format2 = pd.to_datetime(tx["transaction_time"], format="%d-%m-%Y %H:%M", errors="coerce")
add_log("transactions: dates in DD-MM-YYYY format",
        "read both formats and save all as YYYY-MM-DD HH:MM:SS", (format1.isna() & format2.notna()).sum())
tx["transaction_time"] = format1.fillna(format2)

mask = tx["transaction_time"].isna()
add_log("transactions: date could not be read", "remove the row (saved in rejected_rows.csv)", mask.sum())
tx = reject(tx, mask, "transactions", "date could not be read")

new = clean_text(tx["city"], "title")
add_log("transactions: city with wrong case or spaces",
        "strip spaces and use capital first letter", count_changed(tx["city"], new))
tx["city"] = new

new = clean_text(tx["channel"], "title").replace({"Pos": "POS"})
add_log("transactions: channel with wrong case or spaces",
        "strip spaces and use one spelling (Online, POS)", count_changed(tx["channel"], new))
tx["channel"] = new

add_log("transactions: empty city", "fill with 'Unknown'", tx["city"].isna().sum())
tx["city"] = tx["city"].fillna("Unknown")

add_log("transactions: empty channel", "fill with 'Unknown'", tx["channel"].isna().sum())
tx["channel"] = tx["channel"].fillna("Unknown")

mask = tx["amount"].isna()
add_log("transactions: empty amount",
        "remove the row, because a payment needs an amount (saved in rejected_rows.csv)", mask.sum())
tx = reject(tx, mask, "transactions", "empty amount")

mask = tx["amount"] <= 0
add_log("transactions: zero or negative amount",
        "remove the row, because a payment must be more than 0 (saved in rejected_rows.csv)", mask.sum())
tx = reject(tx, mask, "transactions", "zero or negative amount")

mask = ~tx["card_id"].isin(cards["card_id"])
add_log("transactions: card_id not in cards.csv",
        "remove the row, because the card does not exist (saved in rejected_rows.csv)", mask.sum())
tx = reject(tx, mask, "transactions", "card_id not in cards.csv")

mask = ~tx["merchant_id"].isin(merchants["merchant_id"])
add_log("transactions: merchant_id not in merchants.csv",
        "remove the row, because the shop does not exist (saved in rejected_rows.csv)", mask.sum())
tx = reject(tx, mask, "transactions", "merchant_id not in merchants.csv")

# New column for the odd-hour rule
tx["hour"] = tx["transaction_time"].dt.hour
add_log("transactions: no hour column", "make 'hour' (0 to 23) from transaction_time", len(tx))


# ================= 5. Checks =================
# Every row is either kept or in rejected_rows.csv, so nothing is lost
rejected_all = pd.concat(rejected, ignore_index=True)
final_rows = {"cards": len(cards), "merchants": len(merchants), "transactions": len(tx)}
for name in start_rows:
    n_rejected = (rejected_all["file"] == name).sum()
    assert final_rows[name] + n_rejected == start_rows[name], f"rows lost in {name}"

assert cards["card_id"].is_unique
assert merchants["merchant_id"].is_unique
assert tx["transaction_id"].is_unique
assert (tx["amount"] > 0).all()


# ================= 6. Save =================
cards.to_csv(CLEAN + "cards_clean.csv", index=False)
merchants.to_csv(CLEAN + "merchants_clean.csv", index=False)
tx.to_csv(CLEAN + "transactions_clean.csv", index=False)
rejected_all.to_csv(CLEAN + "rejected_rows.csv", index=False)
pd.DataFrame(log).to_csv(LOG_FILE, index=False)

print()
for name in start_rows:
    print(f"{name}: {start_rows[name]} rows in, {final_rows[name]} rows kept")
print(f"Removed rows saved in {CLEAN}rejected_rows.csv: {len(rejected_all)}")
print(f"Log saved in {LOG_FILE}")
