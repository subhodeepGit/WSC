// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

// Student ID Number
// Placement Drive ID
// Round Status

frappe.query_reports["Selection Round Report"] = {
	"filters": [
        {
            "fieldname":"student_id",
            "label": __("Student ID"),
            "fieldtype": "Link",
            "options": "Student",
            "reqd":1,
        },
	]
};
