// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt


// frappe.ui.form.on('Generate certificate tool', {
// 	refresh: function(frm){

// 	},
// 	select_event: function(frm){
// 		alert(1)
// 		frm.set_value('select_program', 'TPP-00001')
// 	}
// })


// -----------------------------------------------------------------------------

frappe.ui.form.on('Generate certificate tool', {
	// select_program : function(frm){
	// 	frappe.call({
	// 		method : 'wsc.wsc.doctype.generate_certificate_tool.generate_certificate_tool.get_program_name',
	// 		args: {
	// 			program_id : frm.doc.select_program
	// 		},
	// 		callback : function(result){
	// 			frm.set_value('program_name', result.message)
	// 		}
	// 	})
	// },
	// select_event : function(frm){
	// 	frappe.call({
	// 		method: 'wsc.wsc.doctype.generate_certificate_tool.generate_certificate_tool.get_event_details',
	// 		args:{
	// 			event_id : frm.doc.select_event
	// 		},
	// 		callback : function(result){
	// 			if(result.message[0] == 0){
	// 				frm.set_value("event_name", result.message[1])
	// 				frm.set_value("select_program", '')
	// 				frm.set_value("program_name", '')
	// 			}
	// 			else if(result.message[0] == 1){
	// 				frm.set_value("event_name", result.message[1])
	// 				frm.set_value("select_program", result.message[2])
	// 			}
	// 		}
	// 	})
	// },
	select_event: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.generate_certificate.generate_certificate.get_program_id',
			args:{
				event_id : frm.doc.select_event
			},
			callback: function(result){
				if(result.message[0] == 0){
					frm.set_value('select_program', '')
				}
				else{
					frm.set_value('select_program', result.message[1])
				}
			}
		})
	},
	// ----------------------------------------------------------------------------------------------------
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
						childTable.participant_type = element.participant_type
					})
				}
				frm.refresh()
				frm.refresh_field('selected_participants_list')
			}
		})
	}
});
