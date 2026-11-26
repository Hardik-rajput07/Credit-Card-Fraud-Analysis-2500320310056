Software Requirements Specification (SRS)

Project: Credit Card Transaction and Fraud Pattern Analysis



1\. Introduction

1.1 Purpose

This document explains what my project must do and how I will check that it

works.



1.2 Scope

The project studies a public credit card transaction dataset, cleans it, flags

suspicious transactions using simple rules, and shows the results in a Power BI

dashboard.



2\. Overall Description

2.1 Users

\- Student (me), who builds and explains the project

\- Mentors, who check the repository and the dashboard

\- Bank analysts (imaginary users), who would read the dashboard to find

&#x20; suspicious transactions



2.2 Assumptions

\- The dataset has a fraud label (fraud or not fraud) for each transaction.

\- The dataset has a card ID, a time, and an amount for each transaction.

\- A sample of the data is enough if the full file is too big for my laptop.



2.3 Constraints

\- Tools are limited to Python, SQL, Power BI, Git and GitHub.

\- No machine learning models.

\- GitHub does not accept files over 100 MB, so the raw dataset is not uploaded.



3\. Functional Requirements

| ID  | Requirement | Priority |

|-----|-------------|----------|

| FR1 | The system shall load the raw dataset from data/raw. | High |

| FR2 | The system shall remove duplicate transactions. | High |

| FR3 | The system shall handle missing and invalid values and record each fix. | High |

| FR4 | The system shall create an hour-of-day column from the transaction time. | High |

| FR5 | The system shall flag transactions with an unusually high amount. | High |

| FR6 | The system shall flag transactions made at unusual hours. | High |

| FR7 | The system shall flag cards with many transactions in a short time. | High |

| FR8 | The system shall compare flagged transactions with the real fraud label. | High |

| FR9 | The system shall calculate precision and recall for each rule. | High |

| FR10 | The system shall store the cleaned data in SQL tables and views. | Medium |

| FR11 | The dashboard shall show flagged transactions with at least 3 slicers. | High |

| FR12 | The system shall save a data-quality log of all cleaning steps. | Medium |



4\. Non-Functional Requirements

| ID   | Requirement | How it is measured |

|------|-------------|--------------------|

| NFR1 | Cleaning script runs without errors. | Run it from start to end with no error. |

| NFR2 | Results can be repeated. | Running the script twice gives the same counts. |

| NFR3 | Dashboard opens quickly. | Opens and refreshes in under 10 seconds. |

| NFR4 | Code is easy to read. | Every script has comments and clear names. |

| NFR5 | Repository is organised. | Folders match the project structure. |

| NFR6 | Dataset licence is respected. | Source and licence are written in docs/dataset.md. |



5\. Data Requirements

\- Source: a public credit card fraud dataset from Kaggle.

\- Needed columns: card ID, transaction time, amount, merchant category,

&#x20; location (if available) and fraud label.

\- Expected problems: duplicates, missing values, wrong time formats, and very

&#x20; few fraud rows compared to normal rows.



6\. Acceptance Criteria

1\. At least 3 fraud rules are working.

2\. Flagged transactions are compared with the real fraud labels.

3\. Precision and recall are reported.

4\. No duplicate transactions are left after cleaning.

5\. Transactions near midnight get the correct hour.

6\. Class imbalance is explained, and accuracy is not used as the only measure.

7\. The Power BI dashboard has a flagged-transactions view with at least 3

&#x20;  slicers.

8\. The repository has the README, the test cases, and all the project files.

