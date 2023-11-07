import frappe

def validate(doc,method):
    if doc.tax_exemption_proofs:
        for i in doc.tax_exemption_proofs:
            if i.amount<0:
                frappe.throw("Amount Should not be less than 0")
            if len(str(i.amount))>12 :
                frappe.thorw("Amount is too High")
    if doc.house_rent_payment_amount:
        if doc.house_rent_apyment_amount<0:
            frappe.throw("House Rent Payment Amount should not be less than 0")
        if len(str(doc.house_rent_payment_amount))>12:
            frappe.throw("House Rent Payment Amount is too high")
