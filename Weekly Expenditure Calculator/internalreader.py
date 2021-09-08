import csv
import pandas as pd

def parse_csv(fname):

    df = pd.read_csv(fname, sep='|', index_col=0, dtype=str)
    df['datetime'] = df['datetime'].astype('datetime64[ns]')
    return df
