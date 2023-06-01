# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantRegistration(Document):
	pass

@frappe.whitelist()
def get_program_name(program_id):
	program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
	print('\n\n\n\n')
	print(program_name[0][0])
	print("\n\n\n\n")
	return program_name[0][0]

@frappe.whitelist()
def get_event_details(event_id):
	event_details = frappe.db.sql(""" SELECT event_name, event_date, start_time FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	print('\n\n\n\n')
	print(event_details[0][0])
	print(event_details[0][1])
	print(event_details[0][2])
	print('\n\n\n\n')
	return [event_details[0][0], event_details[0][1], event_details[0][2]]