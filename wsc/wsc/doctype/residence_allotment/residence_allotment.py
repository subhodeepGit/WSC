# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceAllotment(Document):
	def validate(self):
		dateValidate(self)
		duplicateResidenceAllot(self)
		dateValidate(self)
		

	def on_submit(self):
		allotmentNumberField(self)
		residenceAllotmentStatus(self)
		buildingRoomStatus(self)
		currentResidenceApplicationStatus(self)
		currentResidenceAllotmentStatus(self)
		residenceUpdate(self)
	
	def on_cancel(self):
		allottmentstatusCancel(self)
		allottmentCancelled(self)
		allottmentCancelledRoom(self)
	
# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")

# To validate every employee is alloted only one quarter
def duplicateResidenceAllot(self):
	data=frappe.get_all("Residence Allotment",[["employee_name","=",self.employee_name],['current_employee_allotment_status',"=","Alloted"],['docstatus',"=",1]])
	if data:
		frappe.throw("Employee can't be allotted multiple residences")

############ alternate code written in js but still required for date validation ###########
# To validate if the start date is not after the end date in allotable room type
def dateValidate(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")

# To get the doc series name in a field
def allotmentNumberField(self):
	self.db_set("residence_allotment_number", self.name)

# To change employee allotment status in "Residence Allotment"
def residenceAllotmentStatus(self):
	if self.approval_status=="Approved":
		frappe.db.set_value("Residence Allotment", self.name, "employee_allotment_status", "Alloted")
		frappe.db.set_value("Residence Allotment", self.name, "vacancy_status", "Not Vacant")

# To change employee allotment status and vacancy status in "Building Room"
def buildingRoomStatus(self):
	if self.approval_status=="Approved":
		frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Alloted")
		frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Not Vacant")

# To set value of current Application status
def currentResidenceApplicationStatus(self):
	if self.approval_status=="Approved":
		frappe.db.set_value("Application for Residence", self.application_number, "current_application_status", "Alloted")
	elif self.approval_status=="Pending for Approval":
		frappe.db.set_value("Application for Residence", self.application_number, "current_application_status", "Pending for Approval")
	elif self.approval_status=="Rejected":
		frappe.db.set_value("Application for Residence", self.application_number, "current_application_status", "Rejected")

# To set value of current employee allotment status and current vacancy status in "Residence allotment"
def currentResidenceAllotmentStatus(self):
	if self.approval_status=="Approved":
		self.db_set("current_employee_allotment_status", "Alloted")
		self.db_set("current_vacancy_status", "Not Vacant")

# To set value of allotment details in "Residence Allotted" child table in "Employee" doctype
def residenceUpdate(self):
	if self.current_employee_allotment_status=="Alloted":
		allotmentData=frappe.get_doc('Employee', self.employee_id)
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
			"current_employee_allotment_status":self.current_employee_allotment_status,
			"date":self.last_update_date
		})
		allotmentData.save()

def allottmentstatusCancel(self):
	frappe.db.set_value("Residence Allotment",self.name,"current_employee_allotment_status", "Not Alloted")
	frappe.db.set_value("Residence Allotment",self.name,"current_vacancy_status", "Vacant")

def allottmentCancelled(self):
	frappe.db.set_value("Application for Residence",self.application_number,"current_application_status", "Allottment Cancelled")

def allottmentCancelledRoom(self):
	frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Not Alloted")
	frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Vacant")