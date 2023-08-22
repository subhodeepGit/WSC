import frappe

def validate(doc,method):
    if doc.new_leaves_allocated:
        if doc.new_leaves_allocated<0:
            frappe.throw("Allocated leaves should not be Negative")