// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Application"] = {
	"filters": [
		
		
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 150,
			"reqd": 0,
			"get_query": function(txt) {
				return {
					"filters": {
						"is_group":1,
						"is_stream": 1
					  }
				};
			}
		
		},
		{
			"fieldname": "program_grade",
			"label": __("Program Grade"),
			"fieldtype": "Link",
			"options": "Program Grades",
			"width": 150,
			"reqd": 0,
	
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
			"fieldname": "docstatus",
			"label": __("Status--1 for Submitted Document"),
			"fieldtype": "Int",
			"width": 50,
			"default":1,
			"read_only":1
			}

	]
};
