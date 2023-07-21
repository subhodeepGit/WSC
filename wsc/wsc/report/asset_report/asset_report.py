# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)
    return columns,data

def get_data(filters=None):
    data=[]
    sql_query="""select item_code,status,
                                     item_name,company,
                                     asset_owner,
                                     custodian,location,department,
                                     cost_center,gross_purchase_amount,available_for_use_date,purchase_date,
                                     insured_value,policy_number,insurer,insurance_start_date,insurance_end_date,
                                     fb.finance_book,fb.depreciation_method,
                                     fb.depreciation_start_date,
                                     fb.total_number_of_depreciations,
                                     fb.frequency_of_depreciation
                              from `tabAsset` as a LEFT JOIN `tabAsset Finance Book` AS fb ON a.name=fb.parent
                            """
    if filters:
        sql_query += " WHERE "
        conditions = []
        for key, value in filters.items():
            conditions.append(f" {key} = %s")
        sql_query += " AND ".join(conditions)
        data = frappe.db.sql(sql_query, tuple(filters.values()), as_dict=True)
    else:
        data = frappe.db.sql(sql_query,as_dict=True)

    return data

def get_columns(filters=None):
    columns=[
        {
            "label": _("Company"),
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150,
        },
        {
            "fieldname":"item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150,
        }, 
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"status",
            "label": _("Status"),
            "fieldtype": "Select",
            "width": 150,
        },  
        {
            "fieldname":"asset_owner",
            "label": _("Asset Owner"),
            "fieldtype": "Select",
            "width": 150,
        },
        {
            "fieldname":"location",
            "label": _("Location"),
            "fieldtype": "Link",
            "options": "Location",
            "width": 150,
        },
        {
            "fieldname":"custodian",
            "label": _("Custodian"),
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150,
        },
        {
            "fieldname":"department",
            "label": _("Department"),
            "fieldtype": "Link",
            "options": "Department",
            "width": 150,
        },
        {
            "fieldname":"cost_center",
            "label": _("Cost Center"),
            "fieldtype": "Link",
            "options": "Department",
            "width": 150,
        },
        {
            "fieldname":"gross_purchase_amount",
            "label": _("Gross Purchase Amount"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"available_for_use_date",
            "label": _("Available-for-use Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname":"purchase_date",
            "label": _("Purchase Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname":"finance_book",
            "label": _("Finance Book"),
            "fieldtype": "Link",
            "options": "Asset Finance Book",
            "width": 150,
        },
        {
            "fieldname":"depreciation_method",
            "label": _("Depreciation Method"),
            "fieldtype": "Select",
            "width": 150,
        },
        {
            "fieldname":"total_number_of_depreciations",
            "label": _("Total Number of Depreciations"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"frequency_of_depreciation",
            "label": _("Frequency of Depreciation (Months)"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"depreciation_start_date",
            "label": _("Depreciation Posting Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname":"insured_value",
            "label": _("Insured value"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"policy_number",
            "label": _("Policy number"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"insurer",
            "label": _("Insurer"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname":"insurance_start_date",
            "label": _("Insurance Start Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname":"insurance_end_date",
            "label": _("Insurance End Date"),
            "fieldtype": "Date",
            "width": 150,
        },
    ]
    return columns