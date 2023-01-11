# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class placement_tool(Document):
	pass
@frappe.whitelist()
def get_student():
	# print("Hello function")
	# data = frappe.get_all("",[""])
	# return data
	return "Hello world"