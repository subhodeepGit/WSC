# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _,get_list

class EmployeeReengagement(Document):
	pass
@frappe.whitelist()
def isrfp(docname):
	doc = frappe.get_doc("Employee Reengagement",docname)
	reporting_auth = doc.reporting_authority
	reporting_auth_id = frappe.get_all("Employee",{"name":reporting_auth},["user_id"])
	# print("reporting_auth_id",reporting_auth_id)
	if reporting_auth_id:
		reporting_auth_id=reporting_auth_id[0]["user_id"]
		if reporting_auth_id==frappe.session.user :
			return True
		

		

