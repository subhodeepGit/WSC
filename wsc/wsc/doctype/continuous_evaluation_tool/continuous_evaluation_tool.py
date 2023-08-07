# Copyright (c) 2023, SOUL Limited and Contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt,json
from wsc.wsc.utils import get_courses_by_semester


class ContinuousEvaluationTool(Document):
	def get_course_details(self):
		course=frappe.get_doc("Course",self.course)
		for d in course.get("credit_distribution"):
			if self.assessment_criteria == d.assessment_criteria:
				return d

	@frappe.whitelist()
	def get_student_allocations(self):
		data_list=[]
		if self.exam_cate=="Regular":
			course_details=get_course_details(self)
			for student in frappe.get_all("Course Assessment",{"course":self.course,"assessment_criteria":self.assessment_criteria,
						      				"semester":self.semester,'exam_category':self.exam_cate, "docstatus":1},
											["student","student_name","roll_no","registration_number"],order_by="roll_no asc",group_by="student"):
				total_earned_marks=total_total_marks=weightage_marks=0
				evaluation=[]
				attendence_status=''
				for d in frappe.get_all("Course Assessment",{"student":student.student,"course":self.course,"assessment_criteria":self.assessment_criteria, "docstatus":1},
										["name","earned_marks","total_marks",'attendence_status']):
					attendence_status=d['attendence_status']
					total_earned_marks+=flt(d.earned_marks)
					total_total_marks+=flt(d.total_marks)
					for cr in frappe.get_all("Credit distribution List",{"parent":self.course,"assessment_criteria":self.assessment_criteria},['total_marks']):
						weightage_marks=round((total_earned_marks/total_total_marks)*(cr.total_marks))
					d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
					evaluation.append(d)
				student['rows']=evaluation
				student["weightage_marks"]=weightage_marks
				student["out_of_marks"]=course_details.total_marks or 0
				student["total_credits"]=course_details.credits or 0
				student["attendence_status"]=attendence_status
				data_list.append(student)
		if self.exam_cate=="Re-Exam":
			course_details=get_course_details(self)
			exam_declaration=self.exam_declaration
			student_data=frappe.get_all("Course Assessment",{"exam_declaration":exam_declaration,"docstatus":1},
			       						["student","student_name","roll_no","registration_number"],
										order_by="roll_no asc",group_by="student")
			for student in student_data:
				total_earned_marks=total_total_marks=weightage_marks=0
				evaluation=[]
				attendence_status=''
				for d in frappe.get_all("Course Assessment",{"student":student.student,"course":self.course,
						 				"assessment_criteria":self.assessment_criteria,"exam_declaration":exam_declaration, "docstatus":1},
										["name","earned_marks","total_marks",'attendence_status']):
					attendence_status=d['attendence_status']
					total_earned_marks+=flt(d.earned_marks)
					total_total_marks+=flt(d.total_marks)
					for cr in frappe.get_all("Credit distribution List",{"parent":self.course,"assessment_criteria":self.assessment_criteria},['total_marks']):
						weightage_marks=round((total_earned_marks/total_total_marks)*(cr.total_marks))
					d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
					evaluation.append(d)
				student['rows']=evaluation
				student["weightage_marks"]=weightage_marks
				student["out_of_marks"]=course_details.total_marks or 0
				student["total_credits"]=course_details.credits or 0
				student["attendence_status"]=attendence_status
				data_list.append(student)

		return data_list
		
