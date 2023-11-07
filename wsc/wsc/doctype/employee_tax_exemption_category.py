import frappe

def validate(doc, method):
    if len(str(doc.max_amount)) > 12:
        frappe.throw("Maximum Exemption Amount is too high.")
    if doc.max_amount < 0:
        frappe.throw("Maximum Exemption Amount can not be less than 0.")