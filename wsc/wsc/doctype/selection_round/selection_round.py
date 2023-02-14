# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class SelectionRound(Document):
	pass

@frappe.whitelist()
def update_profile(self):
	profile = frappe.get_doc('Student', self.student_no)
	profile.append('companies_applied_to',{
		'company_name' : self.company_name,
		'current_round' : self.round_of_placement,
		'status':'Passed'
	})
	profile.save()
	return 'echo'