// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Admit Card Generation Tool', {
	refresh: function(frm) {
		// frm.disable_save()
		if (!frm.doc.__islocal){
        frm.add_custom_button(__('Create Admit Card'), function() {
            frappe.call({
                method: 'create_admit_card',
                doc: frm.doc,
                callback: function() {
                    frappe.msgprint(__('Admit Cards created successfully.'));
                    frm.reload.doc();
                }
            
            });
            var isUpdateExecuting = false;
            frappe.call({
                method :"update_job_opening",
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
        }).addClass('btn-primary');;
            
		}
		// frappe.msgprint(__('Admit Cards created successfully.'))
	
	},
	
    get_applicant: function(frm) {
        // alert("Hello")
        frappe.call({
            method: 'wsc.wsc.doctype.recruitment_admit_card_generation_tool.recruitment_admit_card_generation_tool.fetch_applicants',
            args: {
                recruitment_exam_declaration: frm.doc.exam_declaration
            },
            callback: function(r) {
                if (r.message) {
                    var applicants = r.message;

                    frm.clear_table("job_applicant_details");
                    for (var i = 0; i < applicants.length; i++) {
                        var applicant = applicants[i];

                        var row = frappe.model.add_child(frm.doc, "Job Applicant Detail", "job_applicant_details");
                        row.job_applicant = applicant.job_applicant;
                        row.applicant_name = applicant.applicant_name;
                        row.applicant_mail_id = applicant.applicant_mail_id;

                    }

                    frm.refresh_field("job_applicant_details");
                }
            }
        });
    }
});
