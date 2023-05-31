# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document

class ScholarshipApplication(Document):
	pass


@frappe.whitelist()
def calculateAge(student_no):
	student_data=frappe.get_all("Student",{"name":student_no},["date_of_birth"])
	birthDate=student_data[0]['date_of_birth']
	age=''
	if birthDate:
		today = date.today()
		age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
	return age

@frappe.whitelist()
def current_education(student_no):
	current_education_data=frappe.get_all("Current Educational Details",{"parent":student_no},['programs','semesters','academic_year','academic_term'])
	return current_education_data

