# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamAdmitCard(Document):
	pass

@frappe.whitelist()
def center_option(applicant_id , academic_year , academic_term , department):
	
	student_preference = frappe.get_all("Exam Centre Preference" , {'parent':applicant_id } , ['state' , 'districts' , 'center_name' , 'cityvillage'])

	
	print("\n\n\n\n")
	print(student_preference)