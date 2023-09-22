# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitmentExamResultDeclaration(Document):
	def on_submit(doc):
		job_applicant = frappe.get_doc("Job Applicant", doc.job_applicant_id)
		job_opening = frappe.get_doc("Job Opening", {"name": doc.job_opening})
		print("\n\n\n")
		print(job_applicant)

		for round in job_applicant.result_status:
			if round.name_of_the_round == doc.job_selection_round:
				if job_opening:
					round.status = doc.result_status
					print("\n\n Hello")
					print(round.status)	
		job_applicant.save()
		job_applicant.current_status = doc.result_status
		job_applicant.save()

