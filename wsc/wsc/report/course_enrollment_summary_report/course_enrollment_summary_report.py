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
	add_list=''
	if filters.get('district'):
		district=filters.get('district')
		add_list=add_list+" and S.district='%s' "%(district)
	if filters.get('blocks'):
		blocks=filters.get('blocks')
		if len(blocks)==1:
			add_list=add_list+" and S.block= '%s' "%(blocks[0])
		else:
			add_list=add_list+" and S.block IN  %s "%(str(tuple(blocks)))

	data=[]
	if academic_term and academic_year:
		gender_data=get_gender()
		student_category_data=student_category()
		course_data=get_course()
		for t in course_data:
			dic_data={}
				
			data_t=frappe.db.sql(""" select count(PE.name) as total
				 				from `tabProgram Enrollment` PE
				 				JOIN `tabStudent` S on S.name=PE.student
				 			where PE.programs='{program}' and  PE.academic_year='{academic_year}' and PE.academic_term='{academic_term}' 
							and PE.docstatus=1 {add_list}
				""".format(
					**{
						"program":t['name'],
						"academic_term":academic_term,
						"academic_year":academic_year,
						"add_list":add_list
					}),as_dict=True)
			
			# total=frappe.db.count("Program Enrollment",{"programs":t['name'],"academic_year":academic_year,"academic_term":academic_term,"docstatus":1})
			total=data_t[0]['total']
			dic_data['course']=t['name']
			dic_data['total']=total
			for j in gender_data:
				fieldname=j['name'].replace(" ", "")

				data_t=frappe.db.sql(""" select count(PE.name) as total
				 				from `tabProgram Enrollment` PE
				 				JOIN `tabStudent` S on S.name=PE.student
				 			where PE.programs='{program}' and  PE.academic_year='{academic_year}' and PE.academic_term='{academic_term}' 
							and PE.docstatus=1 and PE.gender='{gender}' {add_list}
				""".format(
					**{
						"program":t['name'],
						"academic_term":academic_term,
						"academic_year":academic_year,
						"add_list":add_list,
						"gender":j['name']
					}),as_dict=True)

				# output=frappe.db.count("Program Enrollment",{"programs":t['name'],"gender":j['name'],"academic_year":academic_year,"academic_term":academic_term,"docstatus":1})
				dic_data['%s'%(fieldname)]=data_t[0]['total']

			for j in student_category_data:
				fieldname=j['name'].replace(" ", "")
				data_t=frappe.db.sql(""" select count(PE.name) as total
				 				from `tabProgram Enrollment` PE
				 				JOIN `tabStudent` S on S.name=PE.student
				 			where PE.programs='{program}' and  PE.academic_year='{academic_year}' and PE.academic_term='{academic_term}' 
							and PE.docstatus=1 and PE.student_category='{student_category}' {add_list}
				""".format(
					**{
						"program":t['name'],
						"academic_term":academic_term,
						"academic_year":academic_year,
						"add_list":add_list,
						"student_category":j['name']
					}),as_dict=True)
				
				# output=frappe.db.count("Program Enrollment",{"programs":t['name'],"student_category":j['name'],"academic_year":academic_year,"academic_term":academic_term,"docstatus":1})
				dic_data['%s'%(fieldname)]=data_t[0]['total']


			fieldname=j['name'].replace(" ", "")
			data_t=frappe.db.sql(""" select count(PE.name) as total
				 				from `tabProgram Enrollment` PE
				 				JOIN `tabStudent` S on S.name=PE.student
				 			where PE.programs='{program}' and  PE.academic_year='{academic_year}' and PE.academic_term='{academic_term}' 
							and PE.docstatus=1 and PE.admission_status="Provisional Admission" {add_list}
				""".format(
					**{
						"program":t['name'],
						"academic_term":academic_term,
						"academic_year":academic_year,
						"add_list":add_list
					}),as_dict=True)

			# provisional_admission=frappe.db.count("Program Enrollment",{"programs":t['name'],"academic_year":academic_year,"academic_term":academic_term,"admission_status":"Provisional Admission","docstatus":1})
			dic_data['provisional_admission']=data_t[0]['total']

			data_t=frappe.db.sql(""" select count(PE.name) as total
				 				from `tabProgram Enrollment` PE
				 				JOIN `tabStudent` S on S.name=PE.student
				 			where PE.programs='{program}' and  PE.academic_year='{academic_year}' and PE.academic_term='{academic_term}' 
							and PE.docstatus=1 and PE.admission_status="Admitted" {add_list}
				""".format(
					**{
						"program":t['name'],
						"academic_term":academic_term,
						"academic_year":academic_year,
						"add_list":add_list
					}),as_dict=True)
			# admitted=frappe.db.count("Program Enrollment",{"programs":t['name'],"academic_year":academic_year,"academic_term":academic_term,"admission_status":"Admitted","docstatus":1})	
			dic_data['admitted']=data_t[0]['total']



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