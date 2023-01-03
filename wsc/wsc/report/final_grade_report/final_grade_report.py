# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	# columns, data = [], []
	data,course_details_info=get_data(filters)
	columns=get_columns(course_details_info)
	return columns, data



def get_data(filters):
	programs=filters.get("programs")
	semester=filters.get("semester")
	academic_year=filters.get("academic_year")
	academic_term=filters.get("academic_term")
	students=get_students(programs,semester,academic_year,academic_term)
	evaluation_result=get_evaluation_result(students)
	course_details_info=get_course(students)
	for t in course_details_info:
		for j in evaluation_result:
			if t['name']==j['course']:
				t["total_cr"]=j["total_cr"]
	for t in students:
		for j in evaluation_result:
			if t["name"]==j["parent"]:
				if t['registration_number']!=None:
					t[j['course']]=j['grade']
				else:
					t[j['course']]="Withheld"
					t["sgpa"]="Withheld"
					t["overall_cgpa"]="Withheld"
	full_marks={'name':"",'student':"",'student_name':"Full Marks",'roll_no':"",'registration_number':""}
	total_cr=0
	for t in course_details_info:
		full_marks[t['name']]=t["total_cr"]
		total_cr=total_cr+int(t["total_cr"])

	full_marks["sgpa"]=total_cr
	full_marks["overall_cgpa"]=total_cr
	students.insert(0, full_marks)

	#################### signature print in table
	full_marks={'name':"",'student':"",'student_name':"",'roll_no':"",'registration_number':""}
	for t in course_details_info:
		full_marks[t['name']]=""
	for t in range(0, 4):
		students.append(full_marks)

	full_marks={'name':"",'student':"",'student_name':"",'roll_no':"Exam Co-ordinator",'registration_number':""}
	mid_pos=round(len(course_details_info)/2)
	mid_course=course_details_info[mid_pos]["name"]
	full_marks[mid_course]="Asst. CoE"
	full_marks["sgpa"]="Controller of Examinations"
	students.append(full_marks)
	#################### end


	return students,course_details_info



def get_students(programs=None,semester=None,academic_year=None,academic_term=None):
	students = frappe.db.get_list('Exam Assessment Result',filters=[['programs','=',programs],['program','=',semester],['academic_year','=',academic_year],
																	['academic_term','=',academic_term]],
															fields=['name','student','student_name','roll_no','registration_number',"grading_scale","sgpa","result","overall_cgpa"], order_by="roll_no")

	return students


def get_evaluation_result(students):
	parent_assessment_result= [t['name'] for t in students]
	evaluation_result=frappe.get_all("Evaluation Result Item",filters=[["parent", "in",tuple(parent_assessment_result)]],
															fields=["name","parent","course","course_code","course_name","earned_cr",
															"total_cr","earned_marks","total_marks","grade","result"])														
	return 	evaluation_result



def get_course(student):
	fer_no=[]
	for t in student:
		fer_no.append(t['name'])
	course_details = frappe.get_all("Assessment Result Item",filters=[["parent","in",tuple(fer_no)]],fields=["name","course"])

	course=[]
	for t in course_details:
		course.append(t['course'])

	course = list(set(course))
	course_details_info = frappe.get_all("Course",filters=[["name","in",tuple(course)]],fields=["name","course_name","course_code"],order_by="creation asc")

		
	return course_details_info


def get_columns(course_details_info):	
	columns=[
		{
			"label": _("Sl No"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Roll No"),
			"fieldname": "roll_no",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Registration Number"),
			"fieldname": "registration_number",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Student Name"),
			"fieldname": "student_name",
			"fieldtype": "Data",
			"width": 180
		},
	]
	for t in course_details_info:
		columns_add={
				"label": _("%s %s (%s) "%(t['course_code'],t['course_name'],t['name'])),
				"fieldname": "%s"%(t['name']),
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)
	columns_add={
				"label": _("SGPA"),
				"fieldname": "sgpa",
				"fieldtype": "Data",
				"width":200
			}	
	columns.append(columns_add)	
	columns_add={
				"label": _("CGPA"),
				"fieldname": "overall_cgpa",
				"fieldtype": "Data",
				"width":200
			}	
	columns.append(columns_add)		
	return columns