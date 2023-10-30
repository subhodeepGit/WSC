# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitmentExamCenter(Document):
	def validate(self):
		my_field = self.get("total_seating_capacity")  
		if not my_field.isdigit():
			frappe.throw("Field must contain only digits.")	
		my_field = self.get("total_seating_capacity") 

		my_field_value = int(my_field) if my_field is not None else None

		if my_field_value is not None and my_field_value <= 0:
			frappe.throw("Field cannot accept 0 or negative values.")

		pincode = self.get("pincode")  
		if not pincode.isdigit():
			frappe.throw("Pin code Field must contain only digits.")	

		pincode = self.get("pincode") 

		pincode_value = int(my_field) if pincode is not None else None

		if pincode_value is not None and pincode_value < 6:
			frappe.throw("Pincode value should not be less than 6")