@frappe.whitelist()
def make_continuous_evaluation(continuous_evaluation):
	result=json.loads(continuous_evaluation)
	if result.get("exam_cate")=="Regular":
		student_data=get_student_allocations_dict(frappe._dict({"course":result.get("course"),"assessment_criteria":result.get("criteria")}))
		if not student_data:
			frappe.msgprint("Students are not available for given details")
		else:
			records=False
			for d in result.get('rows'):
				exist_record = [a.get('name') for a in frappe.db.get_list("Assessment Credits Allocation",{"docstatus":("!=",2),"student":result.get('rows')[d].get("student"),
											       "roll_no":result.get('rows')[d].get("roll_no"),"registration_number":result.get('rows')[d].get("registration_number"),
																			"academic_year":result.get("academic_year"),"academic_term":result.get("academic_term"),
																			'course':result.get("course"),"assessment_criteria":result.get("criteria")}, 'name')]
				if len(exist_record) > 0:
					frappe.msgprint("Record <b>{0}</b> is already exist for student <b>{1}</b>.".format(', '.join(map(str, exist_record)),result.get('rows')[d].get("student")))
				elif result.get('rows')[d].get("final_marks") and result.get('rows')[d].get("earned_credits") :
					doc=frappe.new_doc("Assessment Credits Allocation")
					doc.student=result.get('rows')[d].get("student")
					doc.student_name=result.get('rows')[d].get("student_name")
					doc.roll_no=result.get('rows')[d].get("roll_no")
					doc.registration_number=result.get('rows')[d].get("registration_number")
					doc.academic_year=result.get("academic_year")
					doc.academic_term=result.get("academic_term")
					doc.assessment_criteria=result.get("criteria")
					doc.program_grade=result.get("program_grade")
					doc.programs=result.get("programs")
					doc.semester=result.get("semester")
					doc.course=result.get("course")
					doc.course_name=result.get("course_name")
					doc.course_code=result.get("course_code")
					for row in student_data.get(result.get('rows')[d].get("student"))['rows']:
						doc.append("final_credit_item",{
							"course_assessment":row.get("name"),
							"earned_marks":flt(row.get("earned_marks")),
							"total_marks":flt(row.get("total_marks")),
							"grace_marks":flt(result.get('rows')[d].get("grace_marks")),
							"exam_type":result.get("exam_cate"),
							"attendence_status":result.get('rows')[d].get("exam_attendence")	
						})
					doc.grace_marks=flt(result.get('rows')[d].get("grace_marks"))
					doc.weightage_marks=flt(result.get('rows')[d].get("weightage_marks"))
					doc.final_marks=flt(result.get('rows')[d].get("final_marks"))
					doc.earned_credits=flt(result.get('rows')[d].get("earned_credits"))
					doc.total_credits=flt(result.get('rows')[d].get("total_credits"))
					doc.out_of_marks=flt(result.get('rows')[d].get("out_of_marks"))
					doc.attendence_status=result.get('rows')[d].get("exam_attendence")
					doc.program_grade=result.get("program_grade")	
					doc.save()
					# doc.submit()
					records=True
				else:
					frappe.msgprint("Please add final marks and earned credits for student <b>{0}</b>".format(result.get('rows')[d].get("student")))
			if records:
				frappe.msgprint("Records Created")
	if 	result.get("exam_cate")=="Re-Exam":
		criteria=result.get("criteria")
		academic_year=result.get("academic_year")
		academic_term=result.get("academic_term")
		course=result.get("course")
		semester=result.get("semester")
		programs=result.get("programs")
		program_grade=result.get("program_grade")
		exam_declaration=result.get("exam_declaration")
		student_data=get_student_allocations_dict_fail(frappe._dict({"course":result.get("course"),"assessment_criteria":result.get("criteria")}),exam_declaration)
		if not student_data:
			frappe.msgprint("Students are not available for given details")
		else:
			records=False
			for d in result.get('rows'):
				student=result.get('rows')[d].get("student")
				exist_record=frappe.db.sql("""Select ACA.name from `tabAssessment Credits Allocation` as ACA
												Join `tabFinal Credit Item` FCI on FCI.parent=ACA.name
												Where ACA.academic_year="%s" and ACA.academic_term="%s" and ACA.program_grade="%s" 
														and ACA.programs="%s" and ACA.semester="%s" and ACA.course="%s" 
														and ACA.assessment_criteria="%s" and ACA.student="%s" and FCI.exam_declaration="%s" and ACA.docstatus=1 
											"""%(academic_year,academic_term,program_grade,programs,semester,course,criteria,
													student,exam_declaration),as_dict=1)
				if len(exist_record) > 0:
					frappe.msgprint("Record <b>{0}</b> is already exist for student <b>{1}</b>.".format(', '.join(map(str, exist_record)),result.get('rows')[d].get("student")))
				elif not exist_record:
					Assessment_data=frappe.db.sql("""Select ACA.name from `tabAssessment Credits Allocation` as ACA
												Where ACA.academic_year="%s" and ACA.academic_term="%s" and ACA.program_grade="%s" 
														and ACA.programs="%s" and ACA.semester="%s" and ACA.course="%s" 
														and ACA.assessment_criteria="%s" and ACA.student="%s" and ACA.docstatus=1 
												"""%(academic_year,academic_term,program_grade,programs,semester,course,criteria,
														student),as_dict=1)
					name=Assessment_data[0]['name']
					doc=frappe.get_doc("Assessment Credits Allocation",name)
					qualifying_status=''
					final_result=''
					weightage_marks=''
					grace_marks=''
					out_of_marks=''	#	Total Marks	
					passing_marks=''	
					for row in student_data.get(result.get('rows')[d].get("student"))['rows']:
						final_result=flt(result.get('rows')[d].get("grace_marks"))+flt(row.get("earned_marks"))
						cdl_list=frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":criteria},['passing_marks'])
						if flt(final_result)<=cdl_list[0]['passing_marks']:
							qualifying_status="Fail"
						else:
							qualifying_status="Pass"
						weightage_marks=flt(row.get("earned_marks"))
						grace_marks=flt(result.get('rows')[d].get("grace_marks"))
						out_of_marks=flt(row.get("total_marks"))
						passing_marks=flt(cdl_list[0]['passing_marks'])
						doc.append("final_credit_item",{
								"course_assessment":row.get("name"),
								"earned_marks":weightage_marks,
								"total_marks":out_of_marks,
								"grace_marks":grace_marks,
								"passing_marks":passing_marks,
								"final_earned_marks":final_result,
								"exam_type":result.get("exam_cate"),
								"attendence_status":result.get('rows')[d].get("exam_attendence"),
								"exam_declaration":result.get("exam_declaration"),
								"qualifying_status":qualifying_status
							})
					
					doc.weightage_marks=weightage_marks
					doc.out_of_marks=out_of_marks
					doc.qualifying_status=qualifying_status
					doc.grace_marks=grace_marks
					doc.final_marks=final_result
					doc.passing_marks=passing_marks
					doc.save()
					records=True
				else:
					frappe.msgprint("Please add final marks and earned credits for student <b>{0}</b>".format(result.get('rows')[d].get("student")))
			if records:
				frappe.msgprint("Records Created")	

