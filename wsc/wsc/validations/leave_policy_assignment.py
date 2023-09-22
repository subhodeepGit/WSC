import frappe
def validate(doc,method):
    if doc.effective_from>doc.effective_to:
        frappe.throw("Effective from should not be after than Effective to")