# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)

    return columns,data

def get_data(filters):
    # data=[]
    # filter=[]
    
    # data=frappe.get_all("Supplier Quotation",
    #                             fields=['total_net_weight','transaction_date','discount_amount','valid_till','status','grand_total','total_taxes_and_charges'])
    # childData=frappe.get_all("Supplier Quotation Item",
    #                             fields=['item_code','qty','rate','amount'])
    # # data=data+childData
    # # print(filters)    
    # print("\n\n\n\naaaa\n")
    # print(data)
    # print("\n\n\n\naaaa\n")
    # # print(childData)    

    return data

def get_columns(filters=None):
    columns=[
        {
            "label": _("Supplier"),
            "fieldname": "supplier",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname":"transaction_date",
            "label": _("From Date"),
            "fieldtype": "Date",
            "width": 180
        },
        {
            "fieldname":"valid_till",
            "label": _("To Date"),
            "fieldtype": "Date",
            "width": 180
        },
        {
            "fieldname":"status",
            "label": _("Status"),
            "fieldtype": "Select",
            "width": 150
        },
        {
            "fieldname":"item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Supplier Quotation",
            "width": 180
        }, 
        {
            "fieldname":"item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname":"Item group",
            "label": _("Item group"),
            "fieldtype": "Link",
            "options": "Supplier Quotation",
            "width": 180
        }, 
        {
            "fieldname":"qty",
            "label": _("Quantity"),
            "fieldtype": "Text",
            "width": 180
        }, 
        {
            "fieldname":"OUM",
            "label": _("OUM"),
            "fieldtype": "Text",

            "width": 180
        },
        {
            "fieldname":"discount_amount",
            "label": _("Discount"),
            "fieldtype": "Float",
            "width": 180
        }, 
        {
            "fieldname":"rate",
            "label": _("Rate"),
            "fieldtype": "Float",
            "width": 180
        }, 
        {
            "fieldname":"amount",
            "label": _("Amount"),
            "fieldtype": "Float",
            "width": 180
        },
        {
            "fieldname":"total_net_weight",
            "label": _("Weight"),
            "fieldtype": "Float",
            "width": 180
        }, 
        {
            "fieldname":"total_taxes_and_charges",
            "label": _("Taxes and Charges"),
            "fieldtype": "Float",
            "width": 180
        }, 
        {
            "fieldname":"grand_total",
            "label": _("Grand Total"),
            "fieldtype": "Float",
            "width": 180
        }, 
    ]
    return columns