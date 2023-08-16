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
					# "type":"Regular",
			try:
				self.append("programs_pass_",{
					"department":no_of_programs.department,
					"programs":no_of_programs.name,
					"enrolled":enrolled,
					"appeared":appeared,
					"absent":enrolled-appeared,
					"failed":appeared-passed,
					"passed":passed,
					"pass_percentage" : "{:.2f}".format(((passed/appeared)*100))
				})
			except ZeroDivisionError:
				self.append("programs_pass_",{
					"department":no_of_programs.department,
					"programs":no_of_programs.name,
					"type":"Regular",
					"enrolled":enrolled,
					"appeared":appeared,
					"absent":enrolled-appeared,
					"failed":appeared-passed,
					"passed":passed,
					"pass_percentage" : 0
				})
		