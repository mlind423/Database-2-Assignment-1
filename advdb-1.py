# Adv DB Winter 2024 - 1

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

def recovery_script(log:list, indx: int, database:list):  #<--- Your CODE
    '''
    Restore the database to stable and sound condition, by processing the DB log.
    '''
    print("Calling your recovery script with DB_Log as an argument.")
    if(indx != None):
        print("Recovery in process ...\n")
        log[indx - 1][6] = 'Rolledback'
        id = int(log[indx - 1][1])
        attr = log[indx - 1][2]
        print(attr)
        oldVal = log[indx - 1][3]
        col = 0
        for i in database[0]: #finds the col of the attribute to be updated
            if(i == attr):
                break
            col += 1
        database[id][col] = oldVal
    else:
        print("No Rollback nessesary.")
    
    pass

def printToCSV(fileName: str, array:list):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        if(fileName == "log.csv"):
            writer.writerow(["transId,tableId,Attribute,valueBefore,valueAfter,timeStamp,committed/rolledback/neverExecuted"])
       
        writer.writerow(array)

def transaction_processing(indx: int, database: list, log: list): #<-- Your CODE
    '''
    1. Process transaction in the transaction queue.
    2. Updates DB_Log accordingly
    3. This function does NOT commit the updates, just execute them
    '''
    id: int = int(transactions[indx][0])
    attr = transactions[indx][1]
    newVal = transactions[indx][2]
    col: int = 0
    for i in database[0]: #finds the col of the attribute to be updated
        if(i == attr):
            break
        col += 1
    log.append([indx, id, attr, database[id][col], newVal, current_time, "Committed"]) #assumes the transaction completes with no errors but the last value will change if the transaction fails
    database[id][col] = newVal #updates the database list in mainMemory (this will be changed if an error occurs during the transaction)
    pass
    

def read_file(file_name:str)->list:
    '''
    Read the contents of a CSV file line-by-line and return a list of lists
    '''
    data = []
    #
    # one line at-a-time reading file
    #
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
    number_of_transactions = len(transactions)
    must_recover = False
    data_base = read_file('Employees_DB_ADV.csv') #If this is not reading from the file then I need to open the folder that the file is located in since vscode is a little stupid.
    failure = is_there_a_failure()
    #failure = False
    failing_transaction_index = None
    while (not failure and number_of_transactions != 0): 
        # Process transaction
        for index in range(number_of_transactions): #This will go over the transaction list multiple times if there is never a failure
            print(f"\nProcessing transaction No. {index+1}.")   
            #<--- Your CODE (Call function transaction_processing)
            transaction_processing(index, data_base, DB_Log)
            print("UPDATES have not been committed yet...\n")
            failure = is_there_a_failure()
            number_of_transactions -= 1
            if failure:
                must_recover = True
                failing_transaction_index = index + 1
                print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
                break
            elif number_of_transactions == 0:
                break
            else:
                print(f'Transaction No. {index+1} has been commited! Changes are permanent.') 
        if(number_of_transactions == 0):
            break        
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
    printToCSV("log.csv", DB_Log)
    printToCSV("Updated_Employees_DB_ADV.csv", data_base)
main()


