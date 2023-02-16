# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Buildings(Document):
	def validate(self):
		dateValidate(self)
		pincode(self)

# To validate if the start date is not after the end date
def dateValidate(self):
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

# To fetch only those buildings which are between start and end date of the Land with respect to today’s date
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_type_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `name` from `tabLand` WHERE `start_date`<=now() and `end_date`>=now()""")




