// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Applicant Instruction', {
	refresh: function(frm) {
		frm.disable_save();
	}
});
