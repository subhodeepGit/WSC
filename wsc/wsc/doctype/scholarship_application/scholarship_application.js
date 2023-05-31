// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scholarship Application', {
	student_id: function(frm) {
		frappe.call({
			method: 'wsc.wsc.doctype.scholarship_application.scholarship_application.calculateAge',
			args: {
				'student_no': frm.doc.student_id,
			},
			callback: function(r) {
				if (!r.exc) {
					frm.set_value("age", r.message);
				}
			},

		})
		frappe.call({
			method: 'wsc.wsc.doctype.scholarship_application.scholarship_application.current_education',
			args: {
				'student_no': frm.doc.student_id,
			},
			callback: function(r) {
				if (r.message) {
					frappe.model.clear_table(frm.doc, 'current_education');
					(r.message).forEach(element => {
						var c = frm.add_child("current_education")
						c.programs=element.programs
						c.semesters=element.semesters
						c.academic_year=element.academic_year
						c.academic_term=element.academic_term
					});
					frm.refresh_field("current_education")
				}
			},

		})
	}
});
