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
    sql_query="""select item_code,item_name,price_list,price_list_rate,currency,supplier,valid_from,valid_upto from `tabItem Price`"""

    if filters:
        sql_query += " WHERE "
        conditions = []
        for key, value in filters.items():
            conditions.append(f" {key} = %s")
        sql_query += " AND ".join(conditions)
        data = frappe.db.sql(sql_query, tuple(filters.values()), as_dict=True)

    return data

def get_columns(filters=None):
    columns=[
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
            "fieldname":"price_list",
            "label": _("Price List"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150,
        },
        {
            "label": _("Rate"),
            "fieldname": "price_list_rate",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Currency"),
            "fieldname": "currency",
            "fieldtype": "Link",
            "options": "Currency",
            "width": 150,
        },
        {
            "label": _("Supplier"),
            "fieldname": "supplier",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "fieldname":"valid_from",
            "label": _("From Date"),
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname":"valid_upto",
            "label": _("To Date"),
            "fieldtype": "Date",
            "width": 150,
        },
    ]
    return columns