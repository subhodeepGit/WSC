import frappe

def validate(self, doc):
    if self.actual_start_date > self.actual_end_date:
        frappe.throw("Start Date cannot be greater than Actual date")