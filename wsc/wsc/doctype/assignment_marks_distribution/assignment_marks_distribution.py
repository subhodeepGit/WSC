# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AssignmentMarksDistribution(Document):
	def validate(self):
		self.weightage_cal()
		self.passing_marks_cal()
		self.total_marks_cal()
	
	def weightage_cal(self):
		weightage=0
		for t in self.get('assignment_marks_distribution_child'):
			weightage+=t.weightage
		if weightage!=100:
			frappe.throw(" Total Weightage Must Be 100% ")

	def passing_marks_cal(self):
		passing=0
		for t in self.get('assignment_marks_distribution_child'):
			passing+=int(t.passing_marks)
		if passing!=int(self.passing_marks):
			frappe.throw(" Aggregate Passing Marks Should Be Equal To Total Passing Marks ")
	def total_marks_cal(self):
		total=0
		for t in self.get("assignment_marks_distribution_child"):
			total+=t.total_marks

		if total!=int(self.total_marks):
			frappe.throw(" Aggregate Total Marks Should Be Equal To Total Marks ")


