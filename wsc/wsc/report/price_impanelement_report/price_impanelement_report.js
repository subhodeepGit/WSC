// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Price Impanelement Report"] = {
	"filters": [
		{
            fieldname:"item_code",
            label: __("Item Code"),
            fieldtype: "Link",
            options: "Item",
        },
		{
            fieldname:"item_name",
            label: __("Item Name"),
            fieldtype: "Data",
        },
		{
            fieldname:"price_list",
            label: __("Price List"),
            fieldtype: "Link",
            options: "Price List",
        },
        {
            fieldname:"supplier",
            label: __("Supplier"),
            fieldtype: "Link",
            options: "Supplier",
        }
	]
};
