import frappe

def validate(doc, method):
    validate_rates(doc)

def validate_rates(doc):
    if doc.valuation_rate:
        if doc.valuation_rate < 0:
            frappe.throw("<B>Valuation rate</B> cannot be negative")
    if doc.standard_rate:
        if doc.standard_rate < 0:
            frappe.throw("<B>Standard rate</B> cannot be negative")
    if doc.shelf_life_in_days:
        if doc.shelf_life_in_days < 0:
            frappe.throw("<B>Shelf Life</B> cannot be negative")

    if doc.warranty_period:
        int_warranty_period = int(doc.warranty_period)
        if int_warranty_period <= 0:
            frappe.throw("<B>Warranty Period</B> cannot be negative or Zero")
    if doc.weight_per_unit: 
        if doc.weight_per_unit < 0:
            frappe.throw("<B>Weight Per Unit</B> cannot be negative")
    if doc.min_order_qty: 
        if doc.min_order_qty < 0:
            frappe.throw("<B>Minimum order quantity</B> cannot be negative")
    if doc.safety_stock: 
        if doc.safety_stock < 0:
            frappe.throw("<B>Safety Stock</B> cannot be negative")
