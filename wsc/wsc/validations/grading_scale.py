import frappe

def validate(doc,method):
    for t in doc.get("intervals"):
        if t.threshold <0:
            frappe.throw("Threshold value can't be Negative")