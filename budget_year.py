from __future__ import division

"""
Keeps track of all the budget finances for a specific year
"""
class BudgetYear:
	def __init__(self, year):
		self.year = year
		# For convenience, total_by_month[1] ... total_by_month[12] correspond to the months and
		# total_by_month[0] is left as 0
		self.total_by_month = [0] * 13
		self.income_by_month = [0] * 13
		# total_amount_speny_by_month corresponds to the amount spent or earned by category
		self.total_amount_spent_by_month = {}

	def add_item(self, month, amount, category):
		if amount > 0:
			self.income_by_month[month] += amount
		else:
			self.total_by_month[month] += amount
		if not month in self.total_amount_spent_by_month:
			self.total_amount_spent_by_month[month] = {}
		if not category in self.total_amount_spent_by_month[month]:
			self.total_amount_spent_by_month[month][category] = 0
		self.total_amount_spent_by_month[month][category] += amount

	def get_year(self):
		return self.year

	def get_total_by_month(self):
		return self.total_by_month

	def get_income_by_month(self):
		return self.income_by_month

	def get_total_amount_spent_by_month(self):
		return self.total_amount_spent_by_month
