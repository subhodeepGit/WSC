// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Marksheet"] = {
	"filters": [
		{
			"label": "Programs",
			"fieldtype": "Link",
			"options":"Programs",
			"fieldname": "programs",
			// 'width':150
		},
		{
			"label":"Year of Admission",
			"fieldname":"year_of_admission",
			"fieldtype":"Link",
			"options":"Academic Year"
		},
		{
			"label":"Year of Completion",
			"fieldname":"year_of_completion",
			"fieldtype":"Link",
			"options":"Academic Year"
		},
		{
			"label":"Student",
			"fieldname":"student",
			"fieldtype":"Link",
			"options":"Student",
			// 'width':150 
		},
	]
};
