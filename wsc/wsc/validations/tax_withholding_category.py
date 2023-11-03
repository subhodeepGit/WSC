import frappe

def validate(doc):
    for cd in doc.rates:
           if cd.from_date >= cd.to_date:
               frappe.throw("End Date <b>'{0}'</b> Must Be Greater Than Start Date <b>'{1}'</b>".format(doc.to_date, doc.from_date))