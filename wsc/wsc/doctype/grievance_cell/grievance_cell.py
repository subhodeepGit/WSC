# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GrievanceCell(Document):
	pass


@frappe.whitelist()
def get_workflow_components(type_of_grievance):
	print("\n\n\n")
	print(type_of_grievance)
	wf_data=frappe.get_all("Standard WorkFlow For Grievance",{"parent":type_of_grievance},
			["name","emp_no","emp_name","department","designation","email_id","idx"],order_by="idx")		
	print(wf_data)		
	return wf_data
