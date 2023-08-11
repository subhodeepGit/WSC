import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import purchase_requisition_raised, received_in_inventory, received_by_department

def validate(self,method):
    if self.workflow_state == "Approved by Director":
        purchase_requisition_raised(self)
    
    if self.status == "Received":
        received_in_inventory(self)

    if self.status == "Issued" or self.status == "Transferred":
        received_by_department(self)