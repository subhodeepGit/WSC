// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Third Party Attendance', {
	total_number_of_staff_present: function(frm) {
		const absent = frm.doc.total_number_of_staff - frm.doc.total_number_of_staff_present
		frm.set_value('total_number_of_staff_absent', absent)
	},
	total_number_of_staff_absent: function(frm) {
		const absent = frm.doc.total_number_of_staff - frm.doc.total_number_of_staff_absent
		frm.set_value('total_number_of_staff_present', absent)
	}
});
