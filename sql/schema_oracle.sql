CREATE TABLE dim_card (
    card_id VARCHAR2(16) PRIMARY KEY,
    card_type VARCHAR2(20) NOT NULL,
    home_city VARCHAR2(50),
    credit_limit NUMBER(12, 2) CHECK (credit_limit > 0),
    issue_date DATE
);

CREATE TABLE dim_merchant (
    merchant_id VARCHAR2(10) PRIMARY KEY,
    merchant_name VARCHAR2(100) NOT NULL,
    merchant_category VARCHAR2(30) NOT NULL,
    city VARCHAR2(50)
);

CREATE TABLE dim_date (
    date_key NUMBER(8) PRIMARY KEY,
    full_date DATE NOT NULL,
    month NUMBER(2) CHECK (month BETWEEN 1 AND 12),
    year NUMBER(4),
    weekday VARCHAR2(10)
);

CREATE TABLE fact_transaction (
    transaction_id VARCHAR2(10) PRIMARY KEY,
    card_id VARCHAR2(16) NOT NULL REFERENCES dim_card (card_id),
    merchant_id VARCHAR2(10) NOT NULL REFERENCES dim_merchant (merchant_id),
    date_key NUMBER(8) NOT NULL REFERENCES dim_date (date_key),
    transaction_time TIMESTAMP NOT NULL,
    hour NUMBER(2) CHECK (hour BETWEEN 0 AND 23),
    amount NUMBER(12, 2) NOT NULL CHECK (amount > 0),
    channel VARCHAR2(20),
    city VARCHAR2(50),
    is_fraud NUMBER(1) CHECK (is_fraud IN (0, 1)),
    flag_high_amount NUMBER(1) CHECK (flag_high_amount IN (0, 1)),
    flag_odd_hour NUMBER(1) CHECK (flag_odd_hour IN (0, 1)),
    flag_velocity NUMBER(1) CHECK (flag_velocity IN (0, 1))
);
