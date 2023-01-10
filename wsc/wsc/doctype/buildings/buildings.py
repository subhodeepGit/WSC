# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Buildings(Document):
	def validate(doc):
		pincode(doc)
		if doc.start_date > doc.end_date:
			frappe.throw("Start date cannot be greater than End date")
			
def pincode(doc):
	if doc.pin_code:
		if not (doc.pin_code).isdigit():
			frappe.throw("Field <b>Pin Code</b> Accept Digits Only")

	if len(doc.pin_code)>6:
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")

	if len(doc.pin_code)<6:	
			frappe.throw("Field <b>Pin Code</b> must be 6 Digits")



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def room_type_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT `name` from `tabLand` WHERE `start_date`<=now() and `end_date`>=now()""")




