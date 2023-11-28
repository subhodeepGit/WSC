# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	data=get_data(filters)
	columns=get_columns()
	return columns, data

def get_data(filters):
	data=[]
	if filters.get('hostel'):
		hostel=filters.get('hostel')
		course=get_course(hostel)
	if course:
		for t in course:
			a={}
			a['course']=t['programs']
			output=frappe.db.count("Room Allotment",{"programs":t['programs'],"allotment_type":"Allotted","hostel_id":hostel})
			a['total_no_of_student']=output
			output=frappe.db.count("Student Hostel Admission",{"programs":t['programs'],"allotment_status":"Not Reported","hostel":hostel})
			a['total_no_of_student_not_reported']=output
			data.append(a)

	return data

def get_course(hostel):
	course=frappe.db.sql(""" Select DISTINCT programs From `tabStudent Hostel Admission` where   allotment_status in ('Allotted','Not Reported') ORDER BY programs """,as_dict=True)
	return course


def get_columns():
	columns = [
		{
			"label": _("Course"),
			"fieldname": "course",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Total No of Student"),
			"fieldname": "total_no_of_student",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Total No of Students Not Reported"),
			"fieldname": "total_no_of_student_not_reported",
			"fieldtype": "Data",
			"width":300
		}
	]
	return columns