# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PlacementTool(Document):
	@frappe.whitelist()
	def schedule_round(self):
		for d in self.get('student_list'):
			result = frappe.new_doc('Selection Round')
			result.student_name = d.student_name
			result.student_no = d.student_no
			result.program_name = d.program_name
			result.academic_year = d.academic_year
			result.semesters = d.semesters
			result.company_name = self.company_name
			result.placement_batch_year = self.placement_batch_year
			result.placement_drive_name = self.placement_drive_name
			result.round_of_placement = self.round_of_placement
			result.scheduled_date_of_round = self.scheduled_date_of_round
			result.save()
			result.submit()

@frappe.whitelist()
def get_student(drive_name):
    student_data = frappe.get_all('Placement Drive Application', [['placement_drive', '=', drive_name],['status', '=','Shortlisted']], ['student','name', 'student_name'])
    for t in student_data:
        data = frappe.get_all('Current Educational Details',{'parent':t['student'], 'parenttype':'student'},['programs','semesters', 'academic_year'])
        t['programs'] = data[0]['programs']
        t['semesters'] = data[0]['semesters']
        t['academic_year'] = data[0]['academic_year']
    return student_data

@frappe.whitelist()
def get_rounds_of_placement(drive_name):
    print(drive_name)
    data = frappe.db.sql(""" SELECT round_name from `tabRounds of Placement` where parent="%s" """%(drive_name))
    return data

@frappe.whitelist()
def get_date_of_round(doc, drive_name, round_name):
	data = frappe.db.sql(""" SELECT date , reporting_time from `tabRounds of Placement` where parent = '%s' AND round_name = '%s'"""%(drive_name, round_name))
	# print(data)
	return data