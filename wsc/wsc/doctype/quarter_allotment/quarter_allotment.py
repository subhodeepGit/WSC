# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class QuarterAllotment(Document):
	def validate(self):
		dateValidate(self)

# To validate if the start date is not after the end date
def dateValidate(self):
	if self.start_date > self.end_date:
			frappe.throw("Start date cannot be greater than End date")

#To check for duplicate record for 
				