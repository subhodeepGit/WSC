# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeAppraisalCycle(Document):
	def validate(self):
		if self.from_date and self.to_date:
			if self.from_date>self.to_date:
				frappe.throw("From date should precede to date.")
		if self.to_date and self.notify_employee_after:
			if self.notify_employee_after>self.to_date or self.notify_employee_after<self.from_date:
				frappe.throw("Notification sending date must fall within the chosen date range.")
	
	

