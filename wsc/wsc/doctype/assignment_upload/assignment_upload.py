# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
# from frappe.utils import now
import datetime

class AssignmentUpload(Document):
	def validate(self): 
		formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
		start_date = self.start_date
		end_date = self.end_date
		if formatted_datetime < start_date or formatted_datetime > end_date:
			frappe.throw('Cannot submit assignment before or after assigned dates')
		else:
			record_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabAssignment Upload` where participant_group = '%s' AND participant_id = '%s' AND assignment_id = '%s' AND docstatus = '1'"""%(self.participant_group, self.participant_id, self.assignment_id))
			if(record_count[0][0] > 0):
				frappe.throw('Record already exists')

@frappe.whitelist()
def get_details(participant_group_id):
	if(participant_group_id == ''):
		return ['','','','','', '', '']
	else:
		group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['program', 'course', 'academic_year', 'academic_term'])
		participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
		instructors = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
		assignments = frappe.db.sql(""" SELECT name FROM `tabAssignment` WHERE participant_group='%s' AND programs = '%s' AND course='%s'"""%(participant_group_id, group_details[0]['program'], group_details[0]['course']))
		return [group_details[0]['program'], group_details[0]['course'], group_details[0]['academic_year'],group_details[0]['academic_term'], participants, instructors, assignments]

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
def get_assignment_details(assignment_name):
	if(assignment_name == ''):
		return ['','','','','', '', '']
	else:
		criteria_details = frappe.get_all('Assignment', filters = [['name', '=', assignment_name]], fields = ['assessment_criteria', 'total_marks','passing_marks','weightage', 'assignment_name', 'start_date', 'end_date'])
		return [criteria_details[0]['assessment_criteria'] ,criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage'], criteria_details[0]['assignment_name'], criteria_details[0]['start_date'], criteria_details[0]['end_date']]


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

@frappe.whitelist()
def assignment(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

	participant_group_id=filters.get('participant_group_id')
	assignment_details = frappe.db.sql(""" SELECT name FROM `tabAssignment` where ({key} like %(txt)s or {scond}) and
				    participant_group = '{participant_group_id}'
				    """.format(
						**{
						"key": searchfield,
						"scond": searchfields,
						"participant_group_id":participant_group_id
					}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return assignment_details

# -----------------------------------------------------------------------------------------------------------------------------