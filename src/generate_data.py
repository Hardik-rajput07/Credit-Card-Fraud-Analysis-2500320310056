"""
generate_data.py
Makes a synthetic (fake) dataset for the Credit Card Fraud Analysis project.
No real customer data is used. Fixed seed, so every run gives the same files.

How to run (from the repo folder):
    python src/generate_data.py

Output (written to data/raw):
    cards.csv         - one row per credit card
    merchants.csv     - one row per shop
    transactions.csv  - one row per card transaction (with fraud label)

Fraud patterns built in (so the fraud rules have something to find):
    - Fraud is rare (about 1% of transactions)
    - Fraud happens more late at night
    - Fraud amounts are often much higher than normal
    - Fraud often comes in quick bursts on the same card

Data-quality problems built in (so the cleaning step has work to do):
    - Duplicate rows
    - Missing values
    - Invalid values (zero/negative amounts and limits, unknown card IDs)
    - Inconsistent text (upper/lower case, extra spaces, two date formats)
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

# Save files in <repo>/data/raw, wherever the script is run from
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)

N_CARDS = 1500
N_NORMAL_TX = 60000
N_STOLEN_CARDS = 160
START = pd.Timestamp("2025-01-01")
DAYS = 90

CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata",
          "Hyderabad", "Pune", "Jaipur", "Lucknow", "Ahmedabad"]

# category: (typical amount in Rs, spread, weight for normal, weight for fraud)
CATEGORIES = {
    "grocery":         (600,  0.6, 0.22, 0.03),
    "food_dining":     (450,  0.6, 0.18, 0.04),
    "fuel":            (1500, 0.4, 0.12, 0.05),
    "shopping_online": (1800, 0.9, 0.14, 0.30),
    "shopping_store":  (1500, 0.8, 0.10, 0.08),
    "electronics":     (9000, 0.8, 0.04, 0.25),
    "travel":          (7000, 0.9, 0.05, 0.15),
    "entertainment":   (700,  0.6, 0.07, 0.04),
    "health":          (900,  0.7, 0.05, 0.02),
    "utilities":       (1800, 0.5, 0.03, 0.04),
}
CAT_NAMES = list(CATEGORIES)


def normalise(weights):
    weights = np.array(weights, dtype=float)
    return weights / weights.sum()


# ---------------------------------------------------------------- cards
card_ids = np.unique(rng.integers(4000_0000_0000_0000, 4999_9999_9999_9999,
                                  size=N_CARDS * 2, dtype=np.int64))
card_ids = rng.permutation(card_ids)[:N_CARDS]  # 1,500 unique 16-digit numbers
cards = pd.DataFrame({
    "card_id": card_ids,
    "card_type": rng.choice(["Visa", "Mastercard", "RuPay"], size=N_CARDS, p=[0.45, 0.35, 0.20]),
    "home_city": rng.choice(CITIES, size=N_CARDS),
    "credit_limit": rng.choice([25000, 50000, 100000, 200000, 500000],
                               size=N_CARDS, p=[0.25, 0.35, 0.25, 0.1, 0.05]),
    "issue_date": (pd.Timestamp("2018-01-01")
                   + pd.to_timedelta(rng.integers(0, 2500, size=N_CARDS), unit="D")),
})

# ---------------------------------------------------------------- merchants
merchant_rows = []
m_id = 1
for cat in CAT_NAMES:
    for i in range(1, 9):  # 8 shops per category
        name = f"{cat.split('_')[0].title()} {['Mart', 'Hub', 'World', 'Point'][i % 4]} {i}"
        merchant_rows.append([f"M{m_id:03d}", name, cat, rng.choice(CITIES)])
        m_id += 1
merchants = pd.DataFrame(merchant_rows,
                         columns=["merchant_id", "merchant_name", "merchant_category", "city"])
merchants_by_cat = {c: merchants.loc[merchants.merchant_category == c, "merchant_id"].to_numpy()
                    for c in CAT_NAMES}

# ---------------------------------------------------------------- transactions
home_city = dict(zip(cards.card_id, cards.home_city))
card_activity = normalise(rng.gamma(2.0, 1.0, size=N_CARDS))  # some cards used more
normal_cat_w = normalise([CATEGORIES[c][2] for c in CAT_NAMES])
fraud_cat_w = normalise([CATEGORIES[c][3] for c in CAT_NAMES])

# Normal spending is mostly daytime and evening
hour_w = normalise([0.3, 0.2, 0.15, 0.1, 0.1, 0.3, 1, 2, 3.5, 4.5, 5, 5.5,
                    6, 5.5, 5, 5, 5.5, 6, 6.5, 6, 5, 3.5, 2, 1])
# Fraud is much more common between midnight and 5 AM
fraud_hour_w = hour_w.copy()
fraud_hour_w[0:5] *= 25
fraud_hour_w = normalise(fraud_hour_w)

CHANNEL_CATS = {"shopping_online", "travel", "utilities"}


def pick_amount(cat, fraud=False):
    base, spread = CATEGORIES[cat][0], CATEGORIES[cat][1]
    amount = rng.lognormal(np.log(base), spread)
    if fraud:  # small "test" charge, or a big charge
        amount *= rng.choice([0.05, 3, 6], p=[0.15, 0.45, 0.40])
    return round(float(min(amount, 300000)), 2)


def pick_channel(cat):
    if cat in CHANNEL_CATS:
        return "Online" if rng.random() < 0.85 else "POS"
    return "POS" if rng.random() < 0.85 else "Online"


rows = []

# Normal transactions
for _ in range(N_NORMAL_TX):
    card = rng.choice(card_ids, p=card_activity)
    cat = rng.choice(CAT_NAMES, p=normal_cat_w)
    time = (START + pd.Timedelta(days=int(rng.integers(0, DAYS)),
                                 hours=int(rng.choice(24, p=hour_w)),
                                 minutes=int(rng.integers(0, 60)),
                                 seconds=int(rng.integers(0, 60))))
    city = home_city[card] if rng.random() > 0.05 else rng.choice(CITIES)
    rows.append([card, rng.choice(merchants_by_cat[cat]), time,
                 pick_amount(cat), pick_channel(cat), city, 0])

# Fraud: bursts of transactions on stolen cards
for card in rng.choice(card_ids, size=N_STOLEN_CARDS, replace=False):
    for _ in range(int(rng.integers(1, 3))):  # 1 or 2 fraud episodes per card
        time = (START + pd.Timedelta(days=int(rng.integers(0, DAYS)),
                                     hours=int(rng.choice(24, p=fraud_hour_w)),
                                     minutes=int(rng.integers(0, 60))))
        burst = int(rng.choice([1, 2, 3, 4, 5, 6], p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1]))
        for _ in range(burst):
            cat = rng.choice(CAT_NAMES, p=fraud_cat_w)
            city = rng.choice(CITIES) if rng.random() < 0.6 else home_city[card]
            rows.append([card, rng.choice(merchants_by_cat[cat]), time,
                         pick_amount(cat, fraud=True), pick_channel(cat), city, 1])
            time += pd.Timedelta(minutes=int(rng.integers(1, 15)),
                                 seconds=int(rng.integers(0, 60)))

tx = pd.DataFrame(rows, columns=["card_id", "merchant_id", "transaction_time",
                                 "amount", "channel", "city", "is_fraud"])
tx = tx.sort_values("transaction_time", kind="stable").reset_index(drop=True)
tx.insert(0, "transaction_id", [f"T{i:06d}" for i in range(1, len(tx) + 1)])


# ---------------------------------------------------------------- inject problems
def messy_text(value):
    """Return the same text with wrong case or extra spaces."""
    return rng.choice([value.lower(), value.upper(), f" {value}", f"{value}  "])


def add_problems_cards(df):
    n = len(df)
    df["issue_date"] = df["issue_date"].dt.strftime("%Y-%m-%d")
    mask = rng.random(n) < 0.05
    df.loc[mask, "card_type"] = df.loc[mask, "card_type"].map(messy_text)
    df.loc[rng.random(n) < 0.02, "credit_limit"] = np.nan          # missing
    bad = rng.choice(n, size=5, replace=False)
    df.loc[bad, "credit_limit"] = -df.loc[bad, "credit_limit"].abs()  # invalid
    df.loc[rng.random(n) < 0.01, "home_city"] = np.nan              # missing
    dups = df.sample(n=10, random_state=SEED)                        # duplicates
    return pd.concat([df, dups]).sort_index(kind="stable").reset_index(drop=True)


def add_problems_merchants(df):
    n = len(df)
    mask = rng.random(n) < 0.08
    df.loc[mask, "merchant_category"] = df.loc[mask, "merchant_category"].map(messy_text)
    df.loc[rng.choice(n, size=2, replace=False), "city"] = np.nan   # missing
    dups = df.sample(n=3, random_state=SEED)                         # duplicates
    return pd.concat([df, dups]).sort_index(kind="stable").reset_index(drop=True)


def add_problems_transactions(df):
    n = len(df)
    times = pd.to_datetime(df["transaction_time"])
    df["transaction_time"] = times.dt.strftime("%Y-%m-%d %H:%M:%S")
    alt = rng.random(n) < 0.03                                       # second date format
    df.loc[alt, "transaction_time"] = times[alt].dt.strftime("%d-%m-%Y %H:%M")

    mask = rng.random(n) < 0.03
    df.loc[mask, "city"] = df.loc[mask, "city"].map(messy_text)
    mask = rng.random(n) < 0.03
    df.loc[mask, "channel"] = df.loc[mask, "channel"].map(messy_text)

    df.loc[rng.random(n) < 0.003, "amount"] = np.nan                 # missing
    df.loc[rng.random(n) < 0.008, "city"] = np.nan
    df.loc[rng.random(n) < 0.004, "channel"] = np.nan

    bad = rng.choice(n, size=25, replace=False)                      # zero / negative amount
    df.loc[bad, "amount"] = rng.choice([0.0, -1.0], size=25) * df.loc[bad, "amount"].abs()

    orphan = rng.choice(n, size=15, replace=False)                   # card not in cards.csv
    df.loc[orphan, "card_id"] = 9999_0000_0000_0000 + np.arange(15)

    dups = df.sample(frac=0.006, random_state=SEED)                  # duplicates
    return pd.concat([df, dups]).sort_index(kind="stable").reset_index(drop=True)


cards = add_problems_cards(cards)
merchants = add_problems_merchants(merchants)
tx = add_problems_transactions(tx)

# ---------------------------------------------------------------- save
cards.to_csv(OUT_DIR / "cards.csv", index=False)
merchants.to_csv(OUT_DIR / "merchants.csv", index=False)
tx.to_csv(OUT_DIR / "transactions.csv", index=False)

print(f"Saved to {OUT_DIR}")
print(f"cards.csv:        {len(cards):>6} rows")
print(f"merchants.csv:    {len(merchants):>6} rows")
print(f"transactions.csv: {len(tx):>6} rows "
      f"({int(tx['is_fraud'].sum())} fraud, {tx['is_fraud'].mean() * 100:.2f}%)")
