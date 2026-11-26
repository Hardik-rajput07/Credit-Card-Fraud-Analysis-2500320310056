**SRS - Credit Card Fraud Analysis**



**1. Introduction**

This document says what my project must do and how I will check that it works.

In this project I take a credit card transaction dataset, clean it, flag the

suspicious transactions using simple rules, and show the result in a Power BI

dashboard.



**2. Overall Description**



Who will use it:

\- Me, to build and explain the project

\- My mentors, to check the GitHub repo and the dashboard

\- A bank analyst (imaginary), who would use the dashboard to look at suspicious

&#x20; transactions



What I am assuming:

\- Every transaction in the dataset has a fraud label (fraud or not fraud)

\- The dataset has card ID, time and amount columns

\- If the file is too big for my laptop, I will use a smaller sample



Limits:

\- I can only use Python, SQL, Power BI, Git and GitHub

\- No machine learning

\- GitHub does not take files over 100 MB, so I will not upload the raw data



**3. Functional Requirements**



\- FR1 (High): Load the raw dataset from the data/raw folder.

\- FR2 (High): Remove duplicate transactions.

\- FR3 (High): Fix missing and wrong values, and write each fix in a log.

\- FR4 (High): Make an "hour of day" column from the transaction time.

\- FR5 (High): Flag transactions that have a very high amount.

\- FR6 (High): Flag transactions made at odd hours (late night).

\- FR7 (High): Flag cards that make many transactions in a short time.

\- FR8 (High): Compare my flags with the real fraud label.

\- FR9 (High): Calculate precision and recall for each rule.

\- FR10 (Medium): Store the clean data in SQL tables and views.

\- FR11 (High): Show flagged transactions in Power BI with at least 3 slicers.

\- FR12 (Medium): Save a data-quality log of all the cleaning steps.



**4. Non-Functional Requirements**



\- NFR1: The cleaning script runs from start to end without any error.

&#x20; (Measured by running it once.)

\- NFR2: The results are the same each time. (Measured by running the script

&#x20; twice and comparing the counts.)

\- NFR3: The dashboard opens and refreshes in under 10 seconds. (Measured with

&#x20; a stopwatch.)

\- NFR4: The code is easy to read. (Measured by checking that every script has

&#x20; comments and clear names.)

\- NFR5: The repo is well organised. (Measured by checking the folders against

&#x20; the sample repo.)

\- NFR6: The dataset licence is followed. (Measured by checking that the source

&#x20; and licence are written in docs/dataset.md.)



**5. Data Requirements**

\- Source: a public credit card fraud dataset from Kaggle

\- Columns I need: card ID, transaction time, amount, merchant category,

&#x20; location (if there is one) and the fraud label

\- Problems I expect: duplicate rows, missing values, wrong time formats, and

&#x20; very few fraud rows compared to normal rows



**6. Acceptance Criteria**

1\. At least 3 fraud rules work.

2\. The flagged transactions are compared with the real fraud labels.

3\. Precision and recall are reported.

4\. No duplicate transactions are left after cleaning.

5\. Transactions near midnight get the correct hour.

6\. I explain the class imbalance and do not use accuracy alone.

7\. The dashboard has a flagged-transaction view with at least 3 slicers.

8\. The repo has the README, test cases and all project files.

