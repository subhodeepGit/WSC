# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ToTParticipantAttendance(Document):
	def validate(self):
		attendance_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s' AND date = '%s'"""%(self.participant_id, self.participant_group, self.date))
		if(attendance_count[0][0] > 0):
			frappe.throw("Record already exists")

@frappe.whitelist()
def get_details(participant_group_id):
	dates = frappe.db.sql(""" SELECT scheduled_date FROM `tabToT Class Schedule` WHERE participant_group_id = '%s'"""%(participant_group_id))
	group_details = frappe.get_all('Participant Group', filters = [['name','=',participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	participants = frappe.db.sql(""" SELECT participant FROM `tabParticipant Table` Where parent='%s'"""%(participant_group_id))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, participants, dates]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participant_name(participant_group_id, participant_id):
	participant_name = frappe.db.sql(""" SELECT participant_name FROM `tabParticipant Table` WHERE parent = '%s' AND participant = '%s'"""%(participant_group_id, participant_id), as_dict=1)
	return participant_name[0]['participant_name']
