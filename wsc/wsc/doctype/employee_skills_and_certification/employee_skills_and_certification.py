# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeSkillsandCertification(Document):

	def on_submit(self):
		employee = frappe.get_doc("Employee", self.employee)
		print(employee)
		employee.skills = []
		for row in self.skill_sets:
			child_row = employee.append("skills", {})
			child_row.skill_name = row.skill_name
			child_row.from_date = row.from_date
			child_row.to_date=row.to_date
			child_row.duration=row.duration
			child_row.description= row.description
			child_row.documentif_any= row.documentif_any

		employee.certifications = []
		for row in self.professional_certification:	
			child_row = employee.append("certifications", {})
			child_row.certificate_name = row.certificate_name
			child_row.duration = row.duration
			child_row.from_date=row.from_date
			child_row.to_date=row.to_date
			child_row.certification_authority= row.certification_authority
			child_row.place= row.place
			child_row.document= row.document
		frappe.msgprint("Updated")
		employee.save()


@frappe.whitelist()
def get_skill(employee):
	data = frappe.get_all("Skill Set",{"parent":employee},["skill_name","from_date","to_date","duration","description","documentif_any"])
	if data :
   
		return data

@frappe.whitelist()
def get_certification(employee):
	data = frappe.get_all("Certifications",{"parent":employee},["certificate_name","from_date","to_date","duration","certification_authority","place","document"])
	if data :
   
		return data