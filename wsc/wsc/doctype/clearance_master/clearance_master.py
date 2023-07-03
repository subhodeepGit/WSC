# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ClearanceMaster(Document):
	def validate(self):
		self.get_list()

	def get_list(self):
		doc = frappe.db.get_list('Clearance Master',
			   filters={
				'academic_year':self.academic_year,
				'academic_term':self.academic_term,
				'name': ("!=",self.name) if self.name else None
				},
				fields=['name']
				)
		if doc:
			frappe.throw((f"List with Academic Year({self.academic_year}) and Academic Term({self.academic_term}) already Exist"))