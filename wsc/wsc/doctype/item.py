import frappe

def validate(doc, method):
    validate_rates(doc)

def validate_rates(doc):
    if doc.valuation_rate < 0:
        frappe.throw("<B>Valuation rate</B> cannot be less than negative")
    if doc.standard_rate < 0:
        frappe.throw("<B>Standard rate</B> cannot be less than negative")
