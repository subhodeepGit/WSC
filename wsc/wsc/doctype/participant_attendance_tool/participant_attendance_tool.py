# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantAttendanceTool(Document):
	pass



@frappe.whitelist()
def get_participant_group(based_on):
	data = frappe.db.sql(""" SELECT name FROM `tabParticipant Group`""")
	return data

@frappe.whitelist()
def get_details(participant_group_id):
	print('\n\n\n\n')
	print(participant_group_id)
	print('\n\n\n\n')
	group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	sub_modules = frappe.db.sql(""" SELECT topic FROM `tabCourse Topic` WHERE parent = '%s'"""%(group_details[0]['course']))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, sub_modules]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participants(participant_group_id):
	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
	return participants
