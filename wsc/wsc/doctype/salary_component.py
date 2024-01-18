import frappe

def validate(doc, method):
    if doc.max_benefit_amount:
        if len(str(doc.max_benefit_amount)) > 12:
            frappe.throw("Maximum Benefit Amount is too high.")
        if doc.max_benefit_amount < 0:
            frappe.throw("Maximum Benefit Amount can not be less than 0.")