# Copyright (c) 2024, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApprovalLevel(Document):
	def validate(self):
		doc=frappe.new_doc("Role")
		doc.role_name=self.name
		doc.search_bar=0
		doc.notifications=0
		doc.list_sidebar=0
		doc.bulk_actions=0
		doc.view_switcher=0
		doc.form_sidebar=0
		doc.save()

	def on_trash(self):
		doc=frappe.get_doc("Role",self.name)
		doc.delete()

