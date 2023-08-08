// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('My Profile', {
	refresh: function(frm) {
		frm.add_custom_button(__('Apply Profile Update'), function() {
            frappe.new_doc('Employee Profile Updation', {
                // employee: frm.doc.employee  // Pass any relevant data you need
            });
        });
	}
});
