# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantGroup(Document):
	def validate(self):
		for d in self.get("classes"):
			parent_doc = frappe.new_doc("ToT Class Schedule")
			parent_doc.participant_group_id = self.name
			parent_doc.academic_year = self.academic_year
			parent_doc.academic_term = self.academic_term
			parent_doc.course_name = self.program
			parent_doc.module_id = self.course
			parent_doc.module_name = self.module_name
			parent_doc.scheduled_date = d.scheduled_date
			parent_doc.scheduled_time = d.scheduled_time
			parent_doc.room_number = d.room_number
			parent_doc.room_name = d.room_name
			parent_doc.from_time = d.from_time
			parent_doc.to_time = d.to_time
			parent_doc.duration = d.duration

			for td1 in self.get('participants'):
				# print('\n\n')
				# print(td1.participant)
				# print('\n\n')
				parent_doc.append('participants', {
					'participant_id' : td1.participant,
					'participant_name' : td1.participant_name,
					'group_roll_number' : td1.group_roll_number,
					'active' : td1.active,	
				})
			for td2 in self.get('instructor'):
				parent_doc.append('trainers', {
					'trainer_id' : td2.instructors,
					'trainer_name' : td2.instructor_name	
				})
			parent_doc.save()


@frappe.whitelist()
def get_module_name(module_id):
	data = frappe.db.sql(""" SELECT course_name FROM `tabCourse` WHERE name = '%s'"""%(module_id), as_dict =1)
	print('\n\n\n\n')
	print(data)
	print('\n\n\n\n')
	return data[0]['course_name']
	pass

@frappe.whitelist()
def get_participants(academic_year, academic_term, participant_category, program, course):
	data = frappe.get_all("Program Enrollment", filters = [['academic_year', '=', academic_year], ['academic_term', '=', academic_term], ['programs','=',program]], fields =['student', 'student_name'])
	return data
	