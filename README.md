# GROUP 6: Matthew Lindstrom, Justin Savenko, Spencer Reid. Assignment 1: Commit/Rollback

The output file is Updated_Employees_DB_ADV.csv, and the log is log.csv. Multiple executions of advdb-1.py is necessary to view possible outcomes of different failures. 

## Github Repository

https://github.com/mlind423/Database-2-Assignment-1.git

## Report/Rationale

We had the log stored inside a 2 dimensional array, as we needed several different values held together, preferably as one whole for ease of use. Each of the member arrays represents a single transaction log. The arrays must be indexed using numbers, so perhaps an object would serve better in an actual DB context as it would allow indexing by attribute name, but for the sake of this project is unecessary. 

We output to csv files to keep consistent with the data provided to us. 

The setup for the transaction array is as follows:

### 'transId', 'tableId' ,'Attribute', 'ValueBefore', 'valueAfter', 'timeStamp', 'committed/rolledback/neverExecuted'

transId: An index ordering the transactions. 

tableId: A reference to the row being changed in the DB, necessary to know which entry to rollback in the DB. 

Attribute: String of the attribute name which is being changed. Necessary to know attribute needs to rollback. 

ValueBefore and ValueAfter: As the name suggests, contains the state of the data being changed, before and after the transaction. Before is necessary for rolling back, while after is helpful for user feedback, especially if they wish to retry committing. 

timeStamp: As the name suggests, a timestamp of the time the transaction took place. Not strictly necessary, but can be helpful for diagnostic or administrative purposes. 

committed/rolledback/neverExecuted: Holds one of the three values in it's name. Necessary to log if and when a transaction fails, often used for users or administration. 

