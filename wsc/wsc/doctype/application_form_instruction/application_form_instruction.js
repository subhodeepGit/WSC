// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Application Form Instruction', {
	refresh: function(frm) {
		frm.disable_save();
		frm.add_custom_button(__("Go Back"), function() {
			frm.trigger("redirect")
		});
	},
	redirect: function(frm){
		window.location.href="javascript:history.back()"
	   },

});
