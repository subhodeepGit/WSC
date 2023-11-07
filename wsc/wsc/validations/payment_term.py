import frappe

def validate(self, method):
    if self.invoice_portion:
        if self.invoice_portion <=0:
            frappe.throw("Invoice Portion cannot be negative or zero")

    if self.credit_days:
        if self.credit_days <=0:
            frappe.throw("Credit Days cannot be negative or zero")

    if self.credit_months:
        if self.credit_months <=0:
            frappe.throw("Credit Months cannot be negative or zero")

    if self.discount:
        if self.discount <=0:
            frappe.throw("Discount cannot be negative or zero")

    if self.discount_validity:
        if self.discount_validity <=0:
            frappe.throw("Discount Validity cannot be negative or zero")