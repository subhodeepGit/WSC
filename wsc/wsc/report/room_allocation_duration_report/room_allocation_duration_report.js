// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Allocation Duration Report"] = {
	"filters": [
        // {
		// 	"label":"Schedule Date",
		// 	"fieldname":"schedule_date",
		// 	"fieldtype":"Date",
		// 	// "options":"Academic Year",
        //     "reqd":1
		// },
		{
			"label":"From Date",
			"fieldname":"from_date",
			"fieldtype":"Date",
			// "options":"Academic Year",
            "reqd":1
		},
		{
			"label":"To Date",
			"fieldname":"to_date",
			"fieldtype":"Date",
			// "options":"Academic Year",
            "reqd":1
		},
		{
			"label":"Working Hours",
			"fieldname":"daily_hrs",
			"fieldtype":"Select",
			"options":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            "reqd":1
		}
	]
};
