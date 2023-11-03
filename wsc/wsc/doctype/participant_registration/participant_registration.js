// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Registration', {
	
	refresh: function(frm) {
		frm.set_query("participant_id", function () {
			return {
				query:"wsc.wsc.doctype.participant_registration.participant_registration.get_participant_id",
				filters: {
					"enabled":1,
					"status":"Active"
				}
			}
		});
		frm.set_query('select_event', function(){
			return{
				filters:[
					['event_status' ,"=", 'Scheduled'],
					["docstatus", "!=", "2"]
				]
			}
		})
	},
	participant_type : function(frm){

		frm.set_value('participant_id', '')
		frm.set_value('participant_name', '')
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
				if(result.message[0] == '0'){
					frm.set_value("event_name", result.message[1])
					frm.set_value("event_date", result.message[2])
					frm.set_value("event_time", result.message[3])
					frm.set_value("select_program", '')
					frm.set_value("program_name", '')
				}
				else if(result.message[0] == '1'){
					frm.set_value("select_program", result.message[1])
					frm.set_value("event_name", result.message[2])
					frm.set_value("event_date", result.message[3])
					frm.set_value("event_time", result.message[4])
				}
			}
		})
	},
	participant_id : function(frm){	
		frappe.call({
			method: 'wsc.wsc.doctype.participant_registration.participant_registration.get_participant_name',
			args: {
				participant_type : frm.doc.participant_type,
				participant_id : frm.doc.participant_id,
			},
			callback: function(result){
				frm.set_value("participant_name", result.message)
			}
		})
	}
});
