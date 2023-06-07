# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class FeesWaiver(Document):
	def validate(self):
		existing_data=frappe.get_all("Fees Waiver",filters={"student":self.student,"fee_type":self.fee_type,"programs":self.programs,"semester":self.semester,"academic_year":self.academic_year,"academic_term":self.academic_term,"docstatus":1},fields=["name"])
		print(existing_data)
		if existing_data:
			frappe.throw(_("Fees Waiver already exists {0}").format(frappe.bold(existing_data[0]["name"])))
