# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class ApplicationforResidenceDeAllotment(Document):
	def validate(self):
		duplicate(self)
	def on_submit(self):
		fieldName(self)
		applicationStatus(self)
		currentApplicationStatus(self)
		residenceHistoryUpdate(self)

# To check for any duplicate record in "applied" applications for de-allotment
def duplicate(self):
	data=frappe.get_all("Application for Residence De-Allotment",{"application_status":self.application_status,"application_number":self.application_number})
	if data:
		frappe.throw("Same application number cant apply again")

# To get the doc series name in a field
def fieldName(self):
	self.db_set("residence_de_allotment_application_number", self.name)

# To set value for Application status to applied after application
def applicationStatus(self):
	self.db_set("application_status", "Applied")

# To set value for Current Application status to applied after application
def currentApplicationStatus(self):
	self.db_set("current_application_status", "Applied")

#To update value for application of Residence De Allotment in "Residence Allotment History" child table in Employee doctype
def residenceHistoryUpdate(self):
	allotmentData=frappe.get_doc('Employee', self.employee_id)
	allotmentData.append("residence_allotment_history_table",{
			"application_number":self.application_number,
			"residence_serial_number":self.changed_residence_serial_number,
			"residence_number":self.changed_residence_number,
			"residence_type_name":self.changed_residence_type,
			"building_name":self.changed_building_name,
			"residence_allotment_number":self.residence_allotment_number,
			"date":datetime.date.today(),
			"status":"Applied for De-Allotment"
			})
	allotmentData.save()