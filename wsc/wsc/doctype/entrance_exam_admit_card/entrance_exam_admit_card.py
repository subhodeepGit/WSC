# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
from wsc.wsc.notification.custom_notification import admit_card_submit
import frappe
from frappe.model.document import Document

class EntranceExamAdmitCard(Document):
	# pass
	def on_submit(self):
		print("\n\nsubmit")
		admit_card_submit(self)

@frappe.whitelist()
def center_option(applicant_id , academic_year , academic_term , department):
	
	student_preference = frappe.get_all("Exam Centre Preference" , {'parent':applicant_id } , ['state' , 'districts' , 'center_name' , 'cityvillage'])

	
	print("\n\n\n\n")
	print(student_preference)