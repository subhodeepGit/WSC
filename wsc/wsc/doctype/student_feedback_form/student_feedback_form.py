# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StudentFeedbackForm(Document):
	def validate(self):
		data=frappe.get_all("Student Feedback Form",{"student":self.student,"course":self.course,"instructor":self.instructor})
		if data:
			frappe.throw("Your Feedback For This Course and This Instructor Already Exists")
		

# @frappe.whitelist()
# def get_missing_fields(self):
# 	data={}
# 	data["programs"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"programs")
# 	return data
@frappe.whitelist()
def getvalue():
	data = frappe.get_all("Student Feedback Questions",{"enable":1},["question"])
	# print(data)
	return data
# def validate():
# 	data = frappe.get_all("Student Feedback Questions",['question'])
# 	print(data)
# @frappe.whitelist()
# def get_course(doctype, txt, searchfield, start, page_len, filters):
#     return frappe.get_all("Program Course",{"parent":filters.get("program")},['course'],as_list = 1)

@frappe.whitelist()
def getdetails(student_id):
	data =frappe.get_all("Current Educational Details",{'parent':student_id},["academic_year","academic_term","programs","semesters"])
	if len(data) == 0:
		frappe.throw("Student is not enrolled in Any program")
	else :
		print(data[0])
		return data[0]