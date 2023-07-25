// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Resignation', {
	refresh: function(frm) {
		
		if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.doctype.employee_resignation.employee_resignation.is_verified_user',
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
            frappe.call({
                method: 'wsc.wsc.doctype.employee_resignation.employee_resignation.get_joining_date',
                args: {
                    employee: frm.doc.employee,
                },
                callback: function(response) {
                    if (response && response.message) {
                        frm.set_value('joining_date', response.message.date_of_joining);
                    }
                }
            });
			frappe.call({
                method: 'wsc.wsc.doctype.employee_resignation.employee_resignation.get_ra',
                args: {
                    employee: frm.doc.employee,
                },
                callback: function(response) {
                    if (response && response.message) {
                        frm.set_value('reporting_authority', response.message.user_id);
                    }
                }
            });
        
    }
});
