// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Program Intermit Form', {
	// refresh: function(frm) {

	// }
	student:function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.program_intermit_form.program_intermit_form.get_student_details',
			args: {
				"student_id":frm.doc.student
			},
			callback: function(r) {

				if (r.message) {
					if (r.message['academic_year']){
						frm.set_value("academic_year",r.message['academic_year'])
					}

					if (r.message['academic_term']){
						// rm.refresh_field("academic_term")
						frm.set_value("academic_term",r.message['academic_term'])
					}
					if (r.message['programs']){
						// frm.refresh_field("programs")
						frm.set_value("programs",r.message['programs'])

					}
					if (r.message['semesters']){
						// frm.refresh_field("semester")
						frm.set_value("semester",r.message['semesters'])

					}
					// code snippet
				}
				else{
					frm.refresh();
					frm.refresh_field("academic_year")
					frm.refresh_field("academic_term")
					frm.refresh_field("programs")
					frm.refresh_field("semester")
				}
				
			}
		})
	}

});
