# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApplicationforResidence(Document):
	def validate(self):
		duplicate(self)
	def on_submit(self):
		name(self)
		applicationStatus(self)
		currentApplicationStatus(self)
	def on_cancel(self):
		cancelRejected(self)

# To validate for any duplicate application record for residence application
def duplicate(self):
	data=frappe.get_all("Application for Residence",[["employee_name","=",self.employee_name],['current_application_status',"=","Applied"],['docstatus',"=",1]])
	if data:
		frappe.throw("Application for residence can not be applied twice by an employee")

# To get the doc series name in a field
def name(self):
	frappe.db.set_value("Application for Residence", self.name , "application_number", self.name)

# To set value for Application status in Application for Residence
def applicationStatus(self):
	frappe.db.set_value("Application for Residence", self.name, "application_status", "Applied")

# To set value for Application status in Application for Residence
def currentApplicationStatus(self):
	frappe.db.set_value("Application for Residence", self.name, "current_application_status", "Applied")

# To set value for Application status in Application for Residence on cancel
def cancelRejected(self):
	frappe.db.set_value("Application for Residence", self.name, "current_application_status", "Cancelled by Applicant")
	frappe.db.set_value("Application for Residence", self.name, "application_status", "Cancelled by Applicant")

