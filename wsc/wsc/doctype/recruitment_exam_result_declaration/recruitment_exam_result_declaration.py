# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitmentExamResultDeclaration(Document):
	def on_submit(doc):
		job_applicant = frappe.get_doc("Job Applicant", doc.job_applicant_email)
		print("\n\n\n\n")
		print(job_applicant)

		for round in job_applicant.result_status:
			if round.name_of_the_round == doc.job_selection_round:
				round.status = doc.result_status	
		job_applicant.save()
		job_applicant.current_status = doc.result_status
		job_applicant.save()

