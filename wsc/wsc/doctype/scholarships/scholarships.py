# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
import pandas as pd
from pandas import DataFrame


class Scholarships(Document):
		def validate(self):
			sgpaValidate(self)


# To validate if the Lower Cutoff SGPA is not greater than Upper Cutoff SGPA
def sgpaValidate(self):
	if self.upper_cutoff_sgpa < self.lower_cutoff_sgpa:
		frappe.throw("Lower Cutoff SGPA cannot be greater than the Upper Cutoff SGPA")

# To fetch students with Rank 1, 2 & 3 in selected semester group and assign ranks

@frappe.whitelist()
def get_students(programs,semester,academic_year,academic_term):
	# topper=[]
	topper = frappe.db.sql(
		'''SELECT student, student_name, sgpa 
		FROM `tabExam Assessment Result` 
		WHERE programs= %s AND program= %s AND academic_year=%s AND academic_term=%s
		ORDER BY sgpa DESC;''',
		(programs,semester,academic_year,academic_term),
		as_dict=True
	)

	df = pd.DataFrame.from_records(topper, columns=['student', 'student_name','sgpa'])
	df['rank']=df['sgpa'].rank(ascending=False, method='dense')
	df=df[(df['rank'] <= 3)]
	topperlist=df.to_dict('records')
	if not topperlist:
		frappe.msgprint("No Record found")
	return topperlist

# To fetch students based on the cutoff cgpa

@frappe.whitelist()
def get_cutoffStudents(programs,semester,academic_year,academic_term,lower_cutoff_sgpa,upper_cutoff_sgpa):
	cutoff= []
	if lower_cutoff_sgpa:
		cutoff= frappe.db.sql(
		'''SELECT student, student_name, sgpa 
		FROM `tabExam Assessment Result` 
		WHERE programs= %s AND program= %s AND academic_year=%s AND academic_term=%s AND sgpa BETWEEN %s AND %s
		ORDER BY sgpa DESC;''',
		(programs,semester,academic_year,academic_term, lower_cutoff_sgpa, upper_cutoff_sgpa),
		as_dict=1,
		)
	else:
		cutoff= frappe.db.sql(
		'''SELECT student, student_name, sgpa 
		FROM `tabExam Assessment Result` 
		WHERE programs= %s AND program= %s AND academic_year=%s AND academic_term=%s AND sgpa > %s
		ORDER BY sgpa DESC;''',
		(programs,semester,academic_year,academic_term, upper_cutoff_sgpa),
		as_dict=1,
		)
	
	if not cutoff:
		frappe.msgprint("No Record found")	
	return cutoff

		


		

