// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Third Party Attendance Report"] = {
	"filters": [
		{
            "fieldname":"third_party",
            "label": __("Third Party Attendance Contract"),
            "fieldtype": "Link",
            "options": "Third Party Attendance Contract",
            // "reqd":1,
        },
		{
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            // "reqd":1,
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            // "reqd":1,
        },
	]
};
