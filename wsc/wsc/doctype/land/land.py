# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Land(Document):
	def validate(self):
		date(self)
		pincode(self)


# To validate if the start date is not after the end date
def date(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")
		

# Validation for pincode length	
def pincode(self):
	if self.pin_code:
		if not (self.pin_code).isdigit():
			frappe.throw("Field <b>Pin Code</b> Accept Digits Only")

	if len(self.pin_code)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

	if len(self.pin_code)<6:	
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")
