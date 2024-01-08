// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Attendance', {
	refresh: function(frm) {
        frm.set_query("select_event", function () {
			return {
				filters:[
					['event_status' ,"=", 'Scheduled'],
					["docstatus", "!=", "2"]
				]
			}
		});
		frm.set_df_property('selected_participants_table', 'cannot_add_rows', true);
        frm.set_df_property('selected_participants_table', 'cannot_delete_rows', true);
	},
	selected_program : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_attendance.participant_attendance.get_program_name',
			args: {
				program_id : frm.doc.selected_program
			},
			callback : function(result){
				frm.set_value('program_name', result.message)
			}
		})
	},
	select_event : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.participant_attendance.participant_attendance.get_event_details',
			args: {
				event_id : frm.doc.select_event
			},
			callback : function(result){
				if(result.message[0] == 0){
					frm.set_value('event_name', result.message[1])
					frm.set_value('selected_program', '')
					frm.set_value('program_name', '')
				}
				else if(result.message[0] == 1){
					frm.set_value('event_name', result.message[1])
					frm.set_value('selected_program', result.message[2])
				}
			}
		})
	},
	get_participants : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.participant_attendance.participant_attendance.get_participants',
			args:{
				event_id : frm.doc.select_event
			}, 
			callback : function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'selected_participants_table')
					result.message.forEach(element =>{
						var childTable = frm.add_child('selected_participants_table')
						childTable.participant_id = element.participant_id
						childTable.participant_name = element.participant_name
						childTable.participant_type = element.participant_type
					})
				}
				frm.refresh()
				frm.refresh_field('selected_participants_table')
			}
		})
	}
});
