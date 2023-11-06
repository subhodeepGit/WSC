import frappe

def validate(self, doc):
    if self.fg_completed_qty:
        if self.fg_completed_qty <= 0:
            frappe.throw("Finished Good Quantity cannot be negative Zero")

    if self.process_loss_percentage:
        if self.process_loss_percentage <= 0:
            frappe.throw("% Process Loss cannot be negative Zero")

    if self.process_loss_qty:
        if self.process_loss_qty <= 0:
            frappe.throw("Process Loss Quantity cannot be negative Zero")