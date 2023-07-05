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
		print("\n\n\n\n\nData")
		print(data)
		employee_reporting_aprover(data)
		
	def validate(self):
		print("\n\n\n\nHello...Hello")
		print("\n\n\n\n\n\n")
		print(self.workflow_state)
		if self.workflow_state == "Draft":
			self.approver_mail()
		if self.workflow_state=="Pending Approval From HR":
			self.send_to_hr()
			print("\n\n\n\n\nIf Statement is Working")
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


@frappe.whitelist()
def isrfp(reporting_auth):
	# if frappe.db.exists(docname):
	reporting_auth_id = frappe.get_all("Employee",{"name":reporting_auth},["user_id"])
	# print("reporting_auth_id",reporting_auth_id)
	if reporting_auth_id:
		reporting_auth_id=reporting_auth_id[0]["user_id"]
	return reporting_auth_id

@frappe.whitelist()
def get_hr_mail():
	hr_mail = frappe.get_all("User",filters={'role':"HR Admin"},pluck='name')
	if hr_mail:
		hr_mail_id = hr_mail[0]
		return hr_mail_id

@frappe.whitelist()
def is_verified_user(docname):
	# if frappe.db.exists(docname):

	doc = frappe.get_doc("Employee Profile Updation",docname)
	# emp_user_id = frappe.get_all("Employee",{"name":doc.employee},["user_id"])
	# if emp_user_id:
	# 	employee_user_id = emp_user_id[0]["user_id"]
	reporting_auth_id = doc.reporting_auth_id
	if doc.workflow_state == "Draft" and frappe.session.user ==reporting_auth_id:
		return True
	else :
		return False