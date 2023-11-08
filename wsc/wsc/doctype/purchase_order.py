import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import all_items_received

def validate(self,method):
	if self.status == "To Bill" or self.status == "Completed":
		all_items_received(self)

	if self.additional_discount_percentage:
		if self.additional_discount_percentage <0:
			frappe.throw("Total Discount Percentage cannnot be negative")

	if self.discount_amount:
		if self.discount_amount <0:
			frappe.throw("Discount Amount cannnot be negative")

	for cd in self.items:
		if cd.price_list_rate < 0:
			frappe.throw("Price List Rate for Item cannot be negative")

	for cd in self.items:
		if cd.discount_percentage < 0:
			frappe.throw("Discount Percentage for Item cannot be negative")
	
	for cd in self.items:
		if cd.discount_amount < 0:
			frappe.throw("Discount Amount for Item cannot be negative")

	for cd in self.items:
		if cd.rate < 0:
			frappe.throw("Rate for Item cannot be negative")

	for cd in self.items:
		if cd.margin_rate_or_amount < 0:
			frappe.throw("Margin Rate for Item cannot be negative")

	for cd in self.items:
		if cd.rate_with_margin < 0:
			frappe.throw("Rate with margin for Item cannot be negative")
