// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Feedback', {
	// refresh: function(frm) {

	// }
	setup(frm){
		frm.set_query("program", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
		frm.set_query("programs", function() {
			return {
				query: 'wsc.wsc.doctype.feedback.feedback.get_student_program',
				filters: {
					"student":frm.doc.student,
				}
			};
		});
		frm.set_query("student_group", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
		frm.set_query("faculty", function() {
			return {
				query: 'wsc.wsc.doctype.feedback.feedback.get_faculty',
				filters: {
					"student_group":frm.doc.student_group
				}
			};
		});
	}
});
