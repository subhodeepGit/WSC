# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SchoolWisePassPercentage(Document):
	def before_submit(self):
		self.calculate_pass_percentage()

	def calculate_pass_percentage(self):	
		dep_list=[]
		for no_of_programs in frappe.get_all("Programs",{"program_grade":self.program_grade},['department','name'],order_by="department asc"):
			dep_list.append(no_of_programs['department'])
		dep_list=list(set(dep_list))
		for dept in dep_list:
			no_prog=frappe.get_all("Programs",{"department":dept,"program_grade":self.program_grade},['department','name','program_grade'],order_by="department asc")
			count1=0
			count2=0
			department_al = frappe.get_all("Department",{"name":dept},['department_alias'])
			for i in department_al:
				print(i['department_alias'])
			for t in no_prog:
				total_appeared=frappe.db.count("Exam Assessment Result",{"Programs":t['name'],"academic_term":self.academic_term})
				total_passed=frappe.db.count("Exam Assessment Result",{"Programs":t['name'],"academic_term":self.academic_term,"result":"Pass"})
				count1=count1+total_appeared
				count2+=total_passed
			
			self.append("department_pass_percentage",{
					"program_grade":self.program_grade,
					"department_alias":i['department_alias'],
					"appeared_students":count1,
					"passed_students":count2,
					"academic_term":self.academic_term,
					"pass_parcentage" : "{:.2f}".format(((count2/count1)*100))
				})		