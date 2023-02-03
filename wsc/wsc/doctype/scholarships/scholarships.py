# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class Scholarships(Document):
	def validate(self):
		pass

	# @frappe.whitelist()
	# def get_students(self):
	# 	topper=[]
	# 	topper = frappe.db.sql(
	# 		'''SELECT student, student_name, sgpa 
	# 		from `tabExam Assessment Result` 
	# 		where program= %s
	# 		order by sgpa DESC
	# 		limit 1;''',
	# 		(self.semester),
	# 		as_dict=1,
	# 	)
	# 	print("\n\n\n\n\n")
	# 	print(topper)
	# 	return(topper)
		
	@frappe.whitelist()
	def get_cutoffStudents(self):
		cutofftopper =[]
		cutofftopper = frappe.db.sql(
			'''SELECT student, student_name, sgpa 
			from `tabExam Assessment Result` 
			where program= %s AND sgpa >= %s
			order by sgpa DESC
			Limit 11;''',
			(self.semester, self.cutoff_sgpa),
			as_dict=1,
		)
		del cutofftopper[0]
		print("\n\n\n\n\n")
		
		print(cutofftopper)
		return cutofftopper

        

