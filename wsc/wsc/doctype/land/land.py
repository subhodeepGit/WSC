# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Land(Document):
	def validate(self):
		dateValidate(self)
		pincode(self)
		phone(self)


# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")
		

# Validation for pincode length	
def pincode(self):
	if not self.pin_code:
		return

	if len(self.pin_code)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

	if len(self.pin_code)<6:	
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

def phone(self):
	if len(self.phone)>10:
		frappe.throw("Field <b>Phone number</b> must be 10 Digits")
	
	if len(self.phone)<10:
		frappe.throw("Field <b>Phone number</b> must be 10 Digits")