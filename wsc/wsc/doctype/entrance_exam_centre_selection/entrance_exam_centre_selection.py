# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EntranceExamCentreSelection(Document):
	def validate(self):
		self.validate_duplicate_record()

	def validate_duplicate_record(self):
		if self.academic_year and self.academic_term:
			for a in frappe.get_all('Entrance Exam Centre Selection', {'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
				if a.name and a.name != self.name:
					frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
		

