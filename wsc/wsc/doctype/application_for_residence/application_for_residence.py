# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApplicationforResidence(Document):
	def validate(self):
		duplicate(self)
	def on_submit(self):
		applicationNumberField(self)
		applicationStatus(self)
		currentApplicationStatus(self)
	def on_cancel(self):
		cancelRejected(self)

# To validate for any duplicate application record for residence application
def duplicate(self):
	data=frappe.get_all("Application for Residence",[["employee_name","=",self.employee_name],['current_application_status',"=","Applied"],['docstatus',"=",1]])
	data2=frappe.get_all("Application for Residence",[["employee_name","=",self.employee_name],['current_application_status',"=","Alloted"],['docstatus',"=",1]])
	if data:
		frappe.throw("Application for residence can not be applied twice by an employee")
	if data2:
		frappe.throw("Employee already alloted a residence")

# To get the doc series name in a field
def applicationNumberField(self):
	self.db_set("application_number", self.name)

# To set value for Application status in Application for Residence
def applicationStatus(self):
	self.db_set("Application for Residence", self.name, "application_status", "Applied")

# To set value for Application status in Application for Residence
def currentApplicationStatus(self):
	self.db_set("Application for Residence", self.name, "current_application_status", "Applied")

# To set value for Application status in Application for Residence on cancel
def cancelRejected(self):
	self.db_set("Application for Residence", self.name, "current_application_status", "Cancelled by Applicant")
	self.db_set("Application for Residence", self.name, "application_status", "Cancelled by Applicant")

