// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mentor Initiation', {
		refresh: function(frm){
		frappe.call({
			method: "wsc.wsc.doctype.mentor_initiation.mentor_initiation.get_mentor_mentees",
			args : {"user":frappe.session.user},
			callback: function(r){
				if(r.message){
					var get_data = r.message;
					frm.set_value("mentor", get_data["mentor"])
					frm.set_value("mentor_name", get_data["mentor_name"])
					var mentee_info = cur_frm.fields_dict['mentee_information'].grid;
					for (var i= 0; i < get_data["student"].length; i++) {
						var add_mentee = mentee_info.add_new_row();
						add_mentee.student = get_data["student"][i];
						add_mentee.student_name = get_data["student_name"][i];
						add_mentee.programs = get_data["programs"][i];
						cur_frm.refresh_field ("mentee_information");
					frm.set_df_property('mentee_information', 'cannot_add_rows', true);
					frm.set_df_property('mentee_information', 'cannot_delete_rows', true);
					}
				}
			}
		});
	}
});
