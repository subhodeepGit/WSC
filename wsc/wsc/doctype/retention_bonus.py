import frappe

def validate(doc,method):
    if doc.bonus_amount:
        if doc.bonus_amount<0:
            frappe.throw("Bonus Amount Could not be Less Than 0")

        if len(str(doc.bonus_amount))>12:
            frappe.throw("Bonus Amount is too high")