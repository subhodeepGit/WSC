# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json

class Generatecertificatetool(Document):
	pass

@frappe.whitelist()
def get_program_name(program_id):
	program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
	return program_name[0][0]

@frappe.whitelist()
def get_event_details(event_id):
	event_details = frappe.db.sql(""" SELECT event_name FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	return event_details[0][0]

@frappe.whitelist()
def get_eligible_participants(event_id):
	parent_name = frappe.db.sql( """ SELECT name FROM `tabParticipant Attendance` WHERE select_event = '%s' """%(event_id))
	parent_name = parent_name[0][0]
	participant_data = frappe.get_all('Selected participants list', filters = [['parent', '=', parent_name],['present', '=', 1]], fields = ['participant_id', 'participant_name']) 
	print('\n\n\n\n')
	print(participant_data)
	print('\n\n\n\n')
	return participant_data

@frappe.whitelist()
def generate_record(doc):
	obj = json.loads(doc)
	program_status = obj['is_in_a_program']
	participants_table = obj['selected_participants_list']
	# print('\n\n\n\n\n')
	# print(participants_table[0]['participant_id'])
	# print('\n\n\n\n')

	# print('\n\n\n\n')
	# for d in participants_table:
	# 	print(d['participant_id'])
	# print('\n\n\n\n')

	if(program_status == 1):
		for d in participants_table:
			result = frappe.new_doc('Generate Certificate')
			result.is_in_a_program = obj['is_in_a_program']
			result.select_program = obj['select_program']
			result.program_name = obj['program_name']
			result.select_event = obj['select_event']
			result.event_name = obj['event_name']
			result.participant_id = d['participant_id']
			result.participant_name = d['participant_name']
			result.save()
	elif(program_status == 0):
			for d in participants_table:
				result = frappe.new_doc('Generate Certificate')
				result.select_event = obj['select_event']
				result.event_name = obj['event_name']
				result.participant_id = d['participant_id']
				result.participant_name = d['participant_name']
				result.save()