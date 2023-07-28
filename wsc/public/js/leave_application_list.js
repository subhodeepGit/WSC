frappe.listview_settings["Leave Application"] = {
	add_fields: ["leave_type", "employee", "employee_name", "total_leave_days", "from_date", "to_date","current_status"],
	has_indicator_for_draft: 1,
	get_indicator: function (doc) {
		let current_status_color = {
			"Approved": "green",
			"Rejected": "red",
			"Open": "orange",
			"Cancelled": "red",
			"Submitted": "blue",
			"Forwarded to Approving Authority": "pink"
		};
		return [__(doc.current_status), current_status_color[doc.current_status], "current_status,=," + doc.current_status];
	}
};

