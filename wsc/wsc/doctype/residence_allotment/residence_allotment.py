# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceAllotment(Document):
	def validate(self):
		dateValidate(self)
		vacancyChange(self)
		duplicateResidenceAllot(self)
		dateValidate(self)
	
	def on_submit(self):
		allotmentStatusAllot(self)
		allotmentStatusRoom(self)
		
# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")

# To change vacancy status to "Not Vacant" after allotment of residence
def vacancyChange(self):
	frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Not Vacant")

# To validate every employee is alloted only one quarter
def duplicateResidenceAllot(self):
	data=frappe.get_all("Residence Allotment",[["employee_name","=",self.employee_name],['employee_allotment_status',"=","Alloted"],['docstatus',"=",1]])
	if data:
		frappe.throw("Employee can't be allotted multiple residences")

############ alternate code written in js but still required for date validation ###########
# To validate if the start date is not after the end date in allotable room type
def dateValidate(self):
	if self.allotment_status == "Allottable":
		if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")
	else:
		pass

# To change employee allotment status to "Alloted" after allotment of residence
def allotmentStatusAllot(self):
	frappe.db.set_value("Residence Allotment", self.name, "employee_allotment_status", "Alloted")

# To change employee allotment status to "Alloted" after allotment of building room
def allotmentStatusRoom(self):
	frappe.db.set_value("Building Room", self.residence_serial_number, "employee_allotment_status", "Alloted")




















