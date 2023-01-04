// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Final Exam Result Report"] = {
	"filters": [
		{
			"fieldname": "program_grade",
			"label": __("Program Grade"),
			"fieldtype": "Link",
			"options": "Program Grades",
			"width": 150,
			"reqd": 1,
			
		},
		{
			"fieldname": "programs",
			"label": __("Programs"),
			"fieldtype": "Link",
			"options": "Programs",
			"width": 150,
			"reqd": 1,
			"get_query": function(txt) {
				return {
					"filters": {
						'program_grade': frappe.query_report.get_filter_value('program_grade'),
					  }
				};
			}
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
			"label":"Academic Year",
			"fieldname":"academic_year",
			"fieldtype":"Link",
			"options":"Academic Year"
		},
		{
			"label":"Academic Term",
			"fieldname":"academic_term",
			"fieldtype":"Link",
			"options":"Academic Term",
			"get_query": function() {
				return {
					filters: {
						'academic_year': frappe.query_report.get_filter_value('academic_year')
					}
				}
			}
		}
	]
};
