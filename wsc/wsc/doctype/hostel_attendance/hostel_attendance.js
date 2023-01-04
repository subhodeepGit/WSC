// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Attendance', {
	setup: function (frm) {
		frm.set_query("room_allotment_no", function() {
			return {
				query: "wsc.wsc.doctype.hostel_attendance.hostel_attendance.ra_query"
			};
		});
	}
})