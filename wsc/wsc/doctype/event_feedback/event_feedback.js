// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


frappe.ui.form.on('Event feedback', {
	refresh: function(frm){

	},
	participant_id : function(frm){
		frappe.call({
			method :'wsc.wsc.doctype.event_feedback.event_feedback.get_participant_name',
			args:{
				participant_id : frm.doc.participant_id,
				participant_type: frm.doc.participant_type
			},
			callback: function(result){
				frm.set_value('participant_name', result.message)
			}
		})
	},
})
