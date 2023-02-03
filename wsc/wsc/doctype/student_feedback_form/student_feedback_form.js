// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Feedback Form', {
	refresh: function(frm) {
		// frm.set_query('program', function() {
		// 	return{
		// 		filters: {
		// 			"programs":frm.doc.programs
		// 		}
		// 	}
		// });
		// frm.set_query('academic_term', function() {
		// 	return{
		// 		filters: {
		// 			"academic_year":frm.doc.academic_year
		// 		}
		// 	}
		// });
		frm.set_query('instructor', function() {
			return{
				filters: {
					"course":frm.doc.course
				}
			}
		});
		frm.set_query('course', function() {
			return {
                query:"wsc.wsc.doctype.student_feedback_form.student_feedback_form.get_course",
                filters: {
                    "program":frm.doc.program
                }
			}
		});
		// frm.set_query('course', function() {
		// 	return {
        //         query:"wsc.wsc.doctype.student_feedback_form.student_feedback_form.get_course",
        //         filters: {
        //             "program":frm.doc.program
        //         }
		// 	}
		// });
	}
});
frappe.ui.form.on('Student Feedback Form', {
    instructor: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.student_feedback_form.student_feedback_form.getvalue',


           callback: function(r) {
                if(r.message){
                    frappe.model.clear_table(frm.doc, 'questionnarie');
                    (r.message).forEach(element => {
                        var c = frm.add_child("questionnarie")
                        c.questions=element.question
                    });
                }
                frm.refresh();
                frm.refresh_field("questionnarie")
            }
        })
    },
	student:function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.student_feedback_form.student_feedback_form.getdetails',
			args: {
				"student_id":frm.doc.student
			},
			callback: function(r) {
				if (r.message) {
					if (r.message['academic_year']){
						frm.set_value("academic_year",r.message['academic_year'])
					}
					if (r.message['academic_term']){
						frm.set_value("academic_term",r.message['academic_term'])
					}
					if (r.message['programs']){
						frm.set_value("programs",r.message['programs'])
					}
					if (r.message['semesters']){
						frm.set_value("program",r.message['semesters'])
					}
					// code snippet
				}
				frm.refresh();
			}
		})
	}
});
