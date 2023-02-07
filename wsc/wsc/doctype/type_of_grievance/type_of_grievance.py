# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TypeofGrievance(Document):
	def validate(self):
		data=frappe.get_all("Type of Grievance",{"type_of_grievance":self.type_of_grievance,"areas_of_grivence":self.areas_of_grivence,"enable":1})
		if data:
			frappe.throw("Already Workflow for the Grivance is defined")

