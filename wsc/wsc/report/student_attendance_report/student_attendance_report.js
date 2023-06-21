// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Attendance Report"] = {
	"filters": [
		{
            "fieldname":"academic_term",
            "label": __("Academic Term"),
            "fieldtype": "MultiSelectList",
            // "options": "Project",
            // "reqd":1,
            get_data: function(txt) {
				return frappe.db.get_link_options('Academic Term', txt)
			}
        },
        {
            "fieldname":"semester",
            "label": __("Semester"),
            "fieldtype": "MultiSelectList",
            // "options": "Project",
            // "reqd":1,
            get_data: function(txt) {
				return frappe.db.get_link_options('Program', txt)
			}
        },
		{
            "fieldname":"course",
            "label": __("Module"),
            "fieldtype": "MultiSelectList",
            // "options": "Project",
            // "reqd":1,
            get_data: function(txt) {
				return frappe.db.get_link_options('Course', txt)
			}
        },
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            // "reqd":1,
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            // "reqd":1,
        },
	]
};
