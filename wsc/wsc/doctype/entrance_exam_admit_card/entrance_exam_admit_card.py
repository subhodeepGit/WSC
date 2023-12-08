# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt
from wsc.wsc.notification.custom_notification import admit_card_submit
import frappe
from frappe.model.document import Document

class EntranceExamAdmitCard(Document):
	# pass
	def on_submit(self):
		admit_card_submit(self)

		email = frappe.get_all('Student Applicant' , {'name':self.applicant_id},['student_email_id'])
	
		user_perm = frappe.new_doc("User Permission")
		user_perm.user = email[0]['student_email_id']
		user_perm.allow = self.doctype
		user_perm.for_value = self.name

		user_perm.save()
	
	def on_trash(self):
		# perm_data = frappe.get_all('User Permission' , {'for_value':self.name} , ['name' , 'for_value'])
		perm_data = frappe.db.sql("""
			SELECT
				name , for_value 
			FROM `tabUser Permission` 
			WHERE for_value = '{admit_id}';
		""".format(admit_id = self.name) , as_dict=1)

		if perm_data:
			user_perm_data = frappe.get_doc('User Permission' , perm_data[0]['name'])

			user_perm_data.delete()

