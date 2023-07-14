# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import re
import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.utils import duplicate_row_validation
from frappe.utils import flt
from frappe.utils.csvutils import getlink
from education.education.api import get_grade

class CumulativeMarksheet(Document):
	def validate(self):
		self.validate_duplicate_for_submit()
		self.validate_duplicate_for_save()
		self.map_fields()
		self.validate_missing_fields()
		self.set_result()
		duplicate_row_validation(self,"cumulatice_grades_item",['semester_order'])
		self.get_grade()
	def on_submit(self):
		self.validate_duplicate_for_submit()
		self.validate_duplicate_for_save()
	def get_grade(self):
		x = frappe.get_all("Exam Assessment Result",{'student':self.student},['grading_scale'])
		if x:
			y=x[0]
			z=y.values()
			for values in z:
				data=(self.secured_marks/self.total_marks)*100
				self.grade = get_grade(values,data)
		else:
			pass
			# frappe.throw("Result has not published for this student")
	def map_fields(self):
		order_dict={1:"1ST SEM",2:"2ND SEM",3:"3RD SEM",4:"4TH SEM",5:"5TH SEM",6:"6TH SEM",7:"7TH SEM",8:"8TH SEM",9:"9TH SEM",10:"10TH SEM"}
		for d in self.get("cumulatice_grades_item"):
			if not d.semester_order:
				
				db=frappe.db.sql("""select name,semester_order from `tabProgram` where name="%s" """%(d.semester))
				for sem in frappe.db.get_all("Program",{"name":"%s"%(d.semester)},['name',"semester_order"]):
					print(sem.semester_order)
					print(d.semester)
					print(db)
					d.semester_order=order_dict.get(sem.semester_order)
	def validate_duplicate_for_save(self):
		print("\n\nINSAVE")
		assessment_result = frappe.get_list("Cumulative Marksheet", filters={"name": ("not in", [self.name,self.student_name]),
			"student":self.student, "docstatus":0,'programs':self.programs, 'year_of_completion':self.year_of_completion})
		if assessment_result:
			frappe.throw(_("Marksheet of <b>'{0}'</b> having <b>'{1}'</b> Id is already exists.").format(self.student_name,getlink("Cumulative Marksheet",assessment_result[0].name)))
	
	def validate_duplicate_for_submit(self):
		print("\n\nINSubmit")
		assessment_result = frappe.get_list("Cumulative Marksheet", filters={"name": ("not in", [self.name,self.student_name]),
			"student":self.student, "docstatus":1,'programs':self.programs, 'year_of_completion':self.year_of_completion})
		if assessment_result:
			frappe.throw(_("Marksheet of <b>'{0}'</b> having <b>'{1}'</b> Id is already exists.").format(self.student_name,getlink("Cumulative Marksheet",assessment_result[0].name)))
	def validate_missing_fields(self):
		# pass
		for d in self.get("cumulatice_grades_item"):
			if not d.semester_order:
				frappe.throw("#Row {0} Please select Semester Order <b>OR</b> set Semester Order IN Semester Master".format(d.idx))
	def set_result(self):
		self.result_p_f = 0
		for d in self.cumulatice_grades_item:
			self.result_p_f = 0
			if flt(d.percentage) >= 40.0 :
				self.result_p_f="PASS"
			
			else:
				self.result_p_f="FAIL"

	@frappe.whitelist()
	def get_student_details(self):
		for enroll in frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},['name','academic_year'],order_by="creation asc",limit=1):
			self.year_of_admission=enroll.academic_year
		for enroll in frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},['name','academic_year'],order_by="creation desc",limit=1):
			self.year_of_completion=enroll.academic_year
		
		self.set("cummulative_courses_item",[])
		semesters=[]
		for result in frappe.get_all("Exam Assessment Result",{"student":self.student,"docstatus":1},['name','programs','program'],order_by="program asc"):
			for course in frappe.get_all("Evaluation Result Item",{"parent":result.name},['course','earned_cr','earned_marks','total_marks','grade','course_code','course_name'],order_by="creation asc"):
				self.append("cummulative_courses_item",{
					"programs":result.programs,
					"semester":result.program,
					"course":course.course,
					"course_code":course.course_code,
					"course_name":course.course_name,
					"cr":course.earned_cr,
					"gr":course.grade,
					"total_marks":course.total_marks,
					"earned_marks":course.earned_marks
				})
			semesters.append(result.program)

		total_sgpa=0
		earned_marks=0
		percent=0
		order_dict={1:"1ST SEM",2:"2ND SEM",3:"3RD SEM",4:"4TH SEM",5:"5TH SEM",6:"6TH SEM",7:"7TH SEM",8:"8TH SEM",9:"9TH SEM",10:"10TH SEM"}
		for sem in frappe.get_all("Program",{"name":["IN",semesters]},['name',"semester_order"],order_by="semester_order"):
			for result in frappe.get_all("Exam Assessment Result",{"student":self.student,"docstatus":1,'program':sem.name},['total_marks','grade','percentage','secured_marks','programs']):
				# ,'modified'
				self.append("cumulatice_grades_item",{
					"semester":sem.name,
					"semester_order":order_dict.get(sem.semester_order),
					"total_marks":round(result.total_marks,2),
					"secured_marks":round(result.secured_marks,2),
					"percentage":result.percentage,
					"grade":result.grade
				})
				self.programs=result.programs
				total_sgpa+=result.total_marks
				earned_marks+=result.secured_marks
				percent+=result.percentage
				
			self.result_p_f=frappe.db.get_value("Exam Assessment Result",result.exam_assessment_result,'result')
			if len(self.get("cumulatice_grades_item")):
				# self.total_marks=(total_sgpa/len(self.get("cumulatice_grades_item")))
				# self.secured_marks=(earned_marks/len(self.get("cumulatice_grades_item")))
				self.percentage=(percent/len(self.get("cumulatice_grades_item")))
				self.percentage
				res2 = "{:.2f}".format(self.percentage)
				self.percentage=res2
		marks_earned=0
		total_marks=0
		for d in self.get("cumulatice_grades_item"):
				marks_earned += flt(d.secured_marks)
				total_marks += flt(d.total_marks)
									
					# if self.grade and self.grading_scale:
					# if d.secured_marks:
						
				if total_marks > 0 :
					self.total_marks=total_marks
					self.secured_marks=marks_earned
					# self.percentage = round((marks_earned/total_marks)*100, 2)
					# self.percentage = "{:.2f}".format((marks_earned/total_marks)*100)