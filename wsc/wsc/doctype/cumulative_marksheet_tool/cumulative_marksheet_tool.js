// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Cumulative Marksheet Tool', {
	refresh:function(frm){
		if (!frm.doc.__islocal){
			frm.add_custom_button(__('Create Cumulative Marksheet'), function() {
				frappe.call({
					method: 'make_exam_assessment_result',
					doc: frm.doc,
					callback: function() {
						frm.refresh();
					}
				});
			}).addClass('btn-primary');;
		}
		frm.set_df_property('cummulative_marksheet_student', 'cannot_add_rows', true);
		
	},
	employee: function(frm) {
		if(frm.doc.employee){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					if(r.message){
						if (r.message['designation']){
							frm.set_value("designation",r.message['designation'])
						}
						if (r.message['employee_name']){
							frm.set_value("employee_name",r.message['employee_name'])
						}
					}
				} 
			}); 
		}
	},
	get_students:function(frm){
		frm.clear_table("cummulative_marksheet_student");
		frappe.call({
			method: "wsc.wsc.doctype.cumulative_marksheet_tool.cumulative_marksheet_tool.get_students",
			args: {
				programs: frm.doc.programs,
				// semester: frm.doc.semester,
				academic_term: frm.doc.academic_term
				// academic_term: frm.doc.academic_term
			},
			// $.each(r.message, function(i, d) {
			// 	var s = frm.add_child('students');
			// 	s.student = d.student;
				// s.student_name = d.student_name;
			callback: function(r) { 
				
				(r.message).forEach(element => {
					// if(in_list(student_list, element.student)) {
					var row = frm.add_child("cummulative_marksheet_student")
					row.student=element.student
					row.student_name=element.student_name
					row.completion_status=element.completion_status
					// if (d.active === 0) {
					// 	s.active = 0;
					// }
					// }
				});
				frm.refresh_field("cummulative_marksheet_student")
				frm.save();
				frm.set_value("total_enrolled_student",(r.message).length)
			} 
			
		});  
	}

});
