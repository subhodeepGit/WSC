# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssignmentEvaluationTool(Document):
	def validate(self):
		for d in self.get('participant_details_data'):
			result = frappe.new_doc('Assignment Evaluation')
			result.participant_group = self.participant_group
			result.select_course = self.course
			result.select_module = self.module
			result.select_sub_module = self.select_sub_module
			result.academic_year = self.academic_term
			result.academic_term = self.academic_year
			result.participant_id = d.participant_id
			result.participant_name = d.participant_name
			result.instructor_id = self.instructor_id
			result.instructor_name = self.instructor_name
			result.select_assignment = self.select_job_sheetassessment
			result.assignment_name = self.assignment_name
			result.assessment_criteria = self.assessment_criteria
			result.total_marks = self.total_marks
			result.passing_marks = self.passing_marks
			result.weightage = self.weightage
			result.marks_earned = d.earned_marks
			result.save()

@frappe.whitelist()
def get_details(participant_group_id):
	total_participants = frappe.db.sql(""" SELECT COUNT(*) FROM `tabParticipant Table` WHERE parent = '%s'"""%(participant_group_id), as_dict=1)
	group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, participants, total_participants[0]['COUNT(*)']]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_assignment_list(instructor_id, participant_group_id, programs, course, topic):
	assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_id='%s' AND programs = '%s' AND course='%s'"""%(participant_group_id, instructor_id, programs, course))
	exam_assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment Declaration` WHERE participant_group = '%s' AND trainer_id = '%s' AND course = '%s' AND module = '%s'"""%(participant_group_id, instructor_id, programs, course))
	return (assignments + exam_assignments)

@frappe.whitelist()
def get_participants(participant_group_id):
	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
	return participants

@frappe.whitelist()
def get_assignment_details(assignment_name):
	assignment_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment` WHERE name = '%s' """%(assignment_name), as_dict=1)
	exam_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Declaration` WHERE name = '%s' """%(assignment_name), as_dict=1)
	if(int(assignment_count[0]['COUNT(*)']) > 0 ):
		criteria_details = frappe.get_all('Assignment', filters = [['name', '=', assignment_name]], fields = ['assignment_name', 'assessment_criteria', 'total_marks','passing_marks','weightage'])
		return [criteria_details[0]['assessment_criteria'] ,criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage'], criteria_details[0]['assignment_name']]
	elif(int(exam_count[0]['COUNT(*)']) > 0):
		criteria_details = frappe.get_all('Assignment Declaration', filters = [['name', '=', assignment_name]], fields = ['assignment_name', 'select_assessment_criteria', 'total_marks','pass_marks','weightage'])
		return [criteria_details[0]['select_assessment_criteria'] ,criteria_details[0]['total_marks'], criteria_details[0]['pass_marks'], criteria_details[0]['weightage'], criteria_details[0]['assignment_name']]
		