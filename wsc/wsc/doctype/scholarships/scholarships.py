# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document

class Scholarships(Document):
	def validate(self):
		start_date=self.start_date
		end_date=self.end_date

		if start_date>end_date:
			frappe.throw("Start date can't be smaller then end date")



