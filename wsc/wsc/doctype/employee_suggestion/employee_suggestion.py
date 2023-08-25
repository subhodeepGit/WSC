# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import notify_hr,notify_director,notify_employee

class EmployeeSuggestion(Document):
	def notification_to_hr(self):
		data = {}
		hr = get_hr_mail()
		if hr != None:

			data["hr_email"] = hr
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["employee_suggestion"]=self.name
			data["name"]=self.name


			notify_hr(data)
		else :
			frappe.throw("HR Admin Email ID  Not Found")
	def notification_to_director(self):
		data = {}
		director = get_director_mail()
		if director != None :

			data["director_email"] = director
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["employee_suggestion"]=self.name
			data["name"]=self.name


			notify_director(data)
		else :
			frappe.throw("Director Email ID  Not Found")
	def notification_to_employee(self):
		data = {}
		employee_mail = self.user_id
		if employee_mail != None:

			data["employee_email"] = employee_mail
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["employee_suggestion"]=self.name
			data["name"]=self.name


			notify_employee(data)
		else :
			frappe.throw("Employee Email ID  Not Found")
	def validate(self):
		if self.user_id == None :
			frappe.msgprint("Employee User ID not found")
		if self.workflow_state == "Pending Approval From HR":
			self.notification_to_hr()
		if self.workflow_state == "Pending Approval from Director Admin":
			self.notification_to_director()
		if self.workflow_state == "Approved" or self.workflow_state=="Rejected":
			self.notification_to_employee()
	

#Getting HR Mail
@frappe.whitelist()
def get_hr_mail():
	hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
	if hr_mail :
		hr_mail_id = hr_mail[0]
		return hr_mail_id
	# else :
	# 	frappe.msgprint("Set HR Admin Mail ID")

#getting Director Mail
@frappe.whitelist()
def get_director_mail():
	director_mail = frappe.get_all("User",filters={'role':"Director"},pluck='name')
	if director_mail :
		director_mail_id = director_mail[0]
		return director_mail_id
	# else :
	# 	frappe.msgprint("Set Director Mail ID ")