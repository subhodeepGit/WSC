
frappe.ui.form.on('Compensatory Leave Request', {
    refresh: function(frm) {
        if (frm.doc.reason){
            frm.set_read_only()
        }
        if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.doctype.compensatory_leave_request.is_verified_user',
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
