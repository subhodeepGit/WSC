# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FinalAssignmentResult(Document):
	pass

@frappe.whitelist()
def get_details(participant_group_id):
	group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
	course_details = frappe.get_all('Course', filters = [['name', '=', group_details[0]['course']]], fields = ['course_name','course_code'])
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], participants, course_details[0]['course_name'], course_details[0]['course_code']]

@frappe.whitelist()
def get_participant_name(participant_group_id, participant_id):
	participant_name = frappe.db.sql(""" SELECT participant_name FROM `tabParticipant Table` WHERE parent = '%s' AND participant = '%s'"""%(participant_group_id, participant_id), as_dict=1)
	return participant_name[0]['participant_name']

@frappe.whitelist()
def get_assignments(participant_group_id, participant_id, grading_scale):
	assignments = frappe.get_all('Assignment Evaluation', filters = [['participant_group','=', participant_group_id],['participant_id','=', participant_id]], fields = ['select_assignment', 'assessment_criteria', 'marks_earned', 'total_marks', 'assignment_name'])
	for d in assignments:
		percentage = (d['marks_earned'] / d['total_marks']) * 100
		assignment_data = frappe.get_all('Grading Scale Interval', filters = [['parent','=', grading_scale]], fields = ['result', 'threshold', 'grade_code'])
		d['threshold'] = assignment_data[0]['threshold']
		d['result'] = assignment_data[0]['result']
		d['grade_code'] = assignment_data[0]['grade_code']
	return assignments

