PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_transaction;
DROP TABLE IF EXISTS dim_card;
DROP TABLE IF EXISTS dim_merchant;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_card (
    card_id TEXT PRIMARY KEY,
    card_type TEXT NOT NULL,
    home_city TEXT,
    credit_limit REAL CHECK (credit_limit > 0),
    issue_date TEXT
);

CREATE TABLE dim_merchant (
    merchant_id TEXT PRIMARY KEY,
    merchant_name TEXT NOT NULL,
    merchant_category TEXT NOT NULL,
    city TEXT
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL,
    month INTEGER CHECK (month BETWEEN 1 AND 12),
    year INTEGER,
    weekday TEXT
);

CREATE TABLE fact_transaction (
    transaction_id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES dim_card (card_id),
    merchant_id TEXT NOT NULL REFERENCES dim_merchant (merchant_id),
    date_key INTEGER NOT NULL REFERENCES dim_date (date_key),
    transaction_time TEXT NOT NULL,
    hour INTEGER CHECK (hour BETWEEN 0 AND 23),
    amount REAL NOT NULL CHECK (amount > 0),
    channel TEXT,
    city TEXT,
    is_fraud INTEGER CHECK (is_fraud IN (0, 1)),
    flag_high_amount INTEGER CHECK (flag_high_amount IN (0, 1)),
    flag_odd_hour INTEGER CHECK (flag_odd_hour IN (0, 1)),
    flag_velocity INTEGER CHECK (flag_velocity IN (0, 1))
);
