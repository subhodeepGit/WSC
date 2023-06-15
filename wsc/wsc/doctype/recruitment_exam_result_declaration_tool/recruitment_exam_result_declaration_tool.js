// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Exam Result Declaration Tool', {

	refresh:function(frm){
		if (!frm.doc.__islocal){
			frm.add_custom_button(__('Create Result'), function() {
				frappe.call({
					method: 'create_result',
					doc: frm.doc,
					callback: function() {
						frappe.msgprint(__('Result created successfully.'));
						frm.reload.doc();
					}
					
				});
				var isUpdateExecuting = false;
				frappe.call({
					method :'update_job_opening',
					doc:frm.doc,
					callback:function(){
						frappe.msgprint("Status updated in job opening");
						isUpdateExecuting = true;
					}
				})
				if (isUpdateExecuting) {
					console.log("Second frappe.call() is executing.");
				  } else {
					console.log("Second frappe.call() is not executing.");
				  }
			}).addClass('btn-primary');
			}
	
		},
		get_applicants: function(frm) {
		
			frappe.call({
				method: 'wsc.wsc.doctype.recruitment_exam_result_declaration_tool.recruitment_exam_result_declaration_tool.fetch_applicants',
				args: {
					recruitment_exam_declaration: frm.doc.exam_declaration
				},
				callback: function(r) {
					if (r.message) {
						var applicants = r.message;
						frm.clear_table("applicant_details");
						for (var i = 0; i < applicants.length; i++) {
							var applicant = applicants[i];
							var row = frappe.model.add_child(frm.doc, "Job Applicant Result Detail", "applicant_details");
							row.job_applicant = applicant.job_applicant;
							row.applicant_name = applicant.applicant_name;
							row.applicant_mail_id = applicant.applicant_mail_id;
						}
						frm.refresh_field("applicant_details");
					}
				}
			});
		}
		
	});
	
