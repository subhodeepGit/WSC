// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Back Paper Tracker', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
		
		frm.set_query("semester", function() {
			                return {
			                    filters: {
			                        "programs":frm.doc.programs
			                    }
			                };
			            });
		frm.set_query("programs", function() {
			                return {
			                    filters: {
			                        "program_grade":frm.doc.program_grade
			                    }
			                };
			            });
		frm.set_query("academic_terms",function(){
			return{
				filters:{
					"academic_year":frm.doc.academic_year
				}
			};
		});

		frm.set_query("course",function(){
			return{
				filters:{
					"semester":frm.doc.semester
				}
			};
		});
		frm.set_query("course", function() {
			            return {
			                query:"wsc.wsc.doctype.back_paper_tracker.back_paper_tracker.get_course",
			                filters: {
			                    "name":frm.doc.semester
			                }
			            };
			        });
	},
	 
    get_students:function(frm){
		frm.clear_table("backlog_details");
		frappe.call({
			method: "wsc.wsc.doctype.back_paper_tracker.back_paper_tracker.get_student",
			args: {
				"course" : frm.doc.course,
				"academic_year":frm.doc.academic_year,
				"academic_term":frm.doc.academic_terms,
				"program":frm.doc.semester,
			},
			callback: function(r) {
				
				(r.message).forEach(element => {
					var row = frm.add_child("backlog_details")
					row.student=element.student
					row.student_name=element.student_name
                    row.result = element.result
                    // row.registration_number = element.permanant_registration_number
				});
				frm.refresh_field("backlog_details");
                // frm.save();
				// frm.set_value("total_enrolled_student",(r.message).length)
			}
			
		});
	}


});
