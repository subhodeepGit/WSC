// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Module', {
	refresh: function(frm) {
		if(!frm.is_new()){
			frm.set_df_property('module_name', 'read_only', 1)
		}
	}
});
