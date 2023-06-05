# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitmentAdmitCardGenerationTool(Document):
	# def validate(doc):
	# 	update_job_opening(doc)

	@frappe.whitelist()
	def create_admit_card(self):
		for d in self.get('job_applicant_details'):
			result = frappe.new_doc('Recruitment Admit Card Generation')
			result.exam_declaration = self.exam_declaration
			result.exam_date = self.exam_date
			result.exam_time = self.exam_time
			result.center = self.center
			result.applicant_number = d.job_applicant
			result.applicant_name = d.applicant_name
			result.applicant_mail = d.applicant_mail_id
			result.save()
			result.submit()

	@frappe.whitelist()
	def update_job_opening(self):
		job_opening = frappe.get_all("Recruitment Exam Declaration",{"name":self.exam_declaration},["job_opening"])
		print("\n\n\n\n\nJob_opening",job_opening)
		if len(job_opening)==0:
			frappe.msgprint("No job Opening Found")
		else :
			job_opening= job_opening[0].job_opening
		selection_round_details = frappe.get_all("Recruitment Exam Declaration",{"name":self.exam_declaration},["selection_round"])
		if len(selection_round_details)==0:
			frappe.msgprint("No Selection Round Found")
		else :
			
			selection_round= selection_round_details[0]["selection_round"]
		job_opening_details = frappe.get_doc("Job Opening", job_opening)
			
		job_opening_details.job_opening = job_opening
		print("\n\n\n\n\nJob Opening ", job_opening)
		print("\n\n\n\n\nRound",selection_round)
		for round in job_opening_details.job_selection_round:
			
			if round.name_of_rounds==selection_round:
				round.admit_card_status="Declared" 
				# frappe.msgprint("Hello")
		job_opening_details.save()


@frappe.whitelist()
def fetch_applicants(recruitment_exam_declaration):
	applicants = frappe.get_all("Job Applicant Details",filters={"parent":recruitment_exam_declaration},fields=["job_applicant","applicant_name","applicant_mail_id"])
	print(applicants)
	return applicants
