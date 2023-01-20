# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApplicationforResidenceDeAllottment(Document):
	def validate(self):
		duplicate(self)
	def on_submit(self):
		name(self)
		applicationStatus(self)
		currentApplicationStatus(self)

# To check for any duplicate record in "applied" applications for de-allotment
def duplicate(self):
	data=frappe.get_all("Application for Residence De-Allottment",{"application_status":self.application_status,"application_number":self.application_number})
	if data:
		frappe.throw("Same application number cant apply again")

# To get the doc series name in a field
def name(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.name , "residence_de_allotment_number", self.name)

# To set value for Application status to applied after application
def applicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.name, "application_status", "Applied")

# To set value for Current Application status to applied after application
def currentApplicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.name, "current_application_status", "Applied")



