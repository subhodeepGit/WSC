import frappe

def validate(doc,method):
    for t in doc.get("intervals"):
        if 0 <= t.threshold <= 100:
            pass
        else:
           frappe.throw("Threshold value should be in between 0% to 100%")  