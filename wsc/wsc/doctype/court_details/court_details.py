# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CourtDetails(Document):
	def validate(self):
		pincode(self)
		contact_number(self)

def pincode(self):
	if self.pincode:
		if not (self.pincode).isdigit():
			frappe.throw("Field <b>Pin Code</b> Accept Digits Only")
		if len(self.pincode)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")
		if len(self.pincode)<6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

def contact_number(self):
	if self.contact_number:
		if not (self.contact_number).isdigit():
			frappe.throw("Field <b>Contact number</b> Accept Digits Only")
		if len(self.contact_number)>10:
			frappe.throw("Field <b>Contact number</b> must be 10 Digits")
		if len(self.contact_number)<10:
			frappe.throw("Field <b>Contact number</b> must be 10 Digits")