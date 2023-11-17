// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset Report"] = {
	"filters": [
		{
            fieldname:"item_code",
            label: __("Asset Code"),
            fieldtype: "Link",
            options: "Item",
        },
		{
            fieldname:"item_name",
            label: __("Asset Name"),
            fieldtype: "Data",
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
			options: "\nDraft\nSubmitted\nPartially Depreciated\nFully Depreciated\nSold\nScrapped",
        },
	]
};
