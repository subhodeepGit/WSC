# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class QuarterDeAllottment(Document):
	def validate(self):
		vacancyChange(self)

def vacancyChange(self):
	frappe.db.set_value("Building Room",self.allotted_residence_serial_number,"vacancy_status","Vacant")
	frappe.db.set_value("Building Room",self.allotted_residence_serial_number,"employee_allotment_status", "Not Alloted")
