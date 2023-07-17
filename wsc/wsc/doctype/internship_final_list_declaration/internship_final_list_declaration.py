# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class InternshipFinalListDeclaration(Document):
	pass

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]

@frappe.whitelist()
def get_selected_participants(internship_id):
	parent_name = frappe.db.sql(""" SELECT name FROM `tabInternship Participant Selection` WHERE select_internship = '%s'"""%(internship_id))
	parent_name = parent_name[0][0]
	participant_data = frappe.get_all('Internship Select Participants Table', filters = [['parent', '=', parent_name], ['select', '=', 1]], fields = ['applicant_id', 'applicant_name'])
	print('\n\n\n\n')
	print(participant_data)
	print('\n\n\n\n')
	return participant_data