import frappe
import re

def validate(self, method):
    for cd in self.items:
        if cd.qty:
            if cd.qty <= 0:
                frappe.throw("Quantity cannot be equal or less than 0")

def email_validate(self):
    for cd in self.suppliers:
            if cd.email_id:
                if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.email_id):
                    frappe.throw("<b>{0}</b> is invalid email address. Please enter a valid email address.".format(self.email_id))
        