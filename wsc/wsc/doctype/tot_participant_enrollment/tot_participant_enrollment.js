// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant Enrollment', {
	get_participants(frm){
		if (frm.doc.tot_participant_selection_id){
			frappe.call({
				method: "wsc.wsc.doctype.tot_participant_enrollment.tot_participant_enrollment.get_participants",
				args: {
					participant_selection_id: frm.doc.tot_participant_selection_id,
				},
				callback: function(r) { 
					if(r.message){
						frappe.model.clear_table(frm.doc, 'participant_list');
						(r.message).forEach(element => {
							var c = frm.add_child("participant_list")
							c.participant=element.participant_id
							c.hrms_id=element.hrms_id
							c.district=element.district
							c.mobile_number=element.mobile_number
							c.email_address=element.email_address
						});
					}
					frm.refresh_field("participant_list")
				} 
				
			}); 
		
		}
	},
	refresh(frm){

        frm.set_df_property('participant_list', 'cannot_add_rows', true);
        frm.set_df_property('participant_list', 'cannot_delete_rows', true);
	},
	
	// "enroll_particpant": function(frm) {
	// 	if (frm.doc.semester && frm.doc.academic_year){
	// 		frappe.call({
	// 			method: "enroll_participants",
	// 			doc:frm.doc,
	// 			callback: function(r) {
	// 				// frm.set_value("students", []);
	// 				frappe.hide_msgprint(true);
	// 			}
	// 		});
	// 	}

	// },
});
