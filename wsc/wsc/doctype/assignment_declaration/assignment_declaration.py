# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe import msgprint, _

class AssignmentDeclaration(Document):
	def validate(self):
		self.validate_duplication()



	def validate_duplication(self):
		"""Check if the Assignment Declaration Record is Unique"""
		assignment_record = None
		
		assignment_record = frappe.db.exists('Assignment Declaration', {
			'select_assessment_criteria': self.select_assessment_criteria,
			'module': self.module,
			'course': self.course,
			'academic_year': self.academic_year,
			'docstatus': ('!=', 2),
			'name': ('!=', self.name)
		})

		if assignment_record:
			record = get_link_to_form('Assignment Declaration', assignment_record)
			frappe.throw(_('Assignment Declaration record {0} already exists!')
				.format(record), title=_('Duplicate Entry'))


@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	if(participant_group_id == '' or instructor_id == ''):
		return ['','','','','', '', '']
	else:
		instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
		return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_criteria_details(course, assessment_criteria):
	if(course == '' or assessment_criteria == ''):
		return ['','','','','', '', '']
	else:
		criteria_details = frappe.get_all('Credit distribution List', filters = [['parent', '=', course], ['assessment_criteria', '=', assessment_criteria]], fields = ['total_marks','passing_marks','weightage'])
		return [criteria_details[0]['total_marks'], criteria_details[0]['passing_marks'], criteria_details[0]['weightage']]


@frappe.whitelist()
def get_participants(participant_group_id = None, attendance_applicable = 0, attendance_percentage = 0):
	if(participant_group_id == None):
		pass
	else:
		participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
		for d in participants:
			participant_classes = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Class Table` WHERE parent = '%s'"""%(participant_group_id))
			participant_present_for = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s' AND docstatus = 1 AND status = 'Present'"""%(d.participant, participant_group_id))
			try:
				final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
			except ZeroDivisionError:
				final_attendance = 0
			# final_attendance = (participant_present_for[0][0]/participant_classes[0][0])*100
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

@frappe.whitelist()
def criteria(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)
	course =filters.get('course')
	criteria_details = frappe.db.sql(""" SELECT assessment_criteria FROM `tabCredit distribution List` where ({key} like %(txt)s or {scond}) and
													parent = '{course}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"course": course
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return criteria_details
# -----------------------------------------------------------------------------------------------------------------------------

@frappe.whitelist()
def get_assignments(participant_group=None,select_assessment_criteria=None):
	assignments = []
	if participant_group != None:
		assignments = frappe.get_all("Assignment",filters=[["participant_group","=",participant_group],["assessment_criteria","=",select_assessment_criteria],["docstatus","=",1],["evaluate","=",1]],fields=['name','assignment_name','assessment_criteria','weightage','total_marks','passing_marks','start_date','end_date','total_duration'],group_by="name")
	return assignments