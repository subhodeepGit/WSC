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
			result.academic_year = self.academic_year
			result.academic_term = self.academic_term
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
		for d in self.get('disqualified_participants'):
			result = frappe.new_doc('Assignment Evaluation')
			result.participant_group = self.participant_group
			result.select_course = self.course
			result.select_module = self.module
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
def get_assignment_list(instructor_id, participant_group_id, programs, course):
	assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_id='%s' AND programs = '%s' AND course='%s'"""%(participant_group_id, instructor_id, programs, course))
	exam_assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment Declaration` WHERE participant_group = '%s' AND evaluator_id = '%s' AND course = '%s' AND module = '%s'"""%(participant_group_id, instructor_id, programs, course))
	return (assignments + exam_assignments)

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
		

@frappe.whitelist()
def get_participants1(participant_group_id):
	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
	return participants


@frappe.whitelist()
def get_participants(assignment_name, participant_group_id):
	count1 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment` WHERE name = '%s'"""%(assignment_name))
	count2 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Declaration` WHERE name = '%s'"""%(assignment_name))
	if(count1[0][0] > 0):
		submitted = frappe.get_all('Assignment Upload', filters = [['assignment_id', '=', assignment_name]], fields = ['participant_id', 'participant_name'])
		all_students = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
		key_mapping = {'participant': 'participant_id'}
		mod_allstudents = [{key_mapping.get(old_key, old_key): value for old_key, value in dictionary.items()} for dictionary in all_students]
		not_submitted = [item for item in mod_allstudents if item not in submitted]
		return [submitted, not_submitted]
	elif(count2[0][0] > 0):
		# divide participants into two different categories : qualified and not qualified based on the status field in the assignment declaration child table
		qualified_data = frappe.get_all('Participant List Table', filters = [['parent','=',assignment_name],['status','=', 'Qualified']], fields = ['participant_id', 'participant_name'])
		not_qualified_data = frappe.get_all('Participant List Table', filters = [['parent','=',assignment_name],['status','=', 'Not Qualified']], fields = ['participant_id', 'participant_name'])

		return [qualified_data, not_qualified_data]


# ---------------------------------------------------------------------------------------------
@frappe.whitelist()
def instructor(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

	participant_group_id=filters.get('participant_group_id')
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where ({key} like %(txt)s or {scond}) and
				    parent = '{participant_group_id}'
				    """.format(
						**{
						"key": searchfield,
						"scond": searchfields,
						"participant_group_id":participant_group_id
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return instructor_details

@frappe.whitelist()
def participant(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("TP."+field + " like %(txt)s" for field in searchfields)
	participant_group_id=filters.get('participant_group_id')
	participant_details = frappe.db.sql(""" SELECT TP.name 
											FROM `tabParticipant Table` as PT
											JOIN `tabToT Participant` as TP on TP.name=PT.participant
											where (TP.{key} like %(txt)s or {scond}) and
													PT.parent = '{participant_group_id}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"participant_group_id":participant_group_id
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return participant_details
# -----------------------------------------------------------------------------------------------------------------------------