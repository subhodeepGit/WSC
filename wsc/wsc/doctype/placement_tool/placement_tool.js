// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('placement_tool', {
	// refresh: function(frm) {
	refresh : function(frm){
		frm.disable_save();
		frm.set_df_property("student_child_table", "cannot_add_rows", true);
		frm.set_df_property("student_child_table", "cannot_delete_rows", true);

		if(frm.placement_drive_name){
			frappe.call({
				method: "",
				freeze: true,
				freeze_message: __("Fetching details"),
				args:{

				},
				callback: function(r){

				}
			});
		}
	}
	// }
});
