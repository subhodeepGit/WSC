# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantAttendanceTool(Document):
	def validate(self):
		

		for d in self.get('participants'):
			new_doc = frappe.new_doc("ToT Participant Attendance")
			new_doc.participant_group = self.participant_group
			new_doc.select_course = self.select_course
			new_doc.select_module = self.select_module
			new_doc.select_sub_module = self.select_sub_module
			new_doc.academic_year = self.academic_year
			new_doc.academic_term = self.academic_term
			new_doc.instructor_id = self.instructor_id
			new_doc.instructor_name = self.instructor_name
			new_doc.participant_id = d.participant_id
			new_doc.participant_name = d.participant_name
			new_doc.date = self.date
			new_doc.time = self.term
			
			if(d.present == 1):
				new_doc.status = "Present"
			else:
				new_doc.status = "Absent"

			attendance_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabToT Participant Attendance` WHERE participant_id = '%s' AND participant_group = '%s' AND date = '%s'"""%(d.participant_id, self.participant_group, self.date))
			if(attendance_count[0][0] > 0):
				frappe.throw(f"Record already exists for {d.participant_id}")
			else:
				new_doc.save()		
			
@frappe.whitelist()
def get_participant_group(based_on):
	data = frappe.db.sql(""" SELECT name FROM `tabParticipant Group`""")
	return data

@frappe.whitelist()
def get_details(participant_group_id):
	dates = frappe.db.sql(""" SELECT scheduled_date FROM `tabToT Class Schedule` WHERE participant_group_id = '%s'"""%(participant_group_id))
	group_details = frappe.get_all('Participant Group', filters = [['name', '=', participant_group_id]], fields = ['academic_year', 'academic_term', 'program', 'course'])
	instructor_details = frappe.db.sql(""" SELECT instructors FROM `tabInstructor Table` where parent = '%s'"""%(participant_group_id))
	sub_modules = frappe.db.sql(""" SELECT topic FROM `tabCourse Topic` WHERE parent = '%s'"""%(group_details[0]['course']))
	return [group_details[0]['academic_year'], group_details[0]['academic_term'], group_details[0]['program'], group_details[0]['course'], instructor_details, sub_modules, dates]

@frappe.whitelist()
def get_instructor_name(participant_group_id, instructor_id):
	instructor_name = frappe.db.sql(""" SELECT instructor_name FROM `tabInstructor Table` WHERE parent = '%s' AND instructors = '%s'"""%(participant_group_id, instructor_id), as_dict=1)
	return instructor_name[0]['instructor_name']

@frappe.whitelist()
def get_participants(participant_group_id):
	participants = frappe.get_all('Participant Table', filters = [['parent', '=', participant_group_id]], fields = ['participant', 'participant_name'])
	return participants
