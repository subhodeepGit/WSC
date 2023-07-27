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
		percentage = (d['marks_earned'] / d['total_marks']) * 100 #based on the 
		assignment_data_new = frappe.db.sql("""SELECT result, threshold, grade_code FROM `tabGrading Scale Interval` WHERE parent = '%s' """%(grading_scale))
		list = []
		grade = []
		for i in assignment_data_new:
			list.append(i)
		list.sort(key = lambda x:x[1])
		for i in list:
			if(percentage >= i[1]):
				grade = i
		d['result'] = grade[0]
		d['percentage'] = grade[1]
		d['grade_code'] = grade[2]

	total_percentage = 0
	count = 0

	for i in assignments:
		count += 1
		total_percentage += i['percentage']
	over_all_percentage = (total_percentage / count)
	
	final_list = []
	final_grade_components = []
	for i in assignment_data_new:
		final_list.append(i)
	final_list.sort(key = lambda x:x[1])
	for i in list:
		if(over_all_percentage >= i[1]):
			final_grade_components = i

	final_result = final_grade_components[0]
	final_grade = final_grade_components[2]
	
	return([assignments, over_all_percentage, final_grade, final_result])