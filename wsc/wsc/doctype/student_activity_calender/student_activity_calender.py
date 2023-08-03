# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class StudentActivityCalender(Document):
	def validate(self):
		self.date_validation()
		self.calculate_duration()

	def date_validation(self):
		if len(self.activities) > 0:
			for aet in self.get("activities"):
				if aet.end_date and aet.start_date and aet.end_date < aet.start_date:
					frappe.throw("End Date Must Be Greater Than Start Date in <b>Activities</b> table")

	def calculate_duration(self):
		for events in self.get("activities"):
			events.duration=(date_diff(events.end_date,events.start_date)+1)
