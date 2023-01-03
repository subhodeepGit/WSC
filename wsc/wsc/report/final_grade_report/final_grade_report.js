// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Final Grade Report"] = {
	"filters": [
		{
			"fieldname": "programs",
			"label": __("Programs"),
			"fieldtype": "Link",
			"options": "Programs",
			"width": 150,
			"reqd": 1,
	
			},
			{
				"fieldname": "semester",
				"label": __("Semester"),
				"fieldtype": "Link",
				"options": "Program",
				"width": 150,
				"reqd": 1,
				"get_query": function(txt) {
					return {
						"filters": {
							'programs': frappe.query_report.get_filter_value('programs'),
						  }
					};
				}
			},
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
			"get_query": function(txt) {
				return {
					"filters": {
						'academic_year': frappe.query_report.get_filter_value('academic_year'),
					  }
				};
			}
		},
	]
};
