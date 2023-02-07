# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceDeAllottment(Document):
	def on_submit(self):
		residenceAllotmentStatus(self)
		currentApplicationStatus(self)
		buildingRoomStatus(self)
		residenceApplicationStatus(self)
		deallotmentNumberField(self)
		residenceUpdate(self)

# To get the doc series name in a field
def deallotmentNumberField(self):
	self.db_set("residence_de_allotment_number", self.name)

# To set value of current employee allotment status and current vacancy status in "Residence allotment"
def residenceAllotmentStatus(self):
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_vacancy_status","Vacant")
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_employee_allotment_status", "Not Alloted")
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_application_status", "De-Alloted")

# To set value of current application status in "Application for Residence De-Allottment"
def currentApplicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allottment", self.residence_de_allotment_application_number, "current_application_status", "De-Alloted")

# To change employee allotment status and vacancy status in "Building Room"
def buildingRoomStatus(self):
	if self.residence_change_status== "Approved":
		frappe.db.set_value("Building Room", self.changed_residence_serial_number, "employee_allotment_status", "Not Alloted")
		frappe.db.set_value("Building Room",self.changed_residence_serial_number,"vacancy_status","Vacant")
	else:
		frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Not Alloted")
		frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Vacant")
	
# To set value of current application status to De-Alloted in "Application for Residence"
def residenceApplicationStatus(self):
	frappe.db.set_value("Application for Residence", self.application_number, "current_application_status", "De-Alloted")

# To set value of de-allotment details in "Residence Allotted" child table in "Employee" doctype
def residenceUpdate(self):
	allotmentData=frappe.get_doc('Employee', self.employee_id)
	if self.residence_change_status== "Approved":
		allotmentData.append("residence_deallot",{
			"residence_de_allotment_number":self.residence_de_allotment_number,
			"application_number":self.application_number,
			"de_allotment_date":self.de_allotment_date,
			"residence_number":self.changed_residence_number,
			"residence_type_name":self.changed_residence_type_name,
			"residence_allotment_number":self.residence_allotment_number,
			"building_name":self.changed_building_name,
			"current_employee_allotment_status" : "De-Alloted"
			})
		allotmentData.save()
	else:
		allotmentData.append("residence_deallot",{
			"residence_de_allotment_number":self.residence_de_allotment_number,
			"application_number":self.application_number,
			"de_allotment_date":self.de_allotment_date,
			"residence_number":self.residence_number,
			"residence_type_name":self.residence_type_name,
			"residence_allotment_number":self.residence_allotment_number,
			"building_name":self.building_name,
			"current_employee_allotment_status" : "De-Alloted"
			})
		allotmentData.save()