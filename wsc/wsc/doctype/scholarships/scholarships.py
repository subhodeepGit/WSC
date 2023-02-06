# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class Scholarships(Document):
	def validate(self):
		pass

	@frappe.whitelist()
	def get_students(self):
		topper=[]
		topper = frappe.db.sql(
			'''SELECT student, student_name, sgpa 
			FROM `tabExam Assessment Result` 
			WHERE program= %s
			ORDER BY sgpa DESC;''',
			(self.semester),
			as_dict=1,
		)
		topperlist= []
		top = topper[0]['sgpa']
		for x in topper:
			if x['sgpa']==top:
				topperlist.append(x)
				n=(len(topperlist))
				print(n)
		return(topperlist)
		


	@frappe.whitelist()
	def get_cutoffStudents(self):
		cutofftopper =[]
		cutofftopper = frappe.db.sql(
			'''SELECT student, student_name, sgpa 
			FROM `tabExam Assessment Result` 
			WHERE program= %s AND sgpa >= %s
			ORDER BY sgpa DESC;''',
			(self.semester, self.cutoff_sgpa),
			as_dict=1,
		)
		top=cutofftopper[0]['sgpa']
		print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")			
		print (n)
		print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
		for x in cutofftopper:
			if x['sgpa']==top:
				cutofftopper.remove(x)
		for x in cutofftopper:
			if x['sgpa']==top:
				cutofftopper.remove(x)	
		return cutofftopper

        

