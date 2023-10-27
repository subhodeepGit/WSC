# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitmentAdmitCardGeneration(Document):
	pass

@frappe.whitelist()
def fetch_applicants(docname):
    # if docname.exam_declaration:
	exam_declaration = frappe.get_doc('Recruitment Exam Declaration', docname)
	applicants = [applicant.job_applicant for applicant in exam_declaration.applicant_details]
	print(applicants)
	return applicants

@frappe.whitelist()
def get_applicant_details(applicant_number):
	applicant = frappe.get_doc("Job Applicant",applicant_number)
	print("\n\n\nApplicant")
	print(applicant)
	print(applicant.applicant_name)
	print(applicant.email_id)
	return {"applicant_name":applicant.applicant_name,"applicant_email":applicant.email_id}





