# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PsychometricTest(Document):
	pass


@frappe.whitelist()
def get_competencies():
	data = frappe.get_all("Importance of Competencies",["competencies"])
	print("\n\n\n\n\n\nCompetencies")
	print(data)
	return data

@frappe.whitelist()
def get_skills():
	data = frappe.get_all("Psychometric skills",["skills"])
	print("\n\n\n\n\nSkills")
	print(data)
	return data


