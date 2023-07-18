# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReportingDesk(Document):
	def on_submit(self):
		print("\n\n")
		applicant_id = frappe.get_all("Rank Card" , { 'name' : self.applicant_id } , ['applicant_id'])
		print(applicant_id[0]['applicant_id'])
		# frappe.db.sql("""
		# 				UPDATE `tabStudent Applicant` SET couselling_start = 1 FROM  WHERE name = '{id}'
		# 			""".format(id = applicant_id[0]['applicant_id']))
# UPDATE `tabStudent Applicant` SET couselling_start = 0 WHERE name = 'EDU-APP-2023-00024'
		frappe.db.set_value("Student Applicant" , applicant_id[0]['applicant_id'], {
			'couselling_start':1,
		})
		
@frappe.whitelist()
def reporting(applicant_id):

	data_basic = frappe.get_all("Rank Card" , 
		       				{'name':applicant_id} ,
							['applicant_name' ,
							 'gender' , 'student_category' , 'physically_disabled' ,
							 'academic_year' , 'academic_term' , 'department' ,
							 'total_marks' , 'earned_marks'
							])
	
	data_rank = frappe.get_all("Student Ranks List" ,
			    			 {'parent': applicant_id} ,
							 ['general_rank' ,
	 						  'category_based_rank' ,
							  'pwd_based_rank'
	 						])
	data = []
	data.append(data_basic)
	data.append(data_rank)

	return data

