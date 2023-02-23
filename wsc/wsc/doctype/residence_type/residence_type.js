// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Residence Type', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Residence Type', {
	validate: function(frm) {
		frm.get_field('eligibility').grid.cannot_add_rows = true;
	}
});