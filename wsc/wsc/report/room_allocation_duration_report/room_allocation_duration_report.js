// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Allocation Duration Report"] = {
	"filters": [
        {
			"label":"Schedule Date",
			"fieldname":"schedule_date",
			"fieldtype":"Date",
			// "options":"Academic Year",
            "reqd":1
		},
	]
};