def get_student_allocations_dict(doc):
	data_list={}
	course_details=get_course_details(doc)
	for student in frappe.get_all("Course Assessment",{"course":doc.course,"assessment_criteria":doc.assessment_criteria,"exam_category":"Regular" ,"docstatus":1},
			       ["student","student_name","roll_no","registration_number"],group_by="student"):
		total_earned_marks=total_total_marks=weightage_marks=0
		evaluation=[]
		for i,d in enumerate(frappe.get_all("Course Assessment",{"student":student.student,"course":doc.course,"exam_category":"Regular"
							   ,"assessment_criteria":doc.assessment_criteria, "docstatus":1},["name","earned_marks","total_marks"])):
			total_earned_marks+=flt(d.earned_marks)
			total_total_marks+=flt(d.total_marks)
			for cr in frappe.get_all("Credit distribution List",{"parent":doc.course,"assessment_criteria":doc.assessment_criteria},['total_marks']):
				weightage_marks=flt((total_earned_marks/total_total_marks)*flt(cr.total_marks))
			d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
			evaluation.append(d)
		student['rows']=evaluation
		student["weightage_marks"]=weightage_marks
		student["out_of_marks"]=course_details.total_marks or 0
		student["total_credits"]=course_details.credits or 0
		data_list[student.student]=student
	return data_list

def get_student_allocations_dict_fail(doc,exam_declaration):
	data_list={}
	course_details=get_course_details(doc)
	for student in frappe.get_all("Course Assessment",{"course":doc.course,"assessment_criteria":doc.assessment_criteria,'exam_declaration':exam_declaration, "docstatus":1},
			       									["student","student_name","roll_no","registration_number"],group_by="student"):
		total_earned_marks=total_total_marks=weightage_marks=0
		evaluation=[]
		for i,d in enumerate(frappe.get_all("Course Assessment",{"student":student.student,"course":doc.course,"assessment_criteria":doc.assessment_criteria,'exam_declaration':exam_declaration
							   , "docstatus":1},["name","earned_marks","total_marks",])):
			total_earned_marks+=flt(d.earned_marks)
			total_total_marks+=flt(d.total_marks)
			for cr in frappe.get_all("Credit distribution List",{"parent":doc.course,"assessment_criteria":doc.assessment_criteria},['total_marks']):
				weightage_marks=flt((total_earned_marks/total_total_marks)*flt(cr.total_marks))
			d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
			evaluation.append(d)
		student['rows']=evaluation
		student["weightage_marks"]=weightage_marks
		student["out_of_marks"]=course_details.total_marks or 0
		student["total_credits"]=course_details.credits or 0
		data_list[student.student]=student
	return data_list

def validate_duplicate_record(self):
	if self.student and self.course and self.assessment_criteria and self.academic_year and self.academic_term:
		for a in frappe.get_all('Assessment Credits Allocation', {'student':self.student, 'course':self.course,'assessment_criteria':self.assessment_criteria,'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
			if a.name and a.name != self.name:
				frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
def get_course_details(doc):
	course=frappe.get_doc("Course",doc.course)
	for d in course.get("credit_distribution"):
		if doc.assessment_criteria == d.assessment_criteria:
			return d
@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    courses=get_courses_by_semester(filters.get("semester"))
    if courses:
        return frappe.db.sql("""select name,course_name,course_code from tabCourse
			where year_end_date>=now() and name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
			limit %s, %s""".format(", ".join(['%s']*len(courses))),
			tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
    return []