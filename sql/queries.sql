-- name: q1_overall_summary
SELECT
    COUNT(*) AS total_payments,
    SUM(is_fraud) AS fraud_payments,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS fraud_amount
FROM fact_transaction;

-- name: q2_fraud_by_category
SELECT
    m.merchant_category,
    COUNT(*) AS payments,
    SUM(f.is_fraud) AS fraud_payments,
    ROUND(100.0 * SUM(f.is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM fact_transaction f
JOIN dim_merchant m ON f.merchant_id = m.merchant_id
GROUP BY m.merchant_category
ORDER BY fraud_rate_pct DESC;

-- name: q3_fraud_by_card_type
SELECT
    c.card_type,
    COUNT(*) AS payments,
    SUM(f.is_fraud) AS fraud_payments,
    ROUND(100.0 * SUM(f.is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM fact_transaction f
JOIN dim_card c ON f.card_id = c.card_id
GROUP BY c.card_type
ORDER BY fraud_rate_pct DESC;

-- name: q4_fraud_by_channel
SELECT
    channel,
    COUNT(*) AS payments,
    SUM(is_fraud) AS fraud_payments,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct,
    ROUND(AVG(amount), 2) AS avg_amount
FROM fact_transaction
GROUP BY channel
ORDER BY fraud_rate_pct DESC;

-- name: q5_monthly_trend
SELECT
    year,
    month,
    fraud_payments,
    LAG(fraud_payments) OVER (ORDER BY year, month) AS last_month,
    fraud_payments - LAG(fraud_payments) OVER (ORDER BY year, month) AS change
FROM (
    SELECT d.year, d.month, SUM(f.is_fraud) AS fraud_payments
    FROM fact_transaction f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year, d.month
) t
ORDER BY year, month;

-- name: q6_fraud_by_time_of_day
SELECT
    CASE
        WHEN hour BETWEEN 0 AND 5 THEN '1 Night (0-5)'
        WHEN hour BETWEEN 6 AND 11 THEN '2 Morning (6-11)'
        WHEN hour BETWEEN 12 AND 17 THEN '3 Afternoon (12-17)'
        ELSE '4 Evening (18-23)'
    END AS time_of_day,
    COUNT(*) AS payments,
    SUM(is_fraud) AS fraud_payments,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM fact_transaction
GROUP BY time_of_day
ORDER BY time_of_day;

-- name: q7_home_city_vs_away
SELECT
    CASE WHEN f.city = c.home_city THEN 'Home city' ELSE 'Other city' END AS where_paid,
    COUNT(*) AS payments,
    SUM(f.is_fraud) AS fraud_payments,
    ROUND(100.0 * SUM(f.is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM fact_transaction f
JOIN dim_card c ON f.card_id = c.card_id
GROUP BY where_paid
ORDER BY fraud_rate_pct DESC;
