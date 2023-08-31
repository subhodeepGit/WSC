# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Year(Document):
	def validate(doc):
		doc.validate_year()

	def validate_year(doc):
		if doc.year:
			if len(doc.year)<4:
				frappe.throw("<b>Year</b> must be 4 Digits")
		if not check_int(doc.year):
			frappe.throw("Year must be the digit.")

def check_int(year):
	import re
	return re.match(r"[-+]?\d+(\.0*)?$", year) is not None
	