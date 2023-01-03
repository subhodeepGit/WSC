frappe.ui.form.on('Leaving Certificate Tool', {
	refresh:function(frm){
		if (!frm.doc.__islocal){
			frm.add_custom_button(__('Create Leaving Certificate'), function() {
				frappe.call({
					method: 'make_exam_assessment_result',
					doc: frm.doc,
					callback: function() {
						frm.refresh();
					}
				});
			}).addClass('btn-primary');;
		}
		
	},
	get_students:function(frm){
		frm.clear_table("conduct_certificate_student");
		frappe.call({
			method: "wsc.wsc.doctype.leaving_certificate_tool.leaving_certificate_tool.get_students",
			args: {
				programs: frm.doc.programs,
				academic_term: frm.doc.academic_term
			},
			callback: function(r) { 
				
				(r.message).forEach(element => {
					var row = frm.add_child("conduct_certificate_student")
					row.student=element.student
					row.student_name=element.student_name
					row.completion_status=element.completion_status
				});
				frm.refresh_field("conduct_certificate_student")
				frm.save();
				frm.set_value("total_enrolled_student",(r.message).length)
			} 
			
		});  
	}

});