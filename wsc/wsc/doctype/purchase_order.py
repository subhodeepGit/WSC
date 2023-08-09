import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import all_items_received

def validate(self,method):
	if self.qty == self.received_qty:
		all_items_received(self)