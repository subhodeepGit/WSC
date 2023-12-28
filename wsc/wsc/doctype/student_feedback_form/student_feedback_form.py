# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StudentFeedbackForm(Document):
	def validate(self):
		data=frappe.get_all("Student Feedback Form",{"student":self.student,"course":self.course,"instructor":self.instructor,"docstatus":1})
		if data:
			frappe.throw("Your Feedback For This Course and This Instructor Already Exists")

	def on_submit(self):	
		for t in self.get("questionnarie"):
			if not t.ratings:
				frappe.throw("Rating is not Maintained for the line no <b>%s</b>"%(t.idx))

@frappe.whitelist()
def getvalue():
	data = frappe.get_all("Student Feedback Questions",{"enable":1},["question"])
	return data
@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Program Course",{"parent":filters.get("program")},['course','course_name'],as_list = 1)

@frappe.whitelist()
def getdetails(student_id):
	data =frappe.get_all("Current Educational Details",{'parent':student_id},["academic_year","academic_term","programs","semesters"])
	if len(data) == 0:
		frappe.throw("Student is not enrolled in Any program")
	else :
		return data[0]
