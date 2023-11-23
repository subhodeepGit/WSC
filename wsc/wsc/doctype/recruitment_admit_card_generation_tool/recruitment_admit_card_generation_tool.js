// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Admit Card Generation Tool', {
	refresh: function(frm) {
        frm.set_df_property('job_applicant_details', 'cannot_add_rows', true);
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
        frm.set_query('selection_round', function() {
            return{
                query: 'wsc.wsc.doctype.recruitment_exam_declaration.recruitment_exam_declaration.get_selectionround',
                filters: {
                    job_opening: frm.doc.job_opening
                }
            }
        });
    
	},
	
    get_applicant: function(frm) {
        // alert("Hello")
        frappe.call({
            method: 'wsc.wsc.doctype.recruitment_admit_card_generation_tool.recruitment_admit_card_generation_tool.fetch_applicants',
            args: {
                recruitment_exam_declaration: frm.doc.exam_declaration,
                year:frm.doc.year,
                selection_round:frm.doc.selection_round,
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
                        row.caste_category=applicant.caste_category;
                        row.gender=applicant.gender;
                        row.address=applicant.address;
                        row.date_of_birth=applicant.date_of_birth;
                        row.pwd=applicant.pwd;
                    }

                    frm.refresh_field("job_applicant_details");
                }
            }
        });
    }
});
