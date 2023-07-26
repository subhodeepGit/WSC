// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('User Permission for multiple Departments', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
	frm.set_query("department","departments", function(_doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		return {
			filters: {
				'is_group': 0,
			}
		};
	});
}
});