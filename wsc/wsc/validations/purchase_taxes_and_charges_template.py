import frappe

def validate(doc, method):
    validate_amount(doc)

def validate_amount(doc):
    for cd in doc.taxes:
        if cd.rate:
           if cd.rate <= 0:
               frappe.throw("Tax rate cannot be equal or less than 0")

    for cd in doc.taxes:
        if cd.tax_amount:
            if cd.tax_amount <= 0:
                frappe.throw("Amount cannot be equal or less than 0")