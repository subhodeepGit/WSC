import frappe

def validate(doc,method):
    if doc.amount:
        if doc.amount<0:
            frappe.throw("Amount could not be less than 0")
        if len(str(doc.amount))>12:
            frappe.throw("Amount is too high")