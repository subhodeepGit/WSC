// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('placement_tool', {
	refresh: function(frm) {
		// placement_drive_name : function(frm){
		// alert("hello")
		// alert(frm.doc.placement_drive_name)
		frm.disable_save();
		frm.set_df_property("student_child_table", "cannot_add_rows", true);
		frm.set_df_property("student_child_table", "cannot_delete_rows", true);
	},
	"placement_drive_name": function(frm){
		frm.set_query("round_of_placement", function() {
            return {
                filters: [
                    ["Rounds of Placement","parent", "=", [frm.doc.placement_drive_name]],
                ]
            }
        });
	}	
});