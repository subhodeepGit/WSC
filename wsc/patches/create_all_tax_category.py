import frappe
from frappe.utils import now

def execute():
	existing_tax_categories = frappe.get_value("Tax Category",{"name":"All Tax Category"})
	if not existing_tax_categories:
				new_tax_category = {
					"doctype": "Tax Category",
					"title": "All Tax Category",
					"is_group":1,
					"creation": now(),
					"modified": now(),
				}
				frappe.get_doc(new_tax_category).insert()