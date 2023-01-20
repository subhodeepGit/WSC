# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceDeAllottment(Document):
	def on_submit(self):
		# name(self)
		residenceAllotmentStatus(self)
		currentApplicationStatus(self)
		buildingRoomStatus(self)
		residenceApplicationStatus(self)
		
# def name(self):
# 	frappe.db.set_value("Residence De-Allottment",self.name,"residence_de_allotment_number", self.name)

# To set value of current employee allotment status and current vacancy status in "Residence allotment"
def residenceAllotmentStatus(self):
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_vacancy_status","Vacant")
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_employee_allotment_status", "Not Alloted")

# To set value of current application status in "Application for Residence De-Allottment"
def currentApplicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.residence_de_allotment_number, "current_application_status", "De-Alloted")

# To change employee allotment status and vacancy status in "Building Room"
def buildingRoomStatus(self):
	frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Not Alloted")
	frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Vacant")
	
# To set value of current application status to De-Alloted in "Application for Residence"
def residenceApplicationStatus(self):
	frappe.db.set_value("Application for Residence", self.application_number, "current_application_status", "De-Alloted")
