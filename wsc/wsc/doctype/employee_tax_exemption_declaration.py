import frappe

def validate(doc, method):
    if doc.total_declared_amount:
        if doc.total_declared_amount < 0:
            frappe.throw("Declared Amount can not be less than 0.")
        if len(str(doc.total_declared_amount)) > 12:
            frappe.throw("Declared Amount is too high.")
    if doc.monthly_house_rent:
        if doc.monthly_house_rent < 0:
            frappe.throw("Monthly House Rent can not be less than 0.")
        if len(str(doc.monthly_house_rent)) > 12:
            frappe.throw("Monthly House Rent is too high.")