// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Allocation Report"] = {
	onload: function (report) {
        report.page.add_inner_button(__('Room Allocation Duration'), function () {
            
            let from_date_parts = report.filters[1].input.value.split("-")
			let to_date_parts = report.filters[2].input.value.split("-")

			frappe.set_route("query-report", "Room Allocation Duration Report" , {
                from_date: (new Date(from_date_parts[2] , from_date_parts[1] - 1 , from_date_parts[0])),
				to_date: (new Date(to_date_parts[2] , to_date_parts[1] - 1 , to_date_parts[0])),
            });
        });
    },
	"filters": [
        {
            "fieldname":"room_no",
            "label": __("Room"),
            "fieldtype": "Link",
            "options": "Room",
            // "reqd":1,
        },
		{
			"label":"Form Date",
			"fieldname":"from_date",
			"fieldtype":"Date",
            "reqd":1  
		},
        {
			"label":"To date",
			"fieldname":"to_date",
			"fieldtype":"Date",
            "reqd":1
		},
	],
};