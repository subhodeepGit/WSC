# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AssignmentMarksDistribution(Document):
	def validate(self):
		if self.is_new():
			self.duplicate_record()
		self.weightage_cal()
		self.passing_marks_cal()
		self.total_marks_cal()
		self.negtive_value_chk()
	
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
	def duplicate_record(self):
		data=frappe.get_all("Assignment Marks Distribution",{"course":self.course,"assessment_criteria":self.assessment_criteria})
		if data:
			frappe.throw("For the Module %s and For Assessment Component %s Data Already Present"%(self.course,self.assessment_criteria))

	def negtive_value_chk(self):
		for t in self.get("assignment_marks_distribution_child"):
			if t.weightage<=0:
				frappe.throw("Weightage value can't be negative of Zero")
			if t.total_marks<=0:
				frappe.throw("Total Marks value can't be negative of Zero")	
			if t.passing_marks<=0:
				frappe.throw("Passing Marks value can't be negative of Zero")
		


@frappe.whitelist()
def criteria(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)
	course =filters.get('course')


	criteria_details = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where ({key} like %(txt)s or {scond}) and
													parent = '{course}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"course": course
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})

	return criteria_details