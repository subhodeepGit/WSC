# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import flt

class PassPercentage(Document):
	@frappe.whitelist()
	def get_details(self):	
		rem=0
		for no_of_programs in frappe.get_all("Programs",{"program_grade":self.program_grade},['name','program_grade','department'],order_by="department asc"):
			enrolled = frappe.db.count("Program Enrollment",{"academic_term":self.academic_term,"programs":no_of_programs.name,"program_grade":no_of_programs.program_grade})
			appeared=frappe.db.count("Exam Assessment Result",{"Programs":no_of_programs.name,"academic_term":self.academic_term})
			passed=frappe.db.count("Exam Assessment Result",{"Programs":no_of_programs.name,"academic_term":self.academic_term,"result":"Pass"})
			if passed>0 and appeared>0:
				self.programs_pass_.clear()
				self.append("programs_pass_",{
					"department":no_of_programs.department,
					"programs":no_of_programs.name,
					"type":"Regular",
					"enrolled":enrolled,
					"appeared":appeared,
					"absent":enrolled-appeared,
					"failed":appeared-passed,
					"passed":passed,
					"pass_percentage" : "{:.2f}".format(((passed/appeared)*100))
				})

		if passed<=0 and appeared<=0:
			frappe.msgprint("Not a Single Students is Passed or Appeared in Any of the Course Examination")
			rem="Not a Single Student is Passed in Any of the Course Examination"
			return rem
		elif enrolled==0:
			frappe.msgprint("Not a Single Students is Enrolled in Any of the Course Examination")
			rem="Not a Single Student is Enrolled in Any of the Course Examination"
			return rem

			