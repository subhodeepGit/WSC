import frappe

def on_change(doc,method):
    print("\n\n\n\n")
    print("Hellllllloooo")
    if doc.start_date>doc.end_date:
        frappe.throw("Start Date cannot be greater than End Date")