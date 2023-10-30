# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	data,gender_data,student_category_data=get_data(filters)
	columns=get_columns(gender_data,student_category_data)
	return columns, data


def get_data(filters):
	academic_year= filters.get('academic_year')
	academic_term=filters.get('academic_term')
	data=[]
	if academic_term and academic_year:
		gender_data=get_gender()
		student_category_data=student_category()
		course_data=get_course()
		for t in course_data:
			dic_data={}
			total=frappe.db.count("Program Enrollment",{"programs":t['name'],"docstatus":1})
			dic_data['course']=t['name']
			dic_data['total']=total
			for j in gender_data:
				fieldname=j['name'].replace(" ", "")
				output=frappe.db.count("Program Enrollment",{"programs":t['name'],"gender":j['name'],"docstatus":1})
				dic_data['%s'%(fieldname)]=output
			for j in student_category_data:
				fieldname=j['name'].replace(" ", "")
				output=frappe.db.count("Program Enrollment",{"programs":t['name'],"student_category":j['name'],"docstatus":1})
				dic_data['%s'%(fieldname)]=output
			provisional_admission=frappe.db.count("Program Enrollment",{"programs":t['name'],"admission_status":"Provisional Admission","docstatus":1})
			dic_data['provisional_admission']=provisional_admission
			admitted=frappe.db.count("Program Enrollment",{"programs":t['name'],"admission_status":"Admitted","docstatus":1})	
			dic_data['admitted']=admitted



			data.append(dic_data)



		return data,gender_data,student_category_data


def get_gender():
	gender_data=frappe.get_all("Gender",order_by="name asc")
	return gender_data
def student_category():
	student_category_data=frappe.get_all("Student Category")
	return student_category_data
def get_course():
	get_course_data=frappe.get_all("Programs")
	return get_course_data

def get_columns(gender_data,student_category_data):
	columns = [
		{
			"label": _("Course"),
			"fieldname": "course",
			"fieldtype": "Data",
			"width":200
		},
		
	]
	if gender_data:
		for t in gender_data:
			label=t['name']
			fieldname=label.replace(" ", "")
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(fieldname),
				"fieldtype": "Data",
				"width":135
			}
			columns.append(columns_add)
	if student_category_data:
		for t in student_category_data:
			label=t['name']
			fieldname=label.replace(" ", "")
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(fieldname),
				"fieldtype": "Data",
				"width":75
			}
			columns.append(columns_add)
	# Provisional Admission
	# Admitted	
	columns_add={
				"label": _("Provisional Admission"),
				"fieldname": "provisional_admission",
				"fieldtype": "Data",
				"width":150
			}
	columns.append(columns_add)	
	columns_add={
				"label": _("Admitted"),
				"fieldname": "admitted",
				"fieldtype": "Data",
				"width":125
			}
	columns.append(columns_add)	
	columns_add={
				"label": _("Total"),
				"fieldname": "total",
				"fieldtype": "Data",
				"width":75
			}
	columns.append(columns_add)				
	return columns