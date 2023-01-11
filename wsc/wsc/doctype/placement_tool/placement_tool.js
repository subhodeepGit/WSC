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
                    ["Rounds of Placement","parent", "=", frm.doc.placement_drive_name],
                ]
            }
        });
	},
	get_student: function(frm){
		if(frm.doc.placement_drive_name && frm.doc.round_of_placement && frm.doc.date_of_round){
			console.log("Hii");
			frappe.call({
				method : "wsc.wsc.doctype.placement_tool.placement_tool.get_student",
				args: {
					drive_name : frm.doc.placement_drive_name,
					placement_round : frm.doc.round_of_placement,
					round_date : frm.doc.date_of_round
				},
				callback: function(result){
					if(result.message){
						alert(result.message);
						// frappe.model.clear_table(frm.doc, "student_child_table");
						// (result.message).forEach(element => {
						// 	var childTable = frm.add_child("student_child_table");
						// 	childTable.ref_no;
						// 	childTable.student_name;
						// 	childTable.program_name;
						// 	childTable.academic_name;
						// });
					}
				}
			})
		}
	}
});