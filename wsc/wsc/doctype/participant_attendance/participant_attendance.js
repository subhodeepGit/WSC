// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant Attendance', {
	refresh: function(frm) {

	},
	is_in_a_program : function(frm){
		if(frm.doc.is_in_a_program == 1){
			frm.set_query('select_event', function(){
				return{
					filters:{
						'select_program' : frm.doc.selected_program
					}
				}
			})
		}
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
			method: 'wsc.wsc.doctype.participant_attendance.participant_attendance.get_event_name',
			args: {
				event_id : frm.doc.select_event
			},
			callback : function(result){
				frm.set_value('event_name', result.message)
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
						childTable.participant_name = element.student_name
					})
				}
				frm.refresh()
				frm.refresh_field('selected_participants_table')
			}
		})
	}
});
