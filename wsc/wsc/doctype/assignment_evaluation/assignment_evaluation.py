# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssignmentEvaluation(Document):
	pass

@frappe.whitelist()
def get_details(participant_group_id):
	if(participant_group_id == ''):
		return ['','','','','', '']
	else:
		group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
		instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
		participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
		# assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_id='%s' AND programs = '%s' AND course='%s' AND evaluate = 1 """%(participant_group_id, instructor_id, group_details[0]['program'], group_details[0]['course']))
		# exam_assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment Declaration` WHERE participant_group = '%s' AND trainer_id = '%s' AND course = '%s' AND module = '%s'"""%(participant_group_id, instructor_id, group_details[0]['program'], group_details[0]['course']))
		return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, participants]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	if(participant_group_id == ''):
		return ''
	else:
		instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
		return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participant_name(participant_group_id, participant_id):
	if(participant_group_id == ''):
		return ''
	else:
		participant_name = frappe.db.sql(""" SELECT participant_name FROM `tabParticipant Table` WHERE parent = '%s' AND participant = '%s'"""%(participant_group_id, participant_id), as_dict=1)
		return participant_name[0]['participant_name']

@frappe.whitelist()
def get_assignment_list(instructor_id = None, participant_group_id = None, programs = None, course = None):
	if(instructor_id == None or participant_group_id == None or programs == None or course == None):
		return ['','','','','', '']
	else:
		assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND instructor_id='%s' AND programs = '%s' AND course='%s' AND evaluate = 1 """%(participant_group_id, instructor_id, programs, course))
		exam_assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment Declaration` WHERE participant_group = '%s' AND evaluator_id = '%s' AND course = '%s' AND module = '%s'"""%(participant_group_id, instructor_id, programs, course))
		return (assignments + exam_assignments)

@frappe.whitelist()
def get_assignment_details(assignment_name = None):
	if(assignment_name == None):
		return ['','','','','', '']
	else:
		count1 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment` WHERE name = '%s'"""%(assignment_name))
		count2 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Declaration` WHERE name = '%s'"""%(assignment_name))
		if(count1[0][0] > 0):
			criteria_details = frappe.get_all('Assignment', filters = [['name','=',assignment_name]], fields = ['assignment_name','assessment_criteria','total_marks', 'passing_marks', 'weightage'])
			return [criteria_details[0]['assessment_criteria'], criteria_details[0]['total_marks'],criteria_details[0]['passing_marks'],criteria_details[0]['weightage'],criteria_details[0]['assignment_name']]
		elif(count2[0][0] > 0):
			criteria_details = frappe.get_all('Assignment Declaration', filters = [['name','=',assignment_name]], fields = ['assignment_name','select_assessment_criteria','total_marks','pass_marks','weightage'])
			return [criteria_details[0]['select_assessment_criteria'], criteria_details[0]['total_marks'],criteria_details[0]['pass_marks'],criteria_details[0]['weightage'],criteria_details[0]['assignment_name']]

@frappe.whitelist()
def set_marks1(participant_id, assignment_name):
	data = frappe.db.sql(""" SELECT status FROM `tabParticipant List Table` WHERE parent = '%s' AND participant_id = '%s'"""%(assignment_name, participant_id), as_dict =1)
	if(data[0]['status'] == 'Not Qualified'):
		return 0
	
@frappe.whitelist()
def set_marks(participant_id, assignment_name):
	count1 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment` WHERE name = '%s'"""%(assignment_name))
	count2 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Declaration` WHERE name = '%s'"""%(assignment_name))
	if(count1[0][0] > 0):
		data1 = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Upload` WHERE assignment_id = '%s' AND participant_id ='%s'"""%(assignment_name, participant_id))
		if(data1[0][0] == 0):
			return 0
	elif(count2[0][0] > 0):
		data2 = frappe.db.sql(""" SELECT status FROM `tabParticipant List Table` WHERE parent = '%s' AND participant_id = '%s'"""%(assignment_name, participant_id), as_dict =1)
		if(data2[0]['status'] == 'Not Qualified'):
			return 0
		


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