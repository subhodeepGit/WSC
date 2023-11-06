import frappe

def validate(self, method):
    if self.additional_discount_percentage:
        if self.additional_discount_percentage <0:
            frappe.throw("Total Discount Percentage cannnot be negative")

    if self.discount_amount:
         if self.discount_amount <0:
            frappe.throw("Discount Amount cannnot be negative")

    for cd in self.items:
           if cd.discount_percentage < 0:
               frappe.throw("Discount Percentage for Item cannot be negative")
    
    for cd in self.items:
           if cd.discount_amount < 0:
               frappe.throw("Discount Amount for Item cannot be negative")
    
    for cd in self.items:
           if cd.rate < 0:
               frappe.throw("Rate for Item cannot be negative")

    for cd in self.taxes:
        if cd.rate < 0: 
            frappe.throw("Rate of Tax for Item cannot be negative")