# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from wsc.wsc.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
class EmployeeSkillsandCertification(Document):

	def on_submit(self):
		employee = frappe.get_doc("Employee", self.employee)
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
		employee.save()
		frappe.msgprint("Updated")

	def on_change(doc):
		if doc.reporting_authority_id:
			for emp in frappe.get_all("Employee", {'reporting_authority_email':doc.reporting_authority_id}, ['reporting_authority_email']):
				if emp.reporting_authority_email:
					add_user_permission(doc.doctype,doc.name,emp.reporting_authority_email,doc)
				else:
					frappe.msgprint("Reporting Authority Not Found")


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


@frappe.whitelist()
def is_verified_user(docname):

	doc = frappe.get_doc("Employee Skills and Certification",docname)
	
	reporting_auth_id = doc.reporting_authority_id
	roles = frappe.get_roles(frappe.session.user)
	if "HR Admin" in roles or "Department Head" in roles or "HR Manager/CS Officer" in roles or "Administrator" in roles or "Admin" in roles:
		return True
	if doc.workflow_state == "Draft": 
		return True	
	if doc.workflow_state == "Sent For Approval" and frappe.session.user ==reporting_auth_id :
		return True
	# if doc.workflow_state == "Pending Approval From HR" and frappe.session.user ==reporting_auth_id :
	# 	return True
	else :
		return False
