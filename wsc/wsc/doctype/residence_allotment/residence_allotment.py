# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import datetime

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
		currentResidenceDetails(self)
	
	def on_cancel(self):
		allottmentstatusCancel(self)
		allottmentCancelled(self)
		allottmentCancelledRoom(self)
		currentResidenceCancelUpdate(self)
		residenceCancelUpdate(self)
	

############ alternate code written in js but still required for date validation ###########
# To validate if the start date is not after the end date
def dateValidate(self):
	if self.current_start_date > self.current_end_date:
		frappe.throw("Start date cannot be greater than End date")

# To validate every employee is alloted only one quarter
def duplicateResidenceAllot(self):
	data=frappe.get_all("Residence Allotment",[["employee_name","=",self.employee_name],['current_employee_allotment_status',"=","Alloted"],['docstatus',"=",1]])
	if data:
		frappe.throw("Employee can't be allotted multiple residences")

# To get the doc series name in a field
def allotmentNumberField(self):
	self.db_set("residence_allotment_number", self.name)

# To change employee allotment status in "Residence Allotment"
def residenceAllotmentStatus(self):
	if self.approval_status=="Approved":
		frappe.db.set_value("Residence Allotment", self.name, "employee_allotment_status", "Alloted")
		frappe.db.set_value("Residence Allotment", self.name, "vacancy_status", "Not Vacant")
		frappe.db.set_value("Residence Allotment", self.name, "current_application_status", "Alloted")

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
		allotmentData.set("table_109",[])
		allotmentData.append("table_109",{
			"residence_allotment_number":self.residence_allotment_number,
			"application_number":self.application_number,
			"residence_type":self.residence_type,
			"residence_type_name":self.residence_type_name,
			"residence_serial_number":self.residence_serial_number,
			"residence_number":self.residence_number,
			"floor":self.floor,
			"building_address":self.building_address,
			"unit_area_sq_m":self.unit_area_sq_m,
			"parking_available":self.parking_available,
			"parking_type":self.parking_type,
			"parking_area_sq_m":self.parking_area_sq_m,
			"parking_vehicle":self.parking_vehicle,
			"current_employee_allotment_status":self.current_employee_allotment_status,
			"date":datetime.date.today(),
			"start_date":self.current_start_date,
			"end_date":self.current_end_date
		})
		allotmentData.save()

# To update the "Pending for Approval" status in "Residence Allotment History" child table in Employee doctype
	if self.approval_status=="Pending for Approval":	
		allotmentData=frappe.get_doc('Employee', self.employee_id)
		allotmentData.append("residence_allotment_history_table",{
			"residence_allotment_number":self.residence_allotment_number,
			"application_number":self.application_number,
			"residence_type":self.type_of_residence_requested,
			"residence_type_name":self.type_of_residence_name_requested,
			"status":"Pending for Approval",
			"date":datetime.date.today()
		})
		allotmentData.save()
		frappe.db.delete("Residence Allotment", self.name)

# To update the value of Allotment status and vacancy status field in Residence Allotment screen
def allottmentstatusCancel(self):
	if self.current_employee_allotment_status=="Alloted":
		self.db_set("Residence Allotment",self.name,"current_employee_allotment_status", "Not Alloted")
		self.db_set("Residence Allotment",self.name,"current_vacancy_status", "Vacant")
		self.db_set("Residence Allotment",self.name,"current_application_status", "Allottment Cancelled")

# To update value of current application status in Application for Residence screen on cancellation of allotment
def allottmentCancelled(self):
	if self.current_employee_allotment_status=="Alloted":
		frappe.db.set_value("Application for Residence",self.application_number,"current_application_status", "Allottment Cancelled")


# To update the value of Allotment status and vacancy status field in "Building Room" on Cancel
def allottmentCancelledRoom(self):
	if self.current_employee_allotment_status=="Alloted":
		frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Not Alloted")
		frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Vacant")

# To clear all residence details after Allotment cancellation in "Residence Allotment Details" child table in Employee doctype
def currentResidenceCancelUpdate(self):
	if self.current_employee_allotment_status=="Alloted":
		frappe.db.delete("Residence Allotted", {"parent":self.employee_id})

def residenceCancelUpdate(self):
	if self.current_employee_allotment_status=="Alloted":
		allotmentData=frappe.get_doc('Employee', self.employee_id)
		allotmentData.append("residence_allotment_history_table",{
			"residence_allotment_number":self.residence_allotment_number,
			"application_number":self.application_number,
			"residence_type":self.changed_residence_type,
			"residence_type_name":self.changed_residence_type_name,
			"residence_serial_number":self.changed_residence_serial_number,
			"residence_number":self.changed_residence_number,
			"floor":self.floor,
			"building_address":self.building_address,
			"unit_area_sq_m":self.unit_area_sq_m,
			"parking_available":self.parking_available,
			"parking_type":self.parking_type,
			"parking_area_sq_m":self.parking_area_sq_m,
			"parking_vehicle":self.parking_vehicle,
			"status":"Allottment Cancelled",
			"date":datetime.date.today()
		})
		allotmentData.save()


# To initialize current residence details as per the initial allotment details
def currentResidenceDetails(self):
	self.db_set("changed_residence_serial_number", self.residence_serial_number)
	self.db_set("changed_residence_number", self.residence_number)
	self.db_set("changed_building_name", self.building)
	self.db_set("changed_residence_type", self.residence_type)
	self.db_set("changed_residence_type_name", self.residence_type_name)

@frappe.whitelist()
def residence_allotments(application_number,employee_name,employee_id,employee_email,designation,department,type_of_residence_requested,type_of_residence_name_requested):
	ra = frappe.new_doc("Residence Allotment")
	ra.application_number = application_number
	ra.employee_name = employee_name
	ra.employee_id= employee_id
	ra.employee_email=employee_email
	ra.employee_designation=designation
	ra.employee_department=department
	ra.type_of_residence_requested=type_of_residence_requested
	ra.type_of_residence_name_requested=type_of_residence_name_requested
	return ra