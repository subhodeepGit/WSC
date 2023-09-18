// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Preview', {
	refresh: function(frm) {
		frm.disable_save();
		frm.add_custom_button(__("Go to Your Student Applicant Form"), function() {
			frm.trigger("redirect")
		});
		// <a href = "javascript:history.back()">Back to previous page</a>

	},
	redirect: function(frm){
         window.location.href="javascript:history.back()"
        },
});
