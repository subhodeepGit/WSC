import frappe

def validate(doc, method):
    for t in doc.accounts:
        if t.budget_amount<=0:
            frappe.throw("Budget Amount can't be -ve or Zero for the account <b>%s</b>"%(t.account))