# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ToTClassSchedule(Document):
	pass


@frappe.whitelist()
def get_instructor(doctype, txt, searchfield, start, page_len, filters):
	instructor=[]
	lst = []
	fltr={"academic_year":filters["academic_year"],"programs":filters["course"],"program":filters['semester']}
	instructor_data=frappe.get_all("Instructor Log",filters=fltr,fields=['parent'],order_by="parent")
	for t in instructor_data:
		a=[]
		a.append(t['parent'])
		a=tuple(a)
		lst.append(a)
	lst=tuple(lst)
	print(lst)
	instructor=lst
	return instructor
