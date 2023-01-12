# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StudentFeedbackForm(Document):
	pass
@frappe.whitelist()
def getvalue():
	data = frappe.get_all("Student Feedback Questions",{"enable":1},["question"])
	# print(data)
	return data
# def validate():
# 	data = frappe.get_all("Student Feedback Questions",['question'])
# 	print(data)
@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Program Course",{"parent":filters.get("program")},['course'],as_list = 1)