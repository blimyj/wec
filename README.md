This program parses DBS transaction csv files and generates a table of how much you spend each week.
- It allows you to selectively remove certain transactions that you don't want to include in the weekly expenditure calculations.
    in the ignored entries section.
- It allows you to save the new transaction history in a custom format so you don't have to keep reviewing the entries you want to remove.
- You can specify the save location in the savefolder section.
- You specify the DBS transaction csv files in the List of dbs files section.
- You specify the saved internal format files in the List of internal files section.
- All sections to input filepaths and entry indices are found in csvmerge.py.

To run the program: 
1. Navigate to the folder containing the file `csvmerge.py` via commandline
2. Run command: `python csvmerge.py`

- Note that the csv files must use Unix LF Line endings!

Example of Program:

![Example 1](https://github.com/blimyj/wec/blob/main/Examples/Example%201.gif)


![Example 2](https://github.com/blimyj/wec/blob/main/Examples/Example%202.gif)