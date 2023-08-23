# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssignmentUpload(Document):
	pass

@frappe.whitelist()
def get_details(participant_group_id):
	group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['program', 'course', 'academic_year', 'academic_term'])
	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
	instructors = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	return [group_details[0]['program'], group_details[0]['course'], group_details[0]['academic_year'],group_details[0]['academic_term'], participants, instructors]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participant_name(participant_group_id, participant_id):
	participant_name = frappe.db.sql(""" SELECT participant_name FROM `tabParticipant Table` WHERE parent = '%s' AND participant = '%s'"""%(participant_group_id, participant_id), as_dict=1)
	return participant_name[0]['participant_name']

@frappe.whitelist()
def get_assignment_list(instructor_name, participant_group_id, programs, course):
	assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_name='%s' AND programs = '%s' AND course='%s'"""%(participant_group_id, instructor_name, programs, course))
	return assignments

@frappe.whitelist()
def get_assignment_details(assignment_name):
	criteria_details = frappe.get_all('Assignment', filters = [['name', '=', assignment_name]], fields = ['assessment_criteria', 'total_marks','passing_marks','weightage'])
	return [criteria_details[0]['assessment_criteria'] ,criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage']]