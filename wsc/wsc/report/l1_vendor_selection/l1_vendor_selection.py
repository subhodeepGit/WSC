# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)
    return columns,data

def get_data(filters):
    data = []
    doc_filters = {}

    supplier_filter = filters.get("supplier")
    transaction_date_filter = filters.get("transaction_date")
    valid_till_filter = filters.get("valid_till") 
    item_code_filter = filters.get("item_code")
    status_filter = filters.get("status")

    if supplier_filter:
        doc_filters["supplier"] = ["in", supplier_filter]
    if transaction_date_filter:
        doc_filters["transaction_date"] = ("=", transaction_date_filter)
    if valid_till_filter:
        doc_filters["valid_till"] = ("=", valid_till_filter)
    if status_filter:
        doc_filters["status"] = ("=", status_filter)
    if item_code_filter:
        doc_filters["item_code"] = ("=", item_code_filter)
    
    if doc_filters:
        supplier_quotations = frappe.get_all("Supplier Quotation",filters=doc_filters,fields=["name",'supplier','total_net_weight','transaction_date','discount_amount','valid_till','status','grand_total','total_taxes_and_charges'])
        for supplier_quotation in supplier_quotations:
            sq_doc = frappe.get_doc("Supplier Quotation", supplier_quotation.name)
            for item in sq_doc.get("items"):
                data.append({
                    "item_group": item.item_group,
                    "rate": item.rate,
                    "amount": item.amount,
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "qty": item.qty,
                    "uom": item.uom,
                    "request_for_quotation": item.get("request_for_quotation"),
                    "material_request": item.material_request, 
                    "supplier": supplier_quotation.supplier,
                    "status": supplier_quotation.status,
                    "discount_amount": supplier_quotation.discount_amount,
                    "total_net_weight": supplier_quotation.total_net_weight,
                    "transaction_date": supplier_quotation.transaction_date,
                    "grand_total": supplier_quotation.grand_total,
                    "valid_till": supplier_quotation.valid_till,
                    "total_taxes_and_charges": supplier_quotation.total_taxes_and_charges,                    
                })
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
            "label": _("Purchase Requisition"),
            "fieldname": "material_request",
            "fieldtype": "Link",
            "options": "Material Request",
            "width": 180
        },{
            "label": _("Request for Quotation"),
            "fieldname": "request_for_quotation",
            "fieldtype": "Link",
            "options": "Request for Quotation",
            "width": 180
        },  
        {
            "fieldname":"transaction_date",
            "label": _("Transaction Date"),
            "fieldtype": "Date",
            "width": 180
        },
        {
            "fieldname":"valid_till",
            "label": _("Valid Till"),
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
            "options": "Item",
            "width": 180
        }, 
        {
            "fieldname":"item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname":"item_group",
            "label": _("Item group"),
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 180
        }, 
        {
            "fieldname":"qty",
            "label": _("Quantity"),
            "fieldtype": "Float",
            "width": 180
        }, 
        {
            "fieldname":"uom",
            "label": _("UOM"),
            "fieldtype": "Data",

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