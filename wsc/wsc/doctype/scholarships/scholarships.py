# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class Scholarships(Document):
		pass

@frappe.whitelist()
def get_students(semester):
	topper=[]
	topper = frappe.db.sql(
		'''SELECT student, student_name, sgpa 
		FROM `tabExam Assessment Result` 
		WHERE program= %s
		ORDER BY sgpa DESC;''',
		(semester),
		as_dict=1,

	
	)
	print(topper)
	if topper:
		topperlist= []
		nextTopperList=[]
		nextTopperList2=[]
		nextTopperList3=[]

		top = topper[0]['sgpa']
		for x in topper:
			if x['sgpa']==top:
				topperlist.append(x)
			if x['sgpa']!=top:
				nextTopperList.append(x)

		rank2=[]
		top2 = nextTopperList[0]['sgpa']
		for x in nextTopperList:
			if x['sgpa']==top2:
				rank2.append(x)
			if x['sgpa']!=top2:
				nextTopperList2.append(x)

		rank3=[]
		top3= nextTopperList2[0]['sgpa']
		for x in nextTopperList2:
			if x['sgpa']==top3:
				rank3.append(x)
			if x['sgpa']!=top3:
				nextTopperList3.append(x)

		topperlist.extend(rank2)
		topperlist.extend(rank3)
		return topperlist

@frappe.whitelist()
def get_cutoffStudents(semester,lower_cutoff_sgpa,upper_cutoff_sgpa):
		cutoff= []
		if lower_cutoff_sgpa:
			cutoff= frappe.db.sql(
			'''SELECT student, student_name, sgpa 
			FROM `tabExam Assessment Result` 
			WHERE program= %s AND sgpa BETWEEN %s AND %s
			ORDER BY sgpa DESC;''',
			(semester, lower_cutoff_sgpa, upper_cutoff_sgpa),
			as_dict=1,
		
	)
			print("\n\n\n\n\n 1st")
		else:
			cutoff= frappe.db.sql(
			'''SELECT student, student_name, sgpa 
			FROM `tabExam Assessment Result` 
			WHERE program= %s AND sgpa < %s
			ORDER BY sgpa DESC;''',
			(semester, lower_cutoff_sgpa),
			as_dict=1,
		)
			print("\n\n\n\n\n 2st")
			print(cutoff)
		return cutoff

		


		

