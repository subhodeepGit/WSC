import frappe

def validate(doc,method):
    if doc.amount:
        if len(str(doc.amount))>12 :
            frappe.throw("Amount is too high")
        