// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Generate certificate tool', {
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
			method : 'wsc.wsc.doctype.generate_certificate_tool.generate_certificate_tool.get_program_name',
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
			method: 'wsc.wsc.doctype.generate_certificate_tool.generate_certificate_tool.get_event_details',
			args:{
				event_id : frm.doc.select_event
			},
			callback : function(result){
				frm.set_value("event_name", result.message)
			}
		})
	},
	get_eligible_participants_list : function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.generate_certificate_tool.generate_certificate_tool.get_eligible_participants',
			args : {
				event_id : frm.doc.select_event
			},
			callback: function(result){
				if(result.message){
					frappe.model.clear_table(frm.doc, 'selected_participants_list')
					result.message.forEach(element =>{
						var childTable = frm.add_child('selected_participants_list')
						childTable.participant_id = element.participant_id
						childTable.participant_name = element.participant_name
					})
				}
				frm.refresh()
				frm.refresh_field('selected_participants_list')
			}
		})
	},
	generate_certificate : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.generate_certificate_tool.generate_certificate_tool.generate_record',
			args:{
				doc : frm.doc
			},
			callback: function(result){
				console.log('Hello')
			}
		})
	}
});
