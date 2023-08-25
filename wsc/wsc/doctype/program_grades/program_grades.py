# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProgramGrades(Document):
	def validate(self):
		course=frappe.get_all("Programs",{"program_grade":self.name},['name'])
		for t in course:
			semester=frappe.get_all("Program",{"programs":t['name']},['name'])
			for j in semester:
				doc=frappe.get_doc("Program",j['name'])
				doc.is_short_term_course=self.is_short_term_course
				doc.save()

