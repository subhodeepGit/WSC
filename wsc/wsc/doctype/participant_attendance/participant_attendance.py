# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantAttendance(Document):
	pass

@frappe.whitelist()
def get_program_name(program_id = None):
	if(len(program_id) > 0):
		program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
		return program_name[0][0]

@frappe.whitelist()
def get_event_name(event_id):
	event_details = frappe.db.sql(""" SELECT event_name FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	return event_details[0][0]

# @frappe.whitelist()
# def get_participants(event_id):
# 	participant_data = frappe.get_all('Participant Registration', filters = [['select_event', '=', event_id]], fields = ['participant_id'])
# 	for t in participant_data:
# 		student_name = frappe.get_all('Student', filters = [['name', '=', t['participant_id']]], fields = ['student_name'])
# 		t['student_name'] = student_name[0]['student_name']
# 	return participant_data


@frappe.whitelist()
def get_participants(event_id):
	participant_data = frappe.get_all('Participant Registration', filters = [['select_event', '=', event_id]], fields = ['participant_id', 'participant_name', 'participant_type'])
	return participant_data


@frappe.whitelist()
def get_event_details(event_id):
		event_details = frappe.db.sql(""" SELECT in_a_program, event_name FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
		if(event_details[0][0] == 0):
			return [event_details[0][0], event_details[0][1]]
		elif(event_details[0][0] == 1):
			program_id = frappe.db.sql(""" SELECT select_program FROM `tabTnP Event` WHERE name ='%s'"""%(event_id))
			return [event_details[0][0], event_details[0][1], program_id[0][0]]