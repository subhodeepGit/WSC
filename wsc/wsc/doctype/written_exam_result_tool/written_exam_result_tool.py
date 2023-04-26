# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class WrittenExamResultTool(Document):
	@frappe.whitelist()
	def create_result(self):
		for i in self.get("candidates_result"):
			result = frappe.new_doc('Written Exam Result')
			result.job_applicant_id=i.job_applicant_id
			result.email = i.job_applicant_id
			result.name_of_the_candidate = i.name_of_the_candidate
			result.examination_name = self.exam_name
			result.examination_date = self.exam_date
			result.score_obtained = i.score_obtained
			result.result=i.result
			result.rank=i.rank
			result.result_declration_date = self.result_declaration_date
			result.total_score_of_exam=self.total_mark_of_the_exam
			result.examiner_name = self.examiner_name
			result.save()
			# result.submit()
			
			print("\n\n\n\n\n\n\nResult")
			print(result)

@frappe.whitelist()
def get_candidates_details(job):
	data = frappe.get_all("Job Applicant",{"job_title":job,"status":"Accepted"},["applicant_name","name","email_id"])
	if data :
		print("\n\n\n\n\n\n\nFrom Job Applicant")
		return data
	else :
		pass

