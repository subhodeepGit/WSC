# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class InternshipParticipantSelection(Document):
	def validate(self):
		if self.is_new():
			if frappe.get_all("Internship Participant Selection",{"select_internship":self.select_internship,"docstatus":1}):
				frappe.throw("Internship Participant Selection Already Exist For This Internship Drive")

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]

@frappe.whitelist()
def get_applied_participants(internship_id):
	participant_data = frappe.get_all('Internship Application', filters = [['select_internship', '=', internship_id],['docstatus','=','1']], fields = ['participant_id', 'participant_name', 'participant_type'])
	return participant_data

