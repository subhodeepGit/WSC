// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Allocation Duration Report"] = {
	onload: function (report) {
        report.page.add_inner_button(__('Room Allocation Report'), function () {
			
            let from_date_parts = report.filters[0].input.value.split("-")
			let to_date_parts = report.filters[1].input.value.split("-")

			frappe.set_route("query-report", "Room Allocation Report" , {
                from_date: (new Date(from_date_parts[2] , from_date_parts[1] - 1 , from_date_parts[0])),
				to_date: (new Date(to_date_parts[2] , to_date_parts[1] - 1 , to_date_parts[0])),
            });
        });
    },
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
