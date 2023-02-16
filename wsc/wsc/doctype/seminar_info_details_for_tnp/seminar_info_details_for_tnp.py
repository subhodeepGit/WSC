# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SeminarInfoDetailsForTnP(Document):
	def validate(self):
		self.topic_name = self.topic
		# doc = frappe.get_doc('Seminar Info Details For TnP')
		# print(doc)

@frappe.whitelist()
def get_data(topic , date):
	instructor_data = frappe.get_all("Non Teaching Activities" , {"topic":topic , "date":date } , ['activities' , 'description' , 'duration' , 'department' , 'academic_year' , 'date' , 'parent'])
	student_data = frappe.get_all("Seminars And Guest Lecture" , {"topic":topic , "date":date } , ['activities' , 'description' , 'duration' , 'department' , 'academic_year' , 'date' , 'parent'])
	
	data = [instructor_data , student_data]
	print(instructor_data)
	return data