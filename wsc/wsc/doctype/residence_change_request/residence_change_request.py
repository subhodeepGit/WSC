# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class ResidenceChangeRequest(Document):
	def validate(self):
		duplicate(self)
		changeRequestNumberField(self)
		changeRoomStatus(self)
		buildingStatusChange(self)
		changeNewRoomStatus(self)
		residenceUpdate(self)
		residenceChangerequestHistory(self)
		changedResidenceDetails(self)
		residenceChangeCancel(self)

def duplicate(self):
	if self.workflow_state == "Approved":
		data=frappe.get_all("Residence Change Request",[["employee_name","=",self.employee_name],['request_status',"=","Approved"]])
		if data:
			frappe.throw("Can't Apply again as Residence change request for this employee is Pending for Approval")

# To change vacancy status and employee allotment status of alloted residence
def changeRoomStatus(self):
	if self.request_status == "Approved":
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

# To update current residence details in Employee doctype
def residenceUpdate(self):
	if self.request_status== "Approved":
		
		allotmentData=frappe.get_doc('Employee', self.employee)
		allotmentData.set("table_109",[])
		allotmentData.append("table_109",{
			"residence_allotment_number":self.residence_allotment_number,
			"application_number":self.application_number,
			"residence_type":self.residence_type_requested,
			"residence_type_name":self.residence_type_name_requested,
			"residence_number":self.residence_number,
			"floor":self.floor,
			"building_address":self.building_address,
			"unit_area_sq_m":self.unit_area_sq_m,
			"parking_available":self.parking_available,
			"parking_type":self.parking_type,
			"parking_area_sq_m":self.parking_area_sq_m,
			"parking_vehicle":self.parking_vehicle,
			"current_employee_allotment_status" : "Alloted",
			"date":datetime.date.today(),
			"start_date":self.start_date,
			"end_date":self.end_date
			})
		allotmentData.save()

# To Insert the updated residence change request status details in "Residence Allotment History" child table in Employee doctype
def residenceChangerequestHistory(self):
	if self.request_status== "Pending Approval":
		allotmentData=frappe.get_doc('Employee', self.employee)
		allotmentData.append("residence_allotment_history_table",{
			"application_number":self.residence_change_request_number,
			"date":datetime.date.today(),
			"status": "Pending Approval- Change Request"
			})
		allotmentData.save()

	if self.request_status== "Approved":
		allotmentData=frappe.get_doc('Employee', self.employee)
		allotmentData.append("residence_allotment_history_table",{
			"residence_allotment_number":self.residence_allotment_number,
			"residence_type":self.alloted_residence_type,
			"residence_type_name":self.alloted_residence_type_name,
			"residence_serial_number":self.alloted_residence_number,
			"residence_number":self.alloted_residence_number,
			"building_name":self.alloted_building,
			"current_employee_allotment_status" : "Residence Changed",
			"date":datetime.date.today(),
			"start_date":self.alloted_residence_start_date,
			"end_date":self.start_date,
			"status":"Residence Changed"
			})
		allotmentData.save()	

	if self.request_status== "Rejected":
		allotmentData=frappe.get_doc('Employee', self.employee)
		allotmentData.append("residence_allotment_history_table",{
			"application_number":self.residence_change_request_number,
			"date":datetime.date.today(),
			"status": "Rejected- Change Request"
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
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_type",self.residence_type_requested)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_type_name",self.residence_type_name_requested)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"residence_change_status",self.request_status)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"floor",self.floor)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"building_address",self.building_address)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"buidings_land_address",self.buidings_land_address)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"description",self.description)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"unit_area_sq_m",self.unit_area_sq_m)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"residence_orientation",self.residence_orientation)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"lawngarden_available",self.lawngarden_available)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"lawngarden_area_sq_m",self.lawngarden_area_sq_m)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"roof_type",self.roof_type)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"parking_available",self.parking_available)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"parking_type",self.parking_type)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"parking_vehicle",self.parking_vehicle)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"parking_area_sq_m",self.parking_area_sq_m)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_start_date",self.start_date)
		frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"current_end_date",self.end_date)
		

# To restore the previous allotment of the employee if residence change request after approval is cancelled
def residenceChangeCancel(self):
	if self.request_status== "Cancelled":
		data=frappe.db.sql(''' SELECT employee_allotment_status
		FROM `tabBuilding Room`
		WHERE room_no= %s; ''',
		(self.alloted_residence_number),
		)
		if data=="Alloted":
			frappe.throw("The residence change request cant be cancelled, as the previously alloted residence is not vacant")
		else:
			self.db_set("residence_serial_number","")
			self.db_set("residence_number","")
			self.db_set("residence_building","")
			self.db_set("residence_type","")
			self.db_set("residence_type_name","")
			self.db_set("request_status","Cancelled")
			self.db_set("floor","")
			self.db_set("building_address","")
			self.db_set("buidings_land_address","")
			self.db_set("description","")
			self.db_set("unit_area_sq_m","")
			self.db_set("residence_orientation","")
			self.db_set("lawngarden_available","")
			self.db_set("lawngarden_area_sq_m","")
			self.db_set("roof_type","")
			self.db_set("parking_available","")
			self.db_set("parking_type","")
			self.db_set("parking_vehicle","")
			self.db_set("parking_area_sq_m","")

			allotmentData=frappe.get_doc('Employee', self.employee)
			allotmentData.set("table_109",[])
			allotmentData.append("table_109",{
				"residence_allotment_number":self.residence_allotment_number,
				"application_number":self.application_number,
				"residence_type_name":self.alloted_residence_type_name,
				"residence_serial_number":self.alloted_residence_serial_number,
				"residence_number":self.alloted_residence_number,
				"current_employee_allotment_status" : "Alloted",
				"start_date":datetime.date.today,
				"end_date":self.end_date,
				"date":datetime.date.today()
				})
			allotmentData.save()

			allotmentData=frappe.get_doc('Employee', self.employee)
			allotmentData.append("residence_allotment_history_table",{
				"residence_allotment_number":self.residence_allotment_number,
				"application_number":self.application_number,
				"residence_type_name":self.residence_type_name_requested,
				"residence_serial_number":self.residence_serial_number,
				"residence_number":self.residence_number,
				"building_name":self.residence_building,
				"status" : "Changed Residence Cancelled",
				"date":datetime.date.today(),
				"start_date":self.start_date,
				"end_date":datetime.date.today()
				})
			allotmentData.save()

			frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_serial_number",self.alloted_residence_serial_number)
			frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_number",self.alloted_residence_number)
			frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_building_name",self.alloted_building)
			frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_type",self.alloted_residence_type)
			frappe.db.set_value("Residence Allotment",self.residence_allotment_number,"changed_residence_type_name",self.alloted_residence_type_name)