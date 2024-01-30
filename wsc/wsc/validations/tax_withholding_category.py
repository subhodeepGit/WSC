import frappe

def validate(doc, method):
    for cd in doc.rates:
        if cd.tax_withholding_rate:
           if cd.tax_withholding_rate <= 0:
               frappe.throw("<b>Tax Withholding rate</b> cannot be zero or negative number")

    for cd in doc.rates:
        if cd.single_threshold:
           if cd.single_threshold <= 0:
               frappe.throw("<b>Single Threshold</b> cannot be zero or negative number")

    for cd in doc.rates:
        if cd.cumulative_threshold:
           if cd.cumulative_threshold <= 0:
               frappe.throw("<b>Cummulative Threshold</b> cannot be zero or negative number")

    for cd in doc.rates:
           if cd.from_date <= cd.to_date:
               frappe.throw("<b>From date</b> cannot be equal or before <b>To date</b>")