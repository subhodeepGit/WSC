# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.pdf import get_pdf
from frappe.website.serve import get_response_content

class testdoctype(Document):
	def validate(self):
		html = get_response_content("printview")
		a=get_pdf(html, options={}, output=None)
		self.text_field="%s"%(a)
		pass

import frappe
@frappe.whitelist(allow_guest=True)
def get_test():
	return 'okhhhghghh'
