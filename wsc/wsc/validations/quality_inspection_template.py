import frappe

def validate(doc, method):
    validate_amount(doc)

def validate_amount(doc):
    for cd in doc.item_quality_inspection_parameter:
        if cd.min_value and cd.max_value:
           if cd.min_value > cd.max_value:
               frappe.throw("Min Value <b>{0}</b> should not be greater than Max Value <b>{1}</b>.".format(cd.min_value, cd.max_value))