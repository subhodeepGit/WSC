import frappe

def validate(doc,method):
    if doc.claimed_amount:
        if doc.claimed_amount<0 :
            frappe.throw("Claimed Amount should not be less than 0")
