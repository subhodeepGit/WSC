import frappe

def validate(doc,method):
    if doc.max_leaves_allowed:
        if doc.max_leaves_allowed<0 :
            frappe.throw("Max Leaves Allowed should not be Negative")
    if doc.applicable_after:
        if doc.applicable_after<0:
            frappe.throw("Applicable after should not be Negative")
    if doc.max_continuous_days_allowed:
        if doc.max_continuous_days_allowed<0:
            frappe.throw("Max consecutive leaves should not be Negative")