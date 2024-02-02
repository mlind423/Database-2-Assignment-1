# This code does not populate log.csv when transactions are 100% committed more often than it does, the rest of the functionality works 
# Code is meh on transaction_not_executed function wrote this prior to push to Main on Feb 2, 2024 can be improved upon/restructured

# Adv DB Winter 2024 - 1

import random
from datetime import datetime
import csv

now = datetime.now()

current_time = now.strftime("%H:%M:%S")


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

def recovery_script(log:list, indx:int, database:list):  #<--- Your CODE
    '''
    Restore the database to stable and sound condition, by processing the DB log.
    '''
    print("Calling your recovery script with DB_Log as an argument.")
    if(indx != None):
        print("Recovery in process ...\n")
        log[indx][6] = 'Rolledback'
        id = int(log[indx][1])
        attr = log[indx][2]
        print(attr)
        oldVal = log[indx][3]
        col = 0
        for i in database[0]: #finds the col of the attribute to be updated
            if(i == attr):
                break
            col += 1
        database[id][col] = oldVal
    else:
        print("No Rollback nessesary.")
    

    pass

def printToCSV(fileName: str, array: list, unexe: list, valid: bool):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL)
        if fileName == "log.csv":
            writer.writerow(["transId", "tableId", "Attribute", "valueBefore", "valueAfter", "timeStamp", "committed/rolledback/neverExecuted"])

        for row in array:
            writer.writerow([str(item) for item in row])

        if(valid):
            if(unexe != None):
                for row in unexe:
                    writer.writerow([str(item) for item in row])



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

def transaction_not_executed(transaction_list: list, db_log: list, database: list) -> list:
    '''
    Grab Unprocessed Transactions
    '''
    unexecuted_transactions = []
    index = 0

    if(len(db_log) == 3):
        index = -1
    elif(len(db_log) == 2):
        index = 2
    else:
        index = 1
    
    if(index == 2):
        value_before = database[15][3]
        value_after = transaction_list[index][index]
        id = database[15][0]
        attr = transaction_list[index][1]
        unexecuted_transactions.append([index, id, attr, value_before, value_after, current_time, "NeverExcuted"])
    elif(index == 1):
        first_val_before = database[5][5]
        first_val_after = transaction_list[index][2]
        first_id = database[5][0]
        first_attr = transaction_list[index][1]
        second_val_before = database[15][3]
        second_value_after = transaction_list[2][2]
        second_id = database[15][0]
        second_attr = transaction_list[2][1]
        unexecuted_transactions.append([index, first_id, first_attr, first_val_before, first_val_after, current_time, "NeverExcuted"])
        unexecuted_transactions.append([index+1, second_id, second_attr, second_val_before, second_value_after, current_time, "NeverExcuted"])
    elif(index == 0): #Ive never been able to excercise this one in my tests
        first_val_before = database[1][4]
        first_val_after = transaction_list[index][2]
        first_id = database[1][0]
        first_attr = [index][1]
        second_val_before = database[5][5]
        second_val_after = transaction_list[index][2]
        second_id = database[5][0]
        second_attr = transaction_list[index][1]
        third_val_before = database[15][3]
        third_val_after = transaction_list[2][2]
        third_id = database[15][0]
        third_attr = transaction_list[2][1]
        unexecuted_transactions.append([index, first_id, first_attr, first_val_before, first_val_after, current_time, "NeverExcuted"])
        unexecuted_transactions.append([index+1, second_id, second_attr, second_val_before, second_val_after, current_time, "NeverExcuted"])
        unexecuted_transactions.append([index+2, third_id, third_attr, third_val_before, third_val_after, current_time, "NeverExcuted"])
    else:
        unexecuted_transactions = None

    return unexecuted_transactions



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
    after_failure = None
    while (not failure and number_of_transactions != 0): 
        # Process transaction
        for index in range(number_of_transactions): #This will go over the transaction list multiple times if there is never a failure
            transaction_index = index+1
            print(f"\nProcessing transaction No. {transaction_index}.")   
            #<--- Your CODE (Call function transaction_processing)
            transaction_processing(index, data_base, DB_Log)
            print("UPDATES have not been committed yet...\n")
            failure = is_there_a_failure()
            number_of_transactions -= 1
            if failure:
                must_recover = True
                print(f'There was a failure whilst processing transaction No. {transaction_index}.')
                break
            elif number_of_transactions == 0:
                break
            else:
                print(f'Transaction No. {transaction_index} has been commited! Changes are permanent.') 
        if(number_of_transactions == 0):
            break        
    if must_recover:
        #Call your recovery script
        after_failure = transaction_not_executed(transactions, DB_Log, data_base)
        recovery_script(DB_Log, index, data_base,) ### Call the recovery function to restore DB to sound state
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
    if(after_failure != None):
        for i in after_failure:
            print(i)
    printToCSV("log.csv", DB_Log, after_failure, True)
    printToCSV("Updated_Employees_DB_ADV.csv", data_base, after_failure, False)
main()


