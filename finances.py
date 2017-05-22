from __future__ import division
#from helper_classes import BudgetYear
from budget_year import BudgetYear
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
income = 0
column_indices = {}
start_row = 0

def main():
	read_finance_constants()
	budget_years = {}
	total_amount_spent = {}
	get_data(budget_years, total_amount_spent)

	if not income == 0:
		print "Total Income: " + str(income)
	print "Total Expenses: " + str(total)
	if not income == 0:
		print "Total Net Savings: " + str(income + total)
	for category in total_amount_spent:
		print "\t" + category + ": " + str(total_amount_spent[category])
	print

	for year in sorted(budget_years):
		budget_year = budget_years[year]
		total_amount_spent_by_month = budget_year.get_total_amount_spent_by_month()
		income_by_month = budget_year.get_income_by_month()
		total_by_month = budget_year.get_total_by_month()

		for month in months:
			if not month in total_amount_spent_by_month:
				continue
			print "\033[1m" + month_string(month) + " " + str(year) + "\033[0m: "
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
def get_data(budget_years, total_amount_spent):
	global total, income
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
				date = xlrd.xldate.xldate_as_datetime(dates[i].value, book.datemode)
				month = date.month
				year = date.year
				if groups and groups[i].value:
					category = groups[i].value
				else:
					category = categories[i].value
				amount = amounts[i].value
				if not amount:
					continue
				if category in ignore_categories:
					continue

				if not year in budget_years:
					budget_years[year] = BudgetYear(year)

				if amount > 0:
					income = income + amount
				else:
					total = total + amount
				budget_years[year].add_item(month, amount, category)
				if not category in total_amount_spent:
					total_amount_spent[category] = 0
				total_amount_spent[category] += amount

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