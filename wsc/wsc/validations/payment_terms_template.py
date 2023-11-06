import frappe

def validate(self, method):
        for cd in self.terms:
           if cd.discount <= 0:
               frappe.throw("Discount cannot be equal or less than 0")

        for cd in self.terms:
           if cd.discount_validity <= 0:
               frappe.throw("Discount Validity cannot be equal or less than 0")