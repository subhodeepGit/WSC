# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
import pandas as pd
from pandas import DataFrame

class RewardsandAchievements(Document):
	def validate(self):
			PerValidate(self)


# To validate if the Lower Cutoff Percentage is not greater than Upper Cutoff Percentage
def PerValidate(self):
	if self.upper_cutoff_percentage < self.lower_cutoff_percentage:
		frappe.throw("Lower Cutoff Percentage cannot be greater than the Upper Cutoff Percentage")

# To fetch students with Rank 1, 2 & 3 in selected semester group and assign ranks

@frappe.whitelist()
def get_students(programs=None,semester=None,academic_year=None,academic_term=None,no_of_merit_student=None):
	# topper=[]
	topper = frappe.db.sql(
		'''SELECT student, student_name, percentage 
		FROM `tabExam Assessment Result` 
		WHERE programs= %s AND program= %s AND academic_year=%s AND academic_term=%s
		ORDER BY percentage DESC;''',
		(programs,semester,academic_year,academic_term),
		as_dict=True
	)

	df = pd.DataFrame.from_records(topper, columns=['student', 'student_name','percentage'])
	df['rank']=df['percentage'].rank(ascending=False, method='dense')
	total_merit_student = no_of_merit_student
	if total_merit_student:
		df=df[df['rank'] <= float(total_merit_student)]
		topperlist=df.to_dict('records')   
		if not topperlist:
			frappe.msgprint("No Record found")
		return topperlist
	else:
		frappe.throw("Enter <b>No. of Merit Student</b> first")

# To fetch students based on the cutoff percentage

@frappe.whitelist()
def get_cutoffStudents(programs=None,semester=None,academic_year=None,academic_term=None,lower_cutoff_percentage=None,upper_cutoff_percentage=None):
	cutoff= []
	if lower_cutoff_percentage:
		cutoff= frappe.db.sql(
		'''SELECT student, student_name, percentage 
		FROM `tabExam Assessment Result` 
		WHERE programs= %s AND program= %s AND academic_year=%s AND academic_term=%s AND percentage BETWEEN %s AND %s
		ORDER BY percentage DESC;''',
		(programs,semester,academic_year,academic_term, lower_cutoff_percentage, upper_cutoff_percentage),
		as_dict=1,
		)
	else:
		cutoff= frappe.db.sql(
		'''SELECT student, student_name, percentage 
		FROM `tabExam Assessment Result` 
		WHERE programs= %s AND program= %s AND academic_year=%s AND academic_term=%s AND percentage > %s
		ORDER BY percentage DESC;''',
		(programs,semester,academic_year,academic_term, upper_cutoff_percentage),
		as_dict=1,
		)
	
	if not cutoff:
		frappe.msgprint("No Record found")	
	return cutoff