// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Registration', {
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
	select_program : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.participant_registration.participant_registration.get_program_name',
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
			method: 'wsc.wsc.doctype.participant_registration.participant_registration.get_event_details',
			args:{
				event_id : frm.doc.select_event
			},
			callback : function(result){
				frm.set_value("event_name", result.message[0])
				frm.set_value("event_date", result.message[1])
				frm.set_value("event_time", result.message[2])
			}
		})
	},	
});
