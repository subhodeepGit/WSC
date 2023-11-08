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
							c.participant_name=element.participant_name
							c.hrms_id=element.hrms_id
							c.district=element.district
							c.mobile_number=element.mobile_number
							c.email_address=element.email_address
							c.is_hostel_required=element.is_hostel_required
							c.hostel_type=element.room_type
						});
					}
					frm.refresh_field("participant_list")
					frm.save()
				} 
				
			}); 
		
		}
	},
	refresh(frm){
        frm.set_df_property('participant_list', 'cannot_add_rows', true);
        frm.set_df_property('participant_list', 'cannot_delete_rows', true);

		if (frm.doc.docstatus===1 && frm.doc.status==="Not Completed "){
			frm.add_custom_button(__('Enroll Participant'), function() {
				frappe.call({
					// wsc.wsc.doctype.tot_participant_enrollment.tot_participant_enrollment.
					method: 'enroll_participant',
					doc: frm.doc,
					// tot_participant_selection_id:doc.tot_participant_selection_id,
					// callback: function() {
					// 	frm.refresh();
					// }
				});
			}).addClass('btn-primary');
		};
		frm.set_query("tot_participant_selection_id", function () {
			return {
				
				query: 'wsc.wsc.doctype.tot_participant_enrollment.tot_participant_enrollment.tot_participant_selection_id',
				filters: {
                    "docstatus":1
                }
			}
		});
	},
	
});
