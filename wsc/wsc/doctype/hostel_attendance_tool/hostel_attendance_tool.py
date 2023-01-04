# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
import datetime

class HostelAttendanceTool(Document):
	pass


@frappe.whitelist()
def get_employees(date, department = None, branch = None, company = None):
	attendance_not_marked = []
	attendance_marked = []
	filters = {"start_date": ["<=", date],"end_date": [">=", date]}
	for field, value in {'hostel_id': department,'room_id': branch}.items():
		if value:
			filters[field] = value			
	stu_list = frappe.get_list("Room Allotment", fields=["name", "student_name","room_number","room_id","hostel_id"],filters=filters,order_by="room_number")
	marked_employee = {}

	for emp in frappe.get_list("Hostel Attendance", fields=["room_allotment_no","status"],filters={"attendance_date": date}):	
		marked_employee[emp["room_allotment_no"]] = emp['status']	
	for student in stu_list:
		student['status'] = marked_employee.get(student["name"])
		if student["name"] not in marked_employee:
			attendance_not_marked.append(student)
		else:
			attendance_marked.append(student)
	return {
		"marked": attendance_marked,
		"unmarked": attendance_not_marked
	}


@frappe.whitelist()
def mark_employee_attendance(employee_list, status, date):
	Student_list=employee_list
	Student_list = json.loads(Student_list)
	date=datetime.datetime.strptime(date,'%Y-%m-%d').date()
	for student in Student_list:
		info=frappe.db.sql("""SELECT `name`,`start_date`,`end_date` FROM `tabStudent Leave Process`  WHERE `allotment_number`="%s" 
					and (`start_date`<="%s" and `end_date`>="%s")"""%(student["name"],date,date))
		if len(info)!=0:
			status="On Leave"
		room_allotment_no=student["name"]
		hostel=student['hostel_id']
		room_no=student['room_number']
		room_id=student['room_id']
		student_name=student['student_name']
		attendance=frappe.get_doc(dict(
			doctype='Hostel Attendance',
			attendance_date=getdate(date),
			status=status,
			room_allotment_no=room_allotment_no,
			hostel=hostel,
			room_no=room_no,
			room_id=room_id,
			student_name=student_name
		))
		attendance.insert()
		attendance.submit()
