# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
from wsc.wsc.notification.custom_notification import event_feedback_mail

class Eventfeedback(Document):
	def validate(self):
		event_feedback_mail(self)

# @frappe.whitelist()
# def get_participant_name(participant_id, participant_type):
# 	print('\n\n\n')
# 	print('abcd')
# 	print('\n\n\n')
# 	pass


@frappe.whitelist()
def get_participant_name(participant_id, participant_type):
	if(participant_type == 'Student'):
		participant_name = frappe.db.sql(""" SELECT student_name FROM `tabStudent` WHERE name = '%s'"""%(participant_id))
	elif(participant_type == 'Employee'):
		participant_name = frappe.db.sql(""" SELECT employee_name FROM `tabEmployee` WHERE name = '%s'"""%(participant_id))
	return participant_name[0][0]

@frappe.whitelist()
def get_program_name(program_id):
	program_name = frappe.db.sql("""SELECT program_name FROM `tabTnP Program` WHERE name = '%s'"""%(program_id))
	return program_name[0][0]


@frappe.whitelist()
def get_event_details(event_id):
	event_details = frappe.db.sql(""" SELECT in_a_program, event_name FROM `tabTnP Event` WHERE name = '%s'"""%(event_id))
	if(event_details[0][0] == 0):
		return [event_details[0][0] ,event_details[0][1]]
	elif(event_details[0][0] == 1):
		program_id = frappe.db.sql(""" SELECT select_program FROM `tabTnP Event` WHERE name ='%s'"""%(event_id))
		return [event_details[0][0] ,event_details[0][1], program_id[0][0]]
		