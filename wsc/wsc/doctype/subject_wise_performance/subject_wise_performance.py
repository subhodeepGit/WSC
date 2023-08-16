# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import re
import frappe
from frappe import _
from frappe.model.document import Document

class SubjectWisePerformance(Document):
	@frappe.whitelist()
	def get_details(self):	
		appeared=frappe.db.sql(""" select count(*),eri.course,eri.course_code,eri.course_name from `tabExam Assessment Result` ear, `tabEvaluation Result Item` eri 
				where ear.programs="%s" AND ear.academic_term="%s" AND  eri.parent=ear.name 
				GROUP BY eri.course """%(self.programs,self.academic_term))
		enrolled = frappe.db.count("Program Enrollment",{"academic_term":self.academic_term,"programs":self.programs})
		passed=frappe.db.sql(""" select eri.course,count(*) from `tabExam Assessment Result` ear, `tabEvaluation Result Item` eri 
				where ear.programs="%s" AND ear.academic_term="%s" AND eri.result="P" AND  eri.parent=ear.name 
				GROUP BY eri.course """%(self.programs,self.academic_term))
		# if self.programs and self.academic_term:
		try:
			# if passed>0:
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

		except ZeroDivisionError:
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
							"pass_percentage" : 0
					})
		# if len(frappe.get_all("User Permission",{'user':user_id,'allow':"Employee",'for_value':doc.employee,"applicable_for":"Employee"}))==0:
		if len(self.course_pass_)==0:
			frappe.msgprint(_("No Result is Created for <b>{0}</b> Course in <b>{1}</b>").format(self.programs,self.academic_term))
			rem=(_("No Result is Created for {0} Course in {1}").format(self.programs,self.academic_term))
			return rem
		# if  t[1]!=appeared[0]:
		# 		frappe.msgprint("Not a Single Students is Enrolled or Passed in Any of the Course Examination")
# frappe.throw(_("Student having ID No. <b>'{0}'</b> is currently provisionally Admitted in Course Enrollment <b>'{1}'</b>, 
# 	       Kindly change the status to Admitted.").format(self.student,getlink("Program Enrollment",i.name),self.student))
