# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document

class EntranceExamDeclaration(Document):
	def on_submit(self):
		for i in self.get('applicant_list'):
			applicant = frappe.get_doc("Student Applicant" , i.applicant_id)
			if applicant.exam_declared_for_applicant == 0:
				applicant.exam_declared_for_applicant = 1
			applicant.save()
	
	def on_cancel(self):
		for i in self.get('applicant_list'):
			applicant = frappe.get_doc("Student Applicant" , i.applicant_id)
			if applicant.exam_declared_for_applicant == 1:
				applicant.exam_declared_for_applicant = 0
			applicant.save()

@frappe.whitelist()
def get_applicants(body):
	body = json.loads(body)

	academic_year = body['academic_year']
	academic_term = body['academic_term']
	department = body['department']
	
	data = frappe.get_all('Student Applicant' , { "academic_year":academic_year ,
					      						  "academic_term":academic_term , 
												  "department":department ,
												  'docstatus':1 , 
												  'application_status': 'Applied' , 
												  "exam_declared_for_applicant" : 0
												} , 
												['name' , 'title' , 'gender' , 'student_category' , 'physically_disabled']
												,order_by="name asc")
	# data = frappe.get_all("Stude")

	# data2 = frappe.get_all("Student Applicant" , { 'name' : 'EDU-APP-2023-00009'} , ['name' ,'academic_year' , 'department' , 'academic_term' , 'title' , 'gender' , 'student_category' , 'physically_disabled' , 'application_status' , 'exam_declared_for_applicant'])
	return data