# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ToTParticipantSelection(Document):
	def before_submit(self):
		self.create_tot_batch()
	def create_tot_batch(self):
		tot_batch = frappe.get_doc(
			{
				"doctype": "Student Batch Name",
				"batch_name": self.tot_participant_batch,
			}
		)
			# for duplicate_batch_check in frappe.get_all("Student Batch Name",{'name':self.tot_participant_batch},['name']):
			# 	if duplicate_batch_check.name==self.tot_participant_batch:
			# 		pass
			# 	else:
		tot_batch.save()
@frappe.whitelist()
def get_semester(course):
	for sem in frappe.get_all("Program",{'programs':course},['name']):
		semester=sem.name
	return semester
@frappe.whitelist()
def get_academic_term(academic_year):
	for acd_yr in frappe.get_all("Academic Term",{'academic_year':academic_year},['name']):
		academic_term=acd_yr.name
	return academic_term