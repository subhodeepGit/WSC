# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssignmentDeclaration(Document):
	pass

@frappe.whitelist()
def get_details(participant_group_id):
	group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	assessment_criteria = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where parent = '%s'"""%(group_details[0]['course']))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, assessment_criteria]


@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_criteria_details(course, assessment_criteria):
	criteria_details = frappe.get_all('Credit distribution List', filters = [['parent', '=', course], ['assessment_criteria', '=', assessment_criteria]], fields = ['total_marks','passing_marks','weightage'])
	return [criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage']]

# @frappe.whitelist()
# def get_participants(participant_group_id, attendance_applicable, attendance_percentage = 0):
# 	eligible_participants = []
# 	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
# 	for d in participants:
# 		if(attendance_applicable == '0'):
# 			d['attendance'] = 'NA'
# 		elif(attendance_applicable == '1'):
# 			participant_classes = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Class Table` WHERE parent = '%s'"""%(participant_group_id))
# 			participant_present_for = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s'"""%(d.participant, participant_group_id))
# 			final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
# 			d['attendance'] = "{:.2f}".format(final_attendance)	
# 			if(final_attendance >= int(attendance_percentage)):
# 				eligible_participants.append(d)
# 	if(attendance_applicable == '0'):
# 		return participants
# 	elif(attendance_applicable == '1'):
# 		return eligible_participants


@frappe.whitelist()
def get_participants(participant_group_id, attendance_applicable, attendance_percentage = 0):
	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
	for d in participants:
		participant_classes = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Class Table` WHERE parent = '%s'"""%(participant_group_id))
		participant_present_for = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s'"""%(d.participant, participant_group_id))
		final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
		d['attendance'] = "{:.2f}".format(final_attendance)	
				
		if(attendance_applicable == '1'):
			if(final_attendance >= int(attendance_percentage)):
				d['status'] = 'Qualified'
				pass
			else:
				d['status'] = 'Not Qualified'
		else:
			d['status'] = 'Qualified'

	return participants



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