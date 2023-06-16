# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ModuleWiseExamGroup(Document):
	pass


@frappe.whitelist()
def valid_module_as_exam_declation(doctype, txt, searchfield, start, page_len, filters):
	course_date=[]
	if txt:
		course_date=frappe.db.sql(""" Select courses,course_name,course_code,semester from `tabExam Courses` where parent='%s'"""%(txt))
	return	course_date

@frappe.whitelist()
def get_semester(declaration_id=None):
	sem_date=[]
	if declaration_id:
		sem_date=frappe.get_all("Examination Semester",{"parent":declaration_id},['name','semester'])
	return sem_date

@frappe.whitelist()
def module_start_date(modules_id=None,exam_id=None,academic_term=None):
	output_date=[]
	if modules_id and exam_id:
		output_date=frappe.get_all("Exam Courses",{"parent":exam_id,"courses":modules_id},
			     ['examination_date','examination_end_date',"attendance_criteria","minimum_attendance_criteria"])
		if output_date[0]['attendance_criteria']=="Yes":
			acd_date=frappe.get_all('Academic Term',{"name":academic_term},['term_start_date','term_end_date'])
			for t in output_date:
				t['term_start_date']=acd_date[0]['term_start_date']
				t['term_end_date']=acd_date[0]['term_end_date']
		else:
			for t in output_date:
				t['term_start_date']=''
				t['term_end_date']=''		
	return output_date

@frappe.whitelist()
def get_student(academic_term=None, programs=None,class_data=None,minimum_attendance_criteria=None,attendance_criteria=None,
				start_date_of_attendence_duration=None,end_date_of_attendence_duration=None,modules_id=None,
				semester=None):
	enrolled_students = get_program_enrollment(academic_term,programs,class_data)
	student_list=[]
	if enrolled_students:
		student_list=enrolled_students
		total_no_class_scheduled=frappe.db.count('Course Schedule', filters=[["course","=",modules_id],['program','=',semester],
								     ['schedule_date','between',[start_date_of_attendence_duration,end_date_of_attendence_duration]]])
		
		for t in student_list:
			t.update({"total_no_of_classes_scheduled": total_no_class_scheduled})
			class_att_date=frappe.db.count("Student Attendance",filters=[["student","=",t['student']],
								['course','=',modules_id],['program','=',semester],['program','=',semester],
								['date','between',[start_date_of_attendence_duration,end_date_of_attendence_duration]]])
			t.update({"total_no_of_class_attended_by_the_studen":class_att_date})
			t.update({"attendance_percentage":round((t.total_no_of_class_attended_by_the_studen/t.total_no_of_classes_scheduled)*100,2)})
			if attendance_criteria=="No":
				t.update({"elegibility_status": "Qualified"})
				t.update({"examination_qualification_approval":1})
			if attendance_criteria=="Yes":
				if t.attendance_percentage>=float(minimum_attendance_criteria):
					t.update({"elegibility_status": "Qualified"})
					t.update({"examination_qualification_approval":1})
				else:
					t.update({"elegibility_status": "Not-Qualified"})
					t.update({"examination_qualification_approval":0})		
				
		return student_list
	else:
		frappe.msgprint("No students found")
		return student_list



def get_program_enrollment(academic_term,programs=None,class_data=None):
	condition1 = " "
	condition2 = " "

	if programs:
		condition1 += " and pe.programs = %(programs)s"
	if class_data:
		condition1 +=" and pe.school_house = '%s' "%(class_data)
	condition1 +=" and s.enabled =1 "     
	return frappe.db.sql('''
		select
			pe.student, pe.student_name,pe.roll_no,pe.permanant_registration_number,s.enabled
		from
			`tabProgram Enrollment` pe {condition2}
		join `tabStudent` s ON s.name=pe.student
		where
			pe.academic_term = %(academic_term)s  {condition1}
		order by
			pe.student asc
		'''.format(condition1=condition1, condition2=condition2),
				({"academic_term": academic_term,"programs": programs}), as_dict=1) 

























