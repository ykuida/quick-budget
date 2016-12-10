# quick-budget
A Simple Script to compile Income and Expenses from Excel Sheets

## Dependencies:
This script is in python and requires 
* xlrd
* yaml 

Both can be installed via pip.

## Set Up
To use the script you will need excel sheets containing the date, amount, and category of each transaction. You can either create these excel sheets from scratch by manually entering in the data or you can download statements from your bank in excel format. (If they have csv files, you can save them into an excel format.)
For simplicity, the script considers any positive amount to be income and any negative amount to be an expense. If you are using excel files from multiple accounts, transfers between accounts will artificially increase income/expenses (but the net amount will still be the same). If you wish to ignore certain transactions, read the [Optional Parameters](https://github.com/ykuida/quick-budget#optional-parameters) section. 

### Format
In order for the script to read the data, you will need to edit the finance_constants.yaml file to match the format of your excel sheets.

![finances_constants.yaml](/images/constantsScreenshot.png)

By default, it is set up for the dates to be in the first column, the amounts to be in the second column, the categories to be in the third column, and the first data entry to be in the first row. 

If you wish to change this, set the dates, amounts, and categories fields to whatever column index they correspond to in your excel sheets. The first column is index 0, the second column is index 1, and so on. If you wish to change the starting row of your data, change the start_row field.

Now you will need to change the *finances_files* field in the finance_constants.yaml file. This should be a list of the locations of all the excel files you want to include. The script will read from all the sheets of all the files that are in the list. You can list their locations one by one or you can also use regexs. For example, the default value *financeSheets/*\**.xlsx* will use all .xlsx files in the financeSheets directory.

For more options (such as grouping up the categories), read the [Optional Parameters](https://github.com/ykuida/quick-budget#optional-parameters) section.

### Running the script
After the set up is complete, run
> python finances.py

in your terminal.

## Optional Parameters
If there are categories and/or groups that you wish to ignore, add these to the *ignore_categories* list in finance_constants.yaml.

If you downloaded excel files from your bank, the categories/descriptions might be long and sometimes inconsistent. You can shorten and group similar categories by using the *groups* field in finance_constants.yaml. In a separate column, add a name that will serve as the group of the data in that row. When the script parses the data, if it finds a group for the row, it will use the group name instead of the category name. If it finds no group, it will simply use the category. Change the *groups* field to be whatever index the column corresponds to (Similar to above, the first column is index 0, the second column is index 1, and so on).