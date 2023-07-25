# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaterialDistributionMaster(Document):
	def validate(self):
		self.validateStartEndDate()
		self.validateExistingRecordWithStartEndDate()

	def validateStartEndDate(self):
		if self.start_date and self.end_date and self.end_date <= self.start_date:
			frappe.throw("End date must be greater than the start date.")

	def validateExistingRecordWithStartEndDate(self):
		if self.start_date and self.end_date:
			existing_records = frappe.get_all(
                "Material Distribution Master",
                filters={
                    "name": ["!=", self.name],
                    "start_date": ["<=", self.end_date],
                    "end_date": [">=", self.start_date],
                },
                fields=["name"],
            )            
			if existing_records:
				frappe.throw("A record already exists within the selected date range.")
                

