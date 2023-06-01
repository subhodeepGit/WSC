// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
frappe.ui.form.on('Employee Reengagement', {
    refresh: function(frm) {

		frappe.call({
            method: 'wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp',
            args: {
                docname: frm.doc.name
            },
			
			callback: function(r) {
                if (r.message===false) {
					alert(r.message)
                    $('.page-header-actions-block .btn-primary, .page-header-actions-block .btn-default').addClass('hidden');

                }
            }
			
    	});
	}
});

