# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from datetime import datetime, timedelta
from wsc.wsc.utils import get_courses_by_semester

class ParticipantGroup(Document):
	def validate(self):
		
		self.calculate_total_hours()
		for d in self.get("classes"):
			parent_doc = frappe.new_doc("ToT Class Schedule")
			parent_doc.participant_group_id = self.name
			parent_doc.academic_year = self.academic_year
			parent_doc.academic_term = self.academic_term
			parent_doc.course_name = self.program
			parent_doc.module_id = self.course
			parent_doc.module_name = self.module_name
			parent_doc.scheduled_date = d.scheduled_date
			# parent_doc.scheduled_time = d.scheduled_time
			parent_doc.room_number = d.room_number
			parent_doc.room_name = d.room_name
			parent_doc.from_time = d.from_time
			parent_doc.to_time = d.to_time
			parent_doc.duration = d.duration

			for td1 in self.get('participants'):
				parent_doc.append('participants', {
					'participant_id' : td1.participant,
					'participant_name' : td1.participant_name,
					# 'group_roll_number' : td1.group_roll_number,
					'active' : td1.active,	
				})
			for td2 in self.get('instructor'):
				parent_doc.append('trainers', {
					'trainer_id' : td2.instructors,
					'trainer_name' : td2.instructor_name	
				})
			parent_doc.save()	
	def calculate_total_hours(self):
		for d in self.get("classes"):
			if d.to_time and d.from_time:
				d.duration = datetime.strptime(d.to_time, '%H:%M:%S') - datetime.strptime(d.from_time, '%H:%M:%S') 

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
def get_enrollment_details(enrollment_id):
	enrollment_details = frappe.db.sql(""" SELECT  academic_year, academic_term, programs, semester FROM `tabToT Participant Enrollment` WHERE name = '%s'"""%(enrollment_id), as_dict=1)
	# modules = frappe.db.sql(""" SELECT course FROM `tabProgram Course` WHERE parent = '%s'"""%(enrollment_details[0]['programs']))
	return [enrollment_details[0]['academic_year'], enrollment_details[0]['academic_term'], enrollment_details[0]['programs'], enrollment_details[0]['semester']]

@frappe.whitelist()
def get_module_name(module_id):
	data = frappe.db.sql(""" SELECT course_name FROM `tabCourse` WHERE name = '%s'"""%(module_id), as_dict =1)
	return data[0]['course_name']

@frappe.whitelist()
def get_participants(enrollment_id):
	data = frappe.get_all("Reported Participant", filters = [['parent', '=', enrollment_id], ['is_reported', '=', 1]], fields =['participant', 'participant_name'])
	return data