# -*- coding: utf-8 -*-
# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
# from wsc.wsc.utils import get_courses_by_semester_enrollment_date

class Semesters(Document):
	pass

@frappe.whitelist()
def get_courses(semester):
	courses=[d.course for d in frappe.get_all("Program Course",{"parent":semester},["course"])]
	# filters={'is_disable':0,'enrollment_date':[">=",'%s'%(enrollment_date)]}
	return frappe.get_all("Course",{"name":["IN",courses]},['name','course_name','course_code'])
# @frappe.whitelist()
# def get_courses(self,semester,enrollment_date):
# 	course_list = get_courses_by_semester_enrollment_date([d.semester for d in self.semesters],enrollment_date)
# 	print("\n\n\n\n")
# 	print(course_list)
# 	result = []
# 	for course in course_list:
# 		row = {}
# 		course_details = frappe.db.get_all('Course',{'name':course,},['name','course_code','course_name'])
# 		# if c.course not in [d.name for d in frappe.get_all("Course", {"disable":0},['name'])]:
# 		# ,["academic_year","=","%s"%(academic_year)]]
# 		#  {'name':course}, 
# 		semester = frappe.db.get_value('Program Course', {'course': course,"parent":["IN",[d.semester for d in self.semesters]]}, 'parent')
# 		course_details[0].update({'semester': semester})
# 		row.update(course_details[0])
# 		result.append(row)
# 	return result      
# 	return get_courses_by_semester_enrollment_date([d.semester for d in self.semesters])