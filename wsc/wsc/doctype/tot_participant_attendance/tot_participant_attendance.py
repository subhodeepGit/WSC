# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate

class ToTParticipantAttendance(Document):
	def validate(self):
		# attendance_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s' AND date = '%s'"""%(self.participant_id, self.participant_group, self.date))
		# if(attendance_count[0][0] > 0):
		# 	frappe.throw(_('Attendance record already exists against the Participant {0}')
        #         .format(frappe.bold(self.participant_id)), title=_('Duplicate Entry'))
		self.validate_duplication()
		self.validate_date()

	def validate_date(self):
		if getdate(self.date) > getdate():
			frappe.throw(_('Attendance cannot be marked for future dates.'))
			
	def validate_duplication(self):
		"""Check if the Attendance Record is Unique"""
		attendance_record = None
		
		attendance_record = frappe.db.exists('ToT Participant Attendance', {
			'participant_group': self.participant_group,
			'participant_id': self.participant_id,
			'class_schedule': self.class_schedule,
			'date': self.date,
			'docstatus': ('!=', 2),
			'name': ('!=', self.name)
		})

		if attendance_record:
			record = get_link_to_form('ToT Participant Attendance', attendance_record)
			frappe.throw(_('Attendance record {0} already exists against the Participant {1}')
				.format(record, frappe.bold(self.participant_id)), title=_('Duplicate Entry'))

@frappe.whitelist()
def get_details(participant_group_id):
	if(participant_group_id == ''):
		return ['','','','', '', '']
	else:
		dates = frappe.db.sql(""" SELECT scheduled_date FROM `tabToT Class Schedule` WHERE participant_group_id = '%s'"""%(participant_group_id))
		group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
		instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
		# participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
		return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, dates]

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

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	if(participant_group_id == '' or instructor_id == ''):
		return ''
	else:
		instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
		return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participant_name(participant_group_id, participant_id):
	if(participant_group_id == '' or participant_id == ''):
		return ''
	else:
		participant_name = frappe.db.sql(""" SELECT participant_name FROM `tabParticipant Table` WHERE parent = '%s' AND participant = '%s'"""%(participant_group_id, participant_id), as_dict=1)
		return participant_name[0]['participant_name']
