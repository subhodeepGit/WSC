# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProgramIntermitForm(Document):
	def on_submit(self):

		student = self.student
		frappe.db.set_value("Student",student,"enabled",0)



@frappe.whitelist()
def get_student_details(student_id):
	data = frappe.get_all("Current Educational Details",{'parent':student_id},["academic_year","academic_term","programs","semesters"])
	if data == None or len(data)==0:
		return 0 
	else :
		return data[0]

