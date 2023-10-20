// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Program Enrollment"] = {
	"filters": [
	
		// 
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 150,
			"reqd": 1,
			"get_query": function(txt) {
				return {
					"filters": {
						"is_group":0,
						// "is_stream": 1
					  }
				};
			}
		
		},
	
		{
			"fieldname": "programs",
			"label": __("Programs"),
			"fieldtype": "Link",
			"options": "Programs",
			"width": 50,
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
			"fieldname": "student_category",
			"label": __("Caste Category"),
			"fieldtype": "Link",
			"width": 50,
			"reqd": 1,
			"options": "Student Category",
		},
		{
			"fieldname": "transaction_status",
			"label": __("Transcation Status"),
			"fieldtype": "Select",
			// "reqd": 1,
			"width": 50,
			"options": ["Awaited","Failure","Initiated","Success","Rejected","Aborted","Unsuccessful","Shipped"],
		},
		// {
		// 	"fieldname": "docstatus",
		// 	"label": __("Submitted Document"),
		// 	"fieldtype": "Int",
		// 	"width": 50,
		// 	"default":1,
		// 	"read_only":1
		// }


	]
};
