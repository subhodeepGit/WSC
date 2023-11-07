import frappe

def validate(doc, method):
    if doc.expiry_date and  doc.manufacturing_date and doc.expiry_date < doc.manufacturing_date:
        frappe.throw("Expiry Date <b>'{0}'</b> Must Be Greater Than Manufacturing Date <b>'{1}'</b>".format(doc.expiry_date, doc.manufacturing_date))