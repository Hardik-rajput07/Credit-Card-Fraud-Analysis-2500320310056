**Data Dictionary**



This file explains every column in my 3 data files: what it means, its

type, an example, what values are allowed, and what problems it has.



**1. cards.csv**

One row = one credit card.



card\_id

\- Type: integer (16 digits)

\- Example: 4010934721110663

\- Meaning: the card number. Each card has its own number.

\- Allowed: must be unique

\- Problems: 10 cards are repeated (duplicates)



card\_type

\- Type: text

\- Example: Visa

\- Meaning: the company of the card

\- Allowed: Visa, Mastercard, RuPay

\- Problems: some have wrong capital letters or spaces, like "VISA" or " Visa"



home\_city

\- Type: text

\- Example: Hyderabad

\- Meaning: city where the card owner lives

\- Allowed: one of 10 Indian cities

\- Problems: some values are empty



credit\_limit

\- Type: integer (rupees)

\- Example: 100000

\- Meaning: the most money the card can spend

\- Allowed: more than 0

\- Problems: some are empty, and 5 are negative



issue\_date

\- Type: date (YYYY-MM-DD)

\- Example: 2024-05-11

\- Meaning: date the card was made

\- Allowed: a date before the transactions start (2025)

\- Problems: none



**2. merchants.csv**

One row = one shop.



merchant\_id

\- Type: text

\- Example: M001

\- Meaning: the shop ID

\- Allowed: must be unique

\- Problems: 3 shops are repeated (duplicates)



merchant\_name

\- Type: text

\- Example: Grocery Hub 1

\- Meaning: name of the shop

\- Problems: none



merchant\_category

\- Type: text

\- Example: grocery

\- Meaning: the type of shop

\- Allowed: grocery, food\_dining, fuel, shopping\_online, shopping\_store,

&#x20; electronics, travel, entertainment, health, utilities

\- Problems: some have wrong capital letters or spaces, like "GROCERY"



city

\- Type: text

\- Example: Kolkata

\- Meaning: city where the shop is

\- Problems: 2 values are empty



**3. transactions.csv**

One row = one card payment. This is the main file.



transaction\_id

\- Type: text

\- Example: T000001

\- Meaning: the payment ID

\- Allowed: must be unique

\- Problems: 364 rows are repeated (duplicates)



card\_id

\- Type: integer

\- Example: 4128052610547786

\- Meaning: the card used for the payment

\- Allowed: must be a card\_id that is in cards.csv

\- Problems: 15 rows have a card\_id that is not in cards.csv



merchant\_id

\- Type: text

\- Example: M003

\- Meaning: the shop where the payment was made

\- Allowed: must be a merchant\_id that is in merchants.csv

\- Problems: none



transaction\_time

\- Type: date and time

\- Example: 2025-01-01 00:02:51

\- Meaning: when the payment happened

\- Allowed: between 1 January 2025 and 31 March 2025

\- Problems: some are written as 05-01-2025 14:03 (a different format)



amount

\- Type: decimal (rupees)

\- Example: 1010.11

\- Meaning: how much was paid

\- Allowed: more than 0

\- Problems: some are empty, and 25 are 0 or negative



channel

\- Type: text

\- Example: Online

\- Meaning: how the payment was made

\- Allowed: Online, POS (POS means the card was swiped in the shop)

\- Problems: some are empty, and some have wrong capital letters or

&#x20; spaces, like "pos" or " Online"



city

\- Type: text

\- Example: Mumbai

\- Meaning: city where the payment happened

\- Problems: some are empty, and some have wrong capital letters or

&#x20; spaces, like "delhi" or " MUMBAI"



is\_fraud

\- Type: integer

\- Example: 0

\- Meaning: tells if the payment was fraud

\- Allowed: 1 = fraud, 0 = normal

\- Problems: none. Only about 1% of rows are 1.



* **New columns I will make while cleaning**

\- hour: the hour of the payment (0 to 23), taken from transaction\_time

\- flag\_high\_amount: 1 if the amount is very high

\- flag\_odd\_hour: 1 if the payment is between 12 AM and 5 AM

\- flag\_velocity: 1 if the same card made many payments in a short time

