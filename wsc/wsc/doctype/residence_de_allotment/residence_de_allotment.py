# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime


class ResidenceDeAllotment(Document):
	def validate(self):
		endDateUpdate(self)

	def on_submit(self):
		residenceAllotmentStatus(self)
		currentApplicationStatus(self)
		buildingRoomStatus(self)
		residenceApplicationStatus(self)
		deallotmentNumberField(self)
		residenceUpdate(self)
		residenceHistoryUpdate(self)

def endDateUpdate(self):
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_end_date", self.de_allotment_date)
	self.db_set("end_date", self.de_allotment_date)

# To get the doc series name in a field
def deallotmentNumberField(self):
	self.db_set("residence_de_allotment_number", self.name)

# To set value of current employee allotment status and current vacancy status in "Residence allotment"
def residenceAllotmentStatus(self):
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_vacancy_status","Vacant")
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_employee_allotment_status", "Not Alloted")
	frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_application_status", "De-Alloted")

# To set value of current application status in "Application for Residence De-Allotment"
def currentApplicationStatus(self):
	frappe.db.set_value("Application for Residence De-Allotment", self.residence_de_allotment_application_number, "current_application_status", "De-Alloted")

# To change employee allotment status and vacancy status in "Building Room"
def buildingRoomStatus(self):
		frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Not Alloted")
		frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Vacant")
	
# To set value of current application status to De-Alloted in "Application for Residence"
def residenceApplicationStatus(self):
	frappe.db.set_value("Application for Residence", self.application_number, "current_application_status", "De-Alloted")

# To clear all residence details after De-Allotment "Residence Allotment Details" child table in Employee doctype
def residenceUpdate(self):
	frappe.db.delete("Residence Allotted", {"parent":self.employee_id})

#To insert the De-Alloted residence details in "Residence Allotment History" child table in Employee doctype
def residenceHistoryUpdate(self):
	allotmentData=frappe.get_doc('Employee', self.employee_id)
	allotmentData.append("residence_allotment_history_table",{
			"residence_de_allotment_number":self.residence_de_allotment_number,
			"application_number":self.application_number,
			"de_allotment_date":self.de_allotment_date,
			"residence_serial_number":self.residence_serial_number,
			"residence_number":self.residence_number,
			"residence_type_name":self.residence_type_name,
			"residence_allotment_number":self.residence_allotment_number,
			"building_name":self.building_name,
			"date":datetime.date.today(),
			"start_date":self.start_date,
			"end_date":self.end_date,
			"status":"De-Alloted"
			})
	allotmentData.save()

@frappe.whitelist()
def residence_deallotments(residence_de_allotment_application_number,reason_for_de_allotment,residence_allotment_number,application_number,start_date,current_residence_serial_number,current_residence_number,employee_name,employee_id,current_building_name,current_residence_type,current_residence_type_name):
	ra = frappe.new_doc("Residence De-Allotment")
	ra.residence_de_allotment_application_number = residence_de_allotment_application_number
	ra.reason_for_de_allotment = reason_for_de_allotment
	ra.residence_allotment_number= residence_allotment_number
	ra.application_number=application_number
	ra.start_date=start_date
	ra.residence_serial_number= current_residence_serial_number
	ra.residence_number=current_residence_number
	ra.employee_name=employee_name
	ra.employee_id = employee_id
	ra.building_name= current_building_name
	ra.residence_type=current_residence_type
	ra.residence_type_name=current_residence_type_name
	return ra