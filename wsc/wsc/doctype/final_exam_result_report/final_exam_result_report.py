# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FinalExamResultReport(Document):
	pass
	@frappe.whitelist()
	def get_student_allocations(self):
		programs=self.programs
		semester=self.semester
		academic_year=self.academic_year
		academic_term=self.academic_term
		students = get_students(programs,semester,academic_year,academic_term)
		course,assessment_criteria,total_credit,assessment_criteria_head=get_course(students)
		assessment_result=get_assessment_result(students)
		evaluation_result=get_evaluation_result(students,course)
		students=total_credit_credit_point(students,evaluation_result)
		return {"studnet":students,"course":course,"assessment_criteria":assessment_criteria,
				"total_credit":total_credit,"assessment_result":assessment_result,"evaluation_result":evaluation_result,"assessment_criteria_head":assessment_criteria_head}


def get_students(programs=None,semester=None,academic_year=None,academic_term=None):
	if not academic_year:
		frappe.throw("Select Academic Year")
	if not academic_term:
		frappe.throw("Select Academic Term")

	students = frappe.db.get_list('Exam Assessment Result',filters=[['programs','=',programs],['program','=',semester],['academic_year','=',academic_year],['academic_term','=',academic_term]],
															fields=['name','student','student_name','roll_no','registration_number',"grading_scale","sgpa","result","overall_cgpa"],order_by="roll_no")

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


	assessment_criteria_head=[]
	for t in course:
		assessment_criteria_head.append({"course_code":t,'assessment_criteria':[],"assessment_criteria_info":[],"len_assessment_criteria":""})

	for t in assessment_criteria_head:
		for j in course_details:
			if t["course_code"]==j["course"]:
				t['assessment_criteria'].append(j["assessment_criteria"])


	for t in assessment_criteria_head:
		t['assessment_criteria']=list(set(t['assessment_criteria']))
		for j in ["Total","Cr P","Grade","Credit"]:
			t['assessment_criteria'].append(j)

	for t in assessment_criteria_head:
		for j in t['assessment_criteria']:
			b=j.replace(" ", "_")
			t["assessment_criteria_info"].append(b)

	for t in assessment_criteria_head:
		t["len_assessment_criteria"]=len(t["assessment_criteria_info"])

	for t in ["Total","Cr P","Grade","Credit"]:
		assessment_criteria.append(t)

	assessment_criteria_info=[]
	for t in assessment_criteria:
		b=t.replace(" ", "_")
		a="assessment_criteria"
		assessment_criteria_info.append({a:[t,b]})	

	course_details_info = frappe.get_all("Course",filters=[["name","in",tuple(course)]],fields=["name","course_name","course_code"],order_by="creation asc")

	for t in course_details_info:
		for j in assessment_criteria:
			j=j.replace(" ", "_")
			t[j]=""

	for t in course_details:
		for j in course_details_info:
			if t["course"]==j["name"]:
				a=t['assessment_criteria'].replace(" ", "_")
				j[a]=t['total_marks']

	evaluation_result=frappe.get_all("Evaluation Result Item",filters=[["parent", "in",tuple(fer_no)]],
															fields=["course","course_code","total_cr","total_marks"])	
	for t in evaluation_result:
		for j in course_details_info:
			if t["course"]==j["name"]:
				j["Total"]=t["total_marks"]
				j["Credit"]=t["total_cr"]

	total_credit=0
	for t in course_details_info:
		total_credit=total_credit+int(t["Credit"])			
	return course_details_info,assessment_criteria_info,total_credit,assessment_criteria_head



def get_assessment_result(students):
	parent_assessment_result= [t['name'] for t in students]
	assessment_result=frappe.get_all("Assessment Result Item",filters=[["parent", "in",tuple(parent_assessment_result)]],
																fields=['name',"parent","course","assessment_criteria","earned_cr","total_cr",
																"earned_marks","total_marks","grade","result"],order_by="creation asc")	
	for t in assessment_result:
		a=t['assessment_criteria'].replace(" ", "_")
		t["assessment_criteria_info"]=a		
	return assessment_result

def get_evaluation_result(students,course):
	parent_assessment_result= [t['name'] for t in students]
	evaluation_result=frappe.get_all("Evaluation Result Item",filters=[["parent", "in",tuple(parent_assessment_result)]],
															fields=["name","parent","course","course_code","course_name","earned_cr",
															"total_cr","earned_marks","total_marks","grade","result"],order_by="creation asc")													
	for t in students:
		for j in evaluation_result:
			if t["name"]==j["parent"]:
				for z in course:
					if z['name']==j["course"]:
						grade_point=frappe.get_all("Grading Scale Interval",{"parent":t['grading_scale'],"grade_code":j["grade"]},['grade_point'])
						j['Cr_P']=grade_point[0]['grade_point']		
	return 	evaluation_result																



def total_credit_credit_point(students,evaluation_result):
	for t in students:
		t["credit_point"]=[]
		t['total_credit']=[]
	for t in students:
		for j in evaluation_result:
			if t["name"]==j["parent"]:
				t["credit_point"].append(j['Cr_P'])
				t['total_credit'].append(int(j['Cr_P'])*int(j["total_cr"]))

	for t in students:
		t["credit_point"]=sum(t["credit_point"])
		t["total_credit"]=sum(t["total_credit"])
	
	return students















