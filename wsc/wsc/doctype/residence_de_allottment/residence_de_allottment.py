# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ResidenceDeAllottment(Document):
	def validate(self):
		vacancyChange(self)

def vacancyChange(self):
	frappe.db.set_value("Residence Allotment",self.name,"vacancy_status","Vacant")
	frappe.db.set_value("Residence Allotment",self.name,"employee_allotment_status", "Not Alloted")
