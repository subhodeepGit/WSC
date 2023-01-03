# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document

class SubjectWisePerformance(Document):
	def validate(self):
		self.calculate_course_pass_percentage()

	def calculate_course_pass_percentage(self):
		appeared=frappe.db.sql(""" select count(*),eri.course,eri.course_code,eri.course_name from `tabExam Assessment Result` ear, `tabEvaluation Result Item` eri 
				where ear.programs="%s" AND ear.academic_term="%s" AND  eri.parent=ear.name 
				GROUP BY eri.course """%(self.programs,self.academic_term))
		enrolled = frappe.db.count("Program Enrollment",{"academic_term":self.academic_term,"programs":self.programs})
		passed=frappe.db.sql(""" select eri.course,count(*) from `tabExam Assessment Result` ear, `tabEvaluation Result Item` eri 
				where ear.programs="%s" AND ear.academic_term="%s" AND eri.result="P" AND  eri.parent=ear.name 
				GROUP BY eri.course """%(self.programs,self.academic_term))
		if self.programs and self.academic_term:
			for t in appeared:
				enrolled=enrolled
				for appeared in passed:
					if  t[1]==appeared[0]:
						self.append("course_pass_",{
							"course":t[1],
							"course_name":t[3],
							"course_code":t[2],
							"appeared":t[0],
							"enrolled":enrolled,	
							"absent":enrolled-t[0],
							"passed":appeared[1],
							"failed":t[0]-appeared[1],
							"pass_percentage" : "{:.2f}".format(((appeared[1]/t[0])*100))
					})	



