// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Event feedback', {
	refresh: function(frm) {

	},
	is_in_a_program : function(frm){
		if(frm.doc.is_in_a_program == 1){
			frm.set_query('select_event', function(){
				return{
					filters:{
						'select_program' : frm.doc.select_program
					}
				}
			})
		}
	},
	participant_id : function(frm){
		frappe.call({
			method :'wsc.wsc.doctype.event_feedback.event_feedback.get_participant_name',
			args:{
				participant_id : frm.doc.participant_id
			},
			callback: function(result){
				frm.set_value('participant_name', result.message)
			}
		})
	},
	select_program : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.event_feedback.event_feedback.get_program_name',
			args: {
				program_id : frm.doc.select_program
			},
			callback : function(result){
				frm.set_value('program_name', result.message)
			}
		})
	},
	select_event : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.event_feedback.event_feedback.get_event_name',
			args:{
				event_id : frm.doc.select_event
			},
			callback : function(result){
				frm.set_value("event_name", result.message)
			}
		})
	}
});