# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceChangeRequest(Document):
	def validate(self):
		duplicate(self)
		changeRequestNumberField(self)
		changeRoomStatus(self)
		buildingStatusChange(self)
		changeNewRoomStatus(self)
		residenceUpdate(self)
		changedResidenceDetails(self)

def duplicate(self):
	data=frappe.get_all("Residence Change Request",[["employee_name","=",self.employee_name],['request_status',"=","Pending Approval"]])
	if data:
		frappe.throw("Can't Apply again as Residence change request for this employee is Pending for Approval")

# To change vacancy status and employee allotment status of alloted residence
def changeRoomStatus(self):
	data= self.request_status
	if data == "Approved":
		frappe.db.set_value("Residence Allotment",self.alloted_residence_serial_number,"vacancy_status","Vacant")
		frappe.db.set_value("Residence Allotment",self.alloted_residence_serial_number,"employee_allotment_status", "Not Alloted")

# To change allotment and vacancy status of alloted residence in building room
def buildingStatusChange(self):
	if self.request_status== "Approved":
			frappe.db.set_value("Building Room", self.alloted_residence_serial_number, "vacancy_status","Vacant")
			frappe.db.set_value("Building Room", self.alloted_residence_serial_number, "employee_allotment_status", "Not Alloted")
	
# To change vacancy status and employee allotment status of newly alloted residence after approval of change of residence request
def changeNewRoomStatus(self):
	if self.request_status== "Approved":
		frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Not Vacant")
		frappe.db.set_value("Building Room",self.residence_serial_number,"employee_allotment_status", "Alloted")

# To update residence details in Employee doctype
def residenceUpdate(self):
	if self.request_status== "Approved":
		allotmentData=frappe.get_doc('Employee', self.employee)
		allotmentData.append("table_109",{
			"residence_allotment_number":self.residence_allotment_number,
			"application_number":self.application_number,
			"residence_type":self.residence_type,
			"residence_type_name":self.residence_type_name,
			"residence_number":self.residence_number,
			"floor":self.floor,
			"building_address":self.building_address,
			"unit_area_sq_m":self.unit_area_sq_m,
			"parking_available":self.parking_available,
			"parking_type":self.parking_type,
			"parking_area_sq_m":self.parking_area_sq_m,
			"parking_vehicle":self.parking_vehicle,
			"current_employee_allotment_status" : "Re-Alloted",
			"date":self.change_request_date
			})
		allotmentData.save()

# To set value of doc series in residence_change_request_number field
def changeRequestNumberField(self):
	self.db_set("residence_change_request_number", self.name)

# To set value of changed residence details in "Residence Allotment" doctype
def changedResidenceDetails(self):
	if self.request_status== "Approved":
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_serial_number",self.residence_serial_number)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_number",self.residence_number)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_building_name",self.residence_building)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_type",self.residence_type)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_type_name",self.residence_type_name)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"residence_change_status",self.request_status)
