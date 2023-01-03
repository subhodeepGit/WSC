# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	data,label_name=get_data(filters)
	columns=get_columns(label_name)
	return columns,data


def get_data(filters):
	semester=filters.get('semester')
	programs=filters.get('programs')
	academic_year=filters.get('academic_year')
	academic_term=filters.get('academic_term')
	students = get_students(programs,semester,academic_year,academic_term)

	fltr = {}
	if filters.get("academic_year"):
		fltr.update({"academic_year":filters.get("academic_year")})
	if filters.get("academic_term"):
		fltr.update({"academic_term":filters.get("academic_term")})
	if filters.get("programs"):
		fltr.update({"programs":filters.get("programs")})
	if filters.get("semester"):
		fltr.update({"semester":filters.get("semester")})
	course,assessment_criteria,label_name=get_course(students)
	for t in ["Total","Cr  P","Grade","Credit"]:
		assessment_criteria.append(t)
	for t in course:
		for j in assessment_criteria:
			t[j]=""

	############# mapping of the head with the course
	for t in course:
		for j in label_name:
			if (t['course_code'] in j)==True and (t['course_name'] in j)==True:
				for z in assessment_criteria:
					if (z in j)==True:
						t[z]=j
	####################
	parent_assessment_result= [t['name'] for t in students]
	assessment_result=frappe.get_all("Assessment Result Item",filters=[["parent", "in",tuple(parent_assessment_result)]],
																fields=['name',"parent","course","assessment_criteria","earned_cr","total_cr",
																"earned_marks","total_marks","grade","result"])															
	for t in students:
		for j in assessment_result:
			if t["name"]==j["parent"]:
				for z in course:
					if z['name']==j["course"]:
						t[z[j['assessment_criteria']]]=j['earned_marks']
	evaluation_result=frappe.get_all("Evaluation Result Item",filters=[["parent", "in",tuple(parent_assessment_result)]],
															fields=["name","parent","course","course_code","course_name","earned_cr",
															"total_cr","earned_marks","total_marks","grade","result"])

	for t in students:
		for j in evaluation_result:
			if t["name"]==j["parent"]:
				for z in course:
					if z['name']==j["course"]:
						t[z['Total']]=j["earned_marks"]
						t[z['Credit']]=j["earned_cr"]
						t[z['Grade']]=j["grade"]
						grade_point=frappe.get_all("Grading Scale Interval",{"parent":t['grading_scale'],"grade_code":j["grade"]},['grade_point'])
						t[z['Cr  P']]=grade_point[0]['grade_point']

	return students,label_name	

def get_students(programs=None,semester=None,academic_year=None,academic_term=None):
	if not academic_year:
		frappe.throw("Select Academic Year")
	if not academic_term:
		frappe.throw("Select Academic Term")

	students = frappe.db.get_list('Exam Assessment Result',filters=[['programs','=',programs],['program','=',semester],['academic_year','=',academic_year],['academic_term','=',academic_term]],
															fields=['name','student','student_name','roll_no','registration_number',"grading_scale","sgpa","result","overall_cgpa"])

	return students
def get_course(student):
	fer_no=[]
	for t in student:
		fer_no.append(t['name'])
	course_details = frappe.get_all("Assessment Result Item",filters=[["parent","in",tuple(fer_no)]],fields=["name","course","earned_marks","total_marks","assessment_criteria"])
	course=[]
	assessment_criteria=[]
	for t in course_details:
		course.append(t['course'])
		assessment_criteria.append(t['assessment_criteria'])
	course = list(set(course))
	assessment_criteria = list(set(assessment_criteria))

	course_details = frappe.get_all("Course",filters=[["name","in",tuple(course)]],fields=["name","course_name","course_code"])

	label_name=[]
	for t in course_details:
		label_name.append(t['course_code']+" "+t['course_name'])

	name=[]
	for t in label_name:
		for j in assessment_criteria:
			name.append(t+" - "+j)
		a=["Total","Cr  P","Grade","Credit"]
		for j in a:
			name.append(t+" - "+j)
	label_name=name
	return course_details,assessment_criteria,label_name


def get_columns(label_name):
	columns = [
		{
			"label": _("Final Exam Result"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Student No"),
			"fieldname": "student",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Student Name"),
			"fieldname": "student_name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Roll no"),
			"fieldname": "roll_no",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Registration no"),
			"fieldname": "registration_number",
			"fieldtype": "Data",
			"width":200
		},
	]
	if len(label_name)!=0:
		for t in label_name:
			label=t
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(label),
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
				"label": _("Result"),
				"fieldname": "result",
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
