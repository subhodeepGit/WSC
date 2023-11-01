import frappe

def validate(doc, method):
    validate_tax_amount(doc)
    validate_amount(doc)

def validate_tax_amount(doc):
    for cd in doc.taxes:
           if cd.minimum_net_rate >= cd.maximum_net_rate:
               frappe.throw("Maximum net rate <b>{0}</b> should not be greater than Minimum net rate <b>{1}</b>.".format(cd.minimum_net_rate, cd.maximum_net_rate))
def validate_amount(doc):
    for cd in doc.authorization_table:
           if cd.from_amount >= cd.to_amount:
               frappe.throw("To amount <b>{0}</b> should not be greater than From amount <b>{1}</b>.".format(cd.to_amount, cd.from_amount))