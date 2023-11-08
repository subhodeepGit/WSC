import frappe

def validate(doc,method):
    if doc.incentive_amount:
        if doc.incentive_amount<0:
            frappe.throw("Incentive Amount Should not be less than 0")
            
        if len(str(doc.incentive_amount))>12:
            frappe.throw("Incentive amount is too high .")

