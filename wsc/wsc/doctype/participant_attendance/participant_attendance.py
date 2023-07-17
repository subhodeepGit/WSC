# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantAttendance(Document):
	pass

@frappe.whitelist()
def get_program_name(program_id):
	program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
	print('\n\n\n\n')
	print(program_name[0][0])
	print("\n\n\n\n")
	return program_name[0][0]

@frappe.whitelist()
def get_event_name(event_id):
	event_details = frappe.db.sql(""" SELECT event_name FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	print('\n\n\n\n')
	print(event_details[0][0])
	print('\n\n\n\n')
	return event_details[0][0]

@frappe.whitelist()
def get_participants(event_id):
	participant_data = frappe.get_all('Participant Registration', filters = [['select_event', '=', event_id]], fields = ['participant_id'])
	for t in participant_data:
		student_name = frappe.get_all('Student', filters = [['name', '=', t['participant_id']]], fields = ['student_name'])
		t['student_name'] = student_name[0]['student_name']
	print('\n\n\n\n')
	print(participant_data)
	print('\n\n\n\n')
	return participant_data