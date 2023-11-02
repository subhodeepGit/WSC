import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import changed_impaneled_price

def validate(self,method):
	if self.workflow_state == "Approved by CFO":
		changed_impaneled_price(self)
	
	if self.supllier_email is None:
		frappe.throw("Enter <b>Supplier email id</b> in <b>Supplier</b> Form")