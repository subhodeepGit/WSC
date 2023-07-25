# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ParticipantGroup(Document):
	pass

@frappe.whitelist()
def get_participants(academic_year, academic_term, participant_category, program, course):
	print('\n\n\n\n')
	print('hello')
	print('\n\n\n\n')
	data = frappe.get_all("Program Enrollment", filters = [['academic_year', '=', academic_year], ['academic_term', '=', academic_term], ['programs','=',program]], fields =['student', 'student_name'])
	print('\n\n\n\n')
	print(data)
	print('\n\n\n\n')
	return data
	