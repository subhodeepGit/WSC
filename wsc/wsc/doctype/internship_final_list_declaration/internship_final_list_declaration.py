# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class InternshipFinalListDeclaration(Document):
	def validate(self):
		if self.is_new():
			if frappe.get_all("Internship Final List Declaration",{"select_internship":self.select_internship,"docstatus":1}):
				frappe.throw("Internship Final List Declaration Already Exist For This Internship Drive")

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]

@frappe.whitelist()
def get_selected_participants(internship_id):
	parent_name = frappe.db.sql(""" SELECT name FROM `tabInternship Participant Selection` WHERE select_internship = '%s' and docstatus=1 """%(internship_id))
	if(parent_name):
		parent_name = parent_name[0][0]
		participant_data = frappe.get_all('Internship Select Participants Table', filters = [['parent', '=', parent_name], ['select', '=', 1]], fields = ['applicant_id', 'applicant_name'])
		return participant_data
	else:	
		return []
	