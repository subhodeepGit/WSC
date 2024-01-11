import frappe

def validate(doc, method):
    if not doc.__newname.isalpha():
        frappe.throw("Name should only contain alphabets.")
    if len(doc.__newname) > 20:
        frappe.throw("Name length should not be more than 20.")