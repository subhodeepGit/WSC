# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantRegistration(Document):
	pass

@frappe.whitelist()
def get_program_name(program_id = None):
	program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
	if(len(program_name) > 0):
		return program_name[0][0]

@frappe.whitelist()
def get_event_details(event_id):
	event_details = frappe.db.sql(""" SELECT event_name, event_date, start_time FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	program_details = frappe.db.sql(""" SELECT in_a_program FROM `tabTnP Event` WHERE name = '%s'"""%(event_id))
	if(program_details[0][0] == 0):
		return [program_details[0][0], event_details[0][0], event_details[0][1], event_details[0][2]]
	elif(program_details[0][0] == 1):
		program_id = frappe.db.sql(""" SELECT select_program FROM `tabTnP Event` WHERE name ='%s'"""%(event_id))
		return [program_details[0][0], program_id[0][0], event_details[0][0], event_details[0][1], event_details[0][2]]

@frappe.whitelist()
def get_participant_name(participant_type = None, participant_id = None):
	
	if(len(participant_id) > 0):
		if(participant_type == 'Student'):
			student_name = frappe.db.sql(""" SELECT student_name FROM `tabStudent` WHERE name ='%s'"""%(participant_id))
			return student_name[0][0]
		elif(participant_type == 'Employee'):
			employee_name = frappe.db.sql(""" SELECT employee_name FROM `tabEmployee` WHERE name ='%s'"""%(participant_id))
			return employee_name[0][0]