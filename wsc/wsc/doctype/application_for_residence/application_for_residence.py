# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApplicationforResidence(Document):
	def on_submit(self):
		applicationStatus(self)

def applicationStatus(self):
	frappe.db.set_value("Application for Residence", self.name, "application_status", "Applied")

