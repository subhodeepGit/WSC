# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StudentAttritionForm(Document):
	pass


@frappe.whitelist()
def current_education(student_no):
    current_education_data=frappe.get_all("Current Educational Details",{"parent":student_no},['programs','semesters','academic_year','academic_term'])
    return current_education_data

@frappe.whitelist()
def last_attendence(student_no):
	print("\n\n\n\n")
	attendence_data=frappe.get_all("Student Attendance",{"student":student_no},['name','date'],order_by='date DESC')
	print(attendence_data)
	last_date=""
	status=''
	if attendence_data:
		last_date=attendence_data[0]['date']
		status="Attendance Record Found"
	else:
		status="Attendance Record Not Found"
	return {"last_date":last_date,"status":status}		

