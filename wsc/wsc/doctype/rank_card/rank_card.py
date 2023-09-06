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
	# 	print("\n\n\n")

	# 	student_applicant = frappe.get_doc("Student Applicant" , self.applicant_id)

	# 	if(len(student_applicant.student_rank) == 0):
	# 		rank_data = frappe.get_all('Student Ranks List' ,
	# 		      						 {'parent':self.name} ,
	# 									 ['general_rank' , 'category_based_rank' , 'pwd_based_rank'])

	# 		student_applicant.append("student_rank" , {
	# 			'general_rank' : rank_data[0]['general_rank'],
	# 			'category_based_rank' : rank_data[0]['category_based_rank'],
	# 			'pwd_based_rank' : rank_data[0]['pwd_based_rank']
	# 		})
	# 		student_applicant.save()