import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import purchase_requisition_raised

def validate(self,method):
	if self.workflow_state == "Approved by Director":
		purchase_requisition_raised(self)

