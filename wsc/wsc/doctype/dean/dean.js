// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Dean', {
	refresh:function(frm){
		frm.set_df_property('instructors', 'cannot_add_rows', true);
        frm.set_df_property('instructors', 'cannot_delete_rows', true);
		
	},
	department:function(frm){
		frm.clear_table("instructors");
		frappe.call({
			method: "wsc.wsc.doctype.dean.dean.get_enroll_instructors",
			args: {
				department: frm.doc.department
			},
			callback: function(r) { 
				(r.message).forEach(element => {
					var row = frm.add_child("instructors")
					row.instructor_name=element.name
					row.department=element.department
					row.gender=element.gender
				});
				frm.refresh_field("instructors")
				// frm.set_value("total_enrolled_student",(r.message).length)
			} 
			
		});  
	},


});
