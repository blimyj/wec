import csv
import pandas as pd

'''
5 columns
5th column can have multiple delimters that do not function as delimiters
Custom csv reader to modify csv file to new format

Open file
find appropriate row
From first data row
-> split line into max 5
-> for the 5th item in every row, delimit by ',', remove empty items, join with space
    -> Called format_transaction_reference
-> put into format: [Date, Reference Code, Debit Amount, Credit Amount, Transaction Data] <- This will be standard format for all banks
-> This reader will be in its own module/file to be called staticlly
'''

def parse_csv(fname):
    has_header = False
    datarows =[]
    df = pd.DataFrame(columns=['Date'
            , 'Reference Code'
            , 'Debit Amount'
            , 'Credit Amount'
            , 'Transaction Data'])
    with open(fname, newline='') as fin:

        for line in fin:
            line = line.rstrip("\n")

            if len(line) == 0:
                continue 

            if not has_header:
                has_header = match_header_format(line)
                continue
            
            # Due to allowance of commas in csv Transaction Ref Fields by DBS, we consider the fields as 1 field instead.
            row = line.split(sep=',', maxsplit=4)

            #Reformat Transaction References/Descriptions
            row[4] = row[4].rstrip(',').replace(',', ' ')

            datarows.append(row)
            df = pd.DataFrame(datarows,columns=['datetime'
            , 'Reference Code'
            , 'Debit Amount'
            , 'Credit Amount'
            , 'Transaction Data'])
            df['datetime'] = df['datetime'].astype('datetime64[ns]')
    return df

def match_header_format(line):
    dbs_format = 'Transaction Date,Reference,Debit Amount,Credit Amount,Transaction Ref1,Transaction Ref2,Transaction Ref3'
    if (line == dbs_format):
        return True
    return False