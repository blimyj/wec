import os
import csv
import datetime
import pandas as pd
import dbsreader
import internalreader
from decimal import Decimal
from datetime import datetime, timedelta

##### INPUT START #####
weekly_expenditure = 80

# List of dbs files
f2 = "..\\Sample Data\\DBS Sample2.csv"
f3 = "..\\Sample Data\\DBS Sample3.csv"
list_of_dbs_files = [f2, f3]

# List of internal format files
if1 = "..\\Sample Data\\finances_csv_2021-08-27_to_2021-08-31.csv"
list_of_internal_files = [if1]

# Enter entries you would like to ignore here
ignored_debit = [] #
ignored_credit = [] #
ignored_entries = ignored_debit + ignored_credit

# Folder to save internal format file
savefolder = "..\\Sample Data\\"

##### INPUT END #####

def str_to_dec(x):
    x = x.strip()
    
    if (len(x) == 0):
        dec = Decimal('0.0')
    else:
        dec = Decimal(x)
    return dec


def convert_to_dec(df: pd.DataFrame):
    df['Debit Amount'] = df['Debit Amount'].apply(str_to_dec)
    df['Credit Amount'] = df['Credit Amount'].apply(str_to_dec)
    return df

# Use pd.grouper with weekly frequency
def group_data_weekly(df: pd.DataFrame):
    # Lambda function is required to maintain the Decimal type, otherwise auto float conversion will occur
    dfgb =  df.groupby(pd.Grouper(key='datetime',freq='W-SAT'))[["Debit Amount","Credit Amount"]]
    df = dfgb.apply(lambda x: x.sum())
    #print(df.info())
    df['Net Amount'] = df.apply(lambda row: row['Debit Amount']-row['Credit Amount'], axis=1)
    return df


# Driver Code

# Use Pandas & drop duplicates
def concat_df(list_of_df):
    df = pd.concat(list_of_df)
    
    df['Transaction Data'] = [str(x).strip() for x in df['Transaction Data']]

    df = df.sort_values(by=["datetime"], ascending=True)
    df = df.reset_index(drop=True)
    df = convert_to_dec(df)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    # print(concat_df)
    return df

def drop_entries(df, ignored_entries):
    print('=======================DROPPING IGNORED ENTRIES=======================')
    df = df.drop(ignored_entries)
    df = df.reset_index(drop=True)
    return df

# Gets weekly expenditure
def get_wbw_exp(df):
    df = group_data_weekly(df)
    df = _resample_df(df)
    df = df.reset_index()
    df['datetime'] = [backdate(date) for date in df['datetime']]
    return df

def backdate(date):
    date = date - timedelta(days=6)
    return date


# Fills in missing weeks with 0 value if there are any
def _resample_df(df):
    df = df.resample('W-SAT').asfreq().replace(0.0, Decimal('0.0'))
    return df


def get_avg_exp(df):
    sum_net = df['Net Amount'].sum()
    num_weeks = Decimal(len(df.index))
    avg_expend = sum_net/num_weeks
    avg_expend_str = str(avg_expend)
    print("Average Weekly Expenditure: %s" % avg_expend_str)
    return avg_expend


def spare_expense(num_weeks, avg_expense, budgetted_amt):
    leftover: Decimal = (budgetted_amt - avg_expense) * num_weeks
    leftover_str = str(leftover)
    print("Excess Funds: %s" % leftover_str)
    return leftover


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def convert_to_csv(df, savefolder):
    
    # Shift indices 
    df.reset_index(drop=True, inplace=True)

    # Get first and last entry date
    startdate_obj = df.iloc[0]['datetime']
    startdate = str(startdate_obj)[:10]
    enddate_obj = df.iloc[-1]['datetime']
    enddate = str(enddate_obj)[:10]
    
    dt_string = startdate + "_to_" + enddate
    filename = "finances_csv_" + dt_string
    path = savefolder + filename +".csv"
    
    # Check if file already exists
    if os.path.isfile(path):
        response = ask_yes_no("File already exists! Are you sure you would like to overwrite the existing csv file?")
        if response:
            df.to_csv(path_or_buf= path,sep = "|")
        else:
            print("Okay, csv file was not saved.")
    else:
        df.to_csv(path_or_buf= path,sep = "|")

    
    return path

# Ask yes or no
def ask_yes_no(question):
    response = input(question + " (yes/no)")
    response = response.lower().strip()
    if response[:1] == 'y':
        return True
    elif response[:1] == 'n':
        return False
    else:
        return ask_yes_no(question)


# Ask if want to convert to csv
def prompt_convert_to_csv(df):
    response = ask_yes_no("Would you like to convert the dataframe to a csv for saving?")
    if response:
        saved_path = convert_to_csv(df, savefolder)
        print("Saved to %s." % saved_path)
    else:
        print("Okay, was not saved.")



# Ask if we want to import df

# Parse csvs into dfs
internal_format_dfs = [internalreader.parse_csv(filename) for filename in list_of_internal_files]
dbs_dfs = [dbsreader.parse_csv(filename) for filename in list_of_dbs_files]
list_of_df = internal_format_dfs + dbs_dfs

# Concat results
concatenated_df = concat_df(list_of_df)
print_full(concatenated_df)

# Ignore certain entries
pruned_df = drop_entries(concatenated_df, ignored_entries)
print_full(pruned_df)
prompt_convert_to_csv(pruned_df)


# Get week-by-week data (also fills in missing weeks data)
grouped_wbw_df = get_wbw_exp(pruned_df)
print_full(grouped_wbw_df)
# Get Average Weekly Expenditure
avg_expense: Decimal = get_avg_exp(grouped_wbw_df)



spare_expense(len(grouped_wbw_df), avg_expense, weekly_expenditure)




# Note: Datetime displays the date of the last day of that week, not the first day of the week.

# TODO: Fix Bug: For csvs with two transactions of similar price and description on same day, add a tag for duplicate so as not to remove them.
    # TODO: Add note that data for CSVS should all contain the entire day's worth of transactions. If the above mentioned transaction occurs across two CSVs, one will be treated as a dupicated and be removed.
# TODO: Check expenses for longer time period
# TODO: Create GUI for this app
  # Consider GUI such that we can specify csv reader for each file
  # TODO: GUI Ask for files
  # TODO: GUI Prints entries
  # TODO: GUI Prompts for entry indices to be ignored
  # TODO: GUI asks about saving data
  # TODO: GUI prints wbw data
