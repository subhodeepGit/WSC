// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset Report"] = {
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
            fieldname:"asset_owner",
            label: __("Asset Owner"),
            fieldtype: "Select",
			options: "\nSupplier\nCustomer\nCompany",
        },
		{
            fieldname:"location",
            label: __("Location"),
            fieldtype: "Link",
            options: "Location",
        },
        {
            fieldname:"department",
            label: __("Department"),
            fieldtype: "Link",
            options: "Department",
        },
		{
            fieldname:"status",
            label: __("Status"),
            fieldtype: "Select",
			options: "\nDraft\nSubmitted\nPartially Depreciated\nFully Depreciated\nSold\nScrapped\nIn Maintenance\nOut of Order\nIssue\nReceipt\nCapitalized\nDecapitalized",
        },
	]
};
