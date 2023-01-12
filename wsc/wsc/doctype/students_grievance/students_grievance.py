# Copyright (c) 2022, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StudentsGrievance(Document):
	def on_submit(self):
		if self.status not in ["Invalid", "Resolved"]:
			frappe.throw(
				_("Only Employee Grievance with status {0} or {1} can be submitted").format(
					bold("Invalid"), bold("Resolved")
				)
			)
