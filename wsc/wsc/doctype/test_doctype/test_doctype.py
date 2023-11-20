# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class testdoctype(Document):
	pass

import frappe
@frappe.whitelist(allow_guest=True)
def get_test():
	return 'okhhhghghh'
