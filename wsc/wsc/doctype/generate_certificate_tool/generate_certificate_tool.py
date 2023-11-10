# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json

class Generatecertificatetool(Document):
	def validate(self):
		if self.is_new():
			if frappe.get_all("Generate certificate tool",{"docstatus":1,"select_event":self.select_event}):
				frappe.throw("Certificate has been Generate for this Event")
	def on_submit(self):
		for d in self.get('selected_participants_list'):
			result = frappe.new_doc('Generate Certificate')
			result.select_event = self.select_event
			result.event_name = self.event_name
			result.event_start_date = self.event_start_date
			result.event_end_date = self.event_end_date
			result.participant_id = d.participant_id
			result.participant_name = d.participant_name
			result.participant_type = d.participant_type
			result.completion_status = 'Complete'
			if(len(self.select_program) > 0):
				result.program_id = self.select_program
				result.program_name = self.program_name
				result.program_start_date = self.program_start_date
				result.program_end_date = self.program_end_date
			result.save()
			result.submit()

@frappe.whitelist()
def get_program_name(program_id = None):
	if(len(program_id) > 0):
		program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
		return program_name[0][0]

@frappe.whitelist()
def get_event_details(event_id):
	event_details = frappe.db.sql(""" SELECT in_a_program, event_name FROM `tabTnP Event` WHERE name = '%s' """%(event_id))
	if(event_details[0][0] == 0):
		return [event_details[0][0], event_details[0][1]]
	elif(event_details[0][0] == 1):
		program_id = frappe.db.sql(""" SELECT select_program FROM `tabTnP Event` WHERE name ='%s'"""%(event_id))
		return [event_details[0][0], event_details[0][1], program_id[0][0]]

@frappe.whitelist()
def get_eligible_participants(event_id):
	parent_name = frappe.db.sql( """ SELECT name FROM `tabParticipant Attendance` WHERE select_event = '%s' and docstatus = '1'"""%(event_id))
	parent_name = parent_name[0][0]
	participant_data = frappe.get_all('Selected participants list', filters = [['parent', '=', parent_name],['present', '=', 1]], fields = ['participant_id', 'participant_name', 'participant_type']) 
	return participant_data


	