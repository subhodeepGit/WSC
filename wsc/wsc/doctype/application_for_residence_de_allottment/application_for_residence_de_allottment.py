# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApplicationforResidenceDeAllottment(Document):
	def on_submit(self):
		applicationStatus(self)

def applicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.name, "application_status", "Applied")