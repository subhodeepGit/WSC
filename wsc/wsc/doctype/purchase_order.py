import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import all_items_received

def validate(self,method):
	if self.status == "To Bill" or self.status == "Completed":
		all_items_received(self)

	if self.additional_discount_percentage:
		if self.additional_discount_percentage:
			if self.additional_discount_percentage <0:
				frappe.throw("Total Discount Percentage cannnot be negative")

	if self.discount_amount:
		if self.discount_amount:
			if self.discount_amount <0:
				frappe.throw("Discount Amount cannnot be negative")

	for cd in self.items:
		if cd.price_list_rate:
			if cd.price_list_rate < 0:
				frappe.throw("Price List Rate for Item cannot be negative")

	for cd in self.items:
		if cd.discount_percentage:
			if cd.discount_percentage < 0:
				frappe.throw("Discount Percentage for Item cannot be negative")
	
	for cd in self.items:
		if cd.discount_amount:
			if cd.discount_amount < 0:
				frappe.throw("Discount Amount for Item cannot be negative")

	for cd in self.items:
		if cd.rate:
			if cd.rate < 0:
				frappe.throw("Rate for Item cannot be negative")

	for cd in self.items:
		if cd.margin_rate_or_amount:
			if cd.margin_rate_or_amount < 0:
				frappe.throw("Margin Rate for Item cannot be negative")

	for cd in self.items:
		if cd.rate_with_margin:
			if cd.rate_with_margin < 0:
				frappe.throw("Rate with margin for Item cannot be negative")

	for cd in self.taxes:
		if cd.rate:
			if cd.rate < 0:
				frappe.throw("Tax Rate cannot be negative")

	for cd in self.payment_schedule:
		if cd.invoice_portion:
			if cd.invoice_portion < 0:
				frappe.throw("Invoice Portion cannot be negative")

	for cd in self.payment_schedule:
		if cd.discount:
			if cd.discount < 0:
				frappe.throw("Discount cannot be negative")

	for cd in self.payment_schedule:
		if cd.payment_amount:
			if cd.payment_amount < 0:
				frappe.throw("Payment Amount cannot be negative")

	for cd in self.payment_schedule:
		if cd.base_payment_amount:
			if cd.base_payment_amount < 0:
				frappe.throw("Payment Amount cannot be negative")

	for cd in self.payment_schedule:
		if cd.paid_amount:
			if cd.paid_amount < 0:
				frappe.throw("Paid Amount cannot be negative")