"""
Adv DB Winter 2024 - A1

Authors:
- Matthew Lindstrom
- Spencer Reid
- Justin Savenko

Version: 1.3.2 (Final Version)

This script simulates a conceptual logging and rollback system for a simple RDBMS
database. It is designed to be used with the provided Employees_DB_ADV.csv file,
which contains employee information including their ID, name, department, salary,
and civil status.
"""
import random
from datetime import datetime
import csv

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

data_base = []  # Global binding for the Database contents
'''
transactions = [['id1',' attribute2', 'value1'], ['id2',' attribute2', 'value2'],
                ['id3', 'attribute3', 'value3']]
'''
transactions = [['1', 'Department', 'Music'], ['5', 'Civil_status', 'Divorced'],
                ['15', 'Salary', '200000']]
'''
DB_Log = [['transId', 'tableId' ,'Attribute', 'ValueBefore', 'valueAfter', 'timeStamp', 'committed/rolledback/neverExecuted']
'''
DB_Log = [] # <-- You WILL populate this as you go
log_string = "log.csv" # Global Binding String Variable for File output
database_string = "Updated_Employees_DB_ADV.csv" # Global Binding String Variable for File output


def populate_loglist_failed(log:list, indx: int, database:list):
    '''
    This populates the DB_Log with the transactions that will not run after the failing transaction
    and appends them to the log list

    Parameters:
    - log (list): the log list to append too and to identify what transactions never got executed
    - indx (int): the index value of the list
    - database (list): the original database

    Example:
    --------
    populate_loglist_failed(DB_Log, indx, database)
    '''
    if indx == None:
        indx = 0
    while indx < len(transactions):
        id: int = int(transactions[indx][0])
        attr = transactions[indx][1]
        newVal = transactions[indx][2]
        col: int = 0
        for i in database[0]:
            if(i == attr):
                break
            col += 1
        log.append([indx, id, attr, database[id][col], newVal, current_time, "NeverExecuted"])
        indx +=1
    


def recovery_script(log:list, indx: int, database:list):
    '''
    Restore the database to stable and sound condition, by processing the DB log.

    Parameters:
    - log (list): This is a list of the log entries that will be processed to recover the database
    - indx (int): Index value of the list
    - database (list): The original data base before any errors were introduced

    Example:
    --------
    recovery_script(DB_Log, failing_transaction_index, data_base)
    '''
    print("Calling your recovery script with DB_Log as an argument.")
    populate_loglist_failed(DB_Log, indx, database)
    if(indx != None): #This was only added since the loop running the transaction kept running if there was never an error so this is not longer nessesary since we fixed that.
        print("Recovery in process ...\n")
        log[indx - 1][6] = 'Rolledback' #adds the Rolledback tag to the log.
        #Grabs info out of the log in main memory 
        id = int(log[indx - 1][1])
        attr = log[indx - 1][2]
        oldVal = log[indx - 1][3]

        col = 0
        for i in database[0]: #finds the col of the attribute to be updated
            if(i == attr):
                break
            col += 1
        database[id][col] = oldVal #Replaces the value in the main memory with the old value since the transaction failed.
    else:
        print("No Rollback nessesary.")
    
    pass

def print_to_CSV(fileName: str, array: list):
    """
    File output method that is used to output the log and new database into a CSV file

    Parameters:
    - fileName (str): Name of the file you want to save the data to.
    - array (list): A list containing all of the information that needs to pushed to the output file

    Example:
    --------
    print_to_CSV("cool_file_name.csv", DB_Log)
    """
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL)
        if fileName == log_string: # Write the log header as the log does not contain a header within the list
            writer.writerow(["transId", "tableId", "Attribute", "valueBefore", "valueAfter", "timeStamp", "committed/rolledback/neverExecuted"])

        for row in array:
            writer.writerow([str(item) for item in row])
    pass

def transaction_processing(indx: int, database: list, log: list):
    """
    Transaction processing method used to update the database as long as no failure is simulated
    and updates the database main memory accordingly to the transaction details

    Parameters:
    - indx (int): The index number of the current operation within the operations list.
    - database (list): The actual database which will be modified by this function.
    - log (list): This is where we store our logs so far.

    Example:
    --------
    transaction_processing(index, data_base, DB_Log)
    """
    id: int = int(transactions[indx][0]) #Grabs the id from the transaction list. This is the primary key in the database table. 
    attr = transactions[indx][1] #Grabs the attribute name from the transaction at the indx of the transaction
    newVal = transactions[indx][2] #Grabs the new value that will be added to the database from the transaction
    col: int = 0 
    for i in database[0]: #finds the col of the attribute to be updated
        if(i == attr):#if the attribute name is the same as the attribute we need to change it will exit the loop.
            break
        col += 1
    log.append([indx, id, attr, database[id][col], newVal, current_time, "Committed"]) #assumes the transaction completes with no errors but the last value will change if the transaction fails.
    database[id][col] = newVal #updates the database list in mainMemory (this will be changed if an error occurs during the transaction)
    pass
    

def read_file(file_name:str)->list:
    '''
    Read the contents of a CSV file line-by-line and return a list of lists

    Parameters:
    - file_name (string): The name of the file you want to read from

    Returns:
    - list: data from the file  where each element is a sub-list containing the elements on that line

    Example:
    ---------
    read_file('Employees_DB_ADV.csv')
    '''
    data = []
    # one line at-a-time reading file
    with open(file_name, 'r') as reader:
    # Read and print the entire file line by line
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            line = line.strip().split(',')
            data.append(line)
             # get the next line
            line = reader.readline()

    size = len(data)
    print('The data entries BEFORE updates are presented below:')
    for item in data:
        print(item)
    print(f"\nThere are {size} records in the database, including one header.\n")
    return data

def is_there_a_failure()->bool:
    '''
    Simulates randomly a failure, returning True or False, accordingly
    '''
    value = random.randint(0,1)
    if value == 1:
        result = True
    else:
        result = False
    return result

def main():
    '''
    I had to correct a few unintentional behaviours in the original code, you'll see a counter to escape from the normal recording 
    once all transactions have been recorded. Additionally, Failing before any transactions now properly calls recovery_script.
    '''
    number_of_transactions = len(transactions)
    must_recover = False
    data_base = read_file('Employees_DB_ADV.csv')
    failure = is_there_a_failure()
    if failure:
        must_recover = True
    failing_transaction_index = None
    current_transaction_num = 0
    while (not failure and (current_transaction_num < number_of_transactions)):
        # Process transaction
        for index in range(number_of_transactions):
            print(f"\nProcessing transaction No. {index+1}.")   
            transaction_processing(index, data_base, DB_Log)
            current_transaction_num += 1
            print("UPDATES have not been committed yet...\n")
            failure = is_there_a_failure()
            if failure:
                must_recover = True
                failing_transaction_index = index + 1
                print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
                break
            else:
                print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
                
    if must_recover:
        #Call your recovery script
        recovery_script(DB_Log, failing_transaction_index, data_base) ### Call the recovery function to restore DB to sound state
    else:
        # All transactiones ended up well
        print("All transaction ended up well.")
        print("Updates to the database were committed!\n")

    print('The data entries AFTER updates -and RECOVERY, if necessary- are presented below:')
    for item in data_base:
        print(item)
    print("\nDB_log")
    for i in DB_Log:
        print(i)
    print_to_CSV(log_string, DB_Log)
    print_to_CSV(database_string, data_base)


main()


