# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document

class EntranceExamDeclaration(Document):
	pass

@frappe.whitelist()
def get_applicants(body):
	body = json.loads(body)

	academic_year = body['academic_year']
	academic_term = body['academic_term']
	department = body['department']
	
	data = frappe.get_all('Student Applicant' , { "academic_year":academic_year , "academic_term":academic_term , "department":department ,'docstatus':1 , 'application_status': 'Applied'} , ['name' , 'title' , 'gender' , 'student_category' , 'physically_disabled'])
	print("\n\n\n")
	print(data)

	return data