# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BackPaperTracker(Document):
	pass

@frappe.whitelist()
def get_course(doctype,txt,searchfield,start,page_len,filters):
	data = frappe.get_all("Program Course",{'parent':filters.get("semester")},["course"],as_list=1)
	print('\n\n\n\n\n\n')
	# print(data)
	return data


@frappe.whitelist()
def get_student(course,academic_year,academic_term,program):
	print("\n\n\n\nAcademic Term")
	print(academic_term)
	data=frappe.db.get_all("Evaluation Result Item",{'result':"F",'course':course},["course","result","parent"])

	data_list = []
	for value in data:

		print(value["parent"])

		print(value["course"])
		for record in frappe.db.get_all("Exam Assessment Result",{"name":value["parent"],"academic_year":academic_year,"academic_term":academic_term,"program":program},["student","student_name"]):
			a = {"result":"F"}
			record.update(a)


			data_list.append(record)
	print(data_list)
	return data_list


