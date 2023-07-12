frappe.ui.form.on('Shift Request', {
    refresh: function(frm) {
        frappe.call({
            method: 'wsc.wsc.validations.shift_request.get_hr_mail',
            callback: function(r) {
                if (r.message) {
                    var hr_mail = r.message;
                    frm.set_value('hr_mail', hr_mail);
                
                }
            }
        });
    }   
});

frappe.ui.form.on('Shift Request', {
    refresh: function(frm) {
        if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.validations.shift_request.is_verified_user',
                args: {
                    docname: frm.doc.name
                },
                callback: function(r) {
                    if (r.message===false) {
                        $('.actions-btn-group').prop('hidden', true);
                    }
                }
            });
        }
    }
});




