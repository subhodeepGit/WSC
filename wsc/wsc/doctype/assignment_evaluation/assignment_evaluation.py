# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssignmentEvaluation(Document):
	pass

@frappe.whitelist()
def get_details(participant_group_id):
	group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
	# assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_id='%s' AND programs = '%s' AND course='%s' AND evaluate = 1 """%(participant_group_id, instructor_id, group_details[0]['program'], group_details[0]['course']))
	# exam_assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment Declaration` WHERE participant_group = '%s' AND trainer_id = '%s' AND course = '%s' AND module = '%s'"""%(participant_group_id, instructor_id, group_details[0]['program'], group_details[0]['course']))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, participants]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participant_name(participant_group_id, participant_id):
	participant_name = frappe.db.sql(""" SELECT participant_name FROM `tabParticipant Table` WHERE parent = '%s' AND participant = '%s'"""%(participant_group_id, participant_id), as_dict=1)
	return participant_name[0]['participant_name']

@frappe.whitelist()
def get_assignment_list(instructor_id, participant_group_id, programs, course):
	assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_id='%s' AND programs = '%s' AND course='%s' AND evaluate = 1 """%(participant_group_id, instructor_id, programs, course))
	exam_assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment Declaration` WHERE participant_group = '%s' AND evaluator_id = '%s' AND course = '%s' AND module = '%s'"""%(participant_group_id, instructor_id, programs, course))
	return (assignments + exam_assignments)

@frappe.whitelist()
def get_assignment_details(assignment_name):
	criteria_details = frappe.get_all('Assignment', filters = [['name', '=', assignment_name]], fields = ['assignment_name', 'assessment_criteria', 'total_marks','passing_marks','weightage'])
	return [criteria_details[0]['assessment_criteria'] ,criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage'], criteria_details[0]['assignment_name']]