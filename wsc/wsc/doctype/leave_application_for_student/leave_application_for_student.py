# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class LeaveApplicationforStudent(Document):
	pass

@frappe.whitelist()
def get_classes(from_date=None,to_date=None,curr=None):
	course_schedule=[]
	if from_date != None and to_date != None and curr != None:
		curr1=json.loads(curr)
		semester=curr1[0]["semesters"]
		course_schedule=frappe.get_all("Course Schedule",filters=[["program","=",semester],['schedule_date',"between", [from_date,to_date]]],fields=['name','course_name','room_name','schedule_date','from_time','to_time'],group_by="name")
	return course_schedule

@frappe.whitelist()
def current_education(student_no):
    current_education_data=frappe.get_all("Current Educational Details",{"parent":student_no},['programs','semesters','academic_year','academic_term'])
    return current_education_data