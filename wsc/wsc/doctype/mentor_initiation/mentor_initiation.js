// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mentor Initiation', {
	"mentor": function(frm) {
		cur_frm.clear_table("mentee_information")
		frappe.call({
			method: "wsc.wsc.doctype.mentor_initiation.mentor_initiation.get_mentor_mentees",
			args:{
				mentor:frm.doc.mentor,
			},
			callback: function(r) {
				if(r.message) {
					r.message.forEach(element => {
						var c = frm.add_child("mentee_information")
						c.student = element.student,
						c.student_name = element.student_name,
						c.programs= element.program
					});
				}
				frm.refresh();
				frm.refresh_field("mentee_information")
			}
		});
	},
	setup: function (frm) {
		frm.set_query("mentor", function() {
			return {
				query: 'wsc.wsc.doctype.mentor_initiation.mentor_initiation.filter_mentor',
			};
		});
	},
	refresh: function(frm) {
		if(!frm.is_new()){
			frm.set_df_property('mentor', 'read_only', 1)
			frm.set_df_property('date', 'read_only', 1)
			frm.set_df_property('description', 'read_only', 1)
		}
		frm.set_df_property('mentee_information', 'cannot_add_rows', true);
		frm.set_df_property('mentee_information', 'cannot_delete_rows', true);
	}
});
