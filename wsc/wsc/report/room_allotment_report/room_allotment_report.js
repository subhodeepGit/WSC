// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Allotment Report"] = {
	"filters": [
		{
			"fieldname": "hostel",
			"label": __("Hostel"),
			"fieldtype": "Link",
			"options": "Hostel Masters",
			"width": 150,
			"reqd": 1,
		},
	]
};
