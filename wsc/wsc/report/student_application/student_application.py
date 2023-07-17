# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataclasses import fields
from itertools import count
from locale import currency
from unicodedata import name
from frappe import _
import frappe

def execute(filters=None):
	get_data_info,headin_list=get_data(filters)
	get_columns_info=get_columns(headin_list)
	return get_columns_info,get_data_info

def get_data(filters):
	fltr = {}
	if filters.get("academic_year"):
		fltr.update({"academic_year":filters.get("academic_year")})
	if filters.get("program_grade"):
		fltr.update({"program_grade":filters.get("program_grade")})
	if filters.get("department"):
		fltr.update({"department":filters.get("department")})
	if filters.get("docstatus"):
		fltr.update({"docstatus":filters.get("docstatus")})
	

   
	student_data_info=frappe.db.get_list("Student Applicant",filters=fltr,fields=["name",
																									"first_name","middle_name","last_name","gender",
	                                                                             					"fathers_name","fathers_occupation","qualification","mothers_name","mothers_occupation",
																									"mothers_qualification","father_annual_income","blood_group","religion",
                                                                                                     "states","districts","blocks","city","pin_code",
																									 "student_email_id","student_mobile_number", "student_category","date_of_birth",
																								 "program_grade","department"])

	# if student_data_info:
		# education qualification
	st_name=[]
	for t in student_data_info:
		st_name.append(t['name'])
	edu_details=frappe.get_all("Education Qualifications Details",filters=[["parent","in",tuple(st_name)]],fields=["name","qualification","institute","percentage_cgpa",
																													"total_cgpa","cgpa","total_marks","earned_marks","score","year_of_completion",
																													"parent"],order_by="name desc")
	
																									
	
	qualification=[]
	for t in edu_details:
		qualification.append(t['qualification'])
	qualification = list(set(qualification))	

	headin_list=[]
	for t in qualification:
		fildes=["qualification","institute","percentage_cgpa","total_cgpa","cgpa","total_marks","earned_marks","score","year_of_completion"]
		for j in fildes:
			a=t+" "+j
			headin_list.append(a)
	headin_list.reverse()		
	for t in student_data_info:
		for j in edu_details:
			if t['name']==j['parent']:
				qualification_name=j['qualification']
				fildes=["qualification","institute","percentage_cgpa","total_cgpa","cgpa","total_marks","earned_marks","score","year_of_completion"]
				for f in fildes:
					t['%s'%(qualification_name+" "+f)]=j[f]

	program_prio=frappe.get_all("Program Priority",filters=[["parent","in",tuple(st_name)]],fields=["name","programs","parent"],order_by="idx asc") 
	program_priority_field=[]
	for t in student_data_info:
		flag=0
		for j in program_prio:
			if j["parent"]==t["name"]:
				flag=flag+1
				print(flag)
				if(flag<=3):
					field="Option "+str(flag)
					program_priority_field.append(field)
					t[field]=j['programs']

	program_priority_field=list(set(program_priority_field))
	program_priority_field.sort()
	
	for t in program_priority_field:
		headin_list.append(t)
	# for t in student_data_info:
	# 	# t["score"]=round(t["score"],2)
	# 	print(t)
	return student_data_info,headin_list																			 

    
def get_columns(headin_list):
	columns=[
		{
			"label": _("Student Applicant"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width": 180
		},
		
		# {
		# 	"label": _("Last Institute Attended"),
		# 	"fieldname": "last_institute_attended",
		# 	"fieldtype": "Data",
		# 	"width": 180
		# },
		# {
		# 	"label": _("KISS Roll Number"),
		# 	"fieldname": "kiss_roll_number",
		# 	"fieldtype": "Data",
		# 	"width": 180
		# },
		
		{			
			"label": _("First Name"),
			"fieldname": "first_name",
			"fieldtype": "Data",
			"width": 180
		},
		
		{
			"label": _("Middle Name"),
			"fieldname": "middle_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Last Name"),
			"fieldname": "last_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Gender"),
			"fieldname": "gender",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Father's Name"),
			"fieldname": "fathers_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Father's Occupation"),
			"fieldname": "fathers_occupation",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Father's Education Qualification"),
			"fieldname": "qualification",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Mother's Name"),
			"fieldname": "mothers_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Mother's Occupation"),
			"fieldname": "mothers_occupation",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Mother's Education Qualification"),
			"fieldname": "mothers_qualification",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Annual Income"),
			"fieldname": "father_annual_income",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Blood Group"),
			"fieldname": "blood_group",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Religion"),
			"fieldname": "religion",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Date of Birth"),
			"fieldname": "date_of_birth",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Aadhar Number"),
			"fieldname": "adhaar_number",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("State"),
			"fieldname": "states",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("District"),
			"fieldname": "districts",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Block"),
			"fieldname": "blocks",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Village"),
			"fieldname": "city",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Police Station"),
			"fieldname": "police_station",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Pincode"),
			"fieldname": "pin_code",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Email"),
			"fieldname": "student_email_id",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Mobile No."),
			"fieldname": "student_mobile_number",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Student Category"),
			"fieldname": "student_category",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Tribe"),
			"fieldname": "tribe_name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Sub Tribe"),
			"fieldname": "sub_tribes",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Program Grade"),
			"fieldname": "program_grade",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Data",
			"width": 180
		},
		
		
        
		
	]
	if len(headin_list)!=0:
		for t in headin_list:
			label=t
			# fieldname=label.replace(" ", "")
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(label),
				"fieldtype": "Data",
				"width":200
			}
			columns.append(columns_add)
	return columns