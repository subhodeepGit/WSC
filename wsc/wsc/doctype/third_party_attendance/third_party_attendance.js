// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Third Party Attendance', {
	setup: function (frm) {
		frm.set_query("third_party_attendance_contract", function () {
			return {
				filters: [
					["Third Party Attendance Contract", "docstatus", "=", 1],
				]
			}
		});
	},
	total_number_of_staff_present: function(frm) {
		const absent = frm.doc.total_number_of_staff - frm.doc.total_number_of_staff_present
		frm.set_value('total_number_of_staff_absent', absent)
	},
	total_number_of_staff_absent: function(frm) {
		const absent = frm.doc.total_number_of_staff - frm.doc.total_number_of_staff_absent
		frm.set_value('total_number_of_staff_present', absent)
	},
	contract_start_date: function(frm) {
        frm.fields_dict.date.datepicker.update({
            minDate: frm.doc.contract_start_date ? new Date(frm.doc.contract_start_date) : null,
        });
    },
	contract_end_date: function(frm) {
        frm.fields_dict.date.datepicker.update({
            maxDate: frm.doc.contract_end_date ? new Date(frm.doc.contract_end_date) : null,
        });
    },
});
