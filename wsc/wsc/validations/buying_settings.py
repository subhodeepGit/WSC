import frappe

def validate(doc, method):
    if doc.over_order_allowance:
        if doc.over_order_allowance <=0:
            frappe.throw("<b>Over Order Allowance</b> cannot be negative or zero")

    if doc.over_transfer_allowance:
        if doc.over_transfer_allowance <=0:
            frappe.throw("<b>Over Transfer Allowance</b> cannot be negative or zero")