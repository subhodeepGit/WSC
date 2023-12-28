// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["ToT Participant Attendance Report"] = {
	"filters": [
		{
			"fieldname":"participant_group",
			"label": __("Participant Group"),
			"fieldtype": "MultiSelectList",
			"reqd":1,
			get_data: function(txt) {
				return frappe.db.get_link_options('Participant Group', txt)
			}
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
