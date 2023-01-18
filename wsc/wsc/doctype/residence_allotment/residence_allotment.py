# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceAllotment(Document):
	def validate(self):
		dateValidate(self)
		duplicateResidenceAllot(self)
		dateValidate(self)
		deletedoc(self)
	
	def on_submit(self):
		residenceAllotmentStatus(self)
		buildingRoomStatus(self)
		currentResidenceApplicationStatus(self)
		currentResidenceAllotmentStatus(self)
		
# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")

# To validate every employee is alloted only one quarter
def duplicateResidenceAllot(self):
	data=frappe.get_all("Residence Allotment",[["employee_name","=",self.employee_name],['employee_allotment_status',"=","Alloted"],['docstatus',"=",1]])
	if data:
		frappe.throw("Employee can't be allotted multiple residences")

############ alternate code written in js but still required for date validation ###########
# To validate if the start date is not after the end date in allotable room type
def dateValidate(self):
	if self.start_date > self.end_date:
		frappe.throw("Start date cannot be greater than End date")

def deletedoc(self):
	if self.approval_status=="Pending for Approval":
		frappe.delete_doc('Residence Allotment', self.name)
	elif self.approval_status=="Rejected":
		frappe.delete_doc('Residence Allotment', self.name)

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
		frappe.db.set_value("Residence Allotment",self.application_number,"current_vacancy_status", "Not Vacant")
		frappe.db.set_value("Residence Allotment",self.application_number,"current_employee_allotment_status", "Alloted")

		
	























