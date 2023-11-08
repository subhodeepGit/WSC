import frappe
import datetime

def validate(doc, method):
    if doc.posting_date > str(datetime.datetime.now()):
        frappe.throw("Posting Date can not be greater than today.")
    if doc.start_date > doc.end_date:
        frappe.throw("From_Date can not be greater than To_Date.")