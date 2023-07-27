# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import sendHR,sendEmployee,sendDh,sendDirector,sendRa

class EmployeeResignation(Document):

############ Notification Coding Started ############################

	#send mail to HR
	def send_mail_hr(self):
		hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
		if hr_mail!=None and hr_mail[0]!='':
			hr_mail_id = hr_mail[0]
			data={}
			data["hr_mail"]=hr_mail_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			sendHR(data)
		else :
			frappe.msgprint("HR Admin mail id not found")
		
	#send mail to employee
	def send_employee(self):
		employee_user_id = frappe.get_all("Employee",filters={"name":self.employee},pluck="user_id")
		if len(employee_user_id)>0:
			user_id = employee_user_id[0]
			data = {}
			data["employee_mail"]=user_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			sendEmployee(data)
		
	#Send mail to Department Head
	def send_mail_dh(self):
		#take the department of the employee , find the user id of that particular department head
		department = self.department
		department_head = frappe.get_all("Department",filters = {"name":department},pluck="department_head")
		
		if department_head != None and department_head[0] != '':
			dh_id = department_head[0]
			data = {}
			data["dh_mail"]=dh_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			sendDh(data)
		else :
			frappe.msgprint("Department Head Mail Not found")

		

	#Send Mail to Director
	def send_mail_director(self):
		director_mail = frappe.get_all("User",filters={"role":"Director"},pluck='name')
		# print("\n\n\n")
		# print(director_mail)
		if director_mail!=None and director_mail[0]!='':
			director_mail_id = director_mail[0]
			data={}
			data["director_mail"]=director_mail_id
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			sendDirector(data)

		else :
			frappe.msgprint("Director Mail not found")

	#send mail to reporting authority
	def send_mail_ra(self):
		ra_mail = self.reporting_authority
		if len(ra_mail)>0 :
			data={}
			data["ra_mail"]=ra_mail
			data["employee_name"]=self.employee_name
			data["current_status"]=self.workflow_state
			data["name"]=self.name
			sendRa(data)
		else :
			frappe.msgprint("Reporting Authority mail not found")

	#validate
	def validate(self):
		if self.workflow_state == "Pending Approval from Reporting Authority":
			self.send_mail_ra()
		if self.workflow_state == "Pending Approval from Department Head":
			#code needs to be added 
			self.send_mail_dh()
		if self.workflow_state == "Pending Approval from Director Admin":
			self.send_mail_director()
		if self.workflow_state == "Approved" or self.workflow_state=="Rejected":
			self.send_employee()
			self.send_mail_hr


################### Notification coding Ended ##################################
	


@frappe.whitelist()
def get_joining_date(employee):
	joining = frappe.get_all("Employee",{"name":employee},["date_of_joining"])
	if joining:
		return joining[0]
	else :
		frappe.msgprint("Joinig Date is not available ")

#set reporting authority ID	
@frappe.whitelist()
def get_ra(employee):
	# if frappe.db.exists(docname):
	ra = frappe.get_all("Employee",{"name":employee},["reports_to"])
	if ra :
		ra = ra[0]["reports_to"]
		ra_id = frappe.get_all("Employee",{"name":ra},["user_id"])
		if ra_id:
			return ra_id[0]
		else:
			frappe.msgprint("User ID of Reporting Authority Not Found")
	else :
		frappe.msgprint("Reporting Authority Not Found")

@frappe.whitelist()
def is_verified_user(docname):
	# if frappe.db.exists(docname):

	doc = frappe.get_doc("Employee Resignation",docname)
	reporting_auth_id = doc.reporting_authority
	roles = frappe.get_roles(frappe.session.user)

	if "HR Manager/CS Officer" in roles or "HR Admin" in roles or "Director" in roles or "Admin" in roles or "Administrator" in roles or "Department Head" in roles:
		return True
	if doc.workflow_state == "Pending Approval from Reporting Authority" and frappe.session.user ==reporting_auth_id:
		return True
	if doc.workflow_state == "Draft" and frappe.session.user == doc.owner:
		return True
	else :
		return False