import pandas as pd

df = pd.read_csv("data/clean/transactions_clean.csv")
df["transaction_time"] = pd.to_datetime(df["transaction_time"])
df = df.sort_values(["card_id", "transaction_time"]).reset_index(drop=True)

total = len(df)
fraud = df["is_fraud"].sum()
print("Total payments:", total)
print("Fraud payments:", fraud, "(", round(fraud / total * 100, 2), "% )")
print()

avg_amount = df.groupby("card_id")["amount"].transform("mean")
df["flag_high_amount"] = (df["amount"] > 3 * avg_amount).astype(int)

df["flag_odd_hour"] = (df["hour"] <= 5).astype(int)

time_2_before = df.groupby("card_id")["transaction_time"].shift(2)
gap = df["transaction_time"] - time_2_before
df["flag_velocity"] = (gap <= pd.Timedelta(minutes=10)).astype(int)

rules = ["flag_high_amount", "flag_odd_hour", "flag_velocity"]
how_many_rules = df[rules].sum(axis=1)
df["flag_any_rule"] = (how_many_rules >= 1).astype(int)
df["flag_two_or_more"] = (how_many_rules >= 2).astype(int)


def check_rule(name):
    flagged = df[name] == 1
    is_fraud = df["is_fraud"] == 1

    caught = (flagged & is_fraud).sum()
    wrong = (flagged & ~is_fraud).sum()
    missed = (~flagged & is_fraud).sum()

    precision = caught / (caught + wrong) if (caught + wrong) > 0 else 0
    recall = caught / (caught + missed) if (caught + missed) > 0 else 0

    return {
        "rule": name,
        "flagged": int(flagged.sum()),
        "caught_fraud": int(caught),
        "wrong_alarms": int(wrong),
        "missed_fraud": int(missed),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
    }


all_rules = rules + ["flag_any_rule", "flag_two_or_more"]
results = pd.DataFrame([check_rule(r) for r in all_rules])
print(results.to_string(index=False))

results.to_csv("reports/rule_results.csv", index=False)
df.to_csv("data/clean/transactions_flagged.csv", index=False)
print()
print("Saved reports/rule_results.csv and data/clean/transactions_flagged.csv")
