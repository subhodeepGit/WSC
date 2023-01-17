# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceDeAllottment(Document):
	def on_submit(self):
		vacancyChange(self)
		applicationStatus(self)
		allotmentStatusRoom(self)
		vacancyChange(self)

def vacancyChange(self):
	frappe.db.set_value("Residence Allotment",self.name,"vacancy_status","Vacant")
	frappe.db.set_value("Residence Allotment",self.name,"employee_allotment_status", "Not Alloted")

def applicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.application_number, "application_status", "De-Alloted")

# To change employee allotment status to "Alloted" after allotment of building room
def allotmentStatusRoom(self):
	frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Not Alloted")

# To change vacancy status to "Not Vacant" after allotment of residence
def vacancyChange(self):
	frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Vacant")