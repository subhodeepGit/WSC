frappe.ui.form.on('Employee Onboarding', {
    refresh: function(frm) {
        if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.doctype.employee_onboarding.hr_mail_after_complete',
                args: {
                    docname: frm.doc.name
                },
                
            });
        }
	},

});