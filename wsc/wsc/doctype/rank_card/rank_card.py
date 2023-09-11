# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
from wsc.wsc.notification.custom_notification import rank_card_submit
import frappe
from frappe.model.document import Document

class RankCard(Document):
	def on_cancel(self):
		student_applicant = frappe.get_doc("Student Applicant" , self.applicant_id)
		student_applicant.student_rank.clear()
		student_applicant.save()
	
	def on_submit(self):
		rank_card_submit(self)
	