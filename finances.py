from __future__ import division
import xlrd
import yaml
import sys
import glob

months = {
		1 : 'January',
		2 : 'February',
		3 : 'March',
		4 : 'April',
		5 : 'May',
		6 : 'June',
		7 : 'July',
		8 : 'August',
		9 : 'September',
		10 : 'October',
		11 : 'November',
		12 : 'December'
	}

ignore_categories = {}
finance_constants = {}
total = 0
# For convenience, total_by_month[1] ... total_by_month[12] correspond to the months and
# total_by_month[0] is left as 0
total_by_month = [0] * 13
income = 0
income_by_month = [0] * 13
column_indices = {}
start_row = 0

def main():
	read_finance_constants()
	total_amount_spent = {}
	total_amount_spent_by_month = {}
	get_data(total_amount_spent, total_amount_spent_by_month)

	if not income == 0:
		print "Total Income: " + str(income)
	print "Total Expenses: " + str(total)
	if not income == 0:
		print "Total Net Savings: " + str(income + total)
	for category in total_amount_spent:
		print "\t" + category + ": " + str(total_amount_spent[category])
	print

	for month in months:
		if not month in total_amount_spent_by_month:
			continue
		print "\033[1m" + month_string(month) + "\033[0m: "
		if not income_by_month[month] == 0:
			print "Income: " + str(income_by_month[month])
		print "Expenses: " + str(total_by_month[month])
		if not income_by_month[month] == 0:
			print "Net Savings: " + str(income_by_month[month] + total_by_month[month])
		for category in total_amount_spent_by_month[month]:
			print "\t" + category + ": " + str(total_amount_spent_by_month[month][category])

'''
Returns the month string for the corresponding int
'''
def month_string(month):
	return months[month]

'''
Gets the input from the finance_constants.yaml file
'''
def read_finance_constants():
	global finance_constants, ignore_categories, column_indices, start_row
	with open("finance_constants.yaml", "r") as stream:
		try:
			finance_constants = yaml.load(stream)
		except yaml.YAMLError as e:
			print(e)
			sys.exit(1)
	# Checks if ignore categories is in finance_constants and if finance_constants["ignore_categories"] is not null
	if "ignore_categories" in finance_constants and finance_constants["ignore_categories"]:
		ignore_categories = finance_constants["ignore_categories"]
	column_indices = finance_constants["column_indices"]
	start_row = finance_constants["start_row"]

'''
Returns the total amount spent in total and by month
'''
def get_data(total_amount_spent, total_amount_spent_by_month):
	global total, total_by_month, income, income_by_month
	for finance_sheet in get_finance_file_paths():
		try:
			book = xlrd.open_workbook(finance_sheet)
		except xlrd.biffh.XLRDError as xlrde:
			print("Could not open " + finance_sheet)
			sys.exit(1)
		for sheet in book.sheets():
			dates = sheet.col(column_indices["dates"])
			amounts = sheet.col(column_indices["amounts"])
			categories = sheet.col(column_indices["categories"])
			groups = None
			if "groups" in column_indices and column_indices["groups"] < sheet.ncols:
				groups = sheet.col(column_indices["groups"])
			for i in range(0 + start_row, len(dates)):
				month = xlrd.xldate.xldate_as_datetime(dates[i].value, book.datemode).month
				if groups and groups[i].value:
					category = groups[i].value
				else:
					category = categories[i].value
				amount = amounts[i].value
				if not amount:
					continue
				if category in ignore_categories:
					continue

				if amount > 0:
					income = income + amount
					income_by_month[month] = income_by_month[month] + amount
				else:
					total = total + amount
					total_by_month[month] = total_by_month[month] + amount
				if not category in total_amount_spent:
					total_amount_spent[category] = 0
				total_amount_spent[category] = total_amount_spent[category] + amount

				if not month in total_amount_spent_by_month:
					total_amount_spent_by_month[month] = {}
				if not category in total_amount_spent_by_month[month]:
					total_amount_spent_by_month[month][category] = 0
				total_amount_spent_by_month[month][category] = total_amount_spent_by_month[month][category] + amount

'''
Evaluates the regexs for the file paths
'''
def get_finance_file_paths():
	paths = []
	for regex in finance_constants["finances_files"]:
		for f in glob.glob(regex):
			paths.append(f)
	return paths

if __name__ == '__main__':
	main()