# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamCentreMaster(Document):
	def validate(doc):
		pincode_validation(doc)


def pincode_validation(doc):
	if doc.pincode:
		if len(str(doc.pincode))>6:
			frappe.throw("Field Pincode must be 6 Digits")
		if len(str(doc.pincode))<6:
			frappe.throw("Field Pincode must be 6 Digits")
