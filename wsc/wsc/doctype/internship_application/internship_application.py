# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class InternshipApplication(Document):
	pass


@frappe.whitelist()
def get_participant_name(participant_id):
	participant_name = frappe.db.sql(""" SELECT student_name FROM `tabStudent` WHERE name = '%s'"""%(participant_id))
	return participant_name[0][0]

@frappe.whitelist()
def get_internship_name(internship_id):
	internship_name = frappe.db.sql(""" SELECT title_of_drive FROM `tabInternship Drive` WHERE name = '%s'"""%(internship_id))
	return internship_name[0][0]