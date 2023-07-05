// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Profile Updation', {
	refresh: function(frm) {
		// if (frm.doc.status==="Open") {
		// 	frm.add_custom_button(__("Forwarded to Reporting Authority"), function() {
		// 		frm.set_value("current_status", "Forwarded to Reporting Authority")
		// 		frm.save_or_update();
		// 	}, 'Actions');
		// }
		// if (frm.doc.current_status==="Forwarded to Reporting Authority") {
		// 	frm.add_custom_button(__("Approve"), function() {
		// 		frm.set_value("status", "Approved");
		// 		frm.set_value("current_status","Approved")
		// 		frm.save_or_update();
		// 	}, 'Actions');
		// 	frm.add_custom_button(__("Reject"), function() {
		// 		frm.set_value("status", "Rejected");
		// 		frm.set_value("current_status", "Rejected");
		// 		frm.save_or_update();
		// 	}, 'Actions');
		// }
		// frm.set_df_property('status', 'options', ['Open','Approved','Rejected','Cancelled','Forwarded to Approving Authority']);
		if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.is_verified_user',
                args: {
                    docname: frm.doc.name
                },
                
                callback: function(r) {
                    // alert(r)
                    if (r.message===false) {
                        // alert(r.message)
                        // $('.page-header-actions-block .btn btn-primary btn-sm, .page-header-actions-block .btn-default').addClass('hidden');
                        $('.actions-btn-group').prop('hidden', true);

                    }
                }
                
            });
        }
	},
	employee: function(frm) {
        // Get the selected employee

        // Fetch the reporting authority ID based on the selected employee
        frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.isrfp',
            args: {
                reporting_auth: frm.doc.reporting_authority
            },
            callback: function(response) {
                if (response.message) {
                    frm.set_value('reporting_auth_id', response.message);
                }
            }
        });
		frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.get_hr_mail',
            callback: function(response) {
                if (response.message) {
                    frm.set_value('hr_id', response.message);
                }
            }
        });
    }
});
