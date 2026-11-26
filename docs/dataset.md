**Dataset**



* **Where the data comes from**

I did not use a real bank dataset. I made my own fake (synthetic) data

using a Python script called src/generate\_data.py. Because the data is

fake, there is no real customer information in it and I don't need any

licence to use it.



The script uses seed 42, so whenever I run it, I get the same data again.



To make the data, run: python src/generate\_data.py

It saves 3 CSV files in the data/raw folder.



* **The 3 files**



**1.cards.csv**

This file has one row for each credit card.

\- card\_id: the card number (16 digits)

\- card\_type: Visa, Mastercard or RuPay

\- home\_city: the city where the card owner lives

\- credit\_limit: how much the card can spend, in rupees

\- issue\_date: when the card was made



**2.merchants.csv**

This file has one row for each shop.

\- merchant\_id: shop ID, like M001

\- merchant\_name: name of the shop

\- merchant\_category: type of shop, like grocery, travel or electronics

\- city: city where the shop is



**3.transactions.csv** 

This is the main file. Each row is one payment made with a card.

\- transaction\_id: payment ID, like T000001

\- card\_id: which card was used (same as in cards.csv)

\- merchant\_id: which shop it was paid to (same as in merchants.csv)

\- transaction\_time: date and time of the payment

\- amount: how much was paid, in rupees

\- channel: Online, or POS (card swiped in the shop)

\- city: city where the payment happened

\- is\_fraud: 1 if it is fraud, 0 if it is normal



* **What fraud looks like in this data**

\- Only about 1 in 100 payments is fraud, so fraud is very rare.

\- Fraud happens more at night, between 12 AM and 5 AM.

\- Fraud payments are usually much bigger than normal ones.

\- Many fraud payments happen on the same card within a few minutes.



* &#x20;**Problems in the data that I have to clean**

\- Some rows are repeated (duplicates) in all 3 files.

\- Some values are empty, like amount, channel, city and credit limit.

\- Some amounts are 0 or negative, and some credit limits are negative,

&#x20; which is not possible.

\- 15 payments have a card\_id that is not in cards.csv.

\- Dates are written in two ways: 2025-01-05 14:03:22 and 05-01-2025 14:03.

\- Some text has wrong capital letters or extra spaces, like "pos",

&#x20; " POS" or "delhi".

