# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from frappe.model.document import Document

import frappe
import erpnext

def validate(doc, method):
    if doc.company:
        doc.currency = erpnext.get_company_currency(doc.company)
    if doc.standard_tax_exemption_amount:
        if doc.standard_tax_exemption_amount < 0:
            frappe.throw("Standard Tax Exemption Amount can not be negative.")
        if len(str(doc.standard_tax_exemption_amount)) > 12:
            frappe.throw("Standard Tax Exemption Amount is too high.")
    if doc.slabs:
        for i in range(len(doc.slabs)):
            if doc.slabs[i].from_amount and doc.slabs[i].to_amount < 0 and doc.slabs[i].percent_deduction:
                if doc.slabs[i].from_amount < 0 or doc.slabs[i].to_amount < 0 or doc.slabs[i].percent_deduction < 0:
                    frappe.throw("From Amount or To Amount or Percent Deduction can not be less than 0.")
                if doc.slabs[i].percent_deduction > 100:
                    frappe.throw("Percent Deduction can not be greater than 100.")
                if len(str(doc.slabs[i].from_amount)) > 12 or len(str(doc.slabs[i].to_amount)) > 12:
                    frappe.throw("FromAmount / ToAmount is too high.")
    if doc.other_taxes_and_charges:
        for i in range(len(doc.other_taxes_and_charges)):
            if doc.other_taxes_and_charges[i].percent:
                if doc.other_taxes_and_charges[i].percent < 0:
                    frappe.throw("Percent can not be less than 0.")
                if doc.other_taxes_and_charges[i].percent > 100:
                    frappe.throw("Percent can not be more than 100.")
            if doc.other_taxes_and_charges[i].min_taxable_income:
                if doc.other_taxes_and_charges[i].min_taxable_income < 0:
                    frappe.throw("Min Taxable Amount can not be less than 0.")
                if len(str(doc.other_taxes_and_charges[i].min_taxable_income )) > 12:
                    frappe.throw("Min Taxable Amount is too high.")
            if doc.other_taxes_and_charges[i].max_taxable_income:
                if doc.other_taxes_and_charges[i].max_taxable_income < 0:
                    frappe.throw("Max Taxable Amount can not be less than 0.")
                if len(str(doc.other_taxes_and_charges[i].max_taxable_income)) > 12:
                    frappe.throw("Max Taxable Amount is too high.")
