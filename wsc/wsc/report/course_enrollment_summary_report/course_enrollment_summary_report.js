// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Course Enrollment Summary Report"] = {
	"filters": [
		{
			"fieldname": "academic_year",
			"label": __("Academic Year"),
			"fieldtype": "Link",
			"options": "Academic Year",
			"width": 150,
			"reqd": 1,
		},
		{
			"fieldname": "academic_term",
			"label": __("Academic Term"),
			"fieldtype": "Link",
			"options": "Academic Term",
			"width": 150,
			"reqd": 1,
			get_query: () => {
				var academic_year = frappe.query_report.get_filter_value('academic_year');
				return {
					filters: {
						'academic_year': academic_year
					}
				}
			}
		},
		{
			"fieldname": "district",
			"label": __("District"),
			"fieldtype": "Link",
			"options": "Districts",
		},
		{
			"fieldname": "blocks",
			"label": __("Blocks"),
			"fieldtype": "MultiSelectList",
			"options": "Blocks",
			get_data: function(txt) {
				return frappe.db.get_link_options('Blocks', txt,{districts: frappe.query_report.get_filter_value("district")});
			},
			"width": 150,
		},
	]
};
