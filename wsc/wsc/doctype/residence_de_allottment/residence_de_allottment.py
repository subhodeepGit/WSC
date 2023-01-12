# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceDeAllottment(Document):
	def validate(self):
		vacancyChange(self)

# To change vacancy status and employee allotment status to "Vacant" and "Not Alloted" after allotment of residence
def vacancyChange(self):
	frappe.db.set_value("Building Room",self.allotted_residence_serial_number,"vacancy_status","Vacant", "employee_allotment_status", "Not Alloted")
