// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["L1 Vendor Selection"] = {
	filters: [
		{
            fieldname:"supplier",
            label: __("Supplier"),
            fieldtype: "MultiSelectList",
            get_data: function(txt) {
				return frappe.db.get_link_options('Supplier', txt)
			}
        },
		{
            fieldname:"transaction_date",
            label: __("From Date"),
            fieldtype: "Date",
        },
        {
            fieldname:"valid_till",
            label: __("To Date"),
            fieldtype: "Date",
        },
        {
            fieldname:"status",
            label: __("Status"),
            fieldtype: "Select",
			options: "\nSubmitted\nExpired",
        },
		{
            fieldname:"item_code",
            label: __("Item Code"),
            fieldtype: "Link",
            options: "Item",
        },        
	]
};
