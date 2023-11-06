import frappe

def validate(doc, method):
    if doc.base and doc.variable:
        if doc.base < 0 or doc.variable < 0:
            frappe.throw("Base / Variable Amount can not be less than 0.")
        if len(str(doc.base)) > 12 or len(str(doc.variable)) > 12:
            frappe.throw("Base / Variable Amount is too high.")
