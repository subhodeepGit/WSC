# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeAppraisalPortal(Document):
	def validate(self):
		self.check_existing_record()

	def check_existing_record(self):
		existing_record = frappe.get_value("Employee Appraisal Portal",
									 filters={"employee":self.employee,"appraisal_year":self.appraisal_year,"appraisal_cycle":self.appraisal_cycle},
									 fieldname= "name")
		if existing_record and existing_record!= self.name:
			frappe.throw(
            "Employee has already applied for appraisal for the same year and cycle. Duplicate entries are not allowed."
        )



@frappe.whitelist()
def get_appraisal_cycle(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.get_all("Employee Appraisal Cycle",{"year":filters.get("appraisal_year")},["name"],as_list=1)
	if data :
		# print("\n\n\n\n\n\nEmployee Education Details")
		# print(data)
		return data
	else :
		pass

@frappe.whitelist()
def get_goals(appraisal_template):
	data =frappe.get_all("Key Work Goals",{'parent':appraisal_template},["goal","category","due_date","status"])
	# print(data)
	return data

@frappe.whitelist()
def get_dimenssions():
	data = frappe.get_all("Dimenssions for Appraisal",{"is_active":1},["name","description"])
	if data :
		print(data)
		return data
	else :
		pass
@frappe.whitelist()
def get_mid_year_grade(employee,appraisal_year):
	data = frappe.get_all("Employee Appraisal Portal",{"employee":employee,"appraisal_year":appraisal_year,"appraisal_round":'1'},["final_grade"])
	print(data)
	if data :
		print("\n\n\n\n")
		print(data)
		return data[0]
	else :
		pass