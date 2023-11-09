import frappe

def validate(self, method):
        for cd in self.items:
           if cd.qty:
            if cd.qty <= 0:
                frappe.throw("Quantity cannot be equal or less than 0")