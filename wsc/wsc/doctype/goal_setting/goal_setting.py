# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import sendHR_appraisal,sendRa_appraisal,sendDh_appraisal,sendDirector_appraisal

class GoalSetting(Document):
	
	#Send mail to  HR
	def send_mail_hr(self):
		hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
		if hr_mail==[None]:
			frappe.throw("HR Admin mail id not found")
			

			# sendHR(data)
		else :
			hr_mail_id = hr_mail[0]
			data={}
			data["hr_mail"]=hr_mail_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			data["appraisal_cycle"]=self.appraisal_cycle
			sendHR_appraisal(data)

	#Send mail to Department Head
	def send_mail_dh(self):
		#take the department of the employee , find the user id of that particular department head
		department = self.department
		department_head = frappe.get_all("Department",filters = {"name":department},pluck="department_head")
		print("\n\n\n\nDepartment Head")
		print(department_head)
		print(type(department_head[0]))
		# if department_head == [None]:
		# 	print("Hello")
		if department_head==[None]:
			frappe.throw("Department Head Mail Not found")
			

		else :
			dh_id = department_head[0]
			data = {}
			data["dh_mail"]=dh_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			data["appraisal_cycle"]=self.appraisal_cycle
			# sendDh(data)
			sendDh_appraisal(data)
	
	#Send Mail to Director
	def send_mail_director(self):
		director_mail = frappe.get_all("User",filters={"role":"Director"},pluck='name')
		# print("\n\n\n")
		# print(director_mail)
		if director_mail==[None]:
			frappe.throw("Director Mail not found")
			

		else :
			director_mail_id = director_mail[0]
			data={}
			data["director_mail"]=director_mail_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			data["appraisal_cycle"]=self.appraisal_cycle
			# sendDirector(data)
			sendDirector_appraisal(data)

	#send mail to reporting authority
	def send_mail_ra(self):
		ra_mail = self.reporting_authority
		if ra_mail:
			data={}
			data["ra_mail"]=ra_mail
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			data["appraisal_cycle"]=self.appraisal_cycle
			# sendRa(data)
			sendRa_appraisal(data)
		else :
			frappe.throw("Reporting Authority mail not found")
