# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceAllotment(Document):
	def validate(self):
		dateValidate(self)
		vacancyChange(self)
		# duplicate(self)
		
# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")

# To change vacancy status to "Not Vacant" after allotment of residence
def vacancyChange(self):
	frappe.db.set_value("Building Room",self.residence_serial_number,"vacancy_status","Not Vacant")

# def duplicate(self):
# 	data=frappe.get_all("Residence Allotment",{"employee_name":self.employee_name,})
# 	if data:
# 		frappe.throw("Employee cant be allotted multiple residences within the same time period")












