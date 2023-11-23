# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitmentAdmitCardGeneration(Document):
	def on_submit(self):
		print("\n\n\nHJEjadfslk")
		self.admit_card_status()
		# self.admit_card_round()

	def admit_card_status(self):
		print("\n\nWOrking")	
		frappe.db.sql("""UPDATE `tabJob Applicant Details` as JAD 
						JOIN `tabRecruitment  Admit Card Generation` as JA
						ON JAD.job_applicant=JA.applicant_number
						JOIN `tabRecruitment Exam Declaration` as RED
						ON JA.selection_round=RED.selection_round
						SET JAD.admit_card_status = "1" and JAD.selection_round = "%s" 
						WHERE JAD.parenttype="Recruitment Exam Declaration"
						AND
						JAD.selection_round=JA.selection_round;"""%(self.selection_round))
	# def admit_card_round(self):
	# 	print("\n\nWOrking")	
	# 	frappe.db.sql("""UPDATE `tabJob Applicant Details` as JAD 
	# 					INNER JOIN `tabRecruitment Exam Declaration` as RED
	# 					ON JAD.parent=RED.name 
	# 					SET JAD.selection_round = "%s" 
	# 					where JAD.parenttype="Recruitment Exam Declaration";"""%(self.selection_round))
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
	return {"applicant_name":applicant.applicant_name,"applicant_email":applicant.email_id,'caste_category':applicant.caste_category,'domicile':applicant.domicile,'address':applicant.address,'date_of_birth':applicant.date_of_birth,'pwd':applicant.pwd,'fathersspousesguardians_name':applicant.fathersspousesguardians_name}






