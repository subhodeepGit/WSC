// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Auto Roll No Generator', {
	refresh: function(frm) {

		frm.set_query("programs", function() {
			return {
				filters: {
					"program_grade":frm.doc.course_type
				}
			};
		});

		frm.set_query("semester",function(){
			return{
				filters:{
					"programs":frm.doc.programs
				}
			}
		});

		frm.set_query("academic_term",function(){
			return{
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		});
		frm.set_df_property('student_list', 'cannot_add_rows', true);
		frm.set_df_property('student_list', 'cannot_delete_rows', true);
	},
	get_student:function(frm){
		frm.clear_table("student_list");
		frappe.call({
			method: 'wsc.wsc.doctype.auto_roll_no_generator.auto_roll_no_generator.get_student',
			args:{
				course_type:frm.doc.course_type,
				programs:frm.doc.programs,
				semester:frm.doc.semester,
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				course_code:frm.doc.course_code,
				year_code:frm.doc.year_code,
				branch_code:frm.doc.branch_code
			},
			callback: function(r) {
				(r.message).forEach(element => {
					var row = frm.add_child("student_list")
					row.student=element.student
					row.student_name=element.student_name
					row.course_enrollment=element.name
					row.roll_no=element.roll_no
				});
				frm.refresh_field("student_list")
				frm.save();
			}
		})
	}
});
