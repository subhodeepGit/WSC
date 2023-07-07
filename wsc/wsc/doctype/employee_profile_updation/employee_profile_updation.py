# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import employee_reporting_aprover,employee_hr
import datetime
from typing import Dict, Optional, Tuple, Union

import frappe
from frappe import _
from frappe.query_builder.functions import Max, Min, Sum

from frappe.model.document import Document

class EmployeeProfileUpdation(Document):
	def approver_mail(self):
		data={}
		data["reporting_authority_email"]=self.reporting_auth_id
		data["employee_name"]=self.employee_name
		data["current_status"]=self.workflow_state
		data["name"]=self.name
		data["hr_email"]=self.hr_id
		employee_reporting_aprover(data)
		
	def validate(self):
		
		# print(self.workflow_state)
		if self.workflow_state == "Draft":
			self.approver_mail()
		if self.workflow_state=="Pending Approval From HR":
			self.send_to_hr()
			# print("\n\n\n\n\nIf Statement is Working")

		
	# def on_update(self):
	# 	print("\n\n\n\n\nHEeeeeeeeee")
	# 	if self.current_status == "Forwarded to HR":
	# 		self.send_to_hr()
	# 		# notify leave approver about creation
	def send_to_hr(self):
		data = {}
		data["hr_email"] = self.hr_id
		data["employee_name"]=self.employee_name
		data["current_status"]=self.workflow_state
		data["name"]=self.name
		employee_hr(data)
		
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.employee)
		# print("\n\n\n\n\nOn Submit")
		# print(employee)
		# Clear existing child table entries
		employee.education = []

		# Update child table with form data
		for row in self.education:
			child_row = employee.append("education", {})
			child_row.school_univ = row.school_univ
			child_row.qualification = row.qualification
			child_row.level=row.level
			child_row.year_of_passing=row.year_of_passing
			child_row.class_per= row.class_per
		
		#clear existing family details table
		employee.family_background_details = []

		# Update child table with form data
		for row in self.family:
			child_row = employee.append("family_background_details", {})
			child_row.name1 = row.name1
			child_row.relation = row.relation
			child_row.occupation=row.gender
			child_row.contact=row.contact
			
		# Save the changes to the employee document
		employee.current_address=self.current_address
		employee.permanent_address=self.permanent_address
		employee.cell_number=self.mobile
		employee.person_to_be_contacted=self.emergency_contact_name
		employee.emergency_phone_number=self.emergency_contact
		employee.relation=self.relation
		employee.personal_email=self.personal_email

		#save the changes
		employee.save()
		# Print a success message
		frappe.msgprint("Employee profile updated successfully.")


#populate Reporting Authority 
@frappe.whitelist()
def isrfp(reporting_auth):
	# if frappe.db.exists(docname):
	reporting_auth_id = frappe.get_all("Employee",{"name":reporting_auth},["user_id"])
	# print("reporting_auth_id",reporting_auth_id)
	if reporting_auth_id:
		reporting_auth_id=reporting_auth_id[0]["user_id"]
	return reporting_auth_id

#Populate HR Admin
@frappe.whitelist()
def get_hr_mail():
	hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
	if hr_mail:
		hr_mail_id = hr_mail[0]
		return hr_mail_id


#popuate Education Details 
@frappe.whitelist()
def get_education(employee):
	data = frappe.get_all("Employee Education",{"parent":employee},["school_univ","qualification","level","year_of_passing","class_per"])
	if data :
		# print("\n\n\n\n\n",data)
		return data

#populate family details
@frappe.whitelist()
def get_family_background(employee):

	data = frappe.get_all("Family Background Details",{"parent":employee},["name1","relation","occupation","gender","contact"])
	if data :
		# print("\n\n\n\n\n",data)
		return data
	
#get Address and Contact Details
@frappe.whitelist()
def addr_contact(employee):
	data = frappe.get_all("Employee",{"name":employee},["current_address","permanent_address","cell_number","person_to_be_contacted","emergency_phone_number","relation","personal_email"])
	if data :
		# print("\n\n\n\n\n",data)
		return data[0]

@frappe.whitelist()
def is_verified_user(docname):
	# if frappe.db.exists(docname):

	doc = frappe.get_doc("Employee Profile Updation",docname)
	# emp_user_id = frappe.get_all("Employee",{"name":doc.employee},["user_id"])
	# if emp_user_id:
	# 	employee_user_id = emp_user_id[0]["user_id"]
	reporting_auth_id = doc.reporting_auth_id
	roles = frappe.get_roles(frappe.session.user)

	if "HR Manager/CS Officer" in roles or "HR Admin" in roles or "Director" in roles or "Admin" in roles or "Administrator" in roles:
		return True
	if doc.workflow_state == "Draft" and frappe.session.user ==reporting_auth_id or doc.work:
		return True
	else :
		return False