# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document




class Land(Document):
	def validate(self):
		if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")
		pincode(self)

def pincode(doc):
	if doc.pin_code:
		if not (doc.pin_code).isdigit():
			frappe.throw("Field <b>Pin Code</b> Accept Digits Only")

	if len(doc.pin_code)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

	if len(doc.pin_code)<6:	
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")
