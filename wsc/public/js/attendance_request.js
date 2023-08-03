frappe.ui.form.on('Attendance Request', {
	refresh: function(frm) {
		
		if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.doctype.attendance_request.is_verified_user',
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
    }
});
