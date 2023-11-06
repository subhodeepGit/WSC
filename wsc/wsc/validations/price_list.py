import frappe
from frappe import _
from frappe.model.document import Document

def validate(self, method):
        if self.buying == 0:
            frappe.throw("Please Click Buying in the checkbox")