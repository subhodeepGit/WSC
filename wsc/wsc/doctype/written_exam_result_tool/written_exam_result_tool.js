// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Written Exam Result Tool', {
	refresh: function(frm) {
		frm.disable_save()
		frm.set_df_property('candidates_result', 'cannot_add_rows', true)
		frm.set_df_property('candidates_result', 'cannot_delete_rows', true)

		if(!frm.doc.__isLocal){
			frm.add_custom_button(__('Create Result'), function(){
				frappe.call({
					method: 'create_result',
					doc: frm.doc
				})
				frappe.msgprint("Result Created Successfully")
			}).addClass('btn-primary');
			// frm.refresh()
			//For Calendar
		} // end if
	},
	
	get_candidates:function(frm){
		frm.clear_table("candidates_result");
		frappe.call({
			method: "wsc.wsc.doctype.written_exam_result_tool.written_exam_result_tool.get_candidates_details",
			args: {
				job: frm.doc.job,
			},
			callback: function(r) { 
				(r.message).forEach(element => {
					var row = frm.add_child("candidates_result")
					row.name_of_the_candidate=element.applicant_name
					row.job_applicant_id=element.name
					row.email=element.email_id
				});
				frm.refresh();
				frm.refresh_field("name_of_the_candidate")
				frm.refresh_field("job_applicant")
				frm.refresh_field("email")
				frm.refresh_field("score_obtained")
				frm.refresh_field("result")
				frm.refresh_field("rank")
			} 
			
		}); 
	}
});
