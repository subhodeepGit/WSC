// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Offer Creation Request', {
	// refresh: function(frm) {

	// }
	get_applicants: function(frm) {
        // alert("Hello")
        frappe.call({
            method: 'wsc.wsc.doctype.job_offer_creation_request.job_offer_creation_request.fetch_applicants',
            args: {
                job_opening: frm.doc.job_opening,
                year:frm.doc.year
            },
            callback: function(r) {
				if (r.message) {
					var applicants = r.message;
					frm.clear_table("applicant_details");
					for (var i = 0; i < applicants.length; i++) {
						var applicant = applicants[i];
						var row = frappe.model.add_child(frm.doc, "Job Applicant Details", "applicant_details");
						row.job_applicant = applicant.name;
						row.applicant_name = applicant.applicant_name;
						row.applicant_mail_id = applicant.email_id;
					}
					frm.refresh_field("applicant_details");
				}
			}
        });
    }
});
