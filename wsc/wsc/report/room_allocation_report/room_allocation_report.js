// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Allocation Report"] = {
	onload: function (report) {
        report.page.add_inner_button(__('Your Button Label'), function () {
            // Your custom button logic here
            frappe.msgprint('Button Clicked!');
			frappe.route_options = {
                student_id: "",
            };
            frappe.set_route("query-report", "Selection Round Report");
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