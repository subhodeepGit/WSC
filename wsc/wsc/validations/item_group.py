import frappe

def validate(doc, method):
    validate_tax_amount(doc)
    validate_amount(doc)

def validate_tax_amount(doc):
    for cd in doc.taxes:
           
        if cd.minimum_net_rate and cd.maximum_net_rate:
            if cd.minimum_net_rate <0:
                frappe.throw("Minimum net rate cannot be negative")
            if cd.maximum_net_rate <0:
                    frappe.throw("Maximum net rate cannot be negative")

        if cd.minimum_net_rate and cd.maximum_net_rate:
            if cd.minimum_net_rate >= cd.maximum_net_rate:
                frappe.throw("Minimum net rate <b>{0}</b> should be not greater than Maximum net rate <b>{1}</b>.".format(cd.minimum_net_rate, cd.maximum_net_rate))

def validate_amount(doc):
    for cd in doc.authorization_table:
        if cd.to_amount < 0:
            frappe.throw("To amount cannot be zero")
        if cd.to_amount == 0:
            if cd.from_amount>0:
                frappe.throw("To amount cannot be zero")
        if cd.from_amount > cd.to_amount:
            frappe.throw("To amount <b>{0}</b> should be greater than From amount <b>{1}</b>.".format(cd.to_amount, cd.from_amount))
