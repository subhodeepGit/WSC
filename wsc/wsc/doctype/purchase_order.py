import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import all_items_received

def validate(self,method):
	if self.status == "To Bill" or self.status == "Completed":
		all_items_received(self)