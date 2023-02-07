// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Academic Continuation Form', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
        frm.set_query('student', function() {
			return {
                query :"wsc.wsc.doctype.academic_continuation_form.academic_continuation_form.get_student_value",
				// filters: {
				// 	"enabled": 0 
				// }
			}
		})
        frm.set_query('academic_term',function(){
            return{
                filters:{
                    "academic_year":frm.doc.academic_year
                }
            }
        })
        frm.set_query('programs',function(){
            return{
                filters:{
                    "program_grade":frm.doc.program_grade
                }
            }

        })
        frm.set_query("semester",function(){
            return{
                filters:{
                    "programs":frm.doc.programs
                }
            }
        })
    },
	
    student:function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.academic_continuation_form.academic_continuation_form.get_student_previous_records',
			args: {
				"student":frm.doc.student
			},
			callback: function(r) {

				if (r.message) {
					if (r.message['academic_year']){
						frm.set_value("earlier_academic_year",r.message['academic_year'])
					}

					if (r.message['academic_term']){
						// rm.refresh_field("academic_term")
						frm.set_value("earlier_academic_term",r.message['academic_term'])
					}
					if (r.message['programs']){
						// frm.refresh_field("programs")
						frm.set_value("earlier_program",r.message['programs'])

					}
					if (r.message['semesters']){
						// frm.refresh_field("semester")
						frm.set_value("earlier_semester",r.message['semesters'])

					}
					// code snippet
				}
				// else{
					// frm.refresh();
					// frm.refresh_field("academic_year")
					// frm.refresh_field("academic_term")
			}
        })
    },		// frm.refresh_field("programs")
	refresh(frm){
		if (frm.doc.form_status === "Approve" && frm.doc.docstatus === 1) {	
			frm.add_custom_button(__("Enroll"), function() {
				frm.trigger("enroll_student")
			}).addClass("btn-primary");
		}

	},

	
	enroll_student: function(frm) {
		frappe.model.open_mapped_doc({
			method: "wsc.wsc.doctype.academic_continuation_form.academic_continuation_form.enroll_student",
			frm:frm,

		})
	},


});
