// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Attrition Form', {
	// refresh: function(frm) {

	// }
	student_no: function(frm) {
		frappe.call({
            method: 'wsc.wsc.doctype.student_attrition_form.student_attrition_form.current_education',
            args: {
                'student_no': frm.doc.student_no,
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
		frappe.call({
			method: 'wsc.wsc.doctype.student_attrition_form.student_attrition_form.last_attendence',
			args: {
                'student_no': frm.doc.student_no,
            },
			callback: function(r){
				if (r.message){
					var a =r.message
					frm.set_value("last_date_of_attendance",a['last_date']);
					frm.set_value("status_of_attendence",a['status']);
				}
			}
		})
	}
});
